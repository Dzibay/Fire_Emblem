from data.weapon import weapon, weapon_have_triangle_bonus


def triangle(weapon_1, weapon_2):
    if weapon_1 in weapon_have_triangle_bonus:
        return True
    else:
        if weapon_1 == weapon_2:
            return None
        if weapon[weapon_1]['class'] == 'magic' and weapon[weapon_2]['class'] == 'magic':
            weapon_1 = weapon[weapon_1]['subclass']
            weapon_2 = weapon[weapon_2]['subclass']
            if weapon_1 == 'dark':
                if weapon_2 == 'anima':
                    return True
                elif weapon_2 == 'light':
                    return False
            elif weapon_1 == 'anima':
                if weapon_2 == 'light':
                    return True
                elif weapon_2 == 'dark':
                    return False
            elif weapon_1 == 'light':
                if weapon_2 == 'dark':
                    return True
                elif weapon_2 == 'anima':
                    return False
        else:
            weapon_1 = weapon[weapon_1]['class']
            weapon_2 = weapon[weapon_2]['class']
            if weapon_1 == 'sword':
                if weapon_2 == 'axe':
                    return True
                elif weapon_2 == 'lance':
                    return False
            elif weapon_1 == 'axe':
                if weapon_2 == 'lance':
                    return True
                elif weapon_2 == 'sword':
                    return False
            elif weapon_1 == 'lance':
                if weapon_2 == 'sword':
                    return True
                elif weapon_2 == 'axe':
                    return False
    return None