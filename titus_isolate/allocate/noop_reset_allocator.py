from titus_isolate import log
from titus_isolate.allocate.cpu_allocator import CpuAllocator
from titus_isolate.cgroup.file_cgroup_manager import FileCgroupManager


class NoopResetCpuAllocator(CpuAllocator):

    def __init__(self, cgroup_manager=FileCgroupManager()):
        self.__cgroup_manager = cgroup_manager

    def get_cgroup_manager(self):
        return self.__cgroup_manager

    def assign_threads(self, cpu, workload):
        thread_count = len(cpu.get_threads())
        thread_ids = list(range(thread_count))

        log.info("Setting cpuset.cpus to ALL cpus: '{}' for workload: '{}'".format(thread_ids, workload.get_id()))
        self.__cgroup_manager.set_cpuset(workload.get_id(), thread_ids)

        return cpu

    def free_threads(self, workload_id):
        log.info("Ignoring attempt to free threads for workload: '{}'".format(workload_id))

    def set_registry(self, registry):
        pass

    def report_metrics(self, tags):
        pass