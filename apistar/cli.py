import collections
import typing


class Command(collections.abc.Iterable):
    def __init__(self,
                 name: str,
                 handler: typing.Callable,
                 help: str='',
                 description: str='') -> None:
        self.name = name
        self.handler = handler
        self.help = help
        self.description = description

    def __iter__(self) -> typing.Iterator:
        return iter((self.name, self.handler, self.help, self.description))


class SubCommand(collections.abc.Iterable):

    def __init__(self,
                 name: str,
                 commands: typing.Sequence[typing.Union[Command, 'SubCommand']],
                 help: str='',
                 description: str='') -> None:
        self.name = name
        self.commands = commands
        self.help = help
        self.description = description

    def __iter__(self) -> typing.Iterator:
        return iter((self.name, self.commands, self.help, self.description))
