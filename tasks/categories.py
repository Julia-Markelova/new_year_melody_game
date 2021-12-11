import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from typing import List
from typing import Optional

from config.paths import MELODIES_PATH
from tasks.task_handlers import default_handler


@dataclass
class Task:
    point_count: int
    handler: Optional[Callable] = None


@dataclass
class Category:
    name: str
    tasks: List[Task]


def configure_categories(round: int = 1) -> List[Category]:

    path_to_round = Path(f'{MELODIES_PATH}/{round}')
    if not path_to_round.exists():
        raise AssertionError(f'Path for round {round} does not exests in {MELODIES_PATH}')
    categories: List[Category] = []
    for category_name in os.listdir(path_to_round):
        tasks: List[Task] = []
        for task in os.listdir(path_to_round / Path(str(category_name))):
            tasks.append(
                Task(point_count=int(str(task)),
                     handler=default_handler(
                         round_ind=round, category_name=str(category_name), task_name=str(task)))
            )
        categories.append(
            Category(
                name=str(category_name),
                tasks=sorted(tasks, key=lambda t: t.point_count)
            )
        )
    return categories
