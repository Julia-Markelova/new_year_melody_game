from dataclasses import dataclass


@dataclass
class Stats:
    clicks_count: int = 0
    right_answers_count: int = 0
    min_time_for_answer: int = None
