from typing import Any, Self
from dataclasses import dataclass, fields


@dataclass(frozen=True)
class Unit():
    QUANTITY: float
    UNIT: str

    def __add__(self, other: Self) -> Self:
        if not isinstance(other, type(self)):
            return NotImplemented
        if self.UNIT != other.UNIT:
            raise ValueError(f"Incomparable units '{self.UNIT}', '{other.UNIT}'")
        return type(self)(QUANTITY=self.QUANTITY + other.QUANTITY, UNIT=self.UNIT)
    
    def __mul__(self, quantity: float) -> Self:
        if quantity < 0:
            raise ValueError(f"Negative quantities are not allowed but given {quantity}")
        return type(self)(QUANTITY=self.QUANTITY * quantity, UNIT=self.UNIT)
    
    @classmethod
    def from_tuple(cls, unit_tuple: tuple[float, str]) -> Self:
        quantity, unit = unit_tuple
        if quantity < 0:
            raise ValueError(f"Negative quantities are not allowed but {quantity} given")
        return cls(QUANTITY=quantity, UNIT=unit)
    
    @classmethod
    def from_dict(cls, unit_dict: dict[str, Any]) -> Self:
        expected, provided = {"QUANTITY", "UNIT"}, set(unit_dict.keys())
        _missed, _extra = expected - provided, provided - expected
        if _missed | _extra:
            raise ValueError(
                f"Incompatible dict given. Missing: {_missed or None}, Extra: {_extra or None}"
                )
        return cls(**unit_dict)
    
    def as_dict(self) -> dict[str, Any]:
        return {
            "QUANTITY": self.QUANTITY,
            "UNIT": self.UNIT
        }
    
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

    def as_dict(self) -> dict[str, float]:
        return {key: self[key] for key in type(self)._FIELDS}

    @classmethod
    def from_dict(cls, nutrients: dict[str, float]) -> NutritionUnit:
        expected, provided = set(cls._FIELDS), set(nutrients.keys())
        if provided != expected:
            missing, extra = expected - provided, provided - expected
            raise ValueError(
                f"Nutrition schema mismatch.\nMissing: {missing or None}, Extra: {extra or None}"
            )
        return cls(**nutrients)
    
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
        if quantity < 0:
            raise ValueError(
                f"Negative quantities are not allowed but value {quantity} given"
                )
        return type(self)(**{key: self[key] * quantity for key in type(self)._FIELDS})

    @classmethod
    def zero(cls) -> Self:
        return cls._ZERO

    def __str__(self) -> str:
        return "\n".join(f"{f}: {self[f]:.3f}" for f in type(self)._FIELDS)


NutritionUnit._FIELDS = tuple(f.name for f in fields(NutritionUnit))
NutritionUnit._ZERO = NutritionUnit(**{f: 0 for f in NutritionUnit._FIELDS})
