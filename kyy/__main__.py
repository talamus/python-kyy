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

    aaaa

    bbbbbb
    \nfor more complete syntax, please refer the lexagon.py file\n"""

    return argparser.parse_args()


def main() -> None:
    args = parse_args()
    tokens = read_tokens(args.filename)
    tokens = parse_names(tokens)
    program = untokenize(tokens)

    if args.output_python:
        if args.output_python == True:
            args.output_python = "program.py"
            if args.filename:
                args.output_python = args.filename + ".py"
        write_program(args.output_python, program)

    if not args.no_exec:
        exec(program)

if __name__ == "__main__":
    main()
