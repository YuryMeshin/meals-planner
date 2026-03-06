from dataclasses import dataclass
from functools import cached_property
from enum import Enum
from units import Unit, NutritionUnit
from ingredients import Ingredient


class MealKind(Enum):
    FIRST_BREAKFAST = 0
    SECOND_BREAKFAST = 1
    LUNCH = 2
    DINNER = 3


@dataclass(frozen=True)
class Recipe():
    INGREDIENTS: tuple[tuple[Ingredient, float]]
    KIND: MealKind
    PREP_TIME: int
    TAGS: tuple[str]

    @cached_property 
    def NUTRITION(self) -> NutritionUnit:
        return sum(
            (ingredient.NUTRITION * qty for ingredient, qty in self.INGREDIENTS),
            start=NutritionUnit.zero()
            )


if __name__ == "__main__":
    ntr = NutritionUnit._ZERO
    ing = Ingredient(NAME="tmp", NUTRITION=ntr, UNIT=Unit(0, "NULL"))
    print(ing.as_dict())
