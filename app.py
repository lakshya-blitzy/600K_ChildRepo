"""Console entry point for the child submodule sum-and-print application.

This module wires the reusable :func:`service.calculate_total` helper to a tiny
command-line demonstration. When executed directly it computes the sum of a
fixed list of numbers, prints the total, echoes each number, and prints a
completion message. It defines no classes, constants, or module-level state
beyond the ``main`` function and the standard ``__main__`` guard. Its
non-docstring executable implementation mirrors the parent repository's
``app.py`` (the repository-specific docstrings differ).

Note:
    Only :func:`service.calculate_total` is imported here;
    :func:`service.calculate_average` is defined in ``service.py`` but is not
    used by this application.

Usage:
    python app.py

Source: ChildRepo/app.py:L1-L16
"""

from service import calculate_total

def main():
    """Run the sample computation and print results to standard output.

    Builds the fixed list ``[10, 20, 30, 40]``, computes its total via
    :func:`service.calculate_total`, prints ``Total: <total>`` using an
    f-string, prints each number on its own line in input order, and finally
    prints ``Application completed``. The input is hard-coded; the function
    accepts no arguments and reads no configuration.

    Args:
        None.

    Returns:
        None. The function's observable effect is its standard-output writes.
        For the built-in input, the output begins with ``Total: 100``.

    Source: ChildRepo/app.py:L3-L16
    """
    numbers = [10, 20, 30, 40]

    total = calculate_total(numbers)

    print(f"Total: {total}")

    for number in numbers:
        print(number)

    print("Application completed")

if __name__ == "__main__":
    main()
