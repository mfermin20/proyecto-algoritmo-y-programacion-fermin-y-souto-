# Autor: Maria Gracia

class Materia:
    """
    Representa una asignatura que debe ser ofertada en el trimestre.
    
    Consideraciones de eficiencia:
    - Ocupa un espacio de memoria constante O(1) ya que solo almacena tres 
      atributos de tipos de datos primitivos.
    """

    def __init__(self, codigo: str, nombre: str, num_secciones: int):
        """
        Construye una instancia de Materia.
        
        Consideraciones de eficiencia: O(1) tiempo de ejecución.
        """
        self.codigo = codigo
        self.nombre = nombre
        self.num_secciones = num_secciones

    def get_detalles(self) -> str:
        """
        Retorna un string con los datos de la materia.
        
        Consideraciones de eficiencia: O(1), consiste únicamente en formato de cadenas.
        """
        return f"Materia: {self.codigo} - {self.nombre} | Secciones a ofertar: {self.num_secciones}"

    def modificar_secciones(self, num: int) -> None:
        """
        Modifica la cantidad de secciones de la materia.
        
        Consideraciones de eficiencia: O(1) ya que es una asignación directa de valor.
        """
        self.num_secciones = max(0, num)