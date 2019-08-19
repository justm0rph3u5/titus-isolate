ADDED_KEY = 'titus-isolate.added'
REMOVED_KEY = 'titus-isolate.removed'
REBALANCED_KEY = 'titus-isolate.rebalanced'
SUCCEEDED_KEY = 'titus-isolate.succeeded'
FAILED_KEY = 'titus-isolate.failed'
ALLOCATOR_CALL_DURATION = 'titus-isolate.allocatorCallDurationSecs'
QUEUE_DEPTH_KEY = 'titus-isolate.queueDepth'
WORKLOAD_COUNT_KEY = 'titus-isolate.workloadCount'
EVENT_SUCCEEDED_KEY = 'titus-isolate.eventSucceeded'
EVENT_FAILED_KEY = 'titus-isolate.eventFailed'
EVENT_PROCESSED_KEY = 'titus-isolate.eventProcessed'
ADDED_TO_FULL_CPU_ERROR_KEY = 'titus-isolate.addedToFullCpu'

IP_ALLOCATOR_TIMEBOUND_COUNT = 'titus-isolate.ipAllocatorTimeBoundSolutionCount'
FORECAST_REBALANCE_FAILURE_COUNT = 'titus-isolate.forecastRebalanceFailureCount'

WRITE_CPUSET_SUCCEEDED_KEY = 'titus-isolate.writeCpusetSucceeded'
WRITE_CPUSET_FAILED_KEY = 'titus-isolate.writeCpusetFailed'
ISOLATED_WORKLOAD_COUNT = 'titus-isolate.isolatedWorkloadCount'
CPUSET_THREAD_COUNT = 'titus-isolate.cpusetThreadCount'

PACKAGE_VIOLATIONS_KEY = 'titus-isolate.crossPackageViolations'
CORE_VIOLATIONS_KEY = 'titus-isolate.sharedCoreViolations'

EVENT_LOG_SUCCESS = 'titus-isolate.eventLogSuccessCount'
EVENT_LOG_RETRY = 'titus-isolate.eventLogRetryCount'
EVENT_LOG_FAILURE = 'titus-isolate.eventLogFailureCount'

ALLOCATED_SIZE_KEY = 'titus-isolate.allocatedSize'
UNALLOCATED_SIZE_KEY = 'titus-isolate.unallocatedSize'
STATIC_ALLOCATED_SIZE_KEY = 'titus-isolate.staticAllocatedSize'
BURST_ALLOCATED_SIZE_KEY = 'titus-isolate.burstAllocatedSize'
BURST_REQUESTED_SIZE_KEY = 'titus-isolate.burstRequestedSize'
OVERSUBSCRIBED_THREADS_KEY = 'titus-isolate.oversubscribedThreads'
FREE_THREADS_KEY = 'titus-isolate.freeThreads'

PRIMARY_ASSIGN_COUNT = 'titus-isolate.assignThreadsPrimaryCount'
PRIMARY_FREE_COUNT = 'titus-isolate.freeThreadsPrimaryCount'
PRIMARY_REBALANCE_COUNT = 'titus-isolate.rebalancePrimaryCount'
FALLBACK_ASSIGN_COUNT = 'titus-isolate.assignThreadsFallbackCount'
FALLBACK_FREE_COUNT = 'titus-isolate.freeThreadsFallbackCount'
FALLBACK_REBALANCE_COUNT = 'titus-isolate.rebalanceFallbackCount'

SOLVER_GET_CPU_ALLOCATOR_SUCCESS = 'titus-isolate.getCpuAllocatorSuccessCount'
SOLVER_GET_CPU_ALLOCATOR_FAILURE = 'titus-isolate.getCpuAllocatorFailureCount'
SOLVER_ASSIGN_THREADS_SUCCESS = 'titus-isolate.assignThreadsSuccessCount'
SOLVER_ASSIGN_THREADS_FAILURE = 'titus-isolate.assignThreadsFailureCount'
SOLVER_FREE_THREADS_SUCCESS = 'titus-isolate.freeThreadsSuccessCount'
SOLVER_FREE_THREADS_FAILURE = 'titus-isolate.freeThreadsFailureCount'
SOLVER_REBALANCE_SUCCESS = 'titus-isolate.rebalanceSuccessCount'
SOLVER_REBALANCE_FAILURE = 'titus-isolate.rebalanceFailureCount'

STATIC_POOL_USAGE_KEY = 'titus-isolate.staticPoolUsage'
BURST_POOL_USAGE_KEY = 'titus-isolate.burstPoolUsage'

RUNNING = 'titus-isolate.running'

RECONCILE_SKIP_COUNT = 'titus-isolate.reconcileSkipCount'
RECONCILE_SUCCESS_COUNT = 'titus-isolate.reconcileSuccessCount'
