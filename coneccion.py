import mysql.connector

# Configura la conexión a tu base de datos
config = {
    'user': 'root',
    'password': 'L@nacion12',
    'host': 'localhost',  # Puede ser una dirección IP o un nombre de dominio
    'database': 'unlp',
    'raise_on_warnings': True  # Esto levantará excepciones en caso de errores
}

try:
    # Crea la conexión a la base de datos
    conexion = mysql.connector.connect(**config)

    if conexion.is_connected():
        print("Conexión establecida a la base de datos")

        # Por ejemplo, puedes crear un cursor para ejecutar consultas SQL
        cursor = conexion.cursor()

        # Ejemplo: consultar datos de una tabla
        cursor.execute("SELECT * FROM eje1 WHERE legajo = 3")


        filas = cursor.fetchmany(size=3)

        # Mostrar los resultados
        for fila in filas:
            print(fila)

        # No olvides cerrar el cursor y la conexión cuando hayas terminado
        cursor.close()
        conexion.close()
        print("Conexión cerrada")

except mysql.connector.Error as error:
    print("Error al conectar a la base de datos:", error)
