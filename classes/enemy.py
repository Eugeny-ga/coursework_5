import random

from classes.baseunit import BaseUnit


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if not self._is_skill_used:
            skill_chance = random.randint(1, 100)
            if skill_chance < 11:
                return self.use_skill(target)
        damage = self._count_damage(target)

        if damage is None:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        if damage > 0:
            return f"{self.name}, используя {self.weapon.name}, пробивает {target.armor.name} и наносит {damage} урона."

        else:
            return f"{self.name}, используя {self.weapon.name}, наносит удар, но {target.armor.name} его останавливает."

