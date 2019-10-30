from threading import Lock, Thread

import schedule

from titus_isolate import log
from titus_isolate.config.constants import DEFAULT_SAMPLE_FREQUENCY_SEC
from titus_isolate.event.constants import BURST, STATIC
from titus_isolate.metrics.constants import BURST_POOL_USAGE_KEY, STATIC_POOL_USAGE_KEY
from titus_isolate.metrics.metrics_reporter import MetricsReporter
from titus_isolate.monitor.cgroup_metrics_provider import CgroupMetricsProvider
from titus_isolate.monitor.workload_perf_mon import WorkloadPerformanceMonitor
from titus_isolate.utils import get_workload_manager


class WorkloadMonitorManager(MetricsReporter):

    def __init__(self, seconds: int = 3600, agg_granularity_seconds: int = 60, sample_interval=DEFAULT_SAMPLE_FREQUENCY_SEC):
        self.__seconds = seconds
        self.__agg_granularity_seconds = agg_granularity_seconds
        self.__sample_interval = sample_interval

        self.__registry = None

        self.__lock = Lock()
        self.__monitors = {}

        self.__usage_lock = Lock()
        self.__cpu_usage = {}
        self.__mem_usage = {}
        self.__net_recv_usage = {}
        self.__net_trans_usage = {}

        schedule.every(sample_interval).seconds.do(self.__sample)

    def get_cpu_usage(self):
        with self.__usage_lock:
            return self.__cpu_usage

    def get_mem_usage(self):
        with self.__usage_lock:
            return self.__mem_usage

    def get_net_recv_usage(self):
        with self.__usage_lock:
            return self.__net_recv_usage

    def get_net_trans_usage(self):
        with self.__usage_lock:
            return self.__net_trans_usage

    def __get_cpu_usage(self, seconds: int, agg_granularity_secs: int) -> dict:
        with self.__lock:
            cpu_usage = {}
            for workload_id, monitor in self.get_monitors().items():
                cpu_usage[workload_id] = monitor.get_cpu_usage(seconds, agg_granularity_secs)
        return cpu_usage

    def __get_mem_usage(self, seconds: int, agg_granularity_secs: int) -> dict:
        with self.__lock:
            mem_usage = {}
            for workload_id, monitor in self.get_monitors().items():
                mem_usage[workload_id] = monitor.get_mem_usage(seconds, agg_granularity_secs)
        return mem_usage

    def __get_net_recv_usage(self, seconds: int, agg_granularity_secs: int) -> dict:
        with self.__lock:
            net_recv_usage = {}
            for workload_id, monitor in self.get_monitors().items():
                net_recv_usage[workload_id] = monitor.get_net_recv_usage(seconds, agg_granularity_secs)
        return net_recv_usage

    def __get_net_trans_usage(self, seconds: int, agg_granularity_secs: int) -> dict:
        with self.__lock:
            net_trans_usage = {}
            for workload_id, monitor in self.get_monitors().items():
                net_trans_usage[workload_id] = monitor.get_net_trans_usage(seconds, agg_granularity_secs)
        return net_trans_usage

    def set_registry(self, registry, tags):
        self.__registry = registry

    def report_metrics(self, tags):
        if self.__registry is None:
            log.debug("Not reporting metrics because there's no registry available yet.")
            return

        wm = get_workload_manager()
        if wm is None:
            log.debug("Not reporting metrics because there's no workload manager available yet.")
            return

        usage = self.__get_cpu_usage(60, 60)
        static_pool_cpu_usage = self.__get_pool_usage(STATIC, usage)
        burst_pool_cpu_usage = self.__get_pool_usage(BURST, usage)

        self.__registry.gauge(STATIC_POOL_USAGE_KEY, tags).set(static_pool_cpu_usage)
        self.__registry.gauge(BURST_POOL_USAGE_KEY, tags).set(burst_pool_cpu_usage)

    def get_monitors(self):
        return self.__monitors

    def __set_usages(self):
        cpu_usage = self.__get_cpu_usage(self.__seconds, self.__agg_granularity_seconds)
        mem_usage = self.__get_mem_usage(self.__seconds, self.__agg_granularity_seconds)
        net_recv_usage = self.__get_net_recv_usage(self.__seconds, self.__agg_granularity_seconds)
        net_trans_usage = self.__get_net_trans_usage(self.__seconds, self.__agg_granularity_seconds)

        with self.__usage_lock:
            self.__cpu_usage = cpu_usage
            self.__mem_usage = mem_usage
            self.__net_recv_usage = net_recv_usage
            self.__net_trans_usage = net_trans_usage

    def __sample(self):
        try:
            self.__set_usages()
            self.__update_monitors()
            self.__sample_monitors()
        except:
            log.exception("Failed to sample performance monitors.")

    @staticmethod
    def __get_pool_usage(workload_type, usage):
        wm = get_workload_manager()
        if wm is None:
            log.debug("Not reporting metrics because there's no workload manager available yet.")
            return

        workload_map = wm.get_workload_map_copy()

        pool_cpu_usage = 0.0
        for w_id, usage in usage.items():
            if w_id not in workload_map:
                continue

            workload = workload_map[w_id]
            if workload.get_type() == workload_type:
                pool_cpu_usage += usage[len(usage) - 1]

        return pool_cpu_usage

    @staticmethod
    def __get_workloads():
        wm = get_workload_manager()
        if wm is None:
            log.debug("Workload manager not yet present.")
            return []

        return wm.get_workloads()

    def __update_monitors(self):
        workloads = self.__get_workloads()

        with self.__lock:
            # Remove monitors for workloads which are no longer managed
            workload_ids = [w.get_id() for w in workloads]
            for monitored_id in list(self.__monitors.keys()):
                if monitored_id not in workload_ids:
                    self.__monitors.pop(monitored_id, None)

            # Add monitors for new workloads
            for workload in workloads:
                if workload.get_id() not in self.__monitors:
                    self.__monitors[workload.get_id()] = \
                        WorkloadPerformanceMonitor(CgroupMetricsProvider(workload), self.__sample_interval)

    def __sample_monitors(self):
        with self.__lock:
            for workload_id, monitor in self.__monitors.items():
                try:
                    Thread(target=monitor.sample).start()
                except:
                    log.exception("Failed to sample performance of workload: '{}'".format(workload_id))
