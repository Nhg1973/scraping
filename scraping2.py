import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient

def obtener_productos():
    # URL base de la página
    base_url = 'https://cocinerosargentinos.com/saludables?page={}'

    # Configuración del navegador Firefox
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = True  # Ejecución en modo sin cabeza (headless)

    # Inicialización del driver de Firefox
    driver = webdriver.Firefox(options=firefox_options)

    print("Iniciando el navegador Firefox...")

    # Lista para almacenar todos los productos
    lista_productos = []

    # Iterar sobre todas las páginas del paginador
    total_paginas = 1  # Definir el número total de páginas
    for pagina in range(1, total_paginas + 1):
        # Construir la URL de la página actual
        url = base_url.format(pagina)

        # Acceder a la página
        driver.get(url)

        # Esperar a que los elementos se carguen
        wait_time = 10
        print(f"Esperando {wait_time} segundos para que la página {pagina} se cargue...")
        driver.implicitly_wait(wait_time)

        # Encontrar elementos dentro de la etiqueta <div class="item-title">
        elementos_div = driver.find_elements(By.XPATH, "//div[@class='item-title']/a")

        # Obtener la extensión y nombre de cada producto
        productos_pagina = []
        for elemento in elementos_div:
            extension = elemento.get_attribute("href").split("/")[-1]
            nombre = elemento.text.strip()
            productos_pagina.append({"extension": extension, "nombre": nombre})

        # Agregar los productos de la página actual a la lista general
        lista_productos.extend(productos_pagina)

    # Cerrar el navegador
    print("Cerrando el navegador...")
    driver.quit()

    # Devolver la lista de productos obtenida
    return lista_productos

def mostrar_nombres_productos(lista_productos):
    # Mostrar la lista de nombres de productos
    print("Nombres de productos:")
    for idx, producto in enumerate(lista_productos, start=1):
        print(f"{idx}: {producto['nombre']}")

def crear_nuevo_diccionario(lista_productos):
    # Pedir al usuario los productos que desea agregar al nuevo diccionario
    indices_seleccionados = input("Ingrese los números de productos que desea agregar (separados por comas): ")
    indices = [int(idx) - 1 for idx in indices_seleccionados.split(",")]

    # Crear el nuevo diccionario de productos seleccionados
    nuevo_diccionario = {}
    for i, idx in enumerate(indices, start=1):
        if idx < len(lista_productos):
            producto = lista_productos[idx]
            nuevo_diccionario[f"ID-{i}"] = {
                "extension": producto['extension'],
                "nombre": producto['nombre']
            }

    # Mostrar el nuevo diccionario de productos
    print("\nNuevo diccionario de productos:")
    for identificacion, producto in nuevo_diccionario.items():
        print(f"{identificacion}: {producto}")

    # Devolver el nuevo diccionario creado
    return nuevo_diccionario

def obtener_datos_por_extension(extension):
    # Configuración del navegador Firefox
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = True  # Ejecución en modo sin cabeza (headless)

    # Inicialización del driver de Firefox
    driver = webdriver.Firefox(options=firefox_options)

    print(f"Obteniendo datos para la extensión: {extension}...")

    # URL de la página del producto específico
    url = f'https://cocinerosargentinos.com/saludables/{extension}'

    # Acceder a la página del producto específico
    driver.get(url)

    # Esperar a que los elementos se carguen
    wait_time = 10
    print(f"Esperando {wait_time} segundos para que la página se cargue...")
    driver.implicitly_wait(wait_time)


      # Encontrar elementos correspondientes a la descripción, video e imagen
    try:
        description_element = driver.find_element(By.XPATH, "//div[@id='product_tabs_description']//div[@class='std']")
        description = description_element.text
    except NoSuchElementException:
        print("No se encontró el elemento de la descripción.")
        description = None

    try:
        video_element = driver.find_element(By.XPATH, "//div[@id='tutorial']//iframe[@class='embed-responsive-item']")
        video_src = video_element.get_attribute("src")
    except NoSuchElementException:
        print("El elemento de video no se encontró en la página.")
        video_src = None

    try:
        image_element = driver.find_element(By.XPATH, "//div[@class='slick-track']//img[@class='slick-slide slick-current slick-active']")
        image_src = image_element.get_attribute("src")
    except NoSuchElementException:
        print("El elemento de imagen no se encontró en la página.")
        image_src = None

    # Encontrar elementos dentro de la etiqueta <div class="short-description">
    short_description_element = driver.find_element(By.CLASS_NAME, 'short-description')
    short_description = short_description_element.text if short_description_element else None


    # Cerrar el navegador
    print("Cerrando el navegador...")
    driver.quit()

    ingredientes_limpios = []
    lineas = short_description.split('\n')

    # Patrón para detectar títulos como "Omelette de espinaca y queso:"
    titulo_patron = re.compile(r'^.*?:$')

    # Patrón para detectar elementos de lista con viñetas distintas
    viñeta_patron = re.compile(r'^\s*[●•–-]\s*(.*?)$')

    i = 0
    while i < len(lineas):
        # Verificar si la línea coincide con el patrón de título
        titulo_match = titulo_patron.match(lineas[i].strip())
        if titulo_match:
            plato = titulo_match.group().strip(':')
            i += 1

            ingredientes_plato = []
            # Buscar elementos de lista con viñetas bajo el título y agregar a la lista de ingredientes
            while i < len(lineas):
                ingrediente_match = viñeta_patron.match(lineas[i].strip())
                if ingrediente_match:
                    ingredientes_plato.append(ingrediente_match.group(1).strip())
                    i += 1
                else:
                    break
            
            # Agregar ingredientes al resultado si se encontraron
            if ingredientes_plato:
                ingredientes_limpios.append({plato: ingredientes_plato})
        else:
            # Si no hay título, asumir que las líneas contienen ingredientes directamente
            ingredientes_plato = []
            while i < len(lineas):
                ingrediente_match = viñeta_patron.match(lineas[i].strip())
                if ingrediente_match:
                    ingredientes_plato.append(ingrediente_match.group(1).strip())
                    i += 1
                else:
                    break
            
            # Agregar ingredientes al resultado si se encontraron
            if ingredientes_plato:
                ingredientes_limpios.append({"Sin título": ingredientes_plato})
            else:
                i += 1

    return {
        "ingredientes": ingredientes_limpios,
        "description": description,
        "video_src": video_src,
        "image_src": image_src
    }



def obtener_datos_de_productos(nuevo_diccionario):
    for identificacion, producto in nuevo_diccionario.items():
        extension = producto['extension']
        nombre = producto['nombre']
        print(f"\nDatos del producto '{nombre}' con extensión '{extension}':")
        datos = obtener_datos_por_extension(extension)
        print(f"Producto {nombre}:\n{datos}")


        ingredientes = []
        # Expresión regular para encontrar la cantidad y el ingrediente
        cantidad_patron = re.compile(r'^(\d+\s?\w+\.?|\w+\s?-?\s?\d+\s?\w+\.?)')
        for grupo in datos['ingredientes']:
            for items in grupo.values():
                for item in items:
                    # Buscar coincidencias de cantidad con la expresión regular
                    match = cantidad_patron.match(item)
                    if match:
                        cantidad = match.group()
                        ingrediente = item[len(cantidad):].strip('.').strip()  # Obtener el nombre del ingrediente
                        ingredientes.append({'name': ingrediente, 'quantity': cantidad})
                    else:
                        # Establecer un valor por defecto para la cantidad
                        ingredientes.append({'name': item, 'quantity': '1 cda.'})

        datos_modificados = {
            'title': nombre,
            'ingredients': ingredientes,
            'description': datos['description'],
            'video_src': datos['video_src'],
            'image_src': datos['image_src']
        }

        print(datos_modificados)


        consulta = input(f"Deseas guardar {nombre} en la base de datos? (Ingrese 'SI' para confirmar): ")

        if consulta.upper() == 'SI':
            
            # Guardar los datos en MongoDB
            guardar_en_mongo(datos_modificados)

       

def guardar_en_mongo(datos):
    # Reemplaza <usuario> y <contraseña> con tus credenciales de acceso
    usuario = "nahuelguerci"
    contraseña = "uRtpoys95zLVeOM0"

    # URL de conexión con usuario y contraseña incluidos
    uri = f"mongodb+srv://{usuario}:{contraseña}@cluster0.ufximyi.mongodb.net/recetas?retryWrites=true&w=majority"

    print("Conectando a la base de datos de MongoDB...")
    
    try:
        # Conectar a la base de datos de MongoDB
        client = MongoClient(uri)
        db = client['recetas']  # Reemplaza 'recetas' con el nombre de tu base de datos
        collection = db['saludables']  # Reemplaza 'saludables' con el nombre de tu colección

        # Insertar los datos en la colección
        # Envolver el diccionario de datos en una lista antes de insertar
        collection.insert_one(datos)  # Insertar un único documento
        print("Datos guardados en MongoDB")
    except Exception as e:
        print(f"Error al guardar en MongoDB: {e}")





# Llamar a la función para obtener todos los productos de las páginas
lista_productos = obtener_productos()

# Mostrar los nombres de los productos
mostrar_nombres_productos(lista_productos)

# Crear un nuevo diccionario de productos
nuevo_diccionario = crear_nuevo_diccionario(lista_productos)

# Obtiene ingredientes 
obtener_datos_de_productos(nuevo_diccionario)







