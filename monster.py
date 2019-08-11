'''
This package contains functions and methods for simulating
combat between 3rd edition D&D monsters.
'''

# TODO: Test with mypy package

from random import randint
from typing import Dict, List
from mon_enum_types import *

# TODO look into handling value=0 case
def ability_mod(ability_score: int) -> int:
    '''
    Function to calculate the ability modifier from the ability score.

    PARAMETERS
    ability_score: The ability score (int).
    '''
    return (ability_score - 10) // 2

def size_mod(size: Size, category: str) -> int:
    '''
    Function to lookup a monster's size modifier for
    attack and AC.

    PARAMETERS
    size: The size category of the monster (Size).
    category: The type of size modifier (str).
    '''
    if category in ('Attack', 'AC'):
        lookup = {Size.COLOSSAL:-8,
                  Size.GARGANTUAN:-4,
                  Size.HUGE:-2,
                  Size.LARGE:-1,
                  Size.MEDIUM:0,
                  Size.SMALL:1,
                  Size.TINY:2,
                  Size.DIMUNITIVE:4,
                  Size.FINE:8}
    elif category in ('Bull Rush', 'Grapple', 'Overrun', 'Trip', 'Special'):
        lookup = {Size.COLOSSAL:16,
                  Size.GARGANTUAN:12,
                  Size.HUGE:8,
                  Size.LARGE:4,
                  Size.MEDIUM:0,
                  Size.SMALL:-4,
                  Size.TINY:-8,
                  Size.DIMUNITIVE:-12,
                  Size.FINE:-16}
    elif category in ('Hide'):
        lookup = {Size.COLOSSAL:-16,
                  Size.GARGANTUAN:-12,
                  Size.HUGE:-8,
                  Size.LARGE:-4,
                  Size.MEDIUM:0,
                  Size.SMALL:4,
                  Size.TINY:8,
                  Size.DIMUNITIVE:12,
                  Size.FINE:16}
    return lookup[size]

def attack(attacker, attackee, attack):
    '''
    Calculate whether an attacking monster hits a target monster with
    a given attack.

    PARAMETERS
    attacker: The object of the attacking monster.
    attackee: The object of the attacked monster.
    attack: The object of the attack used by the attacker.
    '''
    attack_roll = randint(1, 20)
    if attack_roll == 1:
        pass
    elif attack_roll == 20:
        if randint(1, 20) +\
           ability_mod(attacker.abilities[attack.ability])\
         >= attackee.get_AC():
            attackee.hit_points -= 2 * max(1, sum([sum([randint(1, i) for j in range(attack.damage[i])]) for i in attack.damage]))
    elif attack_roll +\
         ability_mod(attacker.abilities[attack.ability])\
         >= attackee.get_AC():
        attackee.hit_points -= max(1, sum([sum([randint(1, i) for j in range(attack.damage[i])]) for i in attack.damage]))
    else:
        pass
    
class Attack:
    '''
    Object that defines a monster's attack.
    '''
    def __init__(self,
                 name: str,
                 ability: Ability,
                 bonus: int,
                 damage: Dict[int, int],
                 crit_range: List[int] = None,
                 crit_multiplier: int = None):
        '''
        Method that defines a monster's attack.

        PARAMETERS
        name: The name of the attack (str).
        ability: The primary ability for the attack (Ability).
        bonus: The bonus applied to the attack roll (int).
        damage: The damage applied to target (Dict).
        '''
        self.name: str = name
        self.ability: Ability = ability
        self.bonus: int = bonus
        self.damage: Dict[int, int] = damage

# Example of a union: List[Union[Attack, int]]
# Optional[int], which is equiv to Union[None, int]


class Monster:
    '''
    Object that defines a monster.
    '''
    
    def __init__(self,
                 size: Size,
                 abilities: Dict[Ability, int],
                 bab: int,
                 hit_dice: Dict[int, int],
                 attacks: List[Attack],
                 hit_points=None):
        '''
        Method that defines a monster.

        PARAMETERS
        size: The physical size category of the monster (Size).
        abilities: Monster ability scores (Dict).
        bab: Base attack bonus (int).
        hit_dice: Hit dice of the monster (Dict).
        attacks: The attacks the monster can make (list).
        hit_points: The number of hit points the monster has (None).
        '''
        self.size = size
        self.abilities = abilities
        self.bab = bab
        self.hit_dice = hit_dice
        self.hit_points = hit_points or\
                          sum([sum([randint(1, i) for j in range(hit_dice[i])]) for i in hit_dice]) +\
                          max(sum(self.hit_dice.values()),
                              sum(self.hit_dice.values()) *\
                              ability_mod(self.abilities[Ability.CON]))
        self.max_hp = hit_points
        self.attacks = attacks

    def get_AC(self):
        return 10 + size_mod(self.size, 'AC')
        


morningstar = Attack('Morningstar',
                        Ability.STR,
                        0,
                        {8:1})

goblin = Monster(Size.SMALL,
                      {Ability.STR:10,
                       Ability.DEX:10,
                       Ability.CON:10,
                       Ability.INT:10,
                       Ability.WIS:10,
                       Ability.CHA:10},
                      1,
                      {6:1},
                      [morningstar])
