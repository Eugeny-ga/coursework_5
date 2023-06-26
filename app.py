from typing import Type

from flask import Flask, render_template, request, redirect, abort
from flask_session import Session

from classes.arena import Arena
from classes.baseunit import BaseUnit
from classes.enemy import EnemyUnit
from classes.player import PlayerUnit
from classes.units import units
from classes.equipment import Equipment

app = Flask(__name__)

Session(app)

equip = Equipment()
arena = Arena()
heroes = {
    'player': Type[BaseUnit],
    'enemy': Type[BaseUnit],
}



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/choose-hero/', methods=['GET', 'POST'])
def choose_hero():
    if request.method == 'POST':
        name = request.form.get('name')
        unit_class = request.form.get('unit_class')
        weapon = request.form.get('weapon')
        armor = request.form.get('armor')

        if None in (unit_class, weapon, armor):
            abort(400)

        player = PlayerUnit(name=name, unit_class=units[unit_class])
        player.equip_weapon(equip.get_weapon(weapon))
        player.equip_armor(equip.get_armor(armor))
        heroes['player'] = player

        return redirect('/choose-enemy/', 302)

    result = {
        "header": 'Выберите имя!',
        "classes": units.keys(),
        "weapons": equip.get_weapons_names(),
        "armors": equip.get_armors_names()
    }
    return render_template('hero_choosing.html', result=result)


@app.route('/choose-enemy/', methods=['GET', 'POST'])
def choose_enemy():
    if request.method == 'POST':
        name = request.form.get('name')
        unit_class = request.form.get('unit_class')
        weapon = request.form.get('weapon')
        armor = request.form.get('armor')

        if None in (unit_class, weapon, armor):
            abort(400)

        enemy = EnemyUnit(name=name, unit_class=units[unit_class])
        enemy.equip_weapon(equip.get_weapon(weapon))
        enemy.equip_armor(equip.get_armor(armor))
        heroes['enemy'] = enemy

        return redirect('/fight/', 302)

    result = {
        "header": 'Выберите соперника!',
        "classes": units.keys(),
        "weapons": equip.get_weapons_names(),
        "armors": equip.get_armors_names()
    }
    return render_template('hero_choosing.html', result=result)


@app.route('/fight/')
def fight():
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])

    return render_template('fight.html', heroes=heroes)


@app.route('/fight/hit')
def hit():
    result = arena.player_hit()

    return render_template('fight.html', heroes=heroes, result=result)


@app.route('/fight/use-skill')
def use_skill():
    result = arena.player_use_skill()

    return render_template('fight.html', heroes=heroes, result=result)


@app.route('/fight/pass-turn')
def skip_turn():
    if arena.game_is_running:
        result = f"{heroes['player'].name} пропускает ход!" + arena.next_turn()
        return render_template('fight.html', heroes=heroes, result=result)

    return redirect('/fight/end-fight', 302)


@app.route('/fight/end-fight')
def end():
    result = arena.stop_game()

    return render_template('fight.html', heroes=heroes, result=result)


if __name__ == '__main__':
    app.run()
