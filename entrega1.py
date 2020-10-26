from simpleai.search import SearchProblem, breadth_first, depth_first, uniform_cost
from simpleai.search.viewers import WebViewer, BaseViewer

INITIAL_STATE = (
    (
        ('c1', 'rafaela', 0,()), 
        ('c2', 'rafaela', 0, ())
    ), 
    ('p1','p2', 'p3')
    )    

#action = ('truck','destino', 'costo', paquete)

GOAL_STATE = ()

MAP = {
    'rafaela': [('susana', 10),('esperanza', 70),('lehmann',8)],
    'lehmann': [('rafaela', 8),('sunchales',32)],
    'susana': [('angelica', 25),('rafaela',10)],
    'sunchales': [('lehmann', 32)],
    'angelica': [('san_vicente', 18),('sc_de_saguier', 60),('susana',25),('santo_tome',85)],
    'san_vicente': [('angelica',18)],
    'sc_de_saguier': [('angelica',60)],
    'esperanza': [('recreo', 20),('rafaela',70)],
    'recreo': [('santa_fe', 10),('esperanza',20)],
    'santa_fe': [('santo_tome', 5),('recreo',10)],
    'santo_tome': [('angelica', 85),('sauce_viejo', 15),('santa_fe',5)],
    'sauce_viejo': [('santo_tome',15)],
}

PACKAGES = {
    'p1':('rafaela', 'susana'),
    'p2':('susana', 'lehmann'),
    'p3':('esperanza', 'rafaela'),
}

TRUCKS = {
    'c1': 1.5,
    'c2': 2.0
}

class Trucks(SearchProblem):
    def is_goal(self, state):
        return False
    
    def actions(self, state):
        trucks, packages = state
        available_actions = []
        
        for truck in trucks:
            # Moverse
            for city in MAP[truck[1]]:
                if TRUCKS[truck[0]] >= (truck[2] + (city[1]/100)):
                    available_actions.append((truck[0], city[0], (city[1]/100), truck[3]))
                
            # Cargar paquete
            for pack in packages:
                if truck[1] == PACKAGES[pack]:
                    available_actions.append((truck[0], truck[1], 0, [pack]))

        return available_actions

    def result(self, state, action):
        #convert tuples to list
        state_modifiable = list(pile for pile in state)
        truck, city, cost, package = action

        # Trucks list -> state_modifiable[0]

        # Package list -> state_modifiable[1]

        for index, state_truck in enumerate(state_modifiable[0]):
            if state_truck[0] == truck:

                state_truck_modifiable = list(row for row in state_truck) 

                if cost == 0:
                    state_package_modifiable = list(row for row in state_modifiable[1]) 
                    state_package_modifiable.remove(package[0])
                    state_modifiable[1] = tuple(row for row in state_package_modifiable) 

                    state_truck_package_modifiable = list(row for row in state_truck_modifiable[3])
                    state_truck_package_modifiable.append(package[0])
                    state_truck_modifiable[3] = tuple(row for row in state_truck_package_modifiable)
                else:
                    state_truck_modifiable[1] = city
                    state_truck_modifiable[2] += cost
                    state_truck_modifiable = tuple(row for row in state_truck_modifiable) 

                state_modifiable[0] = list(pile for pile in state_modifiable[0])
                state_modifiable[0][index] = state_truck_modifiable
                state_modifiable[0][index] = tuple(pile for pile in state_modifiable[0][index])
                state_modifiable[0] = tuple(pile for pile in state_modifiable[0])

        #convert list to tuples
        state_modifiable = tuple(tuple(row) for row in state_modifiable)
        return state_modifiable


    def cost(self, state1,action, state2):
        return action[2]

    def heuristic(self, state):
        return 1

        
problem = Trucks(INITIAL_STATE)
result = breadth_first(problem, graph_search=True, viewer=WebViewer())