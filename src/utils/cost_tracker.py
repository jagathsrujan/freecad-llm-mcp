import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CostEntry:
    model: str
    operation: str
    tokens_in: int
    tokens_out: int
    cost_usd: float
    duration_seconds: float
    success: bool
    timestamp: float = field(default_factory=time.time)


class CostTracker:
    def __init__(self):
        self._entries: list[CostEntry] = []
        self._start_time = time.time()

    def record(self, entry: CostEntry):
        self._entries.append(entry)

    def total_cost(self) -> float:
        return sum(e.cost_usd for e in self._entries)

    def total_tokens(self) -> tuple[int, int]:
        total_in = sum(e.tokens_in for e in self._entries)
        total_out = sum(e.tokens_out for e in self._entries)
        return total_in, total_out

    def summary(self) -> dict:
        total_in, total_out = self.total_tokens()
        elapsed = time.time() - self._start_time
        return {
            "total_cost_usd": round(self.total_cost(), 4),
            "total_tokens_in": total_in,
            "total_tokens_out": total_out,
            "total_operations": len(self._entries),
            "successful": sum(1 for e in self._entries if e.success),
            "failed": sum(1 for e in self._entries if not e.success),
            "elapsed_seconds": round(elapsed, 2),
        }
