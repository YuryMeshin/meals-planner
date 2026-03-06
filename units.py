from typing import Any
from dataclasses import dataclass, fields


@dataclass(frozen=True)
class Unit():
    QUANTITY: float
    UNIT: str

    def __add__(self, other: Unit) -> Unit:
        if self.UNIT != other.UNIT:
            raise ValueError(f"Incomparable units '{self.UNIT}', '{other.UNIT}'")
        return Unit.from_tuple((self.QUANTITY + other.QUANTITY, self.UNIT))
    
    def __mul__(self, factor: float) -> Unit:
        if factor < 0:
            raise ValueError("Negative quantities are not allowed")
        return Unit.from_tuple((self.QUANTITY * factor, self.UNIT))
    
    @classmethod
    def from_tuple(cls, unit_tuple: tuple[float, str]) -> Unit:
        if unit_tuple[0] <= 0:
            raise ValueError(f"Negative quantities are not allowed but {unit_tuple[0]} given")
        return Unit(QUANTITY=unit_tuple[0], UNIT=unit_tuple[1])
    
    @classmethod
    def from_dict(cls, unit_dict: dict[str, Any]) -> Unit:
        _missed = {"QUANTITY", "UNIT"} - set(unit_dict.keys())
        _extra = set(unit_dict.keys()) - {"QUANTITY", "UNIT"}
        if _missed | _extra:
            raise ValueError(
                f"Incompatible dict given. Missing: {_missed or None}, Extra: {_extra or None}"
                )
        return Unit(**unit_dict)
    
    def as_dict(self) -> dict[str, Any]:
        return {
            "QUANTITY": self.QUANTITY,
            "UNIT": self.UNIT
        }
    
    def __str__(self) -> str:
        return f"{self.QUANTITY:.3f} {self.UNIT}(s)"


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

    @staticmethod
    def zero() -> NutritionUnit:
        return NutritionUnit._ZERO


NutritionUnit._FIELDS = frozenset(f.name for f in fields(NutritionUnit))
NutritionUnit._ZERO = NutritionUnit.from_dict({f: 0 for f in NutritionUnit._FIELDS})
