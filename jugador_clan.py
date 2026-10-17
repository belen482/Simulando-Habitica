# ---------------------------------------------------------------------------
# Jugador
# ---------------------------------------------------------------------------
class Jugador:
    HP_MAXIMA = 50

    def __init__(self, nombre, nivel=1, clase=None):
        self.nombre = nombre
        self.nivel = nivel
        self.experiencia = 0
        self.oro = 0
        self.hp_maxima = self.HP_MAXIMA
        self.hp = self.hp_maxima
        self.clase = clase if clase is not None else Aprendiz()
        self.clan = None
        self.inventario = []      # Equipos adquiridos en la tienda

    # Experiencia necesaria para pasar del nivel actual al siguiente
    def exp_para_subir(self):
        return 50 * self.nivel

    # Agrega experiencia (ya con modificadores aplicados) y sube de nivel si corresponde
    def ganar_experiencia(self, cantidad):
        if cantidad > 0:
            self.experiencia += cantidad
            while self.experiencia >= self.exp_para_subir():
                self.experiencia -= self.exp_para_subir()
                self._subir_nivel()

    def _subir_nivel(self):
        self.nivel += 1
        self.curar(self.clase.curacion_al_subir_nivel(self.hp_maxima))

    def curar(self, cantidad):
        if cantidad > 0:
            self.hp = min(self.hp_maxima, self.hp + cantidad)

    # Recibe daño base; la clase puede reducirlo. Devuelve el daño realmente recibido
    def recibir_dano(self, base):
        dano = self.clase.modificar_dano(base)
        self.hp = max(0, self.hp - dano)
        return dano

    # Aplica una recompensa {"experiencia", "oro", "vida"} usando los modificadores de la clase
    def aplicar_recompensa(self, recompensa):
        if recompensa is None:
            return False
        self.ganar_experiencia(self.clase.modificar_exp(recompensa["experiencia"]))
        self.oro += self.clase.modificar_oro(recompensa["oro"])
        vida = recompensa["vida"]
        if vida > 0:
            self.curar(vida)
        elif vida < 0:
            self.recibir_dano(-vida)
        return True

    # Completa una tarea (o hábito positivo). Devuelve False si ya estaba completada hoy
    def completar_tarea(self, tarea):
        return self.aplicar_recompensa(tarea.completar())

    # Marca un hábito como "Positivo" o "Negativo"
    def marcar_habito(self, habito, forma="Positivo"):
        if forma == "Positivo":
            recompensa = habito.marcar_positivo()
        elif forma == "Negativo":
            recompensa = habito.marcar_negativo()
        else:
            raise ValueError("La forma debe ser 'Positivo' o 'Negativo'.")
        return self.aplicar_recompensa(recompensa)

    # Muestra los datos del jugador
    def mostrar_datos(self):
        print(f"Jugador: {self.nombre}")
        print(f"Clase: {self.clase.nombre}")
        print(f"Nivel: {self.nivel}")
        print(f"Experiencia: {self.experiencia}/{self.exp_para_subir()}")
        print(f"Vida: {self.hp}/{self.hp_maxima}")
        print(f"Oro: {self.oro}")
        print(f"Clan: {self.clan.nombre if self.clan else 'Sin clan'}")
        print(f"Inventario: {', '.join(i.nombre for i in self.inventario) or 'Vacío'}")


# ---------------------------------------------------------------------------
# Clanes
# ---------------------------------------------------------------------------
# Representa un clan de jugadores (base de ClanAbierto y ClanPrivado)
class Clan:
    def __init__(self, nombre, capacidad=10):
        self.nombre = nombre
        self.capacidad = capacidad
        self.miembros = []

    def tiene_espacio(self):
        return len(self.miembros) < self.capacidad

    # Agrega un jugador si hay espacio, no es miembro y no pertenece a otro clan
    def agregar_miembro(self, jugador):
        if not self.tiene_espacio() or jugador in self.miembros or jugador.clan is not None:
            return False
        self.miembros.append(jugador)
        jugador.clan = self
        return True

    # Muestra los miembros del clan
    def mostrar_miembros(self):
        print(f"Clan: {self.nombre}")
        for jugador in self.miembros:
            print(f"- {jugador.nombre} (Nivel {jugador.nivel}, {jugador.clase.nombre})")


# Representa un clan al que cualquiera puede solicitar ingreso
class ClanAbierto(Clan):
    # Permite ingresar mientras haya espacio
    def unirse(self, jugador):
        return self.agregar_miembro(jugador)


# Representa un clan que requiere invitación
class ClanPrivado(Clan):
    def __init__(self, nombre, capacidad=10):
        super().__init__(nombre, capacidad)
        self.invitados = []

    # Registra una invitación para un jugador
    def invitar(self, jugador):
        if jugador not in self.miembros and jugador not in self.invitados:
            self.invitados.append(jugador)

    # En un clan privado solo se ingresa con invitación
    def agregar_miembro(self, jugador):
        return self.aceptar_invitacion(jugador)

    # Permite ingresar a un jugador invitado
    def aceptar_invitacion(self, jugador):
        if jugador not in self.invitados:
            return False
        if super().agregar_miembro(jugador):
            self.invitados.remove(jugador)
            return True
        return False

