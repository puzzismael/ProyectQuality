from Cell import Celda
from _typeshed import FileDescriptor
import json.decoder
from json.decoder import JSONDecoder
import json.scanner


class RWjson:

    def lecturajson(self, ruta): 
       colum = 0
       i = 0
       k= 0
       try:
           f = open(ruta, "r")
           content = f.read()
           jsondecoded = json.loads(content)
           fila = jsondecoded["rows"]
           colum = jsondecoded["cols"]
           Laberinto = [[0] * fila for i in range(colum)] 

           for i in Laberinto[i]:
                for j in Laberinto[i,j]:
                    cel = Celda(i,j)
                    value = jsondecoded("value")
                    if (value==1):
                        cel.visited(value)
                    else:
                        cel.visited(value=0)
                        
                    neighbors = jsondecoded["neighbors"].getAsJsonArray()
                    cel.norte = neighbors[k], k+1
                    cel.este = neighbors[k], k+1
                    cel.sur = neighbors[k], k+1
                    cel.oeste = neighbors[k]
       except IOError as exc:
           print("No se ha podido abrir el fichero")
           exit(1)
       except FileNotFoundError as ex:
           print("No se ha podico encontrar el fichero")
           exit(1)