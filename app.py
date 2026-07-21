"""ChildRepo entry-point application.

Command-line entry point for the ``ChildRepo`` submodule. It computes and
prints the total of a fixed list of integers, delegating the numeric
summation to the local ``service`` module's :func:`calculate_total` helper,
then prints each input value on its own line and a final completion message.

This module performs I/O (it writes results to standard output) and is meant
to be run directly via ``python app.py``. It targets Python 3.6+ and depends
only on the standard library plus the intra-repository ``service`` module.

Source: ChildRepo/app.py
"""
from service import calculate_total

def main():
    """Entry point that sums a hard-coded list and prints the results.

    Builds the fixed list ``[10, 20, 30, 40]``, delegates the summation to
    :func:`service.calculate_total`, prints ``Total: 100``, then prints each
    number on its own line, and finally prints ``Application completed``.

    Args:
        None.

    Returns:
        None: results are written to standard output.

    Source: ChildRepo/app.py:L3
    """
    numbers = [10, 20, 30, 40]

    total = calculate_total(numbers)

    print(f"Total: {total}")

    # Print each input number in order, one per line. This is an
    # iteration/print loop only; the numeric summation is delegated to
    # service.calculate_total (the ``total`` computed above).
    for number in numbers:
        print(number)

    print("Application completed")

# Invoke main() only when this module is executed directly (e.g., `python app.py`),
# not when it is imported by another module, keeping imports free of side effects.
if __name__ == "__main__":
    main()
