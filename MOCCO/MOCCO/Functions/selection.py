from typing import List, Union, Tuple, Optional, Any
from random import choices, sample

Element = Any
Weight = Union[int, float]
    
# Randomly select one element amongst several ones, with a weighted distribution.
# The specified weights sequence must be of the same length as the elements sequence.
# The weights are non-negative integers or floats.
# They are relative weights and not percentages, hence the weight sum does not need to be 1.
# If no weight is provided, then a uniform distribution is used.
def select(elements: List[Element], weights: Optional[List[Weight]] = None) -> Element:
    # as opposed to sample, choices performs a selection with replacement, but this does not matter in our case since the number of returned elements is k = 1
    selected_element = choices(elements, weights = weights, k = 1)[0]
    return selected_element

# Randomly split a list of elements into two balanced halves
# if len(elements) is odd, then len(half1) + 1 == len(half2)
def split(elements: List[Element]) -> Tuple[List[Element], List[Element]]:
    if len(elements) <= 1:
        return elements, []
    else:
        # the previous condition ensures that sample_size >= 1
        sample_size = len(elements)//2
        # sample performs a selection without replacement, using a uniform distribution
        half1 = sample(elements, sample_size)
        half2 = [element for element in elements if element not in half1]
        return half1, half2
    
