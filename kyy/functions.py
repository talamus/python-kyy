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


def name_tokens_to_objects(
    tokens: list[tokenize.TokenInfo],
) -> list[tokenize.TokenInfo | Name]:
    """Replace NAME tokens with Name objects."""
    new_tokens = list()
    for token in tokens:
        if token.type == tokenize.NAME:
            name = Name(token)
            new_tokens.append(name)
        else:
            new_tokens.append(token)
    return new_tokens


def name_objects_to_strings(
    tokens: list[tokenize.TokenInfo | Name],
) -> list[tokenize.TokenInfo | str]:
    """Replace Name objects with corresponding strings."""

    # Expand commands and build a list of known entities (variables, functions, ...)
    known_entities = set()
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

            # Otherwise, we have a named entity
            else:
                if token.only_lemma:
                    known_entities.add(token.only_lemma)

        new_tokens.append(token)
        pos += 1
    tokens = new_tokens

    # Expand known entities, and make a smart guess with unkowns
    new_tokens = list()
    for token in tokens:
        if isinstance(token, Name):
            intersection = known_entities.intersection(token.lemmas)

            # Handle known entities:
            if len(intersection) == 1:
                token = intersection.pop()

            # Otherwise, use alphabetically first lemma:
            else:
                sorted_list = list(token.lemmas)
                sorted_list.sort()
                if len(sorted_list) == 0:
                    token = token.original_token.string
                else:
                    token = sorted_list[0]

        new_tokens.append(token)

    return new_tokens


def tokens_to_program(tokens: list[tokenize.TokenInfo | str]) -> str:
    """Convert tokens to a Python program code."""
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
