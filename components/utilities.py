"""Utility functions"""
from typing import Union


def input_to_set(input_info: Union[str, list, set, tuple]) -> set:
    """Transforms input to set if possible"""
    if isinstance(input_info, set):
        return input_info
    if isinstance(input_info, str):
        return {input_info}
    if isinstance(input_info, (list, tuple)):
        return set(input_info)

    raise ValueError(
        f"Unexpected type could not be converted to set: {type(input_info)}"
    )
