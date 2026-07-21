"""Numeric calculation utilities for the ChildRepo submodule.

This module provides pure, standard-library-only helper functions for simple
numeric aggregation. It exposes two functions:

* ``calculate_total`` -- iteratively sum a numeric iterable.
* ``calculate_average`` -- compute the arithmetic mean of a sized numeric collection.

The module has no imports, no classes, and no module-level state. Every
function is side-effect free: none performs I/O and none mutates its input,
which makes the utilities safe to reuse and trivial to test. The code targets
Python 3.6+.

Source: ChildRepo/service.py
"""


def calculate_total(numbers):
    """Iteratively sum the elements of a numeric iterable.

    Walks the input a single time, accumulating each element into a running
    ``total``. This is a pure function with no side effects; it neither
    performs I/O nor mutates the supplied iterable.

    Args:
        numbers (list[int | float] | iterable of numbers): The numeric values
            to sum. Elements are assumed to be numeric (AAP §3.1).

    Returns:
        int | float: The accumulated total of all elements. Returns ``0`` for
        an empty iterable (the natural result of summing zero elements).

    Source: ChildRepo/service.py:L18
    """
    total = 0

    # Iterate over each element and accumulate it into the running ``total``.
    for number in numbers:
        total += number

    return total


def calculate_average(numbers):
    """Compute the arithmetic mean of a sized numeric collection.

    Delegates summation to :func:`calculate_total` and divides the total by
    the number of elements. Because the mean is computed as
    ``total / len(numbers)``, ``numbers`` must be a *sized* collection (for
    example a ``list`` or ``tuple``); unsized iterables such as generators are
    not supported. Division by zero is guarded by returning ``0`` when the
    input is empty or otherwise falsey.

    Note:
        This function is defined but never invoked anywhere in the project
        (AAP §1.2.2); it is documented here for completeness and API coverage.

    Args:
        numbers (list[int | float]): The numeric values to average. Must be a
            *sized* sequence/collection (for example a ``list`` or ``tuple``),
            because the average is computed as ``total / len(numbers)`` and
            ``len()`` is called on it; unsized iterables such as generators are
            not supported.

    Returns:
        int | float: The average (total divided by count). Returns ``0`` for
        empty/falsey input to avoid division by zero.

    Raises:
        TypeError: If ``numbers`` is an unsized iterable (for example a
            generator), because ``len(numbers)`` is evaluated.

    Source: ChildRepo/service.py:L44
    """
    if not numbers:
        return 0

    return calculate_total(numbers) / len(numbers)
