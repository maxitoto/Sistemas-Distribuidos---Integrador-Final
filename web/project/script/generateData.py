## init 
import json
import os

# 1. Definir la ruta física en el Host
ruta_base = "../data"

# Aseguramos que la carpeta exista
os.makedirs(ruta_base, exist_ok=True)

# 2. Estructura de Editoriales (Contrato: id, nombre, pais)
editoriales = [
    {"id": 1, "nombre": "Distribuidos Sur", "pais": "Argentina"},
    {"id": 2, "nombre": "Tech Books Publishing", "pais": "Estados Unidos"},
    {"id": 3, "nombre": "Alpha Editorial", "pais": "España"},
    {"id": 4, "nombre": "Nova Ciencia", "pais": "México"},
    {"id": 5, "nombre": "Digital Future Press", "pais": "Canadá"},
    {"id": 6, "nombre": "Open Knowledge", "pais": "Reino Unido"},
    {"id": 7, "nombre": "Data Minds", "pais": "Alemania"},
    {"id": 8, "nombre": "Code Masters", "pais": "Chile"},
    {"id": 9, "nombre": "Parallel Systems House", "pais": "Brasil"},
    {"id": 10, "nombre": "Quantum Reads", "pais": "Japón"}
]

# 3. Estructura de Autores (Contrato: id, nombre, editorial_id)
autores = [
    {"id": 1, "nombre": "Carlos Toledo", "editorial_id": 1},
    {"id": 2, "nombre": "Martin Fowler", "editorial_id": 2},
    {"id": 3, "nombre": "Ada Lovelace", "editorial_id": 2},
    {"id": 4, "nombre": "Donald Knuth", "editorial_id": 3},
    {"id": 5, "nombre": "Linus Torvalds", "editorial_id": 4},
    {"id": 6, "nombre": "Grace Hopper", "editorial_id": 5},
    {"id": 7, "nombre": "Leslie Lamport", "editorial_id": 6},
    {"id": 8, "nombre": "Barbara Liskov", "editorial_id": 7},
    {"id": 9, "nombre": "Edsger Dijkstra", "editorial_id": 8},
    {"id": 10, "nombre": "Ken Thompson", "editorial_id": 9},
    {"id": 11, "nombre": "Dennis Ritchie", "editorial_id": 9},
    {"id": 12, "nombre": "Tim Berners-Lee", "editorial_id": 10},
    {"id": 13, "nombre": "Andrew Tanenbaum", "editorial_id": 6},
    {"id": 14, "nombre": "Bjarne Stroustrup", "editorial_id": 3},
    {"id": 15, "nombre": "James Gosling", "editorial_id": 5}
]

# 4. Estructura de Libros (Contrato: id, titulo, autor_id)
libros = [
    {"id": 1, "titulo": "Diseño de Sistemas Distribuidos", "autor_id": 1},
    {"id": 2, "titulo": "Concurrencia en NFS", "autor_id": 1},
    {"id": 3, "titulo": "Refactoring 2nd Edition", "autor_id": 2},
    {"id": 4, "titulo": "Notas sobre la Máquina Analítica", "autor_id": 3},
    {"id": 5, "titulo": "The Art of Computer Programming", "autor_id": 4},
    {"id": 6, "titulo": "Kernel Development Essentials", "autor_id": 5},
    {"id": 7, "titulo": "Compilers and Optimizations", "autor_id": 6},
    {"id": 8, "titulo": "Distributed Algorithms", "autor_id": 7},
    {"id": 9, "titulo": "Programming Methodology", "autor_id": 8},
    {"id": 10, "titulo": "Structured Programming", "autor_id": 9},
    {"id": 11, "titulo": "Unix Internals", "autor_id": 10},
    {"id": 12, "titulo": "The C Programming Language", "autor_id": 11},
    {"id": 13, "titulo": "The Semantic Web", "autor_id": 12},
    {"id": 14, "titulo": "Modern Operating Systems", "autor_id": 13},
    {"id": 15, "titulo": "Computer Networks", "autor_id": 13},
    {"id": 16, "titulo": "The C++ Programming Language", "autor_id": 14},
    {"id": 17, "titulo": "Java for Distributed Systems", "autor_id": 15},
    {"id": 18, "titulo": "Concurrent Programming Patterns", "autor_id": 7},
    {"id": 19, "titulo": "Advanced Refactoring", "autor_id": 2},
    {"id": 20, "titulo": "Clean Architecture Concepts", "autor_id": 8},
    {"id": 21, "titulo": "Parallel Computing Fundamentals", "autor_id": 1},
    {"id": 22, "titulo": "Data Structures in Practice", "autor_id": 4},
    {"id": 23, "titulo": "Operating Systems Design", "autor_id": 13},
    {"id": 24, "titulo": "Algorithms and Complexity", "autor_id": 9},
    {"id": 25, "titulo": "Cloud Native Applications", "autor_id": 15}
]

# 5. Función para guardar los archivos
def guardar_json(nombre_archivo, datos):
    ruta_completa = os.path.join(ruta_base, nombre_archivo)
    with open(ruta_completa, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f"✅ Archivo creado: {ruta_completa}")

# 6. Ejecutar la creación
if __name__ == "__main__":
    print("Iniciando la siembra de datos...")
    guardar_json("editorial.json", editoriales)
    guardar_json("autor.json", autores)
    guardar_json("libro.json", libros)
    
    # Asegurar permisos para que www-data / NFS puedan modificarlos luego
    os.system(f"chmod 664 {ruta_base}/*.json")
    print("🎯 ¡Datos sembrados con éxito!")