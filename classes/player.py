from classes.baseunit import BaseUnit


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:

        damage = self._count_damage(target)

        if damage is None:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        if damage > 0:
            return f"{self.name}, используя {self.weapon.name}, пробивает {target.armor.name} и наносит {damage} урона."

        else:
            return f"{self.name}, используя {self.weapon.name}, наносит удар, но {target.armor.name} его останавливает."
