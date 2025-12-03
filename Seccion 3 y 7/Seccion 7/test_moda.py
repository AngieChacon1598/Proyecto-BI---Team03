# pandas: se utiliza para la manipulación y análisis de datos estructurados, como hojas de Excel o archivos CSV
# matplotlib.pyplot: se usa para crear gráficos y visualizaciones, como gráficos de pastel, barras, líneas, etc.
# os: se utiliza para interactuar con el sistema operativo, como crear carpetas o manejar rutas de archivos
import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargamos el archivo Excel en un DataFrame de pandas
df = pd.read_excel("RecopilacionDeDatos.xlsx")

# Definimos el nombre exacto de la columna que identifica el distrito
col_distrito = "  ¿En qué distrito vives?  "

# Verificamos que la columna del distrito exista en el DataFrame
if col_distrito not in df.columns:
    print(f"No se encontró la columna '{col_distrito}'")
    exit()

# Definimos las áreas vocacionales y las preguntas asociadas a cada una
areas = {
    "Ciencias de la Salud": [
        "¿Te interesa aprender cómo funciona el cuerpo humano?",
        "¿Te motiva la idea de ayudar a otras personas a mejorar su bienestar?",
        "¿Te gustaría trabajar en hospitales, clínicas o centros de investigación médica?"
    ],
    "Ciencias Sociales y Humanidades": [
        "¿Disfrutas conversar y escuchar los problemas de los demás para orientarlos?",
        "¿Te interesa la historia, la filosofía o comprender cómo piensan las personas?",
        "¿Te gusta participar en proyectos sociales, comunitarios o de voluntariado?"
    ],
    "Ingeniería, Tecnología y Matemáticas": [
        "¿Te gustan las matemáticas y resolver problemas lógicos?",
        "¿Te interesa entender cómo funcionan las máquinas, aparatos o sistemas digitales?",
        "¿Te entusiasma diseñar programas, aplicaciones o inventos?"
    ],
    "Arte, Comunicación y Diseño": [
        "¿Te gusta expresarte a través de la música, la pintura, el teatro o la escritura?",
        "¿Disfrutas crear contenidos (videos, redes sociales, diseño gráfico, etc.)?",
        "¿Te interesa trabajar en medios de comunicación o en proyectos artísticos?"
    ],
    "Negocios, Economía y Emprendimiento": [
        "¿Te interesa organizar proyectos, liderar equipos o emprender negocios?",
        "¿Te gustan los números aplicados a la economía y las finanzas?",
        "¿Te motiva la idea de tener tu propio negocio en el futuro?"
    ],
    "Ciencias Naturales y Medio Ambiente": [
        "¿Te interesa la naturaleza y cuidar el medio ambiente?",
        "¿Te gusta trabajar al aire libre, en campos, laboratorios o áreas ecológicas?",
        "¿Te motiva la idea de aportar a la sostenibilidad y seguridad alimentaria?"
    ]
}

# Creamos una carpeta para guardar los gráficos generados por distrito
output_folder = "graficos_por_distrito"
os.makedirs(output_folder, exist_ok=True)

# Obtenemos la lista de distritos únicos presentes en el archivo
distritos = df[col_distrito].dropna().unique()

# Iteramos por cada distrito para generar un gráfico de preferencias vocacionales
for distrito in distritos:
    # Filtramos el DataFrame para el distrito actual
    df_distrito = df[df[col_distrito] == distrito]
    conteo_areas = {}

    # Contamos cuántas respuestas tipo "A" hay por área vocacional
    for area, preguntas in areas.items():
        total_A = 0
        for pregunta in preguntas:
            if pregunta in df_distrito.columns:
                respuestas = df_distrito[pregunta].dropna()
                total_A += respuestas[respuestas.str.startswith("A")].count()
        conteo_areas[area] = total_A

    # Creamos un gráfico de barras para visualizar las preferencias por área
    plt.figure(figsize=(10,6))  # Tamaño del gráfico
    plt.bar(conteo_areas.keys(), conteo_areas.values(), color='darkorange')  # Barras con color definido
    plt.title(f"Moda Vocacional - Distrito: {distrito}", fontsize=14, fontweight='bold')  # Título del gráfico
    plt.xlabel("Áreas Vocacionales")  # Etiqueta del eje X
    plt.ylabel("Cantidad de respuestas A")  # Etiqueta del eje Y
    plt.xticks(rotation=30, ha='right')  # Rotación de etiquetas para mejor lectura
    plt.tight_layout()  # Ajuste automático del layout

    # Guardamos el gráfico como imagen PNG en la carpeta correspondiente
    safe_name = distrito.replace(" ", "_").replace("/", "_")
    plt.savefig(f"{output_folder}/{safe_name}.png")
    plt.close()  # Cerramos el gráfico para liberar memoria

# Mensaje final de confirmación
print("Todos los gráficos fueron generados y guardados en la carpeta 'graficos_por_distrito'.")
