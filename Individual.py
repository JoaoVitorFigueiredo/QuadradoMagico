from Utils import Utils


class Individual:
    def __init__(self, cube: list):
        self.__cube = cube
        self.__loss = Utils.loss_function(cube)

    def get_cube(self):
        return self.__cube

