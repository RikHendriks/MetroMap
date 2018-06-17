from enum import Enum, auto
import copy
import random

import numpy as np

from .canvas import Canvas
from .read_xml import NameListXMLReader


class Direction(Enum):
    UP = auto()
    UPRIGHT = auto()
    RIGHT = auto()
    DOWNRIGHT = auto()
    DOWN = auto()
    DOWNLEFT = auto()
    LEFT = auto()
    UPLEFT = auto()

    @classmethod
    def shift_direction(cls, direction, shift):
        return Direction(((direction.value + shift - 1) % 8) + 1)

    @classmethod
    def random_direction(cls):
        return Direction(random.randint(1, 8))

    @staticmethod
    def direction_to_coordinate(direction):
        if direction is Direction.UP:
            return 0, 1
        elif direction is Direction.UPRIGHT:
            return 1, 1
        elif direction is Direction.RIGHT:
            return 1, 0
        elif direction is Direction.DOWNRIGHT:
            return 1, -1
        elif direction is Direction.DOWN:
            return 0, -1
        elif direction is Direction.DOWNLEFT:
            return -1, -1
        elif direction is Direction.LEFT:
            return -1, 0
        elif direction is Direction.UPLEFT:
            return -1, 1


def coordinate_both_even_uneven(coordinate):
    if coordinate[0] % 2 == coordinate[1] & 2:
        return True
    else:
        return False


class City:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.routes = []
        self.map = {i: {j: None for j in range(height)} for i in range(width)}
        self.cells = []
        self.name_list_xml = NameListXMLReader(r"./data/name_lists.xml")

    def __str__(self):
        string = ''
        for i, j, cell in self.grid_generator():
            if cell is None:
                if self.check_coordinate_is_on_route((i, j)):
                    string += '#'
                else:
                    string += '.'
            else:
                string += str(cell)
            if i == self.width - 1:
                string += '\n'
        return string

    @classmethod
    def generate_city(cls, name, width, height, route_count=10):
        city = cls(name, width, height)
        for i in range(route_count):
            if len(city.routes) == 0:
                route = Route.generate_route_in_city('', city)
                if route is not None:
                    city.routes.append(route)
            else:
                route = Route.generate_route_in_city('', city, city.get_random_coordinate_on_route())
                if route is not None:
                    city.routes.append(route)
        return city

    def plot_city(self, filename):
        # Create a canvas
        canvas = Canvas()
        # Draw every cell
        for cell in self.cells:
            canvas.draw_node(np.array(cell.coordinate) * 10)
            text_coordinate = np.array(copy.deepcopy(cell.coordinate)) * 10.0
            text_coordinate[0] += 2
            text_coordinate[1] += -4
            canvas.draw_text(text_coordinate, cell.name)
        # Draw every route
        for route in self.routes:
            color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            for i in range(len(route.route) - 1):
                canvas.draw_line(np.array(route.route[i]) * 10, np.array(route.route[i + 1]) * 10, color)
        # Plot the canvas
        canvas.save_svg(filename)

    def grid_generator(self):
        for j in range(self.height):
            for i in range(self.width):
                yield i, j, self.map[i][j]

    def get_random_coordinate_on_route(self):
        coordinate_list = []
        for route in self.routes:
            for coord in route.route:
                coordinate_list.append(coord)
        return random.choice(coordinate_list)

    def check_coordinate_is_on_route(self, coordinate):
        for route in self.routes:
            if route.coordinate_is_on_route(coordinate):
                return True
        return False

    def check_coordinate_cell(self, coordinate):
        if self.map[coordinate[0]][coordinate[1]] is not None:
            return True
        else:
            return False

    def check_coordinate_bound(self, coordinate):
        if 0 <= coordinate[0] < self.width and 0 <= coordinate[1] < self.height:
            return True
        else:
            return False

    def add_cell(self, coordinate):
        cell_name = self.name_list_xml.get_random_name('first_word_station') + ' ' +\
                    self.name_list_xml.get_random_name('last_word_station')
        cell = Cell(cell_name, coordinate)
        if not self.check_coordinate_cell(cell.coordinate):
            self.cells.append(cell)
            self.map[cell.coordinate[0]][cell.coordinate[1]] = self.cells[-1]
        else:
            return None


class Route:
    def __init__(self, name, city):
        self.name = name
        self.city = city
        self.route = []
        self.cells = []
        self.direction = Direction.random_direction()

    def __str__(self):
        return self.name

    @classmethod
    def generate_route_in_city(cls, name, city, coordinate=None):
        route = cls(name, city)
        route.generate_route(coordinate)
        if len(route.route) > 4:
            route.generate_cells()
            return route
        else:
            return None

    def coordinate_is_on_route(self, coordinate):
        for coord in self.route:
            if coord[0] == coordinate[0] and coord[1] == coordinate[1]:
                return True
        return False

    def generate_route(self, coordinate=None):
        # If no coordinate is given then generate a random coordinate
        if coordinate is None:
            coordinate = [random.randint(0, self.city.width - 1), random.randint(0, self.city.height - 1)]
        # Add the coordinate to the route
        self.route.append(coordinate)
        # The amount of lines in the route
        count = random.randint(1, 4)
        # Generate the route
        for i in range(count):
            while True:
                # Get the directional coordinate
                direction_coordinate = Direction.direction_to_coordinate(self.direction)
                # Get the new coordinate
                new_coordinate = copy.deepcopy(coordinate)
                new_coordinate[0] += direction_coordinate[0]
                new_coordinate[1] += direction_coordinate[1]
                # If the coordinate is still in bounds
                if self.city.check_coordinate_bound(new_coordinate):
                    # Set the coordinate as the new coordinate
                    coordinate = new_coordinate
                    # Add the new coordinate to the route
                    self.route.append(coordinate)
                else:
                    break
                # If the coordinate is at an even-uneven position then let it turn at random
                if coordinate_both_even_uneven(coordinate) and (random.randint(0, 1) is 0):
                    self.direction = Direction.shift_direction(self.direction, random.choice([-1, 1]))
                    break

    def generate_cells(self):
        # Add the cells
        for i in range(len(self.route)):
            # Add a cell at the beginning and the end of the route
            if i == 0 or i == len(self.route) - 1:
                # Add a cell at the end of the route
                if not self.city.check_coordinate_cell(self.route[i]):
                    self.city.add_cell(self.route[i])
                self.cells.append(i)
            # Check if there is a cell at the given coordinate
            elif self.city.check_coordinate_cell(self.route[i]):
                # At the cell to the route
                self.cells.append(len(self.route) - 1)
            # If a route intersects with another create a cell
            elif self.city.check_coordinate_is_on_route(self.route[i]) and\
                    not self.city.check_coordinate_is_on_route(self.route[i - 1]) and\
                    not self.city.check_coordinate_is_on_route(self.route[i + 1]):
                # Generate a cell
                self.cells.append(len(self.route) - 1)
                self.city.add_cell(self.route[i])
            # Place a cell at random
            elif random.random() < 0.025:
                # Generate a cell
                self.cells.append(len(self.route) - 1)
                self.city.add_cell(self.route[i])


class Cell:
    def __init__(self, name, coordinate):
        self.name = name
        self.coordinate = coordinate

    def __str__(self):
        return "*"
