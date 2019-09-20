import typing
import re

from .base import Filter


class MessageText:
    """
    Next methods should be in class
    """

    def __init__(
        self,
        *,
        startswith: str = None,
        match: str = None,
        commands: typing.List[str] = None
    ):
        self.stack = list(
            filter(
                None,
                (
                    self.startswith(startswith) if startswith else None,
                    self.commands(*commands) if commands else None,
                    self.match(match) if match else None,
                ),
            )
        )

    @staticmethod
    def startswith(prefix: str) -> Filter:
        return Filter(
            lambda update: update.raw_text.startswith(prefix)
            if isinstance(update.raw_text, str)
            else None
        )

    @staticmethod
    def commands(*commands: str) -> Filter:
        return Filter(
            lambda update:
            isinstance(update.raw_text, str)
            and update.raw_text.startswith("/")
            and update.raw_text.split()[0][1:] in commands
        )

    @staticmethod
    def match(expression: str) -> Filter:
        return Filter(lambda update: re.compile(expression).match(update.raw_text))

    @staticmethod
    def exact(text: str) -> Filter:
        return Filter(lambda update: update.raw_text == text)

    @staticmethod
    def between(*texts: str) -> Filter:
        return Filter(lambda update: update.raw_text in texts)

    @staticmethod
    def isdigit() -> Filter:
        return Filter(lambda update: (update.raw_text or "").isdigit())
