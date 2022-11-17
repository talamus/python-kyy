from .__imports import *


def ERROR(error_message: str, error_number: int = 1) -> None:
    """Print error message to STDERR and terminate."""
    print(error_message, file=sys.stderr)
    sys.exit(error_number)
