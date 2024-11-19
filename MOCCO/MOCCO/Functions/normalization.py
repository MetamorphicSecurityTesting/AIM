from typing import Union

Value = Union[int, float]

# this normalization function computes x -> x / (x + 1)
# it normalizes a range of value from [0, infinity) to [0, 1) while preserving the order, i.e., if val1 <= val2 then normalize(val1) <= normalize(val2)
def normalize(value: Value) -> float:
    return value/(value + 1.0)

# this function is similar to normalize as it computes x -> 1 / (x + 1), so normalize_opposite(x) = 1 - normalize(x)
# it normalizes a range of value from [0, infinity) to (0, 1] while reverting the order, i.e., if val1 <= val2 then normalize(val1) >= normalize(val2)
def normalize_complement(value: Value) -> float:
    return 1.0/(value + 1.0)
