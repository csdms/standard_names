from pyparsing import Combine
from pyparsing import Optional
from pyparsing import ParserElement
from pyparsing import Word
from pyparsing import ZeroOrMore
from pyparsing import alphanums
from pyparsing import alphas


def _standard_name() -> ParserElement:
    lowercase_word = Word(alphas.lower())
    alnum_word = Word(alphanums)

    separator = Word("-~_", exact=1)

    object_ = Combine(
        lowercase_word + ZeroOrMore(Optional(separator) + alnum_word)
    ).set_name("object")
    quantity = Combine(
        lowercase_word + ZeroOrMore(Optional(separator) + alnum_word)
    ).set_name("quantitiy")

    return (object_ + "__" + quantity).set_name("standard_name")


STANDARD_NAME = _standard_name()


def findall(line: str) -> list[str]:
    return ["".join(token) for token, _, _ in STANDARD_NAME.scanString(line)]
