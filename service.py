"""Arithmetic helper functions for the child submodule application.

This module provides two dependency-free, standard-library-only helpers used by
``app.py`` to demonstrate a simple modular computation: summation and averaging
of a list of numbers. It performs no I/O, defines no classes or module-level
state, and imports nothing. It is byte-identical to the parent repository's
``service.py`` (see the Known Limitations section of ``ChildRepo/README.md``).

Public API:
    * ``calculate_total(numbers)`` -- return the arithmetic sum of a list.
    * ``calculate_average(numbers)`` -- return the arithmetic mean of a list.

Source: ChildRepo/service.py:L1-L14
"""


def calculate_total(numbers):
    """Return the arithmetic sum of a list of numbers.

    Iterates over the input, accumulating each element into a running total
    that starts at ``0``. Because the accumulator starts at zero, an empty
    list yields ``0``.

    Args:
        numbers: A list (or other iterable) of ``int``/``float`` values to sum.

    Returns:
        The sum of all elements; ``0`` for an empty list.

    Source: ChildRepo/service.py:L1-L7
    """
    total = 0

    for number in numbers:
        total += number

    return total


def calculate_average(numbers):
    """Return the arithmetic mean of a list of numbers.

    Returns ``0`` when ``numbers`` is empty or otherwise falsey; this guard
    prevents a division-by-zero. For a non-empty input it delegates to
    :func:`calculate_total` and divides the sum by the element count.

    Args:
        numbers: A list (or other sized iterable) of ``int``/``float`` values.

    Returns:
        ``0`` for a falsey/empty input; otherwise the sum divided by the
        number of elements (a ``float``).

    Source: ChildRepo/service.py:L10-L14
    """
    if not numbers:
        return 0

    return calculate_total(numbers) / len(numbers)
