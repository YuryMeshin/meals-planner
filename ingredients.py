from typing import Any, Self
from dataclasses import dataclass
from units import Unit, NutritionUnit
from utils import args_cast


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


INGREDIENT_SCHEMA = {
    "NAME": ("NAME", str),
    "NUTRITION": ("NUTRITION", dict),
    "UNIT": ("UNIT", dict)
}
