"""Per-run call budgets. Cost control is a hard gate, not a suggestion."""

from dataclasses import dataclass


class BudgetExceeded(RuntimeError):
    pass


@dataclass
class CallBudget:
    max_serp: int
    max_keyword: int
    serp_calls: int = 0
    keyword_calls: int = 0

    def consume(self, kind: str) -> None:
        if kind == "serp":
            if self.serp_calls >= self.max_serp:
                raise BudgetExceeded(f"SERP call budget exceeded ({self.max_serp}).")
            self.serp_calls += 1
        elif kind == "keyword":
            if self.keyword_calls >= self.max_keyword:
                raise BudgetExceeded(f"Keyword call budget exceeded ({self.max_keyword}).")
            self.keyword_calls += 1
        else:
            raise ValueError(f"Unknown budget kind: {kind}")
