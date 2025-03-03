import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_pdf_viewer import pdf_viewer
import ee
import os
import leafmap.foliumap as leafmap
import folium
import rioxarray
from streamlit_folium import st_folium
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.colors import ListedColormap
from PIL import Image  # Para guardar imágenes con transparencia



# Sidebar
with st.sidebar:
    st.markdown("""
        # Dinámica de procesos fisicoquímicos y biológicos
        Proyecto final del curso \n
        *Uso de imágenes satelitales de Global Surface Water Explorer para la identificación de cuerpos de agua en la región del río Magdalena, Colombia.*
    """)
    st.markdown("<br><br><br>", unsafe_allow_html=True)  # Ajusta el número de <br> según necesites

    st.sidebar.image("images/logo.jpg", width=150)
    # Texto en la barra lateral
    st.sidebar.markdown(
        """
        <div style="text-align: left;">
            <p><strong>Prof. Luis Carlos Belalcazar</strong><br> Universidad Nacional de Colombia</p>
        </div>
        <div style="text-align: rigth;">
            <p><strong>Estudiantes:</strong><br> Pedro José Romero <br> Yeison Herrera <br> Camilo Perez <br> Andres Rodriguez </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Inicializar la variable de página en el estado de sesión si no existe
if "page" not in st.session_state:
    st.session_state.page = 1

# Definir una función para cambiar de página
def next_page():
    if st.session_state.page < total_pages:
        st.session_state.page += 1

def prev_page():
    if st.session_state.page > 1:
        st.session_state.page -= 1

# Definir el número total de páginas
# Mantener el mismo número de páginas que el original
# Cambiar según el número de páginas necesarias

total_pages = 5

# Páginas en blanco
# ----------------------------------------------------------------------------------------------
if st.session_state.page == 1:
# ----------------------------------------------------------------------------------------------
    st.markdown("""
                # Global Surface Water

## Introducción
El proyecto **Global Surface Water** es una iniciativa desarrollada para monitorear y analizar los cuerpos de agua superficiales en todo el mundo utilizando datos satelitales. Esta plataforma proporciona información valiosa sobre la dinámica y la extensión de los cuerpos de agua, facilitando el estudio del cambio climático, la gestión hídrica y la conservación de ecosistemas acuáticos.
                """)
    st.image("images/GWS_intro.jpg")
    st.markdown("""
                
## Descripción del Proyecto
Lanzado por el **Centro Común de Investigación (Joint Research Centre, JRC)** de la **Comisión Europea**, el proyecto utiliza imágenes satelitales capturadas por la misión **Landsat** para mapear y analizar los cambios en los cuerpos de agua desde 1984 hasta la actualidad. Los datos procesados permiten identificar tendencias en la expansión, contracción o desaparición de lagos, ríos, humedales y embalses.

### Objetivos Principales
- Monitorear la variabilidad y el cambio en la superficie de cuerpos de agua a nivel global.
- Proporcionar datos abiertos y accesibles para la investigación y la gestión de recursos hídricos.
- Facilitar la evaluación de riesgos asociados a inundaciones y sequías.

## Herramientas y Metodología
El análisis se basa en imágenes multiespectrales proporcionadas por los satélites **Landsat 5, 7 y 8**. Utilizando algoritmos avanzados de procesamiento de imágenes y aprendizaje automático, se clasifican las áreas de agua y se calculan métricas de cambio temporal.

## Enlaces Útiles
- [Global Surface Water Explorer](https://global-surface-water.appspot.com/) - Explora los datos de cuerpos de agua en el mapa interactivo.
- [European Commission Joint Research Centre (JRC)](https://ec.europa.eu/jrc/en) - Información oficial sobre el proyecto.
- [Landsat Missions](https://landsat.gsfc.nasa.gov/) - Detalles sobre los satélites Landsat y sus capacidades.

## Aplicaciones
1. **Gestión de Recursos Hídricos:** Ayuda a los gestores a planificar el uso sostenible del agua.
2. **Estudio del Cambio Climático:** Proporciona datos históricos para analizar tendencias en la disponibilidad de agua.
3. **Conservación Ambiental:** Permite identificar humedales y cuerpos de agua críticos para la biodiversidad.

Para más información, visita el [sitio oficial](https://global-surface-water.appspot.com/).
    """)
# ----------------------------------------------------------------------------------------------
elif st.session_state.page == 2:
# ----------------------------------------------------------------------------------------------
    st.markdown("""
                # Tipos de Productos
                - **Water Occurrence:** Muestra la frecuencia con la que el agua ha estado presente en un área específica.  
                - **Occurrence Change Intensity:** Indica los aumentos o disminuciones en la ocurrencia de agua entre dos períodos.  
                - **Seasonality:** Diferencia entre cuerpos de agua permanentes y estacionales a lo largo de un año.  
                - **Recurrence:** Captura la frecuencia con la que el agua regresa año tras año.  
                - **Transitions:** Analiza los cambios entre agua permanente, estacional y tierra.  
                - **Maximum Water Extent:** Muestra la máxima extensión que el agua ha alcanzado en cada lugar durante el período observado.  
                """)
    
    product_alias = {
        "Water Occurrence": "occurrence",
        "Occurrence Change Intensity": "change",
        "Seasonality": "seasonality",
        "Recurrence": "recurrence",
        "Transitions": "transitions",
        "Maximum Water Extent": "extent"
    }

    # Mostrar el selectbox con los alias
    alias = st.selectbox(
        "Selecciona una categoría a continuación para explorar más detalles y visualizar los datos en el mapa interactivo.",
        options=list(product_alias.keys()),
        index=0
    )

    # Obtener el valor real basado en el alias seleccionado
    product = product_alias[alias]

    if product == "occurrence":
        st.markdown("""
        # Water Occurrence
        ## Propósito
        Muestra las áreas donde ocurrió agua superficial entre **1984 y 2021**, capturando tanto la **variabilidad intraanual** como la **interanual**.

        ## Descripción
        El **Water Occurrence** (SWO) se calcula sumando las **detecciones de agua (WD)** y las **observaciones válidas (VO)** mensuales:
                     """)

        st.latex(r"""
        \text{SWO} = \frac{\sum \text{WD}}{\sum \text{VO}}
        """)
        st.markdown("""
        Las áreas con agua permanente (100% de ocurrencia) se representan en azul, mientras que las áreas con agua intermitente se muestran en tonos de rosa a morado.

        ## Interpretación
        - **Azul:** Agua permanente.
        - **Rosa a morado:** Agua intermitente.
        - **Gris:** Sin datos.
        """)

    elif product == "change":
        st.markdown("""
        # Occurrence Change Intensity
        ## Propósito
        Muestra los cambios en la ocurrencia de agua superficial entre los períodos **1984-1999** y **2000-2021**.

        ## Descripción
        Calcula la diferencia de ocurrencia entre los dos períodos usando meses homólogos. Los aumentos en la ocurrencia se muestran en **verde** y las disminuciones en **rojo**.

        ## Interpretación
        - **Verde:** Aumento de agua.
        - **Rojo:** Disminución de agua.
        - **Negro:** Sin cambios significativos.
        - **Gris:** Sin datos suficientes.
        """)

    elif product == "seasonality":
        st.markdown("""
        # Seasonality
        ## Propósito
        Muestra el comportamiento **intraanual** de los cuerpos de agua durante **2021**, diferenciando entre agua **permanente** y **estacional**.

        ## Descripción
        - **Agua permanente:** Presente los 12 meses del año.
        - **Agua estacional:** Presente menos de 12 meses.

        ## Interpretación
        - **Azul oscuro:** Agua permanente.
        - **Azul claro:** Agua estacional.
        - **Gris:** Sin datos.
        """)

    elif product == "recurrence":
        st.markdown("""
        # Recurrence
        ## Propósito
        Captura la **frecuencia interanual** con la que el agua regresa de un año a otro, expresada como porcentaje.

        ## Descripción
        Calcula la proporción de años con presencia de agua respecto a los años con observaciones válidas.

        ## Interpretación
        - **Azul:** Alta recurrencia.
        - **Naranja:** Baja recurrencia.
        - **Gris:** Sin datos.
        """)

    elif product == "transitions":
        st.markdown("""
        # Transitions
        ## Propósito
        Muestra los **cambios en la estacionalidad** del agua entre el primer y el último año de observación, identificando transiciones entre agua **permanente**, **estacional** y **ausencia de agua**.

        ## Descripción
        Clasifica los cambios en 10 categorías distintas, incluyendo conversiones de tierra a agua y viceversa.

        ## Interpretación
        - **Azul:** Agua permanente.
        - **Verde:** Nueva agua permanente.
        - **Rojo:** Pérdida de agua permanente.
        - **Amarillo:** Transiciones entre agua estacional y permanente.
        - **Gris:** Sin datos.
        """)

    elif product == "extent":
        st.markdown("""
        # Maximum Water Extent
        ## Propósito
        Muestra todas las ubicaciones donde se detectó agua durante el período de **1984 a 2021**.

        ## Descripción
        Representa la **unión** de todos los demás conjuntos de datos, mostrando las áreas de máxima extensión del agua.

        ## Interpretación
        - **Azul:** Agua detectada.
        - **Blanco:** No se detectó agua.
        - **Gris:** Sin datos.
        """)

    st.divider()
#----------------------------------------------------------------------------------------------------------------------------
    legends = {
        "occurrence": {
            "Agua permanente (100%)": "#0000FF",
            "Agua intermitente (1%-99%)": "#FF0000",
            "Sin agua": "#FFFFFF",
            "Sin datos": "#CCCCCC"
        },
        "change": {
            "Aumento de agua (100%)": "#00FF00",
            "Disminucion de agua (-100%)": "#FF0000",
            "Sin cambios": "#000000",
            "Sin datos": "#CCCCCC",
            "No se puede calcular": "#888888"
        },
        "seasonality": {
            "12 meses (Agua permanente)": "#0000AA",
            "1 mes (Agua estacional)": "#99D9EA",
            "Sin agua": "#FFFFFF",
            "Sin datos": "#CCCCCC"
        },
        "recurrence": {
            "Alta recurrencia (100%)": "#99D9EA",
            "Baja recurrencia (1%)": "#FF7F27",
            "Sin agua": "#FFFFFF",
            "Sin datos": "#CCCCCC"
        },
        "transitions": {
            "Agua permanente": "#0000FF",
            "Nueva agua permanente": "#22B14C",
            "Perdida de agua permanente": "#D1102D",
            "Agua estacional": "#99D9EA",
            "Nueva agua estacional": "#B5E61D",
            "Perdida de agua estacional": "#E6A1AA",
            "Estacional a permanente": "#FF7F27",
            "Permanente a estacional": "#FFC90E",
            "Ephemeral permanente": "#7F7F7F",
            "Ephemeral estacional": "#C3C3C3",
            "Sin agua": "#FFFFFF",
            "Sin datos": "#CCCCCC"
        },
        "extent": {
            "Agua detectada": "#6666FF",
            "Sin agua": "#FFFFFF",
            "Sin datos": "#CCCCCC"
        }
    }
#----------------------------------------------------------------------------------------------------------------------------
    # Mostrar el mapa
    # Crear un mapa centrado en el río Amazonas, Colombia
    
    m = leafmap.Map(center=[9.144571, -74.634518], zoom=8)  # Coordenadas ajustadas para el río Amazonas en Colombia

    # Configuración de los mosaicos
    tile_config = {
        "url_template": "https://storage.googleapis.com/global-surface-water/tiles2021/{product}/{z}/{x}/{y}.png",
        "attr": "2016 EC JRC/Google",
        "max_zoom": 13,
        "error_tile_url": "https://storage.googleapis.com/global-surface-water/downloads_ancillary/blank.png"
    }

    # Generar la URL dinámica basada en el producto seleccionado
    tile_url = tile_config["url_template"].replace("{product}", product)

    # Agregar la capa de mosaico personalizada al mapa
    m.add_tile_layer(
        url=tile_url,
        name=product.capitalize(),
        attribution=tile_config["attr"],
        max_zoom=tile_config["max_zoom"],
        error_tile_url=tile_config["error_tile_url"]
    )

    # Agregar la leyenda al mapa
    if product in legends:
        m.add_legend(title=f"Leyenda - {alias}", legend_dict=legends[product])

    # Mostrar el mapa en la aplicación Streamlit
    m.to_streamlit()

    st.divider() 
    pdf_path = "pdfs/downloads_ancillary_DataUsersGuidev2021.pdf"  # Reemplaza con la ruta de tu archivo PDF local

    # Crear un menú desplegable para mostrar el PDF
    with st.expander("📄 Ver el Manual de Usuario del Global Surface Water"):
        pdf_viewer(pdf_path)
# ----------------------------------------------------------------------------------------------
elif st.session_state.page == 3:
# ----------------------------------------------------------------------------------------------
    st.title("Accediendo a los Datos en Google Earth Engine")
    
    st.markdown("""
    ## ¿Qué es Google Earth Engine?
    **Google Earth Engine (GEE)** es una plataforma en la nube diseñada para el análisis de grandes volúmenes de datos geoespaciales. Ofrece acceso a imágenes satelitales y conjuntos de datos globales, permitiendo la realización de análisis espaciales avanzados.

    ## Accediendo a los Datos de Global Surface Water
    Los datos de **Global Surface Water** se pueden acceder directamente desde el catálogo de GEE utilizando scripts en **JavaScript o Python**.

    ### 1. Crear una cuenta en Google Earth Engine
    - Ve a [Google Earth Engine](https://earthengine.google.com/).
    - Regístrate con tu cuenta de Google y solicita acceso a la plataforma.

    ### 2. Importar el conjunto de datos
    Usa el siguiente código en el **Editor de JavaScript** de GEE:
    ```js
    var dataset = ee.Image('JRC/GSW1_3/GlobalSurfaceWater');
    var occurrence = dataset.select('occurrence');
    Map.addLayer(occurrence, {}, 'Water Occurrence');
    ```
    Esto carga la capa de **Water Occurrence**. Puedes cambiar `'occurrence'` por otros productos como:
    - `'change'` para Occurrence Change Intensity.
    - `'seasonality'` para Seasonality.
    - `'extent'` para Maximum Water Extent.

    ### 3. Exportar datos
    Utiliza la función `Export.image.toDrive()` para descargar los datos procesados:
    ```js
    Export.image.toDrive({
        image: occurrence,
        description: 'WaterOccurrence',
        scale: 30,
        region: geometry
    });
    ```

    ### 4. Acceso mediante Python (API)
    Si prefieres Python, instala la API:
    ```
    pip install earthengine-api
    ```
    Luego autentica y usa:
    ```python
    import ee
    ee.Initialize()
    dataset = ee.Image('JRC/GSW1_3/GlobalSurfaceWater')
    occurrence = dataset.select('occurrence')
    ```

    ### Recursos útiles
    - [Documentación de GEE](https://developers.google.com/earth-engine/guides)
    - [Catálogo de datos](https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_3_GlobalSurfaceWater)

    ¡Explora los datos y realiza análisis avanzados con GEE! 🌍
    """)

    st.divider()
# ----------------------------------------------------------------------------------------------
    st.title("Usando Google Earth Engine en Python")

    st.markdown("""
    ## ¿Qué es Google Earth Engine API en Python?
    La **API de Google Earth Engine (GEE)** para Python permite acceder y procesar grandes volúmenes de datos geoespaciales mediante scripts en Python. Con esta API, puedes trabajar con imágenes satelitales, analizar cambios en el uso del suelo y descargar resultados directamente.

    ## 1. Configurar la API de Google Earth Engine
    Para utilizar la API de GEE en Python, sigue estos pasos:
    1. Crea una cuenta en [Google Earth Engine](https://earthengine.google.com/).
    2. Activa la API y autentica tu cuenta.

    Instala la API ejecutando:
    ```
    pip install earthengine-api
    ```
    """)

    st.divider()
    st.title("Descarga del Notebook - Google Earth Engine y Maximum Water Extent")

    st.markdown("""
        ## 📄 Descripción del Archivo
        Este notebook contiene:
        1. **Autenticación en Google Earth Engine (GEE):** Cómo conectarse usando tus credenciales.
        2. **Carga y visualización de datos:** Muestra cómo cargar y visualizar el dataset **Maximum Water Extent**.
        3. **Recorte y descarga de datos:** Instrucciones para recortar áreas específicas y descargar los datos en formato **GeoTIFF**.

        ---

        ## 🚀 Cómo usar el archivo
        ### 1. Ejecutar en Binder
        - **Haz clic en el enlace:** [Ejecutar en Binder](https://mybinder.org/v2/gh/Peter24K2G/DPPFFBB_APP/blob/main/GEE.ipynb/HEAD)
        - Espera a que se cargue el entorno (puede tomar unos minutos).
        - Ejecuta cada celda siguiendo las instrucciones.

        ### 2. Ejecutar en Google Colab
        - **Sube el archivo a Google Drive.**
        - Abre [Google Colab](https://colab.research.google.com/).
        - Ve a **Archivo > Subir cuaderno** y selecciona el archivo `.ipynb`.
        - Instala las bibliotecas necesarias ejecutando las primeras celdas.

        ---
        """)
    
    # Ruta al archivo local .ipynb
    file_path = "GEE.ipynb"

    # Leer el archivo en modo binario
    with open(file_path, "rb") as file:
        file_data = file.read()

    # Crear botón de descarga
    st.download_button(
        label="📥 Descargar el archivo .ipynb",
        data=file_data,
        file_name="GEE.ipynb",
        mime="application/octet-stream"
    )
# ----------------------------------------------------------------------------------------------
elif st.session_state.page == 4:
# ----------------------------------------------------------------------------------------------
    st.title("Descarga de Históricos Mensuales - Global Surface Water")

    st.markdown("""
    ## 🌍 Descarga de Datos Históricos Mensuales
    **Global Surface Water** ofrece la posibilidad de descargar los históricos mensuales de los mapas de agua superficial. Esto permite analizar los **cambios en periodos específicos** de interés desde **1984** hasta la fecha más reciente.

    Los datos están disponibles en formato **GeoTIFF** y se pueden descargar por medio de enlaces directos.

    **Ejemplo de enlace a un archivo específico:**
    ```
    https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GSWE/MonthlyHistory/LATEST/tiles/1984/1984_04/tile_especifico.tiff
    ```

    En este ejemplo:
    - **1984:** Indica el año.
    - **1984_04:** Indica el mes de abril de ese año.
    - **tile_especifico.tiff:** Es el archivo GeoTIFF del tile específico.

    ---

    ## 📁 Exploración manual de los datos
    Puedes explorar los datos manualmente a través de la navegación por carpetas:
    1. Abre el siguiente enlace en tu navegador:  
       [Carpeta de Open Data](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GSWE/MonthlyHistory/LATEST/)
    2. Navega por las carpetas según el **año** y el **mes** de interés.
    3. Descarga los archivos **GeoTIFF** directamente.

    ---

    ## 🛠️ Descarga automatizada con `wget`
    Si prefieres descargar los datos de forma más eficiente, puedes usar el comando **`wget`** en la terminal:

    ```bash
    wget https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GSWE/MonthlyHistory/LATEST/tiles/1984/1984_04/tile_especifico.tiff
    ```

    **Ejemplo: Descargar múltiples archivos de un mismo mes:**
    ```bash
    wget -r -np -nH --cut-dirs=4 -A "*.tiff" https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GSWE/MonthlyHistory/LATEST/tiles/1984/1984_04/
    ```

    **Explicación del comando:**
    - `-r`: Descarga recursiva.  
    - `-np`: Evita subir a directorios padres.  
    - `-nH`: Evita crear carpetas adicionales.  
    - `--cut-dirs=4`: Elimina los primeros 4 niveles de carpetas para mantener una estructura más limpia.  
    - `-A "*.tiff"`: Descarga solo archivos **GeoTIFF**.

    ---

    ## 📦 Ejemplo práctico
    Imagina que quieres descargar todos los tiles de **abril de 1984**:
    ```bash
    wget -r -np -nH --cut-dirs=4 -A "*.tiff" https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GSWE/MonthlyHistory/LATEST/tiles/1984/1984_04/
    ```

    Esto generará una carpeta con todos los archivos **GeoTIFF** de ese mes, listos para ser analizados.

    ---
    
    ## 📌 Resumen
    - Explora manualmente los datos usando la [carpeta de Open Data](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GSWE/MonthlyHistory/LATEST/).
    - Usa `wget` para descargar los datos de forma automatizada.
    - Utiliza los datos históricos para analizar la evolución de los cuerpos de agua en periodos específicos.

    ¡Explora los históricos y descubre cómo ha cambiado el agua superficial a lo largo de los años! 🌊
    """)
# ----------------------------------------------------------------------------------------------                                                        
elif st.session_state.page == 5:
    tiffs_norte = [
        os.path.join("Tiffs/TiffsNorte", f) for f in os.listdir("Tiffs/TiffsNorte") if f.endswith(".tif")
    ]
    tiffs_sur = [
        os.path.join("Tiffs/TiffsSur", f) for f in os.listdir("Tiffs/TiffsSur") if f.endswith(".tif")
    ]

    # Ordenar los archivos para que se muestren cronológicamente
    tiffs_norte.sort()
    tiffs_sur.sort()

    # Selección de archivos para Zona Norte
    st.subheader("📍 Zona Norte - Ciénaga La Musandra")
    seleccion_norte = st.multiselect(
        "Selecciona los meses a visualizar:",
        format_func=lambda x: x[17:24],  # Mostrar solo los caracteres [15:22] (YYYY-MM)
        options=tiffs_norte,
        default=tiffs_norte[0] if tiffs_norte else []
    )

    # Mapa para la Zona Norte
    if seleccion_norte:
        m_norte = folium.Map(location=[8.018812, -73.722507], zoom_start=14)
        for tiff in seleccion_norte:
            # Cargar el archivo GeoTIFF
            raster = rioxarray.open_rasterio(tiff)

            # Convertir a 8-bit (0-255) para PNG
            data = raster[0].values  # Asumiendo una sola banda

            # Manejo de NaN: Reemplazar NaN por 0 para procesamiento pero guardar una máscara
            nan_mask = np.isnan(data)
            data = np.nan_to_num(data, nan=0)  # Reemplazar NaN por 0 temporalmente

            # Crear una máscara de transparencia
            alpha = np.where((data == 0) | (nan_mask), 0, 255).astype(np.uint8)

            # Crear una capa azul para los valores 1
            blue_layer = np.zeros_like(data, dtype=np.uint8)
            blue_layer[data == 1] = 255  # Azul para el valor 1

            # Crear imagen RGBA
            rgba = np.dstack((np.zeros_like(data, dtype=np.uint8),  # R = 0
                            np.zeros_like(data, dtype=np.uint8),  # G = 0
                            blue_layer,  # B = Azul para 1
                            alpha))  # A = Transparencia

            # Guardar como PNG con transparencia
            temp_png = tiff.replace(".tif", ".png")
            Image.fromarray(rgba).save(temp_png)

            # Agregar al mapa con colormap personalizado
            folium.raster_layers.ImageOverlay(
                image=temp_png,
                bounds=[[raster.rio.bounds()[1], raster.rio.bounds()[0]],
                        [raster.rio.bounds()[3], raster.rio.bounds()[2]]],
                opacity=1,  # Controlar la transparencia general
                name=tiff.split("/")[-1]
            ).add_to(m_norte)

        folium.LayerControl().add_to(m_norte)
        st_folium(m_norte, width=700, height=500)

        # Crear un slider para seleccionar el archivo TIFF por mes
        # Selección de archivos para Zona Sur
        st.subheader("📍 Zona Sur - Ciénaga Yarirí")
        seleccion_sur = st.multiselect(
            "Selecciona los meses a visualizar:",
            format_func=lambda x: x[15:22],  # Mostrar solo los caracteres [15:22] (YYYY-MM)
            options=tiffs_sur,
            default=tiffs_sur[0] if tiffs_sur else []
        )

    # Mapa para la Zona Sur
    if seleccion_sur:
        m_sur = folium.Map(location=[7.353615, -73.885680], zoom_start=14)
        for tiff in seleccion_sur:
            # Cargar el archivo GeoTIFF
            raster = rioxarray.open_rasterio(tiff)

            # Reproyectar a EPSG:4326 (lat/lon) si no está en ese sistema
            if raster.rio.crs != 'EPSG:4326':
                raster = raster.rio.reproject("EPSG:4326")

            # Convertir a 8-bit (0-255) para PNG
            data = raster[0].values  # Asumiendo una sola banda

            # Manejo de NaN: Reemplazar NaN por 0 para procesamiento pero guardar una máscara
            nan_mask = np.isnan(data)
            data = np.nan_to_num(data, nan=0)  # Reemplazar NaN por 0 temporalmente

            # Crear una máscara de transparencia
            alpha = np.where((data == 0) | (nan_mask), 0, 255).astype(np.uint8)

            # Crear una capa azul para los valores 1
            blue_layer = np.zeros_like(data, dtype=np.uint8)
            blue_layer[data == 1] = 255  # Azul para el valor 1

            # Crear imagen RGBA
            rgba = np.dstack((np.zeros_like(data, dtype=np.uint8),  # R = 0
                            np.zeros_like(data, dtype=np.uint8),  # G = 0
                            blue_layer,  # B = Azul para 1
                            alpha))  # A = Transparencia

            # Guardar como PNG con transparencia
            temp_png = tiff.replace(".tif", ".png")
            Image.fromarray(rgba).save(temp_png)

            # Obtener los límites corregidos (reproyectados)
            bounds = raster.rio.bounds()

            # Agregar al mapa con colormap personalizado
            folium.raster_layers.ImageOverlay(
                image=temp_png,
                bounds=[[bounds[1], bounds[0]],
                        [bounds[3], bounds[2]]],
                opacity=1,  # Controlar la transparencia general
                name=tiff.split("/")[-1]
            ).add_to(m_sur)

        folium.LayerControl().add_to(m_sur)
        st_folium(m_sur, width=700, height=500)

# ----------------------------------------------------------------------------------------------
# elif st.session_state.page == 6:
#     st.title("Página 6")
#     st.write("Contenido en blanco para la Página 6")
# elif st.session_state.page == 7:
#     st.title("Página 7")
#     st.write("Contenido en blanco para la Página 7")

# Crear botones de navegación
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.button("Anterior", on_click=prev_page)
with col3:
    st.button("Siguiente️", on_click=next_page)
