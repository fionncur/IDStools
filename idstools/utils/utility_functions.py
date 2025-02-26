def get_slice_from_array(arr, slice_str):
    if ":" not in slice_str:
        index = int(slice_str)
        return [arr[index]]

    parts = slice_str.split(":")

    start = int(parts[0]) if parts[0] else None
    stop = int(parts[1]) if len(parts) > 1 and parts[1] else None
    step = int(parts[2]) if len(parts) > 2 and parts[2] else None

    slice_obj = slice(start, stop, step)

    return arr[slice_obj]
