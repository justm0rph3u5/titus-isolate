import json
import logging

from titus_isolate.allocate.allocate_request import AllocateRequest
from titus_isolate.allocate.greedy_cpu_allocator import GreedyCpuAllocator
from titus_isolate.event.container_batch_event_handler import ContainerBatchEventHandler
from titus_isolate.kub.constants import ANNOTATION_KEY_JOB_ID
import numpy as np
import time
from typing import List

from kubernetes.client import V1Pod

from tests.cgroup.mock_cgroup_manager import MockCgroupManager
from tests.config.test_property_provider import TestPropertyProvider
from titus_isolate import LOG_FMT_STRING, log
from titus_isolate.allocate.constants import INSTANCE_ID
from titus_isolate.config.config_manager import ConfigManager
from titus_isolate.event.rebalance_event_handler import RebalanceEventHandler
from titus_isolate.isolate.workload_manager import WorkloadManager
from titus_isolate.model.legacy_workload import LegacyWorkload
from titus_isolate.model.pod_utils import parse_pod
from titus_isolate.model.processor.config import get_cpu
from titus_isolate.model.processor.cpu import Cpu
from titus_isolate.model.workload_interface import Workload
from titus_isolate.monitor.resource_usage import GlobalResourceUsage
from titus_isolate.predict.cpu_usage_predictor import PredEnvironment
from titus_isolate.utils import set_config_manager

DEFAULT_TIMEOUT_SECONDS = 3
DEFAULT_TEST_CPU = 1
DEFAULT_TEST_MEM = 256
DEFAULT_TEST_DISK = 512
DEFAULT_TEST_NETWORK = 1024
DEFAULT_TEST_APP_NAME = 'test_app_name'
DEFAULT_TEST_OWNER_EMAIL = 'user@email.org'
DEFAULT_TEST_IMAGE = 'test_image'
DEFAULT_TEST_CMD = 'test_cmd'
DEFAULT_TEST_ENTRYPOINT = 'test_entrypoint'
DEFAULT_TEST_JOB_ID = 'test_job_id'
DEFAULT_TEST_JOB_TYPE = 'SERVICE'
DEFAULT_TEST_WORKLOAD_TYPE = 'static'
DEFAULT_TEST_INSTANCE_ID = 'test_instance_id'
DEFAULT_TEST_REQUEST_METADATA = {INSTANCE_ID: DEFAULT_TEST_INSTANCE_ID}
TEST_POD_JOB_ID = "162aa6e7-b33a-4ca5-a9f0-f848379d4112"
TEST_POD_OWNER_EMAIL = "email@address.com"

set_config_manager(ConfigManager(TestPropertyProvider({})))


def wait_until(func, timeout=DEFAULT_TIMEOUT_SECONDS, period=0.01):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if func():
            return
        time.sleep(period)

    raise TimeoutError(
        "Function did not succeed within timeout: '{}'.".format(timeout))


def counter_value_equals(registry, key, expected_value, tags={}):
    value = registry.counter(key, tags).count()
    equal = value == expected_value
    if not equal:
        log.info("counter: '{}'='{}' expected: '{}'".format(key, value, expected_value))

    return equal


def gauge_value_equals(registry, key, expected_value, tags={}):
    value = registry.gauge(key, tags).get()
    equal = value == expected_value
    if not equal:
        log.info("gauge: '{}'='{}' expected: '{}'".format(key, value, expected_value))

    return equal


def gauge_value_reached(registry, key, min_expected_value):
    value = registry.gauge(key).get()
    reached = value >= min_expected_value
    if not reached:
        log.info("gauge: '{}'='{}' min expected: '{}'".format(key, value, min_expected_value))

    return reached


def get_threads_with_workload(cpu, workload_id):
    return [t for t in cpu.get_threads() if workload_id in t.get_workload_ids()]


def get_test_workload(task_id, thread_count, launch_time=None) -> Workload:
    return LegacyWorkload(
        task_id=task_id,
        job_id=DEFAULT_TEST_JOB_ID,
        thread_count=thread_count)


def get_allocate_request(cpu: Cpu, workloads: List[Workload]):
    return AllocateRequest(
        cpu=cpu,
        workloads=__workloads_list_to_map(workloads),
        metadata=DEFAULT_TEST_REQUEST_METADATA)


def __workloads_list_to_map(workloads: List[Workload]) -> dict:
    __workloads = {}
    for w in workloads:
        __workloads[w.get_task_id()] = w
    return __workloads


def config_logs(level):
    logging.basicConfig(
        format=LOG_FMT_STRING,
        datefmt='%d-%m-%Y:%H:%M:%S',
        level=level)

def test_pod_json():
    return {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "annotations": {
                "EniId": "eni-085f82953c8a85369",
                "EniIpAddress": "100.122.85.243",
                "IpAddress": "100.122.85.243",
                "IsRoutableIp": "true",
                "ResourceId": "resource-eni-10",
                "containerInfo": "CgZ1YnVudHUiAHINc2xlZXBfZm9yZXZlcnoAggEAigE4YXJuOmF3czppYW06OjE3OTcyNzEwMTE5NDpyb2xlL1RpdHVzQ29udGFpbmVyRGVmYXVsdFJvbGWSATAKATAaC3NnLWYwZjE5NDk0GgtzZy1mMmYxOTQ5NhoLc2ctOGUxZDI4ZTgggAEqATCaAQCgAQDKATQKDFRJVFVTX0pPQl9JRBIkMTYyYWE2ZTctYjMzYS00Y2E1LWE5ZjAtZjg0ODM3OWQ0MTEyygE1Cg1USVRVU19UQVNLX0lEEiQxMjI0MTNkNi03OWYyLTRhMjQtODJlMy0zMDQwYjk4OTBiNDPKARkKEE5FVEZMSVhfRVhFQ1VUT1ISBXRpdHVzygE7ChNORVRGTElYX0lOU1RBTkNFX0lEEiQxMjI0MTNkNi03OWYyLTRhMjQtODJlMy0zMDQwYjk4OTBiNDPKAT4KFlRJVFVTX1RBU0tfSU5TVEFOQ0VfSUQSJDEyMjQxM2Q2LTc5ZjItNGEyNC04MmUzLTMwNDBiOTg5MGI0M8oBPgoWVElUVVNfVEFTS19PUklHSU5BTF9JRBIkMTIyNDEzZDYtNzlmMi00YTI0LTgyZTMtMzA0MGI5ODkwYjQz0gFHc2hhMjU2OjdjMzA4YzhmZWI0MGEyYTA0YTZlZjE1ODI5NTcyN2I2MTYzZGE4NzA4ZThmNjEyNWFiOTU3MTU1N2U4NTdiMjnYAQDgAQroAQHwAQD6AT5yZWdpc3RyeS51cy1lYXN0LTEuc3RyZWFtaW5ndGVzdC50aXR1cy5uZXRmbGl4Lm5ldDo3MDAyL3VidW50dYACAIgCAKoCLwoWdGl0dXMuYWdlbnQub3duZXJFbWFpbBIVZ2hhcnRtYW5uQG5ldGZsaXguY29tqgIeChN0aXR1cy5hZ2VudC5qb2JUeXBlEgdTRVJWSUNFqgI5ChF0aXR1cy5hZ2VudC5qb2JJZBIkMTYyYWE2ZTctYjMzYS00Y2E1LWE5ZjAtZjg0ODM3OWQ0MTEyqgIsCht0aXR1cy5hZ2VudC5hcHBsaWNhdGlvbk5hbWUSDXNsZWVwX2ZvcmV2ZXKyAhESBXNsZWVwEghpbmZpbml0ecACQNAC7t7yzJAu",
                "jobDescriptor": "H4sIAAAAAAAAAK1US3PTMBC+8ysyPpdiubHj5ERLCpQhTAfa4cAwjGyvHVFZMpKcNHTy31nJ7z5u6LbfPrT77ePh1Wzmyb0A5a1mDyigaICWlyVlHCGv2FJlSirEWwEm5+z+NJWlh4bHE+tKq4qzlBomxRdagvXQHKD6lUsFO4zqrFJa0ZSZwwcl68rarC/fn99+vmm0v2XiFFcil0MW2tD0zto6IwQyMG1OHaLhTw0idb+OUjJGsaQ2oEclMVPr01QBNZBdHF4urIssa9XEdZ416xRtIOAukQx2/tIKvk+GBFIpMNMJpQqaiENK1q6qUSSn/kmHFA4Z5BJKqQ6bCwRDEvRwxvSdA4mPr4exjr1Ud5ukst+QIO41lHOJTYKra1TklGvoVZDrjayFsS4/fvaw3pbf2F9wv0TzAWaFgOw8y7Agfd5ExdY3zs7o2PcmrRW2/FrJnHEY192pXNOdq6eL17mfk+V8OfdOZk4MnBi1YgwkC2KIvSFFRsuv0kX2qBIrutcrhFYrslguggXxCfqvFFq8ubFNe9d1ZQ05rblxvgNDT4cGa5lUxEpaTOoQ7cDXCfJXD7EMLUZT6vpVgDZuN7Y0CKPVIj3z4zTOIZn7NKD+nEaQkzAOliGmnkQkOstovPCx4DwiQUgTVJAwXEAcLpJg6U0Seyb3TgXCqMO1ZMKM2osDWuLgZw3zdlstyUzkTGBXOobRd/cknpa5QSK1UUilmU7zs/BxGLT7yg4NTku3rkNYXMXsf4btV1GD2rF06Fp/icZflMz6kmHr6P1EzkAzBZYu8ohcmnCHG1W3G4Wb7hjHozj5IwNOD862g+xEId+M8rXVbWx5nt8PTefT4HbRxyr7C3P99p+d1ZIVym3m00z0QRso2yV4cdhb4j7JBBcY75aeni68QLb2K2FPqoZ1z9D0uLRma3jW7FGv0FjVlU36os4KGHLDZHi+oQLXb0wgktDdnxtWQkNUZC/idLiQCLgVnJXMjPw7rUHX70xkcq+nK9Jei49AudkiCTuWgeoP3fHV8R85L9lROwcAAA==",
                "titus.agent.applicationName": "sleep_forever",
                "titus.agent.jobId": TEST_POD_JOB_ID,
                "titus.agent.jobType": "SERVICE",
                "titus.agent.ownerEmail": TEST_POD_OWNER_EMAIL,
            },
            "labels": {
                "pod.titus.netflix.com/byteUnits": "true",
                "v3.job.titus.netflix.com/job-id": TEST_POD_JOB_ID,
                "v3.job.titus.netflix.com/task-id": "122413d6-79f2-4a24-82e3-3040b9890b43"
            },
            "creationTimestamp": "2020-03-23T22:56:36Z",
            "name": "122413d6-79f2-4a24-82e3-3040b9890b43",
            "namespace": "default",
            "resourceVersion": "20494089",
            "selfLink": "/api/v1/namespaces/default/pods/122413d6-79f2-4a24-82e3-3040b9890b43",
            "uid": "8c361a70-6d59-11ea-8f49-0efcd15f3973"
        },
        "spec": {
            "containers": [
                {
                    "image": "imageIsInContainerInfo",
                    "imagePullPolicy": "IfNotPresent",
                    "name": "main",
                    "resources": {
                        "limits": {
                            "cpu": str(2),
                            "memory": "512",
                            "titus/disk": "10k",
                            "titus/gpu": "0",
                            "titus/network": "128"
                        },
                        "requests": {
                            "cpu": str(2),
                            "memory": "512",
                            "titus/disk": "10k",
                            "titus/gpu": "0",
                            "titus/network": "128"
                        }
                    },
                    "terminationMessagePath": "/dev/termination-log",
                    "terminationMessagePolicy": "File"
                }
            ],
            "dnsPolicy": "ClusterFirst",
            "enableServiceLinks": True,
            "nodeName": "i-0a76c510b81646393",
            "priority": 0,
            "restartPolicy": "Never",
            "schedulerName": "default-scheduler",
            "securityContext": {},
            "terminationGracePeriodSeconds": 600,
            "tolerations": [
                {
                    "effect": "NoExecute",
                    "key": "node.kubernetes.io/not-ready",
                    "operator": "Exists",
                    "tolerationSeconds": 300
                },
                {
                    "effect": "NoExecute",
                    "key": "node.kubernetes.io/unreachable",
                    "operator": "Exists",
                    "tolerationSeconds": 300
                }
            ]
        },
        "status": {
            "containerStatuses": [
                {
                    "image": "",
                    "imageID": "",
                    "lastState": {},
                    "name": "122413d6-79f2-4a24-82e3-3040b9890b43",
                    "ready": True,
                    "restartCount": 0,
                    "state": {
                        "running": {
                            "startedAt": "2020-03-23T22:56:37Z"
                        }
                    }
                }
            ],
            "message": "running",
            "phase": "Running",
            "podIP": "100.122.85.243",
            "qosClass": "Guaranteed",
            "reason": "TASK_RUNNING"
        }
    }


def get_simple_test_pod(v1=False) -> V1Pod:
    pod = test_pod_json()

    if v1:
        annotations = pod['metadata']['annotations']
        del annotations['containerInfo']
        del annotations['jobDescriptor']

    pod_str = json.dumps(pod)
    return parse_pod(pod_str)


class TestContext:
    def __init__(self, cpu=None, allocator=GreedyCpuAllocator()):
        if cpu is None:
            cpu = get_cpu()
        self.__workload_manager = WorkloadManager(cpu, MockCgroupManager(), allocator)
        self.__container_batch_event_handler = ContainerBatchEventHandler(self.__workload_manager)
        self.__rebalance_event_handler = RebalanceEventHandler(self.__workload_manager)

    def get_cpu(self):
        return self.__workload_manager.get_cpu()

    def get_workload_manager(self):
        return self.__workload_manager

    def get_container_batch_event_handler(self):
        return self.__container_batch_event_handler

    def get_rebalance_event_handler(self):
        return self.__rebalance_event_handler

    def get_event_handlers(self):
        return [self.__container_batch_event_handler, self.__rebalance_event_handler]


class TestPredictor(object):

    def __init__(self):
        self.meta_data = {'model_training_titus_task_id': '123'}


class TestCpuUsagePredictor:

    def __init__(self, constant_percent_busy: float = 100):
        self.__constant_percent_busy = constant_percent_busy
        self.__model = TestPredictor()

    def predict(self, workload: Workload, cpu_usage_last_hour: np.array, pred_env: PredEnvironment) -> float:
        return workload.get_thread_count() * self.__constant_percent_busy / 100

    def get_model(self):
        return self.__model


class TestCpuUsagePredictorManager:

    def __init__(self, predictor=TestCpuUsagePredictor()):
        self.__predictor = predictor

    def get_cpu_predictor(self):
        return self.__predictor

    def set_predictor(self, predictor):
        self.__predictor = predictor


class TestWorkloadMonitorManager:
    def get_resource_usage(self, workload_ids: List[str]) -> GlobalResourceUsage:
        return GlobalResourceUsage({})
