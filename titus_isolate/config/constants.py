# Logs
LOG_FMT_STRING = '%(asctime)s,%(msecs)d %(levelname)s [%(filename)s:%(lineno)d] %(message)s'

# Rebalance
REBALANCE_FREQUENCY_KEY = 'TITUS_ISOLATE_REBALANCE_FREQUENCY'
DEFAULT_REBALANCE_FREQUENCY = 60

# Reconcile
RECONCILE_FREQUENCY_KEY = 'TITUS_ISOLATE_RECONCILE_FREQUENCY'
DEFAULT_RECONCILE_FREQUENCY = 60

# Healthcheck
HEALTH_CHECK_FREQUENCY_KEY = 'TITUS_ISOLATE_HEALTHCHECK_FREQUENCY'
DEFAULT_HEALTH_CHECK_FREQUENCY = 60

MAX_TIME_SINCE_LAST_SUCCESSFUL_EVENT_KEY = 'TITUS_ISOLATE_MAX_TIME_SINCE_LAST_SUCCESSFUL_EVENT'
DEFAULT_MAX_TIME_SINCE_LAST_SUCCESSFUL_EVENT = 600  # Ten minutes

# Oversubscribe
PREDICT_RESOURCE_USAGE_FREQUENCY_KEY = 'TITUS_ISOLATE_PREDICT_RESOURCE_USAGE_FREQUENCY'
DEFAULT_PREDICT_RESOURCE_USAGE_FREQUENCY = 0 # in seconds

CPU_PREDICTOR = 'TITUS_ISOLATE_CPU_PREDICTOR'
LEGACY_CPU_PREDICTOR = 'legacy'
SERVICE_CPU_PREDICTOR = 'service'
DEFAULT_CPU_PREDICTOR = SERVICE_CPU_PREDICTOR


# CPU Allocator
CPU_ALLOCATOR = 'TITUS_ISOLATE_ALLOCATOR'
FALLBACK_ALLOCATOR = 'TITUS_ISOLATE_FALLBACK_ALLOCATOR'

# Remote Allocator
REMOTE_ALLOCATOR_URL = 'TITUS_ISOLATE_REMOTE_ALLOCATOR_URL'
REMOTE_ASSIGN_ALLOCATOR = 'REMOTE_ASSIGN_ALLOCATOR'
REMOTE_FREE_ALLOCATOR = 'REMOTE_FREE_ALLOCATOR'
REMOTE_REBALANCE_ALLOCATOR = 'REMOTE_REBALANCE_ALLOCATOR'

# Grpc Remote Allocator
GRPC_REMOTE_ALLOC_ENDPOINT = 'TITUS_ISOLATE_GRPC_REMOTE_ALLOCATOR_ENDPOINT'
GRPC_REMOTE_ALLOC_CLIENT_CALL_TIMEOUT_MS = 'TITUS_ISOLATE_GRPC_REMOTE_ALLOCATOR_CLIENT_CALL_TIMEOUT_MS'
GRPC_REMOTE_ALLOC_DEFAULT_CLIENT_CALL_TIMEOUT_MS = 3000

# Fallback
FALLBACK_QUEUE_DEPTH = 'TITUS_ISOLATE_FALLBACK_QUEUE_DEPTH'
DEFAULT_FALLBACK_QUEUE_DEPTH = 20

GREEDY = 'GREEDY'
NAIVE = 'NAIVE'
NOOP = 'NOOP'
GRPC_REMOTE = 'GRPC_REMOTE'
DEFAULT_ALLOCATOR = GRPC_REMOTE
DEFAULT_FALLBACK_ALLOCATOR = NAIVE
CPU_ALLOCATORS = [GREEDY, NAIVE, NOOP, GRPC_REMOTE]

# Forecast CPU Allocator
ALPHA_NU = 'TITUS_ISOLATE_ALPHA_NU'
DEFAULT_ALPHA_NU = 10000.0

ALPHA_LLC = 'TITUS_ISOLATE_ALPHA_LLC'
DEFAULT_ALPHA_LLC = 5.0

ALPHA_L12 = 'TITUS_ISOLATE_ALPHA_L12'
DEFAULT_ALPHA_L12 = 250.0

ALPHA_ORDER = 'TITUS_ISOLATE_ALPHA_ORDER'
DEFAULT_ALPHA_ORDER = 1.0

ALPHA_PREV = 'TITUS_ISOLATE_ALPHA_PREV'
DEFAULT_ALPHA_PREV = 10.0

BURST_MULTIPLIER = 'TITUS_ISOLATE_BURST_MULTIPLIER'
DEFAULT_BURST_MULTIPLIER = 0.1

MAX_BURST_POOL_INCREASE_RATIO = 'TITUS_ISOLATE_MAX_BURST_POOL_INCREASE_RATIO'
DEFAULT_MAX_BURST_POOL_INCREASE_RATIO = 3.0

BURST_CORE_COLLOC_USAGE_THRESH = 'TITUS_ISOLATE_BURST_CORE_COLLOC_USAGE_THRESH'
DEFAULT_BURST_CORE_COLLOC_USAGE_THRESH = 0.2

WEIGHT_CPU_USE_BURST = 'TITUS_ISOLATE_WEIGHT_CPU_USE_BURST'
DEFAULT_WEIGHT_CPU_USE_BURST = 1.0

RELATIVE_MIP_GAP_STOP = 'TITUS_RELATIVE_MIP_GAP_STOP'
DEFAULT_RELATIVE_MIP_GAP_STOP = 0.05

MIP_SOLVER = 'TITUS_ISOLATE_MIP_SOLVER'
DEFAULT_MIP_SOLVER = 'GLPK_MI'

# Free Thread Provider
FREE_THREAD_PROVIDER = 'FREE_THREAD_PROVIDER'
EMPTY = 'EMPTY'
OVERSUBSCRIBE = 'OVERSUBSCRIBE'
EMPTY_CORES = 'EMPTY_CORES'
DEFAULT_FREE_THREAD_PROVIDER = EMPTY_CORES

# Threshold Free Thread Provider
TOTAL_THRESHOLD = 'TOTAL_THRESHOLD'
DEFAULT_TOTAL_THRESHOLD = 0.05

# NUMA balancing
TITUS_ISOLATE_MEMORY_MIGRATE = 'TITUS_ISOLATE_MEMORY_MIGRATE'
DEFAULT_TITUS_ISOLATE_MEMORY_MIGRATE = False

TITUS_ISOLATE_MEMORY_SPREAD_PAGE = 'TITUS_ISOLATE_MEMORY_SPREAD_PAGE'
DEFAULT_TITUS_ISOLATE_MEMORY_SPREAD_PAGE = False

TITUS_ISOLATE_MEMORY_SPREAD_SLAB = 'TITUS_ISOLATE_MEMORY_SPREAD_SLAB'
DEFAULT_TITUS_ISOLATE_MEMORY_SPREAD_SLAB = False

# Metrics querying
PROMETHEUS = 'prometheus'
RESOURCE_USAGE_PROVIDER = 'TITUS_ISOLATE_RESOURCE_USAGE_PROVIDER'
DEFAULT_RESOURCE_USAGE_PROVIDER = PROMETHEUS
PROMETHEUS_HOST_OVERRIDE = 'TITUS_ISOLATE_PROMETHEUS_HOST_OVERRIDE'

PROMETHEUS_SHARDING_ENABLED = 'TITUS_ISOLATE_PROMETHEUS_SHARDING_ENABLED'
DEFAULT_PROMETHEUS_SHARDING_ENABLED = True

# Event log
EVENT_LOG_FORMAT_STR = 'EVENT_LOG_FORMAT_STR'

# S3 Buckets
PROD = 'prod'
V1 = 'v1'
LATEST = 'latest'

MODEL_BUCKET_FORMAT_STR = 'TITUS_ISOLATE_MODEL_BUCKET_FORMAT_STR'
MODEL_PREFIX_FORMAT_STR = 'TITUS_ISOLATE_MODEL_PREFIX_FORMAT_STR'

MODEL_BUCKET_PREFIX = 'TITUS_ISOLATE_MODEL_BUCKET_PREFIX'
DEFAULT_MODEL_BUCKET_PREFIX = PROD

MODEL_BUCKET_LEAF = 'TITUS_ISOLATE_MODEL_BUCKET_LEAF'
DEFAULT_MODEL_BUCKET_LEAF = LATEST

# Prediction Service
PREDICTION_SERVICE_URL_FORMAT_STR = 'TITUS_ISOLATE_PREDICTION_SERVICE_URL_FORMAT_STR'

# Credentials
CREDENTIALS_PATH = 'TITUS_ISOLATE_CREDENTIALS_PATH'

# Kubernetes
GET_WORKLOAD_RETRY_COUNT = 'TITUS_ISOLATE_GET_WORKLOAD_RETRY_COUNT'
DEFAULT_GET_WORKLOAD_RETRY_COUNT = 5

GET_WORKLOAD_RETRY_INTERVAL_SEC = 'TITUS_ISOLATE_GET_WORKLOAD_RETRY_INTERVAL_SEC'
DEFAULT_GET_WORKLOAD_RETRY_INTERVAL_SEC = 0.5

# Static environment variables
PROPERTY_URL_ROOT = 'http://localhost:3002/properties'
EC2_INSTANCE_ID = "EC2_INSTANCE_ID"
EC2_LOCAL_IPV4 = "EC2_LOCAL_IPV4"
EC2_INSTANCE_TYPE = "EC2_INSTANCE_TYPE"

MAX_SOLVER_RUNTIME = 'TITUS_ISOLATE_MAX_SOLVER_RUNTIME'
DEFAULT_MAX_SOLVER_RUNTIME = 5

MAX_SOLVER_CONNECT_SEC = 'TITUS_ISOLATE_MAX_SOLVER_CONNECT_SEC'
DEFAULT_MAX_SOLVER_CONNECT_SEC = 1

DEFAULT_SHARES_SCALE = 100
DEFAULT_QUOTA_SCALE = 100000

RESTART_PROPERTIES = [
    ALPHA_NU,
    ALPHA_LLC,
    ALPHA_L12,
    ALPHA_ORDER,
    ALPHA_PREV,
    BURST_CORE_COLLOC_USAGE_THRESH,
    BURST_MULTIPLIER,
    CPU_ALLOCATOR,
    FALLBACK_ALLOCATOR,
    FALLBACK_QUEUE_DEPTH,
    FREE_THREAD_PROVIDER,
    MAX_BURST_POOL_INCREASE_RATIO,
    MAX_SOLVER_RUNTIME,
    MODEL_BUCKET_FORMAT_STR,
    MODEL_PREFIX_FORMAT_STR,
    PREDICT_RESOURCE_USAGE_FREQUENCY_KEY,
    PROMETHEUS_HOST_OVERRIDE,
    PROMETHEUS_SHARDING_ENABLED,
    REBALANCE_FREQUENCY_KEY,
    RECONCILE_FREQUENCY_KEY,
    REMOTE_ALLOCATOR_URL,
    RESOURCE_USAGE_PROVIDER,
    TOTAL_THRESHOLD,
    WEIGHT_CPU_USE_BURST,
    GRPC_REMOTE_ALLOC_ENDPOINT,
    GRPC_REMOTE_ALLOC_CLIENT_CALL_TIMEOUT_MS]
