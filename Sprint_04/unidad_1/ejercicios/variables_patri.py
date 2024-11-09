#Clase tablero 

class Barco: 

    def __init__(self, longitud, posicion_x, posicion_y, orientacion):
        self.longitud = longitud  
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.orientacion = orientacion
        self.total_disparos = 0 
        self.disparos_pendientes = longitud

    def disparos(self): #registra cada vez que disparan y dan al barco
        self.total_disparos += 1
        self.disparos_pendientes -= 1

    def hundido(self, disparos_pendientes): 
        if disparos_pendientes == 0: 
            print("¡Te han hundido el barco!")

#######################################

class Tablero: 
    dimensiones = 10
    
    def __init__(self,usuario,barcos): 
        self.usuario = usuario
        self.barcos = 4 

        def __init__(self, usuario, barcos):
        self.usuario = usuario        # Nombre del usuario
        self.barcos = barcos          # Lista de barcos del usuario
        self.tablero_barcos = np.full((self.dimensiones, self.dimensiones), "AGUA")  # Tablero donde se colocan los barcos
        self.tablero_disparos = np.full((self.dimensiones, self.dimensiones), " ")  # Tablero de disparos hechos
        self.barcos_restantes = len(barcos)  # Número total de barcos en el tablero
        self.colocar_barcos() 

