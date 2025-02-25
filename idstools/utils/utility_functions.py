import re


def parse_slice(slice_str):
    """
    Parses a list slice string like 'start:stop:step' and returns a tuple (start, stop, step).
    Args:
        slice_str (str): The slice string to parse. It can be in the format 'start:stop:step' or a single index.
    Returns:
        tuple: A tuple containing (start, stop, step) where each element is an integer or None if not specified.
    Raises:
        ValueError: If the slice string is not in a valid format.
    """

    slice_str = slice_str.strip()

    if slice_str.isdigit() or (slice_str.startswith("-") and slice_str[1:].isdigit()):
        return (int(slice_str), None, None)

    slice_pattern = re.fullmatch(r"(-?\d+)?:(-?\d+)?(?::(-?\d+))?", slice_str)

    if not slice_pattern:
        raise ValueError("Invalid slice format. Use 'start:stop:step' or a single index.")

    start, stop, step = slice_pattern.groups()
    return tuple(None if val is None else int(val) for val in (start, stop, step))
