# Autores: valentina souto 
import json
import requests
from profesor import Profesor
from materia import Materia

class SistemaGestor:
    """
    Clase principal que gestiona las operaciones del sistema de horarios.
    
    Consideraciones de eficiencia:
    - Complejidad de Espacio: O(P + M + H), donde P es la cantidad de profesores, 
      M la cantidad de materias y H el tamaño del horario generado.
    - Complejidad de Tiempo: Depende de cada método invocado.
    """

    def __init__(self):
        """
        Constructor de la clase SistemaGestor. Inicializa las listas de almacenamiento.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(1), inicialización de variables.
        - Complejidad de Espacio: O(1), se crean listas vacías.
        """
        self.lista_profesores = []
        self.lista_materias = []
        self.horario_generado = []

    def iniciar_sistema(self):
        """
        Bucle principal que controla el flujo de la aplicación mostrando el menú.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(1) por cada iteración del menú (sin contar las operaciones de los submódulos).
        - Complejidad de Espacio: O(1).
        """
        self.cargar_datos_api()
        
        while True:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Profesores")
            print("2. Materias")
            print("3. Generar Horarios")
            print("4. Modificar Horarios")
            print("5. Estadísticas")
            print("6. Salir")
            
            try:
                opcion = int(input("Seleccione una opción: "))
                
                if opcion == 1:
                    self.menu_profesores()
                elif opcion == 2:
                    self.menu_materias()
                elif opcion == 3:
                    print("Funcionalidad en desarrollo...")
                elif opcion == 4:
                    print("Funcionalidad en desarrollo...")
                elif opcion == 5:
                    print("Funcionalidad en desarrollo...")
                elif opcion == 6:
                    print("Saliendo del sistema...")
                    break
                else:
                    print("Opción no válida. Por favor, intente de nuevo.")
            except ValueError:
                print("Error: Debe introducir un número entero. Intente de nuevo.")

    def _solicitar_json(self, url: str) -> list:
        """
        Método auxiliar privado para realizar la petición GET y retornar el JSON.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(N) donde N es el tamaño del JSON de respuesta, más el tiempo de red.
        - Complejidad de Espacio: O(N) para almacenar la estructura de datos parseada.
        """
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        return respuesta.json()

    def cargar_datos_api(self):
        """
        Carga datos iniciales mediante un enfoque mixto: profesores desde un archivo local y materias vía peticiones web.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(P + M + N), donde P es el número de profesores procesados localmente, 
          M el número de materias obtenidas de la red, y N la latencia de respuesta de la petición HTTP.
        - Complejidad de Espacio: O(P + M), correspondiente al espacio en memoria para almacenar las 
          estructuras de datos leídas (diccionarios temporales) y los objetos finales instanciados.
        """
        respuesta = input("¿Desea cargar datos iniciales en el sistema? (s/n): ").strip().lower()
        if respuesta != 's':
            return

        print("\nSeleccione el trimestre para cargar materias desde la red:")
        print("1. 2425-3")
        print("2. 2526-1")
        print("3. 2526-2")
        
        try:
            opcion_trimestre = int(input("Opción: "))
            if opcion_trimestre == 1:
                url_materias = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/materias2425-3.json"
            elif opcion_trimestre == 2:
                url_materias = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/materias2526-1.json"
            elif opcion_trimestre == 3:
                url_materias = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/materias2526-2.json"
            else:
                print("Opción inválida. No se cargarán materias desde la red.")
                url_materias = None

            print("\nIniciando proceso de carga...")

            # 1. Carga Local de Profesores
            try:
                with open('profesores.json', 'r', encoding='utf-8') as archivo:
                    datos_profesores = json.load(archivo)
                    
                for p in datos_profesores:
                    profesor = Profesor(
                        p["nombre"], 
                        p["cedula"], 
                        p["correo"], 
                        p["max_materias_permitidas"], 
                        p["materias_permitidas"]
                    )
                    self.lista_profesores.append(profesor)
                print(" > Profesores cargados localmente con éxito.")
                
            except FileNotFoundError:
                print(" > Advertencia: No se encontró el archivo local 'profesores.json'. La lista de profesores estará vacía.")
            except json.JSONDecodeError:
                print(" > Error: El archivo 'profesores.json' está mal formateado. Por favor, verifique su sintaxis JSON.")

            # 2. Carga Web de Materias
            if url_materias:
                datos_materias = self._solicitar_json(url_materias)
                
                for m in datos_materias:
                    materia = Materia(
                        m["codigo"], 
                        m["nombre"], 
                        m["num_secciones"]
                    )
                    self.lista_materias.append(materia)
                print(" > Materias cargadas desde la red con éxito.")

            print("\n¡Proceso de carga finalizado!")

        except ValueError:
            print("\nError: Entrada no válida al seleccionar opciones del menú.")
        except requests.exceptions.RequestException:
            print("\nError de conexión: No se pudieron cargar las materias desde internet.")
        except KeyError:
            print("\nError de estructura: Los datos cargados no coinciden con los atributos esperados.")
    def menu_profesores(self):
        """
        Submenú para la gestión de profesores.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(1) por iteración.
        - Complejidad de Espacio: O(1).
        """
        while True:
            print("\n--- GESTIÓN DE PROFESORES ---")
            print("1. Ver profesores")
            print("2. Agregar profesor")
            print("3. Eliminar profesor")
            print("4. Volver")
            
            try:
                opcion = int(input("Seleccione una opción: "))
                if opcion == 1:
                    self.ver_profesores()
                elif opcion == 2:
                    self.agregar_profesor()
                elif opcion == 3:
                    self.eliminar_profesor()
                elif opcion == 4:
                    break
                else:
                    print("Opción no válida.")
            except ValueError:
                print("Error: Debe introducir un número entero.")

    def ver_profesores(self):
        """
        Muestra la lista actual de profesores.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(P), donde P es la cantidad de profesores.
        - Complejidad de Espacio: O(1), solo imprime en consola.
        """
        if not self.lista_profesores:
            print("No hay profesores registrados.")
            return
            
        print("\n--- LISTA DE PROFESORES ---")
        for i, profesor in enumerate(self.lista_profesores):
            # Asumiendo que get_detalles() devuelve un string descriptivo
            print(f"{i}. {profesor.get_detalles() or profesor.nombre}")

    def agregar_profesor(self):
        """
        Solicita datos al usuario y añade un nuevo profesor a la lista.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(1) amortizado por el append.
        - Complejidad de Espacio: O(1) adicional para el nuevo objeto.
        """
        print("\n--- AGREGAR PROFESOR ---")
        nombre = input("Nombre: ")
        cedula = input("Cédula: ")
        correo = input("Correo: ")
        
        try:
            max_materias = int(input("Máximo de materias permitidas: "))
            materias_str = input("Códigos de materias permitidas (separados por coma): ")
            materias_lista = [m.strip() for m in materias_str.split(",") if m.strip()]
            
            nuevo_profesor = Profesor(nombre, cedula, correo, max_materias, materias_lista)
            self.lista_profesores.append(nuevo_profesor)
            print("Profesor agregado con éxito.")
            
        except ValueError:
            print("Error: El límite máximo de materias debe ser un número entero.")

    def eliminar_profesor(self):
        """
        Elimina un profesor de la lista basado en su índice.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(P) en el peor caso, por el desplazamiento de elementos en la lista tras hacer pop.
        - Complejidad de Espacio: O(1).
        """
        self.ver_profesores()
        if not self.lista_profesores:
            return
            
        try:
            indice = int(input("Ingrese el índice del profesor a eliminar: "))
            profesor_eliminado = self.lista_profesores.pop(indice)
            print(f"Profesor {profesor_eliminado.nombre} eliminado exitosamente.")
        except ValueError:
            print("Error: Debe ingresar un número entero.")
        except IndexError:
            print("Error: Índice fuera de rango.")

    def menu_materias(self):
        """
        Submenú para la gestión de materias.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(1) por iteración.
        - Complejidad de Espacio: O(1).
        """
        while True:
            print("\n--- GESTIÓN DE MATERIAS ---")
            print("1. Ver materias")
            print("2. Agregar materia")
            print("3. Eliminar materia")
            print("4. Modificar secciones de materia")
            print("5. Volver")
            
            try:
                opcion = int(input("Seleccione una opción: "))
                if opcion == 1:
                    self.ver_materias()
                elif opcion == 2:
                    self.agregar_materia()
                elif opcion == 3:
                    self.eliminar_materia()
                elif opcion == 4:
                    self.modificar_secciones_materia()
                elif opcion == 5:
                    break
                else:
                    print("Opción no válida.")
            except ValueError:
                print("Error: Debe introducir un número entero.")

    def ver_materias(self):
        """
        Muestra la lista actual de materias.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(M), donde M es la cantidad de materias.
        - Complejidad de Espacio: O(1).
        """
        if not self.lista_materias:
            print("No hay materias registradas.")
            return
            
        print("\n--- LISTA DE MATERIAS ---")
        for i, materia in enumerate(self.lista_materias):
            print(f"{i}. {materia.get_detalles() or materia.nombre}")

    def agregar_materia(self):
        """
        Solicita datos al usuario y añade una nueva materia a la lista.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(1) amortizado por el append.
        - Complejidad de Espacio: O(1) adicional para el nuevo objeto.
        """
        print("\n--- AGREGAR MATERIA ---")
        codigo = input("Código: ")
        nombre = input("Nombre de la materia: ")
        
        try:
            num_secciones = int(input("Número de secciones: "))
            nueva_materia = Materia(codigo, nombre, num_secciones)
            self.lista_materias.append(nueva_materia)
            print("Materia agregada con éxito.")
        except ValueError:
            print("Error: El número de secciones debe ser un número entero.")

    def eliminar_materia(self):
        """
        Elimina una materia verificando previamente si afecta a los profesores.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(P * K + M), donde P son los profesores, K las materias por profesor, 
          y M el desplazamiento de la lista al hacer pop.
        - Complejidad de Espacio: O(1).
        """
        self.ver_materias()
        if not self.lista_materias:
            return
            
        try:
            indice = int(input("Ingrese el índice de la materia a eliminar: "))
            materia_a_eliminar = self.lista_materias[indice]
            
            # Verificación cruzada
            for prof in self.lista_profesores:
                if materia_a_eliminar.codigo in prof.materias_permitidas:
                    print(f"Advertencia: Esta eliminación afecta al profesor {prof.nombre}, quien la tiene permitida.")
            
            self.lista_materias.pop(indice)
            print(f"Materia '{materia_a_eliminar.nombre}' eliminada con éxito.")
            
        except ValueError:
            print("Error: Debe ingresar un número entero.")
        except IndexError:
            print("Error: Índice fuera de rango.")

    def modificar_secciones_materia(self):
        """
        Modifica el número de secciones de una materia, notificando si baja a cero.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(P * K) en el peor caso (si secciones == 0) para verificar los profesores.
        - Complejidad de Espacio: O(1).
        """
        self.ver_materias()
        if not self.lista_materias:
            return
            
        try:
            indice = int(input("Ingrese el índice de la materia a modificar: "))
            materia_seleccionada = self.lista_materias[indice]
            
            nuevas_secciones = int(input("Ingrese el nuevo número de secciones: "))
            
            if nuevas_secciones == 0:
                for prof in self.lista_profesores:
                    if materia_seleccionada.codigo in prof.materias_permitidas:
                        print(f"Advertencia: La materia no tendrá secciones. Afecta al profesor {prof.nombre}.")
            
            materia_seleccionada.modificar_secciones(nuevas_secciones)
            # Como los métodos están en "pass" en la base, actualizamos manualmente para asegurar funcionalidad
            materia_seleccionada.num_secciones = nuevas_secciones 
            print(f"Secciones actualizadas a {nuevas_secciones}.")
            
        except ValueError:
            print("Error: Debe ingresar un número entero.")
        except IndexError:
            print("Error: Índice fuera de rango.")