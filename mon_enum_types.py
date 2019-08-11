from enum import Enum

class Ability(Enum):
    '''
    An Enum object that defines ability scores.
    '''
    STR = 'Str'
    DEX = 'Dex'
    CON = 'Con'
    INT = 'Int'
    WIS = 'Wis'
    CHA = 'Cha'

class Size(Enum):
    '''
    An Enum object that defines monster sizes.
    '''
    COLOSSAL = 'Colossal'
    GARGANTUAN = 'Gargantuan'
    HUGE = 'Huge'
    LARGE = 'Large'
    MEDIUM = 'Medium'
    SMALL = 'Small'
    TINY = 'Tiny'
    DIMUNITIVE = 'Dimunitive'
    FINE = 'Fine'

class Save(Enum):
    '''
    An Enum object that defines types of saves.
    '''
    FORT = 'Fort'
    REF = 'Ref'
    WILL = 'Will'
