import enum


class SqlKewords(enum.Enum):
    Select = 'select',
    Union = 'union',
    Insert = 'insert',
    Delete = 'delete',
    Create = 'create',
    Drop = 'drop',
    Alter = 'alter',
    Update = 'update',
    And = 'and',
    OR = 'or',
    NOT = 'not',
    Comment = '--',
    Truism = '1=1',


def get_keywords():
    return [k.value[0] for k in SqlKewords]

