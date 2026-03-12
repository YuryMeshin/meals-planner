from typing import Any, Self
from dataclasses import dataclass, fields
from enum import Enum
from utils import args_cast


@dataclass(frozen=True)
class Unit():
    QUANTITY: float
    UNIT: str

    def __post_init__(self):
        if self.QUANTITY < 0:
            _template = "Negative quantities are not allowed but given {}"
            raise ValueError(_template.format(self.QUANTITY))

    def __add__(self, other: Self) -> Self:
        if not isinstance(other, type(self)):
            return NotImplemented
        if self.UNIT != other.UNIT:
            raise ValueError(f"Incomparable units '{self.UNIT}', '{other.UNIT}'")
        return type(self)(QUANTITY=self.QUANTITY + other.QUANTITY, UNIT=self.UNIT)
    
    def __mul__(self, quantity: float) -> Self:
        return type(self)(QUANTITY=self.QUANTITY * quantity, UNIT=self.UNIT)
    
    @classmethod
    def from_tuple(cls, unit_tuple: tuple[float, str]) -> Self:
        quantity, unit = unit_tuple
        return cls(QUANTITY=quantity, UNIT=unit)
    
    @classmethod
    def from_dict(cls, unit_dict: dict[str, Any]) -> Self:
        return cls(**args_cast(UNIT_SCHEMA, unit_dict))
    
    def as_dict(self) -> dict[str, Any]:
        return {"QUANTITY": self.QUANTITY, "UNIT": self.UNIT}
    
    def __str__(self) -> str:
        return f"{self.QUANTITY:.3f} {self.UNIT}"


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

    def __post_init__(self):
        for f in self._FIELDS:
            value = getattr(self, f)
            if value < 0:
                _template = "Negative nutrients are not allowed but given '{}' is set {}"
                raise ValueError(_template.format(f, value))

    def as_dict(self) -> dict[str, float]:
        return {key: self[key] for key in type(self)._FIELDS}

    @classmethod
    def from_dict(cls, nutrients: dict[str, float]) -> Self:
        return cls(**args_cast(NUTRITION_SCHEMA, nutrients))
    
    def __getitem__(self, key: str) -> float:
        expected = type(self)._FIELDS
        if  key not in expected:
            raise KeyError(f"No such nutrient component: '{key}'")
        return getattr(self, key)

    def __add__(self, other: Self) -> Self:
        if not isinstance(other, type(self)):
            return NotImplemented
        return type(self)(**{key: self[key] + other[key] for key in type(self)._FIELDS})
    
    def __mul__(self, quantity: float) -> Self:
        return type(self)(**{key: self[key] * quantity for key in type(self)._FIELDS})

    @classmethod
    def zero(cls) -> Self:
        return cls._ZERO

    def __str__(self) -> str:
        return "\n".join(f"{f}: {self[f]:.3f}" for f in type(self)._FIELDS)


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
        args = args_cast(INGREDIENT_SCHEMA, ingredient)
        args["NUTRITION"] = NutritionUnit.from_dict(args["NUTRITION"])
        args["UNIT"] = Unit.from_dict(args["UNIT"])
        return cls(**args)


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

    
NutritionUnit._FIELDS = tuple(f.name for f in fields(NutritionUnit))
NutritionUnit._ZERO = NutritionUnit(**{f: 0 for f in NutritionUnit._FIELDS})

NUTRITION_SCHEMA = {f: (f, float) for f in NutritionUnit._FIELDS}

UNIT_SCHEMA = {
    "QUANTITY": ("QUANTITY", float), 
    "UNIT": ("UNIT", str)
}

INGREDIENT_SCHEMA = {
    "NAME": ("NAME", str),
    "NUTRITION": ("NUTRITION", dict),
    "UNIT": ("UNIT", dict)
}

RECIPE_SCHEMA = {
    "INGREDIENTS": ("INGREDIENTS", dict),
    "KIND": ("KIND", str),
    "PREP_TIME": ("PREP_TIME", float),
    "TAGS": ("TAGS", tuple)
}
