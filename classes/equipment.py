import json
from dataclasses import dataclass
from random import uniform
import marshmallow.exceptions
import marshmallow_dataclass

from config import EQUIP_DATA


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float

@dataclass
class Weapon:
    id: int
    name: str
    max_damage: float
    min_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return round(uniform(self.min_damage, self.max_damage), 1)

@dataclass
class EquipmentData:
    armors: list[Armor]
    weapons: list[Weapon]

class Equipment:
    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        '''Возвращает объект оружия по имени'''
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon
        raise NotImplementedError

    def get_armor(self, armor_name) -> Armor:
        """Возвращает объект брони по имени"""
        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor
        raise NotImplementedError

    def get_weapons_names(self) -> list[str]:
        """Возвращает список достопного оружия"""
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list[str]:
        """Возвращает список доступной брони"""
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        """Загружает данные из JSON и возвращает объект EquipmentData,
        который содержит список объектов брони и список объектов оружия."""
        with open(EQUIP_DATA, 'r', encoding='utf-8') as file:
            data = json.load(file)

        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)

        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError


