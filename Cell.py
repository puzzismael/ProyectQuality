class Celda:
    def __init__(self,x,y):  
        self.positionx = x
        self.positiony = y     
        self.visited = False
    
        self.norte = True
        self.este  = True
        self.sur = True
        self.oeste  = True

    def pintarposicion(self):
        return [self.positionx, self.positiony]
    
    
