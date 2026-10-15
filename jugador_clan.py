
# Representa a un jugador de Habitica
class Jugador:
    def __init__(self, nombre, nivel=1):
        self.nombre = nombre
        self.nivel = nivel
        self.experiencia = 0

    # Agrega experiencia al jugador
    def ganar_experiencia(self, cantidad):
        if cantidad > 0:
            self.experiencia += cantidad

    # Muestra los datos del jugador
    def mostrar_datos(self):
        print(f"Jugador: {self.nombre}")
        print(f"Nivel: {self.nivel}")
        print(f"Experiencia: {self.experiencia}")


# Representa un clan de jugadores
class Clan:
    def __init__(self, nombre, capacidad=10):
        self.nombre = nombre
        self.capacidad = capacidad
        self.miembros = []

    # Agrega un jugador si hay espacio
    def agregar_miembro(self, jugador):
        if len(self.miembros) < self.capacidad:
            self.miembros.append(jugador)
            return True
        return False

    # Muestra los miembros del clan
    def mostrar_miembros(self):
        print(f"Clan: {self.nombre}")
        for jugador in self.miembros:
            print(f"- {jugador.nombre}")


# Representa un clan al que cualquiera puede solicitar ingreso
class ClanAbierto:
    def __init__(self, nombre, capacidad=10):
        self.nombre = nombre
        self.capacidad = capacidad
        self.miembros = []

    # Permite ingresar mientras haya espacio
    def unirse(self, jugador):
        if len(self.miembros) >= self.capacidad:
            return False

        if jugador in self.miembros:
            return False

        self.miembros.append(jugador)
        return True


# Representa un clan que requiere invitación
class ClanPrivado:
    def __init__(self, nombre, capacidad=10):
        self.nombre = nombre
        self.capacidad = capacidad
        self.miembros = []
        self.invitados = []

    # Registra una invitación para un jugador
    def invitar(self, jugador):
        if jugador not in self.miembros and jugador not in self.invitados:
            self.invitados.append(jugador)

    # Permite ingresar a un jugador invitado
    def aceptar_invitacion(self, jugador):
        if jugador not in self.invitados:
            return False

        if len(self.miembros) >= self.capacidad:
            return False

        self.invitados.remove(jugador)
        self.miembros.append(jugador)
        return True
