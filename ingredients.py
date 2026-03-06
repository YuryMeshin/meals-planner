import json
from pathlib import Path
from typing import Any, Union
from dataclasses import dataclass, fields
from functools import cached_property
from enum import Enum
from units import Unit, NutritionUnit


@dataclass(frozen=True)
class Ingredient():
    NAME: str
    NUTRITION: NutritionUnit
    UNIT: Unit

    def as_dict(self) -> dict[str, Any]:
        return {
            "NAME": self.NAME,
            "NUTRITION": self.NUTRITION.as_dict(),
            "UNIT": self.UNIT.as_dict()
        }

    @classmethod
    def from_dict(cls, ingredient: dict[str, Any]) -> Ingredient:
        if "NAME" not in ingredient:
            raise ValueError("No name for ingredient given")
        
        for key in ("NUTRITION", "UNIT"):
            if key not in ingredient:
                raise ValueError(f"No {key.lower()} for ingredient given")
            if not isinstance(ingredient[key], dict):
                raise ValueError(f"Cannot extract {key.lower()} from non-dict")
            
        return cls(
            NAME=str(ingredient["NAME"]), 
            NUTRITION=NutritionUnit.from_dict(ingredient["NUTRITION"]),
            UNIT=Unit.from_dict(ingredient["UNIT"])
            )


class IngredientsBook():

    def __init__(self, ingredients: dict[int, Ingredient]):
        self._ingredients = ingredients

    def as_dict(self):
        return {key: ing.as_dict() for key, ing in self._ingredients.items()}
    
    def append(self, ingredient: Ingredient):
        self._ingredients[len(self._ingredients)] = ingredient

    @classmethod
    def from_dict(cls, book: dict[str, dict[str, Any]]) -> IngredientsBook:
        return cls({int(key): Ingredient.from_dict(ing) for key, ing in book.items()})
