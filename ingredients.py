import json
import hashlib
from typing import Any, Self
from dataclasses import dataclass
from functools import cached_property
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
    def from_dict(cls, ingredient: dict[str, Any]) -> Self:
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
    
    @cached_property
    def id(self) -> str:
        json_str = json.dumps(self.as_dict(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(json_str.encode("utf-8")).hexdigest()


class IngredientsBook():

    def __init__(self, ingredients: dict[str, Ingredient]):
        self._ingredients = ingredients

    def as_dict(self):
        return {key: ing.as_dict() for key, ing in self._ingredients.items()}
    
    def append(self, ingredient: Ingredient):
        if ingredient.id in self._ingredients:
            return
        self._ingredients[ingredient.id] = ingredient

    @classmethod
    def from_dict(cls, book: dict[str, dict[str, Any]]) -> Self:
        return cls({key: Ingredient.from_dict(ing) for key, ing in book.items()})
