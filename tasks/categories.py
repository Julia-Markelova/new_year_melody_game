import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from config.paths import MELODIES_PATH

QUESTION_NAME = 'question.mp3'
ANSWER_NAME = 'answer.mp3'


@dataclass
class Task:
    point_count: int
    category_name: str
    path_to_question: str
    path_to_answer: str
    answer: str


@dataclass
class Category:
    name: str
    tasks: List[Task]


class Round:
    def __init__(self, index: int, categories: List[Category]):
        if index > 5:
            raise ValueError('Unsupported round index. Max 5.')
        self.index: int = index
        self.categories: List[Category] = categories

    def get_name(self) -> str:
        dec_to_rome = {
            1: 'I',
            2: 'II',
            3: 'III',
            4: 'IV',
            5: 'V',
        }
        return f'Раунд {dec_to_rome[self.index]}'


def configure_rounds() -> List[Round]:
    path_to_round = Path(f'{MELODIES_PATH}')
    if not path_to_round.exists():
        raise AssertionError(f'Path for melodies does not exests in {MELODIES_PATH}')
    rounds: List[Round] = []

    for i, round_path in enumerate(sorted(os.listdir(path_to_round)), start=1):
        categories: List[Category] = []
        for category_name in os.listdir(path_to_round / Path(str(round_path))):
            tasks: List[Task] = []
            for task in os.listdir(path_to_round / Path(str(round_path)) / Path(str(category_name))):
                path_to_task = path_to_round / Path(str(round_path)) / Path(str(category_name)) / Path(str(task))
                tasks.append(
                    Task(
                        point_count=int(str(task)),
                        category_name=category_name,
                        path_to_question=str(path_to_task / Path(QUESTION_NAME)),
                        path_to_answer=str(path_to_task / Path(ANSWER_NAME)),
                        answer='',
                    )
                )
            categories.append(
                Category(
                    name=str(category_name),
                    tasks=sorted(tasks, key=lambda t: t.point_count)
                )
            )
        rounds.append(
            Round(
                index=i,
                categories=sorted(categories, key=lambda c: c.name)
            )
        )
    return sorted(rounds, key=lambda r: r.index)
