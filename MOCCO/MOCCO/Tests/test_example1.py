from MOCCO.Classes.class_input import Input
from MOCCO.Classes.class_individual import Individual
from MOCCO.Classes.class_population import Population


# inputId, cost, cover
input56 = Input(56, 229, set(['49']))
input150 = Input(150, 294, set(['18', '19']))
input151 = Input(151, 300, set(['18', '19', '49']))
example1_population = Population(Individual([input56, input150, input151]))

test1_groundTruth = {input151}
