from typing import Union, Set

# both should be immutable
InputId = Union[str, int]
CoverId = Union[str, int]

class Input:

    def __init__(self, inputId: InputId, cost: int, coveredEntities: Set[CoverId]):
        self.inputId = inputId
        if cost <= 0:
            raise ValueError("The cost of input", inputId, "should be > 0")
        self.cost = cost
        if len(coveredEntities) == 0:
            raise ValueError("Input", inputId, "should cover something.")
        self.cover = coveredEntities
    
    def __repr__(self):
        repr = f"<Input (id {id(self)}): "
        repr += f"inputId = {self.inputId}, "
        repr += f"cost = {self.cost}, "
        repr += f"cover = {self.cover}"
        repr += f">"
        return repr
