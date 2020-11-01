#!/usr/bin/env python
from PIL import Image, ImageDraw
from time import perf_counter
import random
import os
import glob
import imageio
import shutil


class celda:
    def __init__(self, PosFila, PosColumna, filas, columnas):

        if PosFila >= filas or PosFila < 0:
            raise ValueError(f'Expected a fila index in range(0, {filas}) exclusive, got {PosFila}')
        if PosColumna >= columnas or PosColumna < 0:
            raise ValueError(f'Expected a column index in range(0, {columnas} exclusive, got {PosColumna}')
        self.fila = PosFila
        self.column = PosColumna
        self.filas = filas
        self.columnas = columnas
        self.linked_celdas = []

    def Vecinos(self, cuadricula):
        Vecinos = []
        norte = self.fila - 1, self.column
        if norte[0] < 0:
            norte = 0
            Vecinos.append(0)
        if norte:
            Vecinos.append(cuadricula[norte[0]][norte[1]])
        sur = self.fila + 1, self.column
        if sur[0] >= self.filas:
            sur = 0
            Vecinos.append(0)
        if sur:
            Vecinos.append(cuadricula[sur[0]][sur[1]])
        este = self.fila, self.column + 1
        if este[1] >= self.columnas:
            este = 0
            Vecinos.append(0)
        if este:
            Vecinos.append(cuadricula[este[0]][este[1]])
        oeste = self.fila, self.column - 1
        if oeste[1] < 0:
            oeste = 0
            Vecinos.append(0)
        if oeste:
            Vecinos.append(cuadricula[oeste[0]][oeste[1]])
        return Vecinos

    def link(self, celdaAux, cuadricula):
        """Link 2 unconnected celdas."""
        if self in celdaAux.linked_celdas or celdaAux in self.linked_celdas:
            raise ValueError(f'{self} and {celdaAux} are already connected.')
        if self.columnas != celdaAux.columnas or self.filas != celdaAux.filas:
            raise ValueError('Cannot connect celdas in different cuadriculas.')
        if self not in celdaAux.Vecinos(cuadricula) or celdaAux not in self.Vecinos(cuadricula):
            raise ValueError(f'{self} and {celdaAux} are not Vecinos and cannot be connected.')
        if not isinstance(celdaAux, celda):
            raise TypeError(f'Cannot link celda to {type(celdaAux)}.')
        self.linked_celdas.append(celdaAux)
        celdaAux.linked_celdas.append(self)

    def unlink(self, celdaAux):
        """Unlink 2 connected celdas."""
        if self not in celdaAux.linked_celdas or celdaAux not in self.linked_celdas:
            raise ValueError(f'{self} and {celdaAux} are not connected.')
        self.linked_celdas.remove(celdaAux)
        celdaAux.linked_celdas.remove(self)

    def coordinates(self):
        """Return celda (fila, column)."""
        return self.fila, self.column

    def is_linked(self, celdaAux):
        """Return True if 2 celdas are linked."""
        return celdaAux in self.linked_celdas

    def __str__(self):
        """celda display."""
        return f'celda{self.coordinates()}'

    def __repr__(self):
        """celda representation."""
        return f'celda{self.coordinates()}'


class Maze:
    def __init__(self, filas, columnas, anchura, altura, line_anchura=5, line_color='black', colorFondo='white'):
        if anchura % columnas != 0:
            raise ValueError(f'anchura: {anchura} not divisible by number of columnas: {columnas}.')
        if altura % filas != 0:
            raise ValueError(f'altura: {altura} not divisible by number of {filas}.')
        self.filas = filas
        self.columnas = columnas
        self.anchura = anchura
        self.altura = altura
        self.line_anchura = line_anchura
        self.line_color = line_color
        self.colorFondo = colorFondo
        self.celda_anchura = anchura // columnas
        self.celda_altura = altura // filas
        self.drawing_constant = line_anchura // 2
        self.configurations = {'w': self._wilson_configuration()}
        self.algorithm_names = {'w': 'WILSON'}

    def _make_cuadricula_image(self):
        """Initiate maze initial cuadricula image."""
        cuadricula = Image.new('RGB', (self.anchura, self.altura), self.colorFondo)
        for x in range(0, self.anchura, self.celda_anchura):
            x0, y0, x1, y1 = x, 0, x, self.altura
            column = (x0, y0), (x1, y1)
            ImageDraw.Draw(cuadricula).line(column, self.line_color, self.line_anchura)
        for y in range(0, self.altura, self.celda_altura):
            x0, y0, x1, y1 = 0, y, self.anchura, y
            fila = (x0, y0), (x1, y1)
            ImageDraw.Draw(cuadricula).line(fila, self.line_color, self.line_anchura)
        x_end = (0, self.altura - self.drawing_constant),\
                (self.anchura - self.drawing_constant, self.altura - self.drawing_constant)
        y_end = (self.anchura - self.drawing_constant, 0), (self.anchura - self.drawing_constant, self.altura)
        ImageDraw.Draw(cuadricula).line(x_end, self.line_color, self.line_anchura)
        ImageDraw.Draw(cuadricula).line(y_end, self.line_color, self.line_anchura)
        return cuadricula

    def _create_maze_celdas(self):
        """Return maze celdas."""
        return [[celda(fila, column, self.filas, self.columnas) for column in range(self.columnas)]
                for fila in range(self.filas)]

    def _wilson_configuration(self):
        maze_celdas = self._create_maze_celdas()
        unvisited = {celda for fila in maze_celdas for celda in fila}
        starting_celda = random.choice(list(unvisited))
        unvisited.remove(starting_celda)
        visited = {starting_celda}
        path = [random.choice(list(unvisited))]
        unvisited.remove(path[-1])
        modified_celdas = []
        while unvisited:
            current_celda = path[-1]
            new_celda = random.choice([neighbor for neighbor in current_celda.Vecinos(maze_celdas) if neighbor])
            if new_celda in path and new_celda not in visited:
                to_erase_from = path.index(new_celda)
                del path[to_erase_from + 1:]
            if new_celda in visited:
                for celda in path:
                    visited.add(celda)
                    if celda in unvisited:
                        unvisited.remove(celda)
                path.append(new_celda)
                for index in range(len(path) - 1):
                    path[index].link(path[index + 1], maze_celdas)
                    modified_celdas.append((path[index], path[index + 1]))
                path.clear()
                if unvisited:
                    path.append(random.choice(list(unvisited)))
            if new_celda not in path and new_celda not in visited:
                path.append(new_celda)
        return modified_celdas

    def produce_maze_image(self, configuration):
        if configuration not in self.configurations:
            raise ValueError(f'Invalid configuration {configuration}')
        celdas = self.configurations[configuration]
        maze = self._make_cuadricula_image()
        linked_celdas = {celda.coordinates(): [linked.coordinates() for linked in celda.linked_celdas]
                        for fila in celdas for celda in fila}
        for fila in range(self.filas):
            for column in range(self.columnas):
                current_celda_coordinates = (fila, column)
                if (fila, column + 1) in linked_celdas[current_celda_coordinates]:
                    x0 = (column + 1) * self.celda_anchura
                    y0 = (fila * self.celda_altura) + (self.line_anchura - 2)
                    x1 = x0
                    y1 = y0 + self.celda_altura - (self.line_anchura + 1)
                    wall = (x0, y0), (x1, y1)
                    ImageDraw.Draw(maze).line(wall, self.colorFondo, self.line_anchura)
                if (fila + 1, column) in linked_celdas[current_celda_coordinates]:
                    x0 = column * self.celda_anchura + self.line_anchura - 2
                    y0 = (fila + 1) * self.celda_altura
                    x1 = x0 + self.celda_anchura - (self.line_anchura + 1)
                    y1 = y0
                    wall = (x0, y0), (x1, y1)
                    ImageDraw.Draw(maze).line(wall, self.colorFondo, self.line_anchura)
        x_end = (0, self.altura - self.drawing_constant),\
                (self.anchura - self.drawing_constant, self.altura - self.drawing_constant)
        y_end = (self.anchura - self.drawing_constant, 0), (self.anchura - self.drawing_constant, self.altura)
        ImageDraw.Draw(maze).line(x_end, self.line_color, self.line_anchura)
        ImageDraw.Draw(maze).line(y_end, self.line_color, self.line_anchura)
        total_celdas = self.filas * self.columnas
        return maze

if __name__ == '__main__':
    start_time = perf_counter()
    Laberinto = Maze(50, 100, 1000, 500)
    Laberinto.produce_maze_image('w').show()
    end_time = perf_counter()
    print(f'Time: {end_time - start_time} seconds.')