class City:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.map = {i: {j: None for j in range(height)} for i in range(width)}
        self.cells = []

    def __str__(self):
        string = ''
        for i, j, cell in self.grid_generator():
            if cell is None:
                string += '.'
            else:
                string += str(cell)
            if i == self.width - 1:
                string += '\n'
        return string

    def grid_generator(self):
        for j in range(self.height):
            for i in range(self.width):
                yield i, j, self.map[i][j]

    def check_coordinate(self, coordinate):
        if self.map[coordinate[0]][coordinate[1]] is None:
            return True
        else:
            return False

    def add_cell(self, cell):
        if self.check_coordinate(cell.coordinate):
            self.cells.append(cell)
            self.map[cell.coordinate[0]][cell.coordinate[1]] = self.cells[-1]
        else:
            return None


class Cell:
    def __init__(self, name, coordinate):
        self.name = name
        self.coordinate = coordinate

    def __str__(self):
        return "*"


class Route:
    pass
