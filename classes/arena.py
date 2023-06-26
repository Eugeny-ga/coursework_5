from classes.baseunit import BaseUnit


class BaseSingleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player: BaseUnit
    enemy: BaseUnit
    game_is_running = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        """
        Начало игры
        """
        self.game_is_running = True
        self.player = player
        self.enemy = enemy

    def stop_game(self) -> str:
        """
        Конец
        Returns:
            text stating that the battle is over
        """
        return self._end_game()

    def _check_players_hp(self) -> str | None:
        """
        Проверка здоровья героя. Возвращает результат битвы или None
        """
        match (self.player.health_points > 0, self.enemy.health_points > 0):
            case (False, False):
                return 'Ничья!<br>'
            case (True, False):
                return f'{self.player.name} выиграл битву!'
            case (False, True):
                return f'{self.player.name} проиграл битву!'
            case _:
                return None

    def _stamina_regeneration(self) -> None:
        """
        Восстановление выносливости у обоих игроков
        """
        for hero in (self.player, self.enemy):
            calc_stamina_to_add = round(self.STAMINA_PER_ROUND * hero.unit_class.stamina, 1)
            if hero.stamina + calc_stamina_to_add <= hero.unit_class.max_stamina:
                hero.stamina = round(hero.stamina + calc_stamina_to_add, 1)
            else:
                hero.stamina = hero.unit_class.max_stamina

    def next_turn(self) -> str:
        """
        Проверка очков здоровья обоих игроков
        Восстановление выносливости для обоих игроков.
        Возвращается:
            результат действий и/или "игра окончена"
        """
        result = self.enemy.hit(self.player)
        if (battle_result := self._check_players_hp()) is not None:
            return result + battle_result + self._end_game()
        self._stamina_regeneration()
        return result

    def player_hit(self) -> str:
        """
        Игрок нажал действие.
        Проверка, запущена ли игра, игрок наносит удар, и ход передается противнику.
        Возвращается результат действий или "игра уже окончена"
        """
        if not self.game_is_running:
            return 'Битва уже окончена!'

        result = self.player.hit(self.enemy)
        result += self.next_turn()
        return result

    def player_use_skill(self) -> str:
        """
        Действие игрока с использованием навыка.
        Возвращается результат действий или "игра уже окончена"
        """
        if not self.game_is_running:
            return 'Битва уже окончена!'

        result = self.player.use_skill(self.enemy)
        result += self.next_turn()
        return result

    def _end_game(self) -> str:
        """
        Очистка арены и остановка битвы.
        Возвращается результат действий или "игра уже окончена"
        """
        if not self.game_is_running:
            return 'Битва уже окончена!'

        self._instances: dict = {}
        self.game_is_running = False
        return 'Битва окончена!'


