from typing import Any, Self
from dataclasses import dataclass
from enum import Enum
from units import NutritionUnit
from utils import args_cast


class MealKind(Enum):
    FIRST_BREAKFAST = 0
    SECOND_BREAKFAST = 1
    LUNCH = 2
    DINNER = 3


@dataclass(frozen=True)
class Recipe():
    INGREDIENTS: dict[str, float]
    KIND: MealKind
    PREP_TIME: int
    TAGS: tuple[str, ...]
 
    def nutrition(self, mapper) -> NutritionUnit:
        return sum(
            (mapper[key].NUTRITION * quantity for key, quantity in self.INGREDIENTS.items()),
            start=NutritionUnit.zero()
            )
    
    def as_dict(self) -> dict[str, Any]:
        return {
            "INGREDIENTS": {key: self.INGREDIENTS[key] for key in sorted(self.INGREDIENTS)},
            "KIND": self.KIND.name,
            "PREP_TIME": self.PREP_TIME,
            "TAGS": sorted(self.TAGS)
            }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        args = args_cast(RECIPE_SCHEMA, data)
        args["KIND"] = MealKind[args["KIND"]]
        return cls(**args)

    
RECIPE_SCHEMA = {
    "INGREDIENTS": ("INGREDIENTS", dict),
    "KIND": ("KIND", str),
    "PREP_TIME": ("PREP_TIME", float),
    "TAGS": ("TAGS", tuple)
}
