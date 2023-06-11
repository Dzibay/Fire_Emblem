from data.weapon import weapon, weapon_have_triangle_bonus, weapon_effective
from data.classes import types


def types_class(class_):
    for type_ in types:
        if class_ in types[type_]:
            return type_
    return None


def calculate_damage(triangle, person, enemy):
    if person.weapon in weapon_have_triangle_bonus:
        bonus = 2
    else:
        if triangle(person.weapon.name, enemy.weapon.name) is None:
            bonus = 0
        elif triangle(person.weapon.name, enemy.weapon.name):
            bonus = 1
        else:
            bonus = -1

        if person.weapon.class_ != 'magic' or enemy.weapon.class_ != 'magic':
            if person.weapon.class_ == enemy.weapon.class_:
                bonus = 0
        else:
            if weapon[person.weapon.name]['subclass'] == weapon[enemy.weapon.name]['subclass']:
                bonus = 0

    effective = 1
    if types_class(enemy.class_) is None:
        pass
    elif person.weapon.name in weapon_effective[types_class(enemy.class_)]:
        effective = 2
    dmg = (person.dmg + bonus) * effective
    def_ = enemy.res if person.weapon.class_ == 'magic' else enemy.def_
    return dmg - def_