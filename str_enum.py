from typing import Iterable, Union
import enum

class StrEnumMeta(enum.EnumMeta):
    def __call__(cls, value: str, names: Iterable[Union[str, 'StrEnum']] | None = None, **kwds):
        """
        In order to use the functional API in the following way (while ignoring duplicates):
        MyEnum = StrEnum('MyEnum', ('FOO', 'BAR', *MyEnum1, *MyEnum2))

        Where MyEnum1 and MyEnum2 are instances of StrEnumMeta
        """
        if names: names = tuple(set(names)) # ignore duplicates
        return super().__call__(value, names, **kwds)
        
    def __new__(metacls, cls, bases, classdict, **kwds):
        """
        In order to be able to use ellipsis or the empty tuple instead of enum.auto() or object()

        This:
        class MyEnum(StrEnum):
            A = ()
            B = ()

        Or this:
        class MyEnum(StrEnum):
            A = ...
            B = ...

        Becomes equivalent to:
        class MyEnum(StrEnum):
            A = enum.auto()
            B = enum.auto()
        """
        automembers = [field for field, value in classdict.items() if value in (..., ())]
        for field in automembers:
            classdict._member_names.remove(field) # hacky af
            del classdict[field]
            classdict[field]=enum.auto()
        return super().__new__(metacls, cls, bases, classdict, **kwds)

class StrEnum(str, enum.Enum, metaclass=StrEnumMeta):
    def _generate_next_value_(name, *_):
        return name

    # https://www.cosmicpython.com/blog/2020-10-27-i-hate-enums.html
    def __str__(self) -> str:
        return str.__str__(self)
