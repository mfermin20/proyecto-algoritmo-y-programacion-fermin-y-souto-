# Autor: Maria Gracia

class Profesor:
    """
    Representa a un profesor dentro del sistema de horarios.
    
    Consideraciones de eficiencia:
    - La inicialización es O(1) en tiempo.
    - El almacenamiento en memoria es proporcional al tamaño de los strings y la 
      lista de materias_permitidas, siendo una huella de memoria ligera O(N) donde
      N es el número de materias que puede dictar.
    """

    def __init__(self, nombre: str, cedula: str, correo: str, max_materias_permitidas: int, materias_permitidas: list):
        """
        Inicializa un nuevo objeto Profesor.
        
        Consideraciones de eficiencia: O(1) para la asignación de variables.
        """
        self.nombre = nombre
        self.cedula = cedula
        self.correo = correo
        self.max_materias_permitidas = max_materias_permitidas
        self.materias_permitidas = materias_permitidas

    def get_detalles(self) -> str:
        """
        Retorna una cadena formateada con los detalles del profesor.
        
        Consideraciones de eficiencia: O(N) donde N es la cantidad de materias 
        permitidas, debido a la concatenación de la lista en un string.
        """
        materias_str = ", ".join(self.materias_permitidas)
        return f"Profesor: {self.nombre} | C.I: {self.cedula} | Correo: {self.correo} | Max Materias: {self.max_materias_permitidas} | Materias: [{materias_str}]"

    def agregar_materia(self, codigo: str) -> None:
        """
        Agrega el código de una materia a la lista de materias permitidas del profesor.
        
        Consideraciones de eficiencia: O(1) amortizado, ya que el método append de las 
        listas en Python tiene complejidad constante.
        """
        if codigo not in self.materias_permitidas:
            self.materias_permitidas.append(codigo)

    def eliminar_materia(self, codigo: str) -> None:
        """
        Elimina el código de una materia de la lista de materias permitidas.
        
        Consideraciones de eficiencia: O(N) en el peor de los casos, donde N es la 
        cantidad de materias en la lista, ya que el método remove debe buscar el elemento.
        """
        try:
            self.materias_permitidas.remove(codigo)
        except ValueError:
            pass