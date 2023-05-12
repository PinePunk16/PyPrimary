# person.py
# Example of implementation of "Instance".

from enum import Enum
import random


from pyprimary.instance import Instance



class Life_stage(Enum):
    BABY = 0
    CHILD = 1
    TEEN = 2
    ADULT = 3
    ELDER = 4

class Person(Instance):
    def __init__(self) -> None:
        super().__init__("people")
        
        self.name: str = ""
        self.life_stage_: Life_stage = None
        self.days_in_life_stage: int = 0
    def generate(self) -> None:
        super().generate()
        
        self.life_stage_ = random.choice(list(Life_stage))
        