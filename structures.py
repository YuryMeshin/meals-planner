import json
from pathlib import Path
from typing import Any, Union
from dataclasses import dataclass, fields
from functools import cached_property


@dataclass(frozen=True)
class NutritionUnit():
    CALORIES: float
    PROTEIN: float
    CARBS: float
    FATS: float
    FIBER: float
    SUGAR: float
    SODIUM: float
    SATURATED_FAT: float

    def as_dict(self) -> dict[str, float]:
        return {key: self[key] for key in self._FIELDS}

    @classmethod
    def from_dict(cls, nutrients: dict[str, float]) -> NutritionUnit:
        expected = cls._FIELDS
        provided = set(nutrients.keys())

        if provided != expected:
            missing = expected - provided
            extra = provided - expected
            raise ValueError(
                f"Nutrition schema mismatch. "
                f"Missing: {missing or None}, Extra: {extra or None}"
            )

        return cls(**nutrients)
    
    def __getitem__(self, key: str) -> float:
        expected = self._FIELDS
        if  key not in expected:
            raise KeyError(f"No such nutrient component: '{key}'")
        return getattr(self, key)

    def __add__(self, other: NutritionUnit) -> NutritionUnit:
        if not isinstance(other, NutritionUnit):
            return NotImplemented
        return NutritionUnit.from_dict({key: self[key] + other[key] for key in self._FIELDS})
    
    def __mul__(self, quantity: float) -> NutritionUnit:
        if quantity <= 0:
            raise ValueError(
                "Given value of quantity must be positive"
                f"Value of {quantity} given")
        return NutritionUnit.from_dict({key: self[key] * quantity for key in self._FIELDS})


NutritionUnit._FIELDS = frozenset(f.name for f in fields(NutritionUnit))


@dataclass(frozen=True)
class Ingredient():
    NAME: str
    NUTRITION: NutritionUnit

    def to_dict(self) -> dict[str, Any]:
        return {
            "NAME": self.NAME,
            "NUTRITION": self.NUTRITION.as_dict()
        }

    @classmethod
    def from_dict(cls, ingredient: dict[str, Any]) -> Ingredient:
        if "NAME" not in ingredient:
            raise ValueError("No name for ingredient given")
        _name = str(ingredient["NAME"])
        
        if "NUTRITION" not in ingredient:
            raise ValueError("No nutrition for ingredient given")
        if not isinstance(ingredient["NUTRITION"], dict):
            raise ValueError("Cannot extract nutrition from non-dict")
        
        return cls(NAME=_name, NUTRITION=NutritionUnit.from_dict(ingredient["NUTRITION"]))


class IngredientsBook():

    def __init__(self, ingredients: dict[int, Ingredient]):
        self._ingredients = ingredients

    def to_json(self, dest: Union[str, Path]):
        with open(dest, "w") as stream:
            json.dump({key: ing.to_dict() for key, ing in self._ingredients.items()}, stream, indent=4)
    
    def append(self, ingredient: Ingredient):
        self._ingredients[len(self._ingredients)] = ingredient

    @classmethod
    def from_json(cls, source: Union[str, Path]) -> IngredientsBook:
        with open(source, "r") as stream:
            return cls({int(key): Ingredient.from_dict(ing) for key, ing in json.load(stream).items()})


# nutrients = {
#     "Calories": ["lower", "upper"],
#     "Protein": ["lower", "upper"],
#     "Carbs": ["lower", "upper"],
#     "Fats": ["lower", "upper"],
#     "Fiber": ["lower", "upper"],
#     "Sugar": ["upper"],
#     "Sodium": ["upper"],
#     "Saturated-Fat": ["upper"]
#     }

# with open("nutrients-schema.json", "w") as stream:
#     json.dump({key.upper(): [x.upper() for x in nutrients[key]] for key in nutrients}, stream, indent=4)

if __name__ == "__main__":
    ntr = NutritionUnit(
        CALORIES=0, 
        PROTEIN=0,
        CARBS=0,
        FATS=0,
        FIBER=0,
        SUGAR=0,
        SODIUM=0,
        SATURATED_FAT=0)
    ing = Ingredient(NAME="tmp", NUTRITION=ntr)
    print(ing.to_dict())