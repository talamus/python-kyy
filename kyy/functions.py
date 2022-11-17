from collections import defaultdict
from .__imports import *
from .classes import Name


def read_tokens(filename: str | None = None) -> list[tokenize.TokenInfo]:
    """Read program from either a file, or from STDIN."""
    tokens = []
    try:
        if filename:
            with open(filename) as file:
                tokens = list(tokenize.generate_tokens(file.readline))
        else:
            tokens = list(tokenize.generate_tokens(sys.stdin.readline))
    except Exception as error:
        errno = 1
        if hasattr(error, "errno"):
            errno = error.errno  # type: ignore
        ERROR(f"Unable to read program: {error}", errno)
    return tokens


def write_program(filename: str, program: str) -> None:
    """Write program to a file."""
    try:
        with open(filename, "w") as file:
            file.write(program)
    except Exception as error:
        errno = 1
        if hasattr(error, "errno"):
            errno = error.errno  # type: ignore
        ERROR(f"Unable to write program: {error}", errno)


def parse_names(
    tokens: list[tokenize.TokenInfo],
) -> list:

    # Parse all NAME tokens to Name objects
    new_tokens = list()
    for token in tokens:
        if token.type == tokenize.NAME:
            name = Name(token)
            new_tokens.append(name)
        else:
            new_tokens.append(token)
    tokens = new_tokens

    known_variables = set()
    new_tokens = list()
    pos = 0
    while pos < len(tokens):
        token = tokens[pos]
        if isinstance(token, Name):

            # Replace known Kyy lexicon with Python commands
            if token.command:
                new_tokens.append(token.command["python"])
                pos += len(token.command["kyy"])
                continue

            # Otherwise, we have a variable (or other nameable entity)
            else:
                if token.only_lemma:
                    known_variables.add(token.only_lemma)

        new_tokens.append(token)
        pos += 1
    tokens = new_tokens

    new_tokens = list()
    for token in tokens:
        if isinstance(token, Name):
            intersection = known_variables.intersection(token.lemmas)

            # Parse known variables:
            if len(intersection) == 1:
                token = intersection.pop()

            # Otherwise, use the first lemma:
            else:
                token = token.lemmas.pop()

        new_tokens.append(token)

    return new_tokens


def untokenize(tokens) -> str:
    indents = []
    program = []
    for token in tokens:
        if isinstance(token, tokenize.TokenInfo):
            if token.type == tokenize.DEDENT:
                indents.pop()
                if len(indents):
                    token = indents[-1]
                else:
                    token = ""
            elif token.type == tokenize.INDENT:
                indents.append(token.string)
                token = token.string
            else:
                token = token.string
        if token != "\n" and token != "":
            token += " "
        program.append(token)
    program = "".join(program)
    return black.format_str(program, mode=black.Mode())  # type: ignore
