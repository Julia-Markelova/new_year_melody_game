from dataclasses import dataclass
from typing import Callable
from typing import List
from typing import Optional

from tasks.task_handlers import handle_a_100
from tasks.task_handlers import handle_a_200


@dataclass
class Task:
    point_count: int
    handler: Optional[Callable] = None


@dataclass
class Category:
    name: str
    tasks: List[Task]


def configure_categories(round: int = 1) -> List[Category]:
    return [
        Category(
            name=f'category A round {round}',
            tasks=[
                Task(point_count=100, handler=handle_a_100),
                Task(point_count=200, handler=handle_a_200)
            ]
        ),
        Category(
            name=f'category B round {round}',
            tasks=[
                Task(point_count=100),
                Task(point_count=200)
            ]
        ),
        Category(
            name=f'category C round {round}',
            tasks=[
                Task(point_count=100),
                Task(point_count=200)
            ]
        ),
        Category(
            name=f'category D round {round}',
            tasks=[
                Task(point_count=100),
                Task(point_count=200)
            ]
        ),
    ]
