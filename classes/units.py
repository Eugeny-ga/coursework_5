from dataclasses import dataclass

from classes.baseskill import BaseSkill
from classes.skills import DivinePower, BackBlow, FuryPunch


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: BaseSkill

Warrior = UnitClass(
    name='Воин',
    max_health=40.0,
    max_stamina=32.0,
    attack=1.0,
    stamina=1.2,
    armor=1.1,
    skill=FuryPunch()
)

Thief = UnitClass(
    name='Вор',
    max_health=30.0,
    max_stamina=26.0,
    attack=1.2,
    stamina=1.4,
    armor=1.0,
    skill=BackBlow()
)

Dwarf = UnitClass(
    name='Гном',
    max_health=35.0,
    max_stamina=35.0,
    attack=1.1,
    stamina=1.3,
    armor=1.2,
    skill=DivinePower()
)

units = {
    Thief.name: Thief,
    Warrior.name: Warrior,
    Dwarf.name: Dwarf
}