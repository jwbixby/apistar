import argparse
import inspect
import typing

from apistar import exceptions
from apistar.cli import Command, SubCommand
from apistar.interfaces import CommandConfig, CommandLineClient, HandlerLookup


def main(usage):
    return usage


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise exceptions.CommandLineError(message)


class ArgParseCommandLineClient(CommandLineClient):
    def __init__(self,
                 commands: CommandConfig) -> None:
        parser = ArgumentParser()
        parser.set_defaults(handler=main)
        subparsers = parser.add_subparsers(title='Commands', metavar='[COMMAND]')

        initialize_subparser(subparsers, commands)

        self._parser = parser

    def parse(self,
              args: typing.Sequence[str]) -> HandlerLookup:
        kwargs = vars(self._parser.parse_args(args))
        handler = kwargs.pop('handler')
        if handler is main:
            kwargs['usage'] = self._parser.format_usage()
        return handler, kwargs


def initialize_subparser(subparsers: argparse._SubParsersAction,
                         commands: CommandConfig) -> None:
    for command in commands:
        if isinstance(command, Command):
            name, handler, help, description = command

            subparser = subparsers.add_parser(name, help=help, description=description)
            subparser.set_defaults(handler=handler)

            parameters = inspect.signature(handler).parameters
            for param_name, param in parameters.items():
                annotation = param.annotation
                if annotation is inspect.Parameter.empty:
                    annotation = str

                if issubclass(annotation, (str, int, float, bool)):
                    name = param_name.replace('_', '-')
                    default = param.default
                    if default is inspect.Parameter.empty:
                        subparser.add_argument(
                            param_name,
                            metavar=name.upper(),
                            type=annotation
                        )
                    elif default is False:
                        subparser.add_argument(
                            '--%s' % name,
                            dest=param_name,
                            action='store_true',
                            default=default
                        )
                    elif default is True:
                        subparser.add_argument(
                            '--no-%s' % name,
                            dest=param_name,
                            action='store_false',
                            default=default
                        )
                    else:
                        subparser.add_argument(
                            '--%s' % name,
                            dest=param_name,
                            type=annotation,
                            action='store',
                            default=default
                        )

        elif isinstance(command, SubCommand):
            name, commands, help, description = command

            subparser = subparsers.add_parser(name, help=help, description=description)
            sub_subparsers = subparser.add_subparsers(title='Commands', metavar='[COMMAND]')

            initialize_subparser(sub_subparsers, commands)
