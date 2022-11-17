from .__imports import *
from .name import Name


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
            token = Name(token)
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
                # TODO: Check that rest of the command matches...
                continue

            # Otherwise, we have a named entity
            else:
                if token.only_lemma:
                    known_entities.add(token.only_lemma)

        new_tokens.append(token)
        pos += 1
    tokens = new_tokens

    # Expand known entities, and make smart guesses with unkowns
    new_tokens = list()
    for token in tokens:
        if isinstance(token, Name):

            # Handle known entities:
            if canonical_lemma := token.seek_lemma_from(known_entities):
                token = canonical_lemma

            # Otherwise, make a guess:
            else:
                token = token.canonical_lemma()

        new_tokens.append(token)

    return new_tokens


def tokens_to_program(tokens: list[tokenize.TokenInfo | str]) -> str:
    """Convert tokens to a Python program code."""
    indents = []
    program = []
    indent = ""
    for token in tokens:
        if isinstance(token, tokenize.TokenInfo):
            if token.type == tokenize.INDENT:
                indents.append(token.string)
                indent = token.string
                token = ""
            elif token.type == tokenize.DEDENT:
                indents.pop()
                indent = indents[-1] if indents else ""
                token = ""
            else:
                token = token.string

        if token:
            if token == "\n":
                program.append("\n")
                indent = indents[-1] if indents else ""
            else:
                program.append(indent + token + " ")
                indent = ""

    program = "".join(program)
    return black.format_str(program, mode=black.Mode())  # type: ignore
