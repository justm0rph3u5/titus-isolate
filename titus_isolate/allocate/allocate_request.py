import copy
from typing import Dict

from deprecated import deprecated

from titus_isolate.allocate.constants import CPU, CPU_USAGE, WORKLOADS, METADATA, CPU_ARRAY, MEM_USAGE, NET_RECV_USAGE, \
    NET_TRANS_USAGE, DISK_USAGE, RESOURCE_USAGE
from titus_isolate.allocate.utils import parse_cpu, parse_legacy_workloads, parse_usage
from titus_isolate.model.processor.cpu import Cpu
from titus_isolate.model.workload_interface import Workload
from titus_isolate.monitor.resource_usage import GlobalResourceUsage, deserialize_global_resource_usage


class AllocateRequest:

    def __init__(self,
                 cpu: Cpu,
                 workloads: dict,
                 resource_usage: GlobalResourceUsage,
                 cpu_usage: dict,
                 mem_usage: dict,
                 net_recv_usage: dict,
                 net_trans_usage: dict,
                 disk_usage: dict,
                 metadata: dict):
        """
        A rebalance request encapsulates all information needed to rebalance the assignment of threads to workloads.

        :param cpu: An object indicating the state of the CPU before workload assignment
        :param workloads: A map of all relevant workloads including the workload to be assigned
                          The keys are workload ids, the objects are Workload objects
        :param cpu_usage: A map of cpu usage per workload
        """
        self.__cpu = copy.deepcopy(cpu)
        self.__workloads = copy.deepcopy(workloads)
        self.__resource_usage = copy.deepcopy(resource_usage)
        self.__cpu_usage = copy.deepcopy(cpu_usage)
        self.__mem_usage = copy.deepcopy(mem_usage)
        self.__net_recv_usage = copy.deepcopy(net_recv_usage)
        self.__net_trans_usage = copy.deepcopy(net_trans_usage)
        self.__disk_usage = copy.deepcopy(disk_usage)
        self.__metadata = copy.deepcopy(metadata)

    def get_cpu(self):
        return self.__cpu

    def get_workloads(self) -> Dict[str, Workload]:
        return self.__workloads

    def get_resource_usage(self) -> GlobalResourceUsage:
        return self.__resource_usage

    def get_metadata(self):
        return self.__metadata

    @deprecated
    def get_cpu_usage(self):
        return self.__cpu_usage

    @deprecated
    def get_mem_usage(self):
        return self.__mem_usage

    @deprecated
    def get_net_recv_usage(self):
        return self.__net_recv_usage

    @deprecated
    def get_net_trans_usage(self):
        return self.__net_trans_usage

    @deprecated
    def get_disk_usage(self):
        return self.__disk_usage

    def to_dict(self):
        return {
            CPU: self.get_cpu().to_dict(),
            CPU_ARRAY: self.get_cpu().to_array(),
            CPU_USAGE: self.__get_serializable_usage(self.get_cpu_usage()),
            MEM_USAGE: self.__get_serializable_usage(self.get_mem_usage()),
            NET_RECV_USAGE: self.__get_serializable_usage(self.get_net_recv_usage()),
            NET_TRANS_USAGE: self.__get_serializable_usage(self.get_net_trans_usage()),
            DISK_USAGE: self.__get_serializable_usage(self.get_disk_usage()),
            WORKLOADS: self.__get_serializable_workloads(list(self.get_workloads().values())),
            RESOURCE_USAGE: self.__resource_usage.serialize(),
            METADATA: self.get_metadata()
        }

    @staticmethod
    def __get_serializable_usage(cpu_usage: dict):
        serializable_usage = {}
        for w_id, usage in cpu_usage.items():
            serializable_usage[w_id] = [str(u) for u in usage]
        return serializable_usage

    @staticmethod
    def __get_serializable_workloads(workloads: list):
        serializable_workloads = {}
        for w in workloads:
            serializable_workloads[w.get_id()] = w.to_dict()

        return serializable_workloads


def deserialize_allocate_request(serialized_request: dict) -> AllocateRequest:
    cpu = parse_cpu(serialized_request[CPU])
    workloads = parse_legacy_workloads(serialized_request[WORKLOADS])
    cpu_usage = parse_usage(serialized_request.get(CPU_USAGE, {}))
    mem_usage = parse_usage(serialized_request.get(MEM_USAGE, {}))
    net_recv_usage = parse_usage(serialized_request.get(NET_RECV_USAGE, {}))
    net_trans_usage = parse_usage(serialized_request.get(NET_TRANS_USAGE, {}))
    disk_usage = parse_usage(serialized_request.get(DISK_USAGE, {}))

    resource_usage = serialized_request.get(RESOURCE_USAGE, None)
    if resource_usage is None:
        resource_usage = {}
    else:
        resource_usage = deserialize_global_resource_usage(resource_usage)

    metadata = serialized_request[METADATA]
    return AllocateRequest(
        cpu=cpu,
        workloads=workloads,
        resource_usage=resource_usage,
        cpu_usage=cpu_usage,
        mem_usage=mem_usage,
        net_recv_usage=net_recv_usage,
        net_trans_usage=net_trans_usage,
        disk_usage=disk_usage,
        metadata=metadata)
