from MOCCO.Classes.class_input import Input
from MOCCO.Classes.class_individual import Individual
from MOCCO.Classes.class_population import Population


# inputId, cost, cover
input5 = Input(5, 179, set(['33']))
input117 = Input(117, 87, set(['23']))
input119 = Input(119, 110, set(['23', '24']))
input120 = Input(120, 252, set(['23', '24', '33']))
example2_population = Population(Individual([input5, input117, input119, input120]))

test2_groundTruth = {input120}
