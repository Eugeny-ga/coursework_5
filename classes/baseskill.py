from abc import ABC

class BaseSkill(ABC):
    user = NotImplemented
    target = NotImplemented
    _name: str
    _stamina: float
    _damage: float

    @property
    def name(self) -> str:
        return self._name

    @property
    def stamina(self) -> float:
        return self._stamina

    @property
    def damage(self) -> float:
        return self._damage


    def skill_effect(self) -> str:
        """Возвращает результат выполнения навыка"""
        self.user.stamina = round(self.user.stamina_points - self.stamina, 1)

        if self.target.health_points <= self.damage:
            self.target.hp = 0
        else:
            self.target.hp = round(self.target.health_points - self.damage, 1)
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику."

    def _is_stamina_enough(self) -> bool:
        """Проверка, хватает ли ловкости"""
        return self.user.stamina_points >= self.stamina

    def use(self, user, target) -> str:
        """Возвращает результат использования (или не использования) навыка героем"""

        self.user = user
        self.target = target
        if self._is_stamina_enough():
            self.user._is_skill_used = True
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name}, но у него не хватило выносливости."
