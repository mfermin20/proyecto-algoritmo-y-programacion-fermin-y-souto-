# Autores: valentina souto y Maria Gracia
import json
import requests
import csv
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_INSTALADO = True
except ImportError:
    MATPLOTLIB_INSTALADO = False

from profesor import Profesor
from materia import Materia
from bloque_horario import BloqueHorario
from seccion_asignada import SeccionAsignada

class SistemaGestor:
    """
    Clase principal que gestiona las operaciones del sistema de horarios.
    
    Consideraciones de eficiencia:
    - Complejidad de Espacio: O(P + M + H), donde P es la cantidad de profesores, 
      M la cantidad de materias y H el tamaño del horario generado.
    - Complejidad de Tiempo: Depende de cada método invocado; el ciclo principal es O(1) amortizado.
    """

    def __init__(self):
        """
        Constructor de la clase SistemaGestor. Inicializa las listas de almacenamiento.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(1), inicialización de variables en memoria.
        - Complejidad de Espacio: O(1), se crean listas vacías.
        """
        self.lista_profesores = []
        self.lista_materias = []
        self.horario_generado = []

    def iniciar_sistema(self):
        """
        Bucle principal que controla el flujo de la aplicación mostrando el menú.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(1) por cada iteración del menú (sin contar operaciones internas).
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
            print("6. Guardar Horario (CSV)")
            print("7. Cargar Horario (CSV)")
            print("8. Salir")
            
            try:
                opcion = int(input("Seleccione una opción: "))
                
                if opcion == 1:
                    self.menu_profesores()
                elif opcion == 2:
                    self.menu_materias()
                elif opcion == 3:
                    self.generar_horarios()
                elif opcion == 4:
                    self.modificar_horarios()
                elif opcion == 5:
<<<<<<< Updated upstream
                    self.mostrar_reportes_generacion()
=======
                    self.mostrar_estadisticas()
>>>>>>> Stashed changes
                elif opcion == 6:
                    self.guardar_horario_csv()
                elif opcion == 7:
                    self.cargar_horario_csv()
                elif opcion == 8:
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
<<<<<<< Updated upstream
        - Complejidad de Tiempo: O(N) donde N es el tamaño del JSON de respuesta, más el tiempo de latencia de red.
=======
        - Complejidad de Tiempo: O(N) donde N es el tamaño del JSON de respuesta.
>>>>>>> Stashed changes
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
                    import json
                    datos_profesores = json.load(archivo)
                    
                for p in datos_profesores:
                    # Unimos Nombre y Apellido, y pasamos la Cédula a texto para la clase Profesor
                    nombre_completo = f"{p['Nombre']} {p['Apellido']}"
                    
                    profesor = Profesor(
                        nombre_completo, 
                        str(p["Cedula"]), 
                        p["Email"], 
                        p["Max Carga"], 
                        p["Materias"]
                    )
                    self.lista_profesores.append(profesor)
                print(" > Profesores cargados localmente con éxito.")
                
            except FileNotFoundError:
                print(" > Advertencia: No se encontró el archivo local 'profesores.json'. Verifique estar ejecutando en la misma carpeta.")
            except Exception as e:
                print(f" > Error al procesar el archivo local: {e}")

            # 2. Carga Web de Materias
            if url_materias:
                datos_materias = self._solicitar_json(url_materias)
                
                for m in datos_materias:
                    # Ajuste de claves exactas según el formato del servidor
                    materia = Materia(
                        m["Código"], 
                        m["Nombre"], 
                        m["Secciones"]
                    )
                    self.lista_materias.append(materia)
                print(" > Materias cargadas desde la red con éxito.")

            print("\n¡Proceso de carga finalizado!")

        except ValueError:
            print("\nError: Entrada no válida al seleccionar opciones del menú.")
        except requests.exceptions.RequestException:
            print("\nError de conexión: No se pudieron cargar las materias desde internet.")
<<<<<<< Updated upstream
        except KeyError:
            print("\nError de estructura: Los datos cargados no coinciden con los atributos esperados.")
    
    
=======
        except KeyError as e:
            print(f"\nError de estructura: La clave {e} no se encontró en los datos cargados.")
            
>>>>>>> Stashed changes
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
        - Complejidad de Espacio: O(1).
        """
        if not self.lista_profesores:
            print("No hay profesores registrados.")
            return
            
        print("\n--- LISTA DE PROFESORES ---")
        for i, profesor in enumerate(self.lista_profesores):
            print(f"{i}. {profesor.nombre} - Cédula: {profesor.cedula}")

    def agregar_profesor(self):
        """
        Solicita datos al usuario y añade un nuevo profesor a la lista.
        
        Consideraciones de eficiencia:
<<<<<<< Updated upstream
        - Complejidad de Tiempo: O(1) amortizado por el append a la lista.
        - Complejidad de Espacio: O(1) adicional para el nuevo objeto instanciado.
=======
        - Complejidad de Tiempo: O(1) amortizado por el append.
        - Complejidad de Espacio: O(1) adicional.
>>>>>>> Stashed changes
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
        - Complejidad de Tiempo: O(P) en el peor caso.
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
            print(f"{i}. {materia.codigo} - {materia.nombre} ({materia.num_secciones} secciones)")

    def agregar_materia(self):
        """
        Solicita datos al usuario y añade una nueva materia a la lista.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(1) amortizado.
        - Complejidad de Espacio: O(1).
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
<<<<<<< Updated upstream
        - Complejidad de Tiempo: O(P * K + M), donde P son los profesores, K las materias por profesor, 
          y M el desplazamiento al hacer pop en la lista.
=======
        - Complejidad de Tiempo: O(P * K + M).
>>>>>>> Stashed changes
        - Complejidad de Espacio: O(1).
        """
        self.ver_materias()
        if not self.lista_materias:
            return
            
        try:
            indice = int(input("Ingrese el índice de la materia a eliminar: "))
            materia_a_eliminar = self.lista_materias[indice]
            
            for prof in self.lista_profesores:
                if materia_a_eliminar.codigo in prof.materias_permitidas:
                    print(f"Advertencia: Afecta al profesor {prof.nombre}, quien la tiene permitida.")
            
            self.lista_materias.pop(indice)
            print(f"Materia '{materia_a_eliminar.nombre}' eliminada con éxito.")
            
        except ValueError:
            print("Error: Debe ingresar un número entero.")
        except IndexError:
            print("Error: Índice fuera de rango.")

    def modificar_secciones_materia(self):
        """
        Modifica el número de secciones de una materia.
        
        Consideraciones de eficiencia:
<<<<<<< Updated upstream
        - Complejidad de Tiempo: O(P * K) en el peor caso (si secciones == 0) para verificar las asignaciones.
=======
        - Complejidad de Tiempo: O(P * K).
>>>>>>> Stashed changes
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
            materia_seleccionada.num_secciones = nuevas_secciones 
            print(f"Secciones actualizadas a {nuevas_secciones}.")
            
        except ValueError:
            print("Error: Debe ingresar un número entero.")
        except IndexError:
            print("Error: Índice fuera de rango.")

    def _inicializar_bloques(self):
        """
        Instancia y retorna una lista estática de los bloques horarios válidos.
        
        Consideraciones de eficiencia:
<<<<<<< Updated upstream
        - Complejidad de Tiempo: O(1), se crean y retornan instancias predefinidas.
        - Complejidad de Espacio: O(1), una lista pequeña y constante de bloques.
=======
        - Complejidad de Tiempo: O(1).
        - Complejidad de Espacio: O(1).
>>>>>>> Stashed changes
        """
        return [
            BloqueHorario("Lunes y Miércoles", "7:00-8:30"),
            BloqueHorario("Lunes y Miércoles", "8:45-10:15"),
            BloqueHorario("Martes y Jueves", "7:00-8:30"),
            BloqueHorario("Martes y Jueves", "8:45-10:15")
        ]

    def generar_horarios(self):
        """
        Algoritmo principal que distribuye las materias, secciones y profesores en los salones y bloques.
        
        Consideraciones de eficiencia:
<<<<<<< Updated upstream
        - Complejidad de Tiempo: O(M * S * B * (P * H)), donde M son materias, S secciones por materia, 
          B bloques horarios, P profesores y H tamaño del horario actual.
        - Complejidad de Espacio: O(B + H), diccionario auxiliar para uso de salones y la lista de secciones asignadas.
        """
        if not self.lista_materias or not self.lista_profesores:
            print("Advertencia: No se puede generar el horario sin materias y profesores registrados en el sistema.")
=======
        - Complejidad de Tiempo: O(M * S * B * (P * H)).
        - Complejidad de Espacio: O(B + H).
        """
        if not self.lista_materias or not self.lista_profesores:
            print("Advertencia: No se puede generar el horario sin materias y profesores registrados.")
>>>>>>> Stashed changes
            return

        self.horario_generado = []
        bloques_validos = self._inicializar_bloques()
        
        uso_salones = {bloque: 0 for bloque in bloques_validos}

        for materia in self.lista_materias:
            if materia.num_secciones <= 0:
                continue

            for _ in range(materia.num_secciones):
                bloque_seleccionado = None
                
                for bloque in bloques_validos:
                    if uso_salones[bloque] < 30:
                        bloque_seleccionado = bloque
                        break

                profesor_asignado = None
                numero_salon = 0

                if bloque_seleccionado is not None:
                    profesor_asignado = self._buscar_profesor_disponible(materia.codigo, bloque_seleccionado)
                    uso_salones[bloque_seleccionado] += 1
                    numero_salon = uso_salones[bloque_seleccionado]

                nueva_seccion = SeccionAsignada(materia, profesor_asignado, bloque_seleccionado, numero_salon)
                self.horario_generado.append(nueva_seccion)

        print("\nGeneración completada.")
        self.mostrar_reportes_generacion()

    def _buscar_profesor_disponible(self, codigo_materia, bloque):
        """
<<<<<<< Updated upstream
        Verifica la viabilidad de un profesor comprobando sus materias permitidas, carga actual y choques de horario.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(P * H), itera por P profesores y en cada uno verifica el tamaño del horario H.
        - Complejidad de Espacio: O(1), solo usa variables contadoras.
=======
        Verifica la viabilidad de un profesor comprobando sus materias permitidas, carga actual y choques.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(P * H).
        - Complejidad de Espacio: O(1).
>>>>>>> Stashed changes
        """
        for profesor in self.lista_profesores:
            if codigo_materia not in profesor.materias_permitidas:
                continue

            carga_actual = 0
            choque_horario = False

            for seccion in self.horario_generado:
                if seccion.profesor == profesor:
                    carga_actual += 1
                    if seccion.bloque == bloque:
                        choque_horario = True

            if carga_actual >= profesor.max_materias_permitidas:
                continue

            if choque_horario:
                continue

            return profesor

        return None

    def mostrar_reportes_generacion(self):
        """
        Calcula e imprime métricas estadísticas resultantes de la asignación de horarios.
        
        Consideraciones de eficiencia:
<<<<<<< Updated upstream
        - Complejidad de Tiempo: O(H + M + B), donde H es el tamaño del horario generado, M las materias pedidas y B los bloques.
        - Complejidad de Espacio: O(B + M), diccionarios auxiliares para agrupar capacidades y rastrear el éxito de materias.
=======
        - Complejidad de Tiempo: O(H + M + B).
        - Complejidad de Espacio: O(B + M).
>>>>>>> Stashed changes
        """
        if not self.horario_generado:
            print("\nNo hay horarios generados para mostrar reportes.")
            return

        secciones_huerfanas = 0
        secciones_sin_salon = 0
        capacidad_bloques = {}
        materias_seguimiento = {}

        for seccion in self.horario_generado:
            if seccion.profesor is None:
                secciones_huerfanas += 1
                
            if seccion.bloque is None:
                secciones_sin_salon += 1
            else:
                clave_bloque = f"{seccion.bloque.dia} {seccion.bloque.rango_hora}"
                capacidad_bloques[clave_bloque] = capacidad_bloques.get(clave_bloque, 0) + 1

            cod_mat = seccion.materia.codigo
            if cod_mat not in materias_seguimiento:
                materias_seguimiento[cod_mat] = {"pedidas": seccion.materia.num_secciones, "asignadas_con_exito": 0}
                
            if seccion.profesor is not None and seccion.bloque is not None:
                materias_seguimiento[cod_mat]["asignadas_con_exito"] += 1

        materias_cerradas = 0
        for datos in materias_seguimiento.values():
            if datos["asignadas_con_exito"] == datos["pedidas"] and datos["pedidas"] > 0:
                materias_cerradas += 1

        print("\n--- REPORTE ESTADÍSTICO DE GENERACIÓN ---")
<<<<<<< Updated upstream
        print(f"Secciones huérfanas (falta de profesores calificados/disponibles): {secciones_huerfanas}")
        print(f"Secciones sin salón (exceso de límite físico de 30 salones): {secciones_sin_salon}")
=======
        print(f"Secciones huérfanas (falta de profesores): {secciones_huerfanas}")
        print(f"Secciones sin salón (exceso de capacidad): {secciones_sin_salon}")
>>>>>>> Stashed changes
        print(f"Materias cerradas exitosamente al 100%: {materias_cerradas}")

        try:
            total_materias = len(self.lista_materias)
            porcentaje = (materias_cerradas / total_materias) * 100
            print(f"Porcentaje de éxito general: {porcentaje:.2f}%")
        except ZeroDivisionError:
            print("Porcentaje de éxito general: 0.00% (División por cero evitada)")

        print("\nCapacidad sobrante por bloque:")
        bloques_base = self._inicializar_bloques()
        for b in bloques_base:
            clave = f"{b.dia} {b.rango_hora}"
            usados = capacidad_bloques.get(clave, 0)
            disponibles = 30 - usados
<<<<<<< Updated upstream
            print(f"  > {clave}: {disponibles} salones disponibles")
=======
            print(f"  > {clave}: {disponibles} salones disponibles")

    def modificar_horarios(self):
        """
        Permite al usuario editar manualmente las asignaciones de profesores y bloques en el horario.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(H + P*H + B*H), itera sobre el horario y luego valida disponibilidad.
        - Complejidad de Espacio: O(U + S), almacena materias únicas y secciones filtradas en memoria.
        """
        if not self.horario_generado:
            print("\nError: El horario está vacío. Genere o cargue un horario primero.")
            return

        # Extraer materias únicas presentes en el horario
        materias_unicas = {}
        for sec in self.horario_generado:
            if sec.materia and sec.materia.codigo not in materias_unicas:
                materias_unicas[sec.materia.codigo] = sec.materia

        lista_mat = list(materias_unicas.values())
        print("\n--- MATERIAS EN EL HORARIO ---")
        for i, mat in enumerate(lista_mat):
            print(f"{i}. {mat.codigo} - {mat.nombre}")

        try:
            indice_mat = int(input("Seleccione el índice de la materia a modificar: "))
            materia_seleccionada = lista_mat[indice_mat]
            
            # Filtrar secciones de esa materia
            secciones_filtradas = [s for s in self.horario_generado if s.materia == materia_seleccionada]
            
            print(f"\n--- SECCIONES DE {materia_seleccionada.nombre} ---")
            for i, sec in enumerate(secciones_filtradas):
                prof_nombre = sec.profesor.nombre if sec.profesor else "Sin Profesor"
                bloque_info = f"{sec.bloque.dia} {sec.bloque.rango_hora}" if sec.bloque else "Sin Bloque"
                print(f"{i}. Bloque: {bloque_info} | Profesor: {prof_nombre} | Salón: {sec.numero_salon}")
                
            indice_sec = int(input("Seleccione el índice de la sección a editar: "))
            seccion_a_editar = secciones_filtradas[indice_sec]

            print("\n--- OPCIONES DE MODIFICACIÓN ---")
            print("A. Cambiar Profesor")
            print("B. Cambiar Horario (Bloque)")
            opcion_mod = input("Elija una opción (A/B): ").strip().upper()

            if opcion_mod == 'A':
                profesores_validos = []
                for p in self.lista_profesores:
                    if materia_seleccionada.codigo in p.materias_permitidas:
                        # Reutilizar lógica manual para medir carga y choques
                        carga = sum(1 for s in self.horario_generado if s.profesor == p)
                        choque = any(s.bloque == seccion_a_editar.bloque and s.profesor == p for s in self.horario_generado)
                        
                        if carga < p.max_materias_permitidas and not choque:
                            profesores_validos.append(p)
                
                if not profesores_validos:
                    print("No hay profesores disponibles para esta materia en este bloque.")
                    return
                    
                print("\n--- PROFESORES DISPONIBLES ---")
                for i, p in enumerate(profesores_validos):
                    print(f"{i}. {p.nombre}")
                
                indice_prof = int(input("Seleccione el índice del nuevo profesor: "))
                seccion_a_editar.profesor = profesores_validos[indice_prof]
                print("Profesor actualizado exitosamente.")

            elif opcion_mod == 'B':
                bloques_base = self._inicializar_bloques()
                bloques_validos = []
                
                for b in bloques_base:
                    # Validar salones disponibles (< 30)
                    ocupacion = sum(1 for s in self.horario_generado if s.bloque and s.bloque.dia == b.dia and s.bloque.rango_hora == b.rango_hora)
                    if ocupacion < 30:
                        bloques_validos.append(b)
                
                if not bloques_validos:
                    print("No hay bloques con salones disponibles.")
                    return
                    
                print("\n--- BLOQUES DISPONIBLES ---")
                for i, b in enumerate(bloques_validos):
                    print(f"{i}. {b.dia} {b.rango_hora}")
                
                indice_bloque = int(input("Seleccione el índice del nuevo bloque: "))
                nuevo_bloque = bloques_validos[indice_bloque]
                
                # Buscar profesor para este nuevo bloque
                nuevo_profesor = self._buscar_profesor_disponible(materia_seleccionada.codigo, nuevo_bloque)
                
                seccion_a_editar.bloque = nuevo_bloque
                seccion_a_editar.profesor = nuevo_profesor
                # Mantenemos o recalculamos el número de salón (por simplicidad, mantenemos si había o damos uno nuevo)
                ocupacion_nuevo = sum(1 for s in self.horario_generado if s.bloque and s.bloque.dia == nuevo_bloque.dia and s.bloque.rango_hora == nuevo_bloque.rango_hora)
                seccion_a_editar.numero_salon = ocupacion_nuevo  # Simplificación de reasignación
                
                print("Bloque (y profesor asociado) actualizados exitosamente.")
                if nuevo_profesor is None:
                    print("Nota: Ningún profesor estaba disponible en ese nuevo bloque, se asignó None.")

            else:
                print("Opción no válida.")

        except ValueError:
            print("Error: Entrada inválida. Debe introducir un número entero.")
        except IndexError:
            print("Error: Índice fuera de rango.")

    def guardar_horario_csv(self):
        """
        Exporta el horario generado a un archivo CSV.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(H), donde H es el número de secciones asignadas.
        - Complejidad de Espacio: O(1) auxiliar en memoria (escritura en flujo).
        """
        if not self.horario_generado:
            print("\nError: No hay horario generado para guardar.")
            return
            
        try:
            with open("horario_exportado.csv", mode="w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(["Materia", "Profesor", "Dia", "Rango Hora", "Salon"])
                
                for sec in self.horario_generado:
                    codigo_mat = sec.materia.codigo if sec.materia else "Ninguna"
                    cedula_prof = sec.profesor.cedula if sec.profesor else "Ninguno"
                    dia = sec.bloque.dia if sec.bloque else "Ninguno"
                    hora = sec.bloque.rango_hora if sec.bloque else "Ninguno"
                    salon = sec.numero_salon if sec.numero_salon else "0"
                    
                    escritor.writerow([codigo_mat, cedula_prof, dia, hora, salon])
                    
            print("\nHorario exportado exitosamente a 'horario_exportado.csv'.")
        except (IOError, PermissionError):
            print("\nError: No se pudo escribir en el archivo. Asegúrese de que no esté abierto en otra aplicación.")

    def cargar_horario_csv(self):
        """
        Carga y reconstruye un horario desde un archivo CSV previamente guardado.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(N * (M + P)), donde N son las filas del CSV, M materias y P profesores.
        - Complejidad de Espacio: O(N), reconstruye la lista completa en memoria.
        """
        try:
            with open("horario_exportado.csv", mode="r", encoding="utf-8") as archivo:
                lector = csv.reader(archivo)
                next(lector)  # Omitir encabezados
                
                self.horario_generado = []
                for fila in lector:
                    if len(fila) < 5:
                        continue
                        
                    mat_cod, prof_ced, dia, hora, salon_str = fila
                    
                    # Buscar referencias cruzadas
                    materia_obj = next((m for m in self.lista_materias if m.codigo == mat_cod), None)
                    profesor_obj = next((p for p in self.lista_profesores if p.cedula == prof_ced), None)
                    
                    bloque_obj = None
                    if dia != "Ninguno" and hora != "Ninguno":
                        bloque_obj = BloqueHorario(dia, hora)
                        
                    try:
                        num_salon = int(salon_str)
                    except ValueError:
                        num_salon = 0
                        
                    nueva_seccion = SeccionAsignada(materia_obj, profesor_obj, bloque_obj, num_salon)
                    self.horario_generado.append(nueva_seccion)
                    
            print("\nHorario cargado exitosamente desde 'horario_exportado.csv'.")
        except FileNotFoundError:
            print("\nError: No se encontró el archivo 'horario_exportado.csv'. Guarde uno primero.")

    def mostrar_estadisticas(self):
        """
        Procesa y renderiza gráficas visuales utilizando matplotlib.
        
        Consideraciones de eficiencia:
        - Complejidad de Tiempo: O(H + P + M), itera el horario, profesores y materias.
        - Complejidad de Espacio: O(B + P + M), almacena los vectores de datos para graficar.
        """
        if not MATPLOTLIB_INSTALADO:
            print("\nError: La librería matplotlib no está instalada en este entorno.")
            print("Ejecute 'pip install matplotlib' en la terminal para habilitar esta función.")
            return
            
        if not self.horario_generado:
            print("\nError: No hay datos de horario para graficar estadísticas.")
            return

        try:
            # Preparar el lienzo general
            fig, axs = plt.subplots(1, 3, figsize=(15, 5))
            fig.suptitle('Estadísticas del Sistema de Horarios', fontsize=16)

            # --- Gráfica 1: Salones ocupados por bloque ---
            conteo_bloques = {}
            for sec in self.horario_generado:
                if sec.bloque:
                    clave = f"{sec.bloque.dia[:3]} {sec.bloque.rango_hora}"
                    conteo_bloques[clave] = conteo_bloques.get(clave, 0) + 1
            
            etiquetas_b = list(conteo_bloques.keys())
            valores_b = list(conteo_bloques.values())
            
            axs[0].bar(etiquetas_b, valores_b, color='skyblue')
            axs[0].set_title('Ocupación de Salones por Bloque')
            axs[0].set_ylabel('Cant. Salones')
            axs[0].tick_params(axis='x', rotation=45)

            # --- Gráfica 2: Porcentaje de materias asignadas vs límite (Profesores) ---
            etiquetas_p = []
            porcentajes_p = []
            for prof in self.lista_profesores:
                carga = sum(1 for s in self.horario_generado if s.profesor == prof)
                if prof.max_materias_permitidas > 0:
                    pct = (carga / prof.max_materias_permitidas) * 100
                else:
                    pct = 0
                etiquetas_p.append(prof.nombre.split()[0]) # Solo primer nombre
                porcentajes_p.append(pct)

            axs[1].bar(etiquetas_p, porcentajes_p, color='lightgreen')
            axs[1].set_title('% de Carga Asignada por Profesor')
            axs[1].set_ylabel('% del Límite Máximo')
            axs[1].tick_params(axis='x', rotation=45)
            axs[1].set_ylim(0, 110)

            # --- Gráfica 3: Porcentaje de secciones cerradas (Materias) ---
            etiquetas_m = []
            porcentajes_m = []
            for mat in self.lista_materias:
                asignadas = sum(1 for s in self.horario_generado if s.materia == mat and s.profesor is not None)
                if mat.num_secciones > 0:
                    pct = (asignadas / mat.num_secciones) * 100
                else:
                    pct = 0
                etiquetas_m.append(mat.codigo)
                porcentajes_m.append(pct)

            axs[2].bar(etiquetas_m, porcentajes_m, color='salmon')
            axs[2].set_title('% Secciones Cubiertas por Materia')
            axs[2].set_ylabel('% de Éxito')
            axs[2].tick_params(axis='x', rotation=45)
            axs[2].set_ylim(0, 110)

            plt.tight_layout()
            plt.show()

        except ZeroDivisionError:
            print("\nError interno: Intento de división por cero al calcular porcentajes.")
        except Exception as e:
            print(f"\nOcurrió un error inesperado al generar las gráficas: {e}")
>>>>>>> Stashed changes
