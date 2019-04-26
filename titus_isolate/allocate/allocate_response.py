from titus_isolate.allocate.constants import CPU, METADATA, TITUS_ISOLATE_CELL_HEADER, UNKNOWN_CELL, CELL, CPU_ALLOCATOR
from titus_isolate.allocate.utils import parse_cpu
from titus_isolate.model.processor.cpu import Cpu


class AllocateResponse:

    def __init__(self, cpu: Cpu, cpu_allocator_name: str, metadata: dict = {}):
        self.__cpu = cpu
        self.__metadata = metadata
        self.__metadata[CPU_ALLOCATOR] = cpu_allocator_name

    def get_cpu(self):
        return self.__cpu

    def get_metadata(self):
        return self.__metadata

    def to_dict(self):
        return {
            CPU: self.get_cpu().to_dict(),
            METADATA: self.get_metadata()
        }


def deserialize_response(headers, body) -> AllocateResponse:
    cell = headers.get(TITUS_ISOLATE_CELL_HEADER, UNKNOWN_CELL)
    cpu = parse_cpu(body[CPU])
    metadata = body[METADATA]
    metadata[CELL] = cell
    cpu_allocator_name = metadata[CPU_ALLOCATOR]
    return AllocateResponse(cpu, cpu_allocator_name, metadata)