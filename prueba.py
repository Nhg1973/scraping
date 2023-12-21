from pymongo import MongoClient
import re

# Lista de productos de interés
productos = ["Huevos","salo"]

# Reemplaza <usuario> y <contraseña> con tus credenciales de acceso
usuario = "nahuelguerci"
contraseña = "000000000000000000"

# URL de conexión con usuario y contraseña incluidos
uri = f"mongodb+srv://{usuario}:{contraseña}@cluster0.ufximyi.mongodb.net/recetas?retryWrites=true&w=majority"

# Conectar a la base de datos de MongoDB
client = MongoClient(uri)
db = client['recetas']  # Reemplaza 'recetas' con el nombre de tu base de datos
collection = db['saludables']  # Reemplaza 'saludables' con el nombre de tu colección

# Patrón de expresión regular para buscar los productos en los ingredientes
patron_busqueda = re.compile('|'.join(productos), re.IGNORECASE)  # Búsqueda insensible a mayúsculas y minúsculas

# Lista de consultas individuales por cada producto en la lista
consultas = []
for producto in productos:
    consulta = {
        "ingredientes": {
            "$elemMatch": {
                "Sin título": {
                    "$regex": producto,
                    "$options": "i"  # Hacer la búsqueda insensible a mayúsculas y minúsculas
                }
            }
        }
    }
    consultas.append(consulta)

# Realizar la consulta combinada para que estén presentes todos los productos en los ingredientes
resultados = collection.find({
    "$and": consultas
})

# Mostrar los resultados de la consulta
for resultado in resultados:
    print(resultado)

