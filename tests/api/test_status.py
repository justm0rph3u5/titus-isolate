import json
import unittest
import uuid

from tests.cgroup.mock_cgroup_manager import MockCgroupManager
from tests.config.test_property_provider import TestPropertyProvider
from tests.docker.mock_docker import MockEventProvider
from titus_isolate.allocate.integer_program_cpu_allocator import IntegerProgramCpuAllocator
from titus_isolate.api import status
from titus_isolate.api.status import set_wm, get_workloads, get_violations, get_wm_status, set_em, \
    get_isolated_workload_ids, isolate_workload
from titus_isolate.config.config_manager import ConfigManager
from titus_isolate.docker.constants import STATIC, BURST
from titus_isolate.docker.event_manager import EventManager
from titus_isolate.isolate.workload_manager import WorkloadManager
from titus_isolate.model.processor.config import get_cpu
from titus_isolate.model.processor.utils import DEFAULT_PACKAGE_COUNT, DEFAULT_CORE_COUNT, DEFAULT_THREAD_COUNT
from titus_isolate.model.workload import Workload
from titus_isolate.utils import override_config_manager


class TestStatus(unittest.TestCase):

    def test_get_workloads_endpoint(self):
        override_config_manager(ConfigManager(TestPropertyProvider({})))

        thread_count = 2
        workload_id = str(uuid.uuid4())
        workload = Workload(workload_id, thread_count, STATIC)

        workload_manager = self.__get_default_workload_manager()
        set_wm(workload_manager)

        workloads = json.loads(get_workloads())
        self.assertEqual(0, len(workloads))

        workload_manager.add_workload(workload)

        workloads = json.loads(get_workloads())
        self.assertEqual(workload_id, workloads[0]["id"])
        self.assertEqual(STATIC, workloads[0]["type"])
        self.assertEqual(thread_count, workloads[0]["thread_count"])

    def test_get_isolated_workloads_endpoint(self):
        workload_manager = self.__get_default_workload_manager()
        set_wm(workload_manager)

        isolated_workload_ids = json.loads(get_isolated_workload_ids())
        self.assertEqual(0, len(isolated_workload_ids))

        workload = Workload(str(uuid.uuid4()), 2, BURST)
        workload_manager.add_workload(workload)

        isolated_workload_ids = json.loads(get_isolated_workload_ids())
        self.assertEqual(1, len(isolated_workload_ids))
        self.assertEqual(workload.get_id(), isolated_workload_ids[0])

    def test_isolate_workload_endpoint(self):
        workload_manager = self.__get_default_workload_manager()
        set_wm(workload_manager)

        _, code, _ = isolate_workload(str(uuid.uuid4()), timeout=0.5)
        self.assertEqual(404, code)

        workload = Workload(str(uuid.uuid4()), 2, BURST)
        workload_manager.add_workload(workload)

        _, code, _ = isolate_workload(workload.get_id(), timeout=0.5)
        self.assertEqual(200, code)

    def test_get_cpu_endpoint(self):
        set_wm(self.__get_default_workload_manager())

        cpu_dict = json.loads(status.get_cpu())
        self.assertEqual(1, len(cpu_dict))
        self.assertEqual(DEFAULT_PACKAGE_COUNT, len(cpu_dict["packages"]))
        for p in cpu_dict["packages"]:
            self.assertEqual(DEFAULT_CORE_COUNT, len(p["cores"]))
            for c in p["cores"]:
                self.assertEqual(DEFAULT_THREAD_COUNT, len(c["threads"]))

    def test_get_violations_endpoint(self):
        set_wm(self.__get_default_workload_manager())

        violations = json.loads(get_violations())
        self.assertEqual(2, len(violations))

    def test_get_wm_status_endpoint(self):
        set_wm(self.__get_default_workload_manager())

        event_manager = EventManager(MockEventProvider([]), [], 0.01)
        set_em(event_manager)
        event_manager.start_processing_events()

        s = json.loads(get_wm_status())
        self.assertEqual(2, len(s))
        self.assertEqual(4, len(s["event_manager"]))
        self.assertEqual(7, len(s["workload_manager"]))

        event_manager.stop_processing_events()

    @staticmethod
    def __get_default_workload_manager():
        cpu = get_cpu()
        return WorkloadManager(cpu, MockCgroupManager(), IntegerProgramCpuAllocator())
