from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from requests_html import HTMLSession
import time

def obtener_cantidad_productos(termino_busqueda):
    # Crear una sesión HTML
    session = HTMLSession()

    # Construir la URL de búsqueda
    base_url = 'https://www.jumbo.com.ar/'
    busqueda_url = f'{base_url}{termino_busqueda}?_q={termino_busqueda}&map=ft'

    # Realizar la solicitud GET a la URL de búsqueda
    response = session.get(busqueda_url)

    # Renderizar la página y esperar a que se cargue completamente
    response.html.render(timeout=30, sleep=5)  # Esperar hasta 30 segundos y esperar 5 segundos después de cargar

    # Encontrar el elemento que contiene la cantidad de productos
    cantidad_productos_element = response.html.find('.vtex-search-result-3-x-totalProducts--layout', first=True)

    # Verificar si se encontró el elemento y extraer la cantidad de productos
    if cantidad_productos_element:
        cantidad_texto = cantidad_productos_element.text
        # Obtener el número de productos desde el texto
        cantidad_productos = cantidad_texto.split()[0]
        return cantidad_productos
    else:
        return None

def obtener_productos(termino_busqueda):
   
    # Construir la URL de búsqueda
    base_url = 'https://www.jumbo.com.ar/'
    busqueda_url = f'{base_url}{termino_busqueda}?_q={termino_busqueda}&map=ft'


    # Ruta al driver de Gecko (GeckoDriver)
    gecko_driver_path = 'C:\\Users\\nahue\\OneDrive\\Desktop\\scraping\\geckodriver.exe'

    # Configuración del navegador Firefox
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = True  # Ejecución en modo sin cabeza (headless)

    # Inicialización del driver de Firefox sin executable_path
    driver = webdriver.Firefox(options=firefox_options)

    print("Iniciando el navegador Firefox...")

    # URL de la página
    url = busqueda_url

    print(f"Accediendo a la página: {url}")
    # Acceder a la página
    driver.get(url)

    # Esperar a que los elementos se carguen (puedes ajustar el tiempo según la velocidad de carga de la página)
    wait_time = 20
    print(f"Esperando {wait_time} segundos para que la página se cargue...")
    driver.implicitly_wait(wait_time)

    # Realizar dos scrolls en la página
    for i in range(2):
        print(f"Esperando {i} scroll ")
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)  # Scroll hasta el final de la página
        time.sleep(15)  # Esperar un poco después de cada scroll

    # Obtener la cantidad total de productos
    cantidad_total = int(obtener_cantidad_productos(termino_busqueda))

    # Calcular el número total de páginas necesarias
    productos_por_pagina = 20
    paginas_totales = -(-cantidad_total // productos_por_pagina)  # Cálculo del número de páginas redondeando hacia arriba

    # Hacer clic en el botón "Mostrar más" si es necesario
    for _ in range(paginas_totales - 1):
        try:
            mostrar_mas = driver.find_element(By.XPATH, "//div[contains(text(), 'Mostrar más')]")
            action = ActionChains(driver)
            action.move_to_element(mostrar_mas).click().perform()
            time.sleep(5)  # Esperar a que se carguen los productos
        except Exception as e:
            print(f"No se pudo encontrar el botón 'Mostrar más': {str(e)}")

    # Encontrar elementos de marca y descripción después de los scrolls y la carga adicional
    marcas_elementos = driver.find_elements(By.CLASS_NAME, 'vtex-product-summary-2-x-productBrandName')
    descripciones_elementos = driver.find_elements(By.CLASS_NAME, 'vtex-product-summary-2-x-brandName')

    # Crear un diccionario para almacenar los productos
    productos = {}
    for i in range(len(marcas_elementos)):
        productos[f'ID-{i+1}'] = (marcas_elementos[i].text, descripciones_elementos[i].text)

    # Imprimir el diccionario de productos con sus respectivos ID
    print("Productos:")
    for product_id, (marca, descripcion) in productos.items():
        print(f"ID: {product_id}, Marca: {marca}, Descripción: {descripcion}")

    # Cerrar el navegador
    print("Cerrando el navegador...")
    driver.quit()


# Obtener el término de búsqueda del usuario
termino_busqueda = input("Ingrese el producto a buscar: ")

# Obtener la cantidad de productos para el término de búsqueda
cantidad = obtener_cantidad_productos(termino_busqueda)

if cantidad is not None:
    print(f"Para '{termino_busqueda}' hay {cantidad} productos disponibles en Jumbo.")
    # Obtener la lista de productos por marca y descripción
    obtener_productos(termino_busqueda)
else:
    print(f"No se encontraron resultados para '{termino_busqueda}' en Jumbo.")
