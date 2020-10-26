from simpleai.search import (
    SearchProblem, 
    breadth_first, 
    depth_first, 
    uniform_cost,
    astar,
    iterative_limited_depth_first
)

from simpleai.search.viewers import WebViewer, BaseViewer


PACKAGES = {}
TRUCKS = {}


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
HEADQUARTERS = ['rafaela','santa_fe']

class Trucks(SearchProblem):
    def is_goal(self, state):
        isGoal = False
        if(len(state[1]) > 0):
            return False
        
        for truck in state[0]:
            if truck[1] in HEADQUARTERS:
                isGoal = True
            else:
                return False
            
            for package in truck[3]:
                if PACKAGES[package][1] == truck[1]:
                    isGoal == True
                else:
                    return False

        return isGoal

    def actions(self, state):
        #action = ('truck','destination', 'cost', package)

        trucks, packages = state
        available_actions = []
        
        for truck in trucks:
            # Moverse
            for city in MAP[truck[1]]:
                if TRUCKS[truck[0]] >= (truck[2] + (city[1]/100)):
                    available_actions.append((truck[0], city[0], (city[1]/100), truck[3]))
            # Cargar paquete
            for pack in packages:
                if truck[1] == PACKAGES[pack][0]:
                    available_actions.append((truck[0], truck[1], 0, tuple([pack])))

        return available_actions

    def result(self, state, action):
        #convert tuples to list
        state_modifiable = list(pile for pile in state)
        truck, city, cost, package = action

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
                    
                    if city in HEADQUARTERS:
                        state_truck_modifiable[2] = 0
                    else:
                        state_truck_modifiable[2] += cost
                    
                    for package in state_truck[3]:
                        if PACKAGES[package][1] == city:
                            state_truck_package_modifiable = list(row for row in state_truck_modifiable[3])
                            state_truck_package_modifiable.remove(package)
                            state_truck_modifiable[3] = tuple(row for row in state_truck_package_modifiable)



                    state_truck_modifiable = tuple(row for row in state_truck_modifiable)

                state_modifiable[0] = list(pile for pile in state_modifiable[0])
                state_modifiable[0][index] = state_truck_modifiable
                state_modifiable[0][index] = tuple(pile for pile in state_modifiable[0][index])
                state_modifiable[0] = tuple(pile for pile in state_modifiable[0])

        #convert list to tuples
        state_modifiable = tuple(tuple(row) for row in state_modifiable)
        return state_modifiable


    def cost(self, state1,action, state2):
        # Costo en combustible (cargar un paquete cuesta 0)
        return action[2]

    def heuristic(self, state):
        # La cantidad de paquetes que falta cargar
        return len(state[1])

        


def planear_camiones(metodo, camiones, paquetes):
    total_packages = []
    total_trucks = []

    for package in paquetes:
        PACKAGES[package[0]] = (package[1], package[2])
        total_packages.append(package[0])

    for truck in camiones:
        TRUCKS[truck[0]] = truck[2]
        total_trucks.append((truck[0], truck[1], 0, ()))

    INITIAL_STATE = (
        tuple(pile for pile in total_trucks),
        tuple(pile for pile in total_packages),
    )

    METHODS = {
        'breadth_first': breadth_first,
        'depth_first': depth_first,
        'iterative_limited_depth_first': iterative_limited_depth_first,
        'uniform_cost': uniform_cost,
        'astar': astar,
    }

    problem = Trucks(INITIAL_STATE)
    #result = METHODS[metodo](problem)
    result = METHODS[metodo](problem, graph_search=True)
    
    itinerario = []
    for action, _ in result.path():
        if action is not None:
            if action[2] > 0:
                itinerario.append(action)
    return itinerario


if __name__ == '__main__': 
    itinerario = planear_camiones(
    # método de búsqueda a utilizar. Puede ser: astar, breadth_first, depth_first, uniform_cost o greedy
    metodo="breadth_first",
    camiones=[
        # id, ciudad de origen, y capacidad de combustible máxima (litros)
        ('c_normal', 'rafaela', 1.5),
    ],
    paquetes=[
        # id, ciudad de origen, y ciudad de destino
        ('p_normal', 'rafaela', 'lehmann')
    ],
    )
    print(itinerario)


