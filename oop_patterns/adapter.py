# class Light:
#     def __init__(self, dim):
#         self.dim = dim
#         self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
#         self.lights = []
#         self.obstacles = []
        
#     def set_dim(self, dim):
#         self.dim = dim
#         self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
    
#     def set_lights(self, lights):
#         self.lights = lights
#         self.generate_lights()
    
#     def set_obstacles(self, obstacles):
#         self.obstacles = obstacles
#         self.generate_lights()
        
#     def generate_lights(self):
#         return self.grid.copy()


# class System:
#     def __init__(self):
#         self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
#         self.map[5][7] = 1 # Источники света
#         self.map[5][2] = -1 # Стены
    
#     def get_lightening(self, light_mapper):
#         self.lightmap = light_mapper.lighten(self.map)

class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        dim = (len(grid[0]), len(grid))
        self.adaptee.set_dim(dim)
        
        lights = []
        obstacles = []
        for hight in range(dim[1]):
            for width in range(dim[0]):
                if grid[hight][width] == 1:
                    lights.append((width, hight))
                if grid[hight][width] == -1:
                    obstacles.append((width, hight))
        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)
        print(lights)
        print(obstacles)
        return self.adaptee.generate_lights()

# system = System()
# light = Light((1,1))
# adapter = MappingAdapter(light)
# system.get_lightening(adapter)
# print(system.lightmap)
