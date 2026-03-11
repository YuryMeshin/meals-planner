from typing import Any
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
class RecipeIngredient():
    INGREDIENT: Ingredient
    QUANTITY: float

    def as_dict(self) -> dict[str, float]:
        return {self.INGREDIENT.id: self.QUANTITY}


@dataclass(frozen=True)
class Recipe():
    INGREDIENTS: tuple[RecipeIngredient, ...]
    KIND: MealKind
    PREP_TIME: int
    TAGS: tuple[str, ...]

    @cached_property 
    def NUTRITION(self) -> NutritionUnit:
        return sum(
            (r.INGREDIENT.NUTRITION * r.QUANTITY for r in self.INGREDIENTS),
            start=NutritionUnit.zero()
            )
    
    def as_dict(self) -> dict[str, Any]:
        return {
            "INGREDIENTS": [ingr.as_dict() for ingr in self.INGREDIENTS],
            "KIND": self.KIND.name,
            "PREP_TIME": self.PREP_TIME,
            "TAGS": sorted(self.TAGS)
            }


if __name__ == "__main__":
    ntr = NutritionUnit._ZERO
    ing = Ingredient(NAME="tmp", NUTRITION=ntr, UNIT=Unit(0, "NULL"))
    print(ing.as_dict())
