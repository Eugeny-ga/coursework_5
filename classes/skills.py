from classes.baseskill import BaseSkill


class FuryPunch(BaseSkill):
    """Навык воина"""
    _name = "Яростный удар"
    _stamina = 6.0
    _damage = 12.0

class BackBlow(BaseSkill):
    """Навык вора"""

    _name = "Ответный удар"
    _stamina = 4.0
    _damage = 9.0

class DivinePower(BaseSkill):
    """Навык гнома"""

    _name = "Божественная сила"
    _stamina = 5.0
    _damage = 15.0