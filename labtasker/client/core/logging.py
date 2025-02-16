import sys
from contextlib import contextmanager
from pathlib import Path

from loguru import logger  # noqa
from rich.console import Console

stdout_console = Console(markup=True)
stderr_console = Console(markup=True, stderr=True)


@contextmanager
def log_to_file(
    file_path: Path,
    capture_stdout: bool = True,
    capture_stderr: bool = True,
    **kwargs,
):
    """Temporarily redirect log to a file.

    Args:
        file_path (Path): Path to the log file.
        capture_stdout (bool): Whether to redirect stdout to the log file.
        capture_stderr (bool): Whether to redirect stderr to the log file.
        **kwargs: Additional arguments for the `logger.add` method.
    """
    log_file = open(file_path, "a")

    # Save original stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # Redirect stdout and stderr if requested
    if capture_stdout:
        sys.stdout = log_file
    if capture_stderr:
        sys.stderr = log_file

    # Add a loguru handler to the file
    handler_id = logger.add(log_file, **kwargs)

    try:
        yield
    finally:
        # Restore original stdout and stderr
        if capture_stdout:
            sys.stdout = original_stdout
        if capture_stderr:
            sys.stderr = original_stderr

        # Remove the loguru handler and close the file
        logger.remove(handler_id)
        log_file.close()
