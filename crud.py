from pymongo import MongoClient

# Reemplaza <usuario> y <contraseña> con tus credenciales de acceso
usuario = "nahuelguerci"
contraseña = "uRtpoys95zLVeOM0"

# URL de conexión con usuario y contraseña incluidos
uri = f"mongodb+srv://{usuario}:{contraseña}@cluster0.ufximyi.mongodb.net/recetas?retryWrites=true&w=majority"

# Establecer la conexión con MongoDB
client = MongoClient(uri)
db = client['recetas']  # Selecciona la base de datos

# Selecciona la colección
collection = db['saludables']  # Reemplaza 'mi_coleccion' con el nombre de tu colección

while True:
    # Input para la acción
    print("Elige una acción:")
    print("1 - Listar recetas")
    print("2 - Leer (buscar) documentos")
    print("3 - Actualizar un documento")
    print("4 - Eliminar un documento")
    print("S - Salir")
    opcion = input("Ingresa el número de la acción que deseas realizar: ")

    # Realizar acciones según la opción seleccionada
    if opcion == "1":
        # Operación de listar documentos por el campo 'title'
        documentos = collection.find({}, {"_id": 0, "title": 1})  # Obtiene solo el campo 'title'
        print("Documentos con campo 'title':")
        for documento in documentos:
            print(documento.get('title'))

    elif opcion == "2":
        # Operación de leer (buscar) documentos por nombre de receta
        nombre_receta = input("Ingrese el nombre de la receta a buscar: ")
        resultado_busqueda = collection.find_one({"title": nombre_receta})
        if resultado_busqueda:
            print("\nResultado de la búsqueda:")
            print(resultado_busqueda)
        else:
            print(f"No se encontró la receta '{nombre_receta}' en la base de datos.")

    elif opcion == "3":
        # Operación de actualizar un documento por nombre de receta
        nombre_receta = input("Ingrese el nombre de la receta a actualizar: ")
        documento_actual = collection.find_one({"title": nombre_receta})
        if documento_actual:
            print("\nValores actuales del documento:")
            print(documento_actual)

            campo_a_modificar = input("Ingrese el nombre del campo que desea modificar: ")
            nuevo_valor = input(f"Ingrese el nuevo valor para '{campo_a_modificar}': ")

            filtro_actualizacion = {"title": nombre_receta}
            nuevos_valores = {"$set": {campo_a_modificar: nuevo_valor}}
            resultado_actualizacion = collection.update_one(filtro_actualizacion, nuevos_valores)
            if resultado_actualizacion.modified_count > 0:
                print(f"Documento de '{nombre_receta}' actualizado.")
            else:
                print(f"No se encontró la receta '{nombre_receta}' para actualizar.")
    elif opcion == "4":
        # Operación de eliminar un documento por nombre de receta
        nombre_receta = input("Ingrese el nombre de la receta a eliminar: ")
        resultado_eliminacion = collection.delete_one({"title": nombre_receta})
        if resultado_eliminacion.deleted_count > 0:
            print(f"Documento de '{nombre_receta}' eliminado.")
        else:
            print(f"No se encontró la receta '{nombre_receta}' para eliminar.")

    elif opcion.upper() == "S":
        # Salir del bucle
        break

    else:
        print("Opción no válida. Por favor, elige un número del 1 al 4.")

# Cerrar la conexión
client.close()
