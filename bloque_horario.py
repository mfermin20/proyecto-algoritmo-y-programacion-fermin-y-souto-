# Autor: Maria Gracia

class BloqueHorario:
    """
    Define un espacio temporal específico en la semana donde puede ocurrir una clase.
    
    Consideraciones de eficiencia:
    - Instanciación y almacenamiento son O(1).
    """

    def __init__(self, dia: str, rango_hora: str):
        """
        Inicializa un bloque horario con los días y horas correspondientes.
        
        Consideraciones de eficiencia: O(1) tiempo de ejecución.
        """
        self.dia = dia
        self.rango_hora = rango_hora

    def get_bloque(self) -> str:
        """
        Devuelve la representación en texto del bloque horario completo.
        
        Consideraciones de eficiencia: O(1), simple concatenación.
        """
        return f"{self.dia} ({self.rango_hora})"