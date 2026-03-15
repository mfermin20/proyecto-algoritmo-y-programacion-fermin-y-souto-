# Autor: Maria Gracia

class SeccionAsignada:
    """
    Representa una sección de una materia que ya ha sido asignada a un profesor,
    en un bloque horario específico y en un salón determinado.
    
    Consideraciones de eficiencia:
    - Funciona como un contenedor de referencias a otros objetos. Su creación y 
      almacenamiento es de tiempo y espacio O(1).
    """

    def __init__(self, materia: 'Materia', profesor: 'Profesor', bloque: 'BloqueHorario', numero_salon: int):
        """
        Crea el vínculo entre las entidades del horario.
        
        Consideraciones de eficiencia: O(1).
        """
        self.materia = materia
        self.profesor = profesor
        self.bloque = bloque
        self.numero_salon = numero_salon

    def get_info_seccion(self) -> str:
        """
        Genera el resumen de la sección programada para ser mostrado al usuario.
        
        Consideraciones de eficiencia: O(1). Accede a los atributos de objetos ya
        instanciados en memoria.
        """
        nombre_profesor = self.profesor.nombre if self.profesor else "SIN ASIGNAR"
        nombre_materia = self.materia.nombre if self.materia else "DESCONOCIDA"
        info_bloque = self.bloque.get_bloque() if self.bloque else "SIN HORARIO"
        
        return f"[{info_bloque}] Salón {self.numero_salon} | {nombre_materia} | Prof. {nombre_profesor}"