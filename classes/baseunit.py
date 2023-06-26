from abc import ABC, abstractmethod

from classes.equipment import Weapon, Armor
from classes.units import UnitClass

class BaseUnit(ABC):
    def __init__(self, name: str, unit_class: UnitClass):
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon: Weapon
        self.armor: Armor
        self._is_skill_used = False

    @property
    def health_points(self) -> float:
        return self.hp

    @property
    def stamina_points(self) -> float:
        return self.stamina

    def equip_weapon(self, weapon: Weapon) -> None:
        self.weapon = weapon

    def equip_armor(self, armor: Armor) -> None:
        self.armor = armor

    def _count_damage(self, target) -> float | None:
        if self.stamina_points < self.weapon.stamina_per_hit:
            return None

        damage = round(self.weapon.damage * self.unit_class.attack, 1)
        self.stamina = round(self.stamina_points - self.weapon.stamina_per_hit, 1)

        if target.stamina_points >= target.armor.stamina_per_turn:
            defence = round(target.armor.defence * target.unit_class.armor, 1)
            target.stamina = round(target.stamina_points - target.armor.stamina_per_turn, 1)
        else:
            defence = 0

        damage = round(damage - defence, 1)
        target.get_damage(damage)
        return damage


    def get_damage(self, damage: float) -> None:
        if damage > 0:
            if self.hp - damage >= 0:
                self.hp = round(self.hp - damage, 1)
            else:
                self.hp = 0

    @abstractmethod
    def hit(self, target) -> str:
        pass

    def use_skill(self, target) -> str:
        if self._is_skill_used:
            return 'Навык уже использован.'

        return self.unit_class.skill.use(user=self, target=target)