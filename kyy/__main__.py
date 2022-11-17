import argparse
from .__imports import *
from .functions import *


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    argparser = argparse.ArgumentParser(
        prog="python -m kyy",
        description="A Finnish language variant of the Python programming language.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    argparser.add_argument(
        "filename",
        nargs="?",
        metavar="program.kyy",
        help="the program file to be executed; defaults to stdin",
    )
    argparser.add_argument(
        "-o",
        "--output-python",
        nargs="?",
        const=True,
        metavar="program.py",
        help="output python source code",
    )
    argparser.add_argument(
        "-n",
        "--no-exec",
        action="store_true",
        help="don't execute the program",
    )
    argparser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="be more verbose",
    )
    argparser.epilog = """example program:

  eläimet = ["kissa", "karhu", "koira"]

  jokaiselle sijainnille, eläimelle joka löytyy numeroiduista(eläimistä):
      jos sijainti > 1:
          tulosta(f"Tosi iso {eläin}")
      muuten:
          tulosta(sijainti, eläin)
    \nfor more complete syntax, please refer to the kyy/lexicon.py file\n"""

    return argparser.parse_args()


def print_title(label, file=sys.stderr):
    """A nice title"""
    print(f"\n=== {label} {'=' * (40-len(label))} === == =\n", file=file)


def print_tokens(tokens, file=sys.stderr):
    """Pretty print for tokens"""
    for token in tokens:
        if isinstance(token, tokenize.TokenInfo):
            string = tokenize.tok_name[token.type]
            if token.string == "\n":
                string += "\n"
            elif token.string != "":
                string += f'"{token.string}" '
            else:
                string += " "
        else:
            string = f'"{str(token)}" '

        print(string, end="", file=file)
    print(file=file)


def main() -> None:
    """Command line program."""
    args = parse_args()

    tokens = read_tokens(args.filename)
    if args.verbose:
        print_title("Raw Kyy Tokens")
        print_tokens(tokens)

    tokens = name_tokens_to_objects(tokens)
    if args.verbose:
        print_title("Canonized Names")
        print_tokens(tokens)

    tokens = name_objects_to_strings(tokens)
    program = tokens_to_program(tokens)
    if args.verbose:
        print_title("Final Python Program")
        print(program, file=sys.stderr)

    if args.output_python:
        if args.output_python == True:
            if args.filename:
                args.output_python = args.filename + ".py"
            else:
                args.output_python = "program.py"
        write_program(args.output_python, program)

    if not args.no_exec:
        if args.verbose:
            print_title("Program Output")
        exec(program)


if __name__ == "__main__":
    main()
