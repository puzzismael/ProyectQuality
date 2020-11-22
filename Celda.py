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

