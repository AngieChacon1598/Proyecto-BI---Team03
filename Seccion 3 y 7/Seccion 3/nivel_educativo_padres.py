# pandas: se utiliza para la manipulación y análisis de datos estructurados, como hojas de Excel o archivos CSV
# numpy: se emplea para realizar cálculos numéricos eficientes, como contar valores únicos y calcular porcentajes
# matplotlib.pyplot: se usa para crear gráficos y visualizaciones, como gráficos de pastel, barras, líneas, etc.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargamos el archivo Excel en un DataFrame de pandas
df = pd.read_excel("RecopilacionDeDatos.xlsx")

# Definimos el nombre exacto de la columna que queremos analizar
col_nivel_educativo = '¿Qué nivel educativo alcanzaron sus padres o tutores?'

# Verificamos si la columna existe en el DataFrame
if col_nivel_educativo in df.columns:
    # Contamos la cantidad de respuestas por cada nivel educativo
    edu_counts = df[col_nivel_educativo].value_counts()

    # Mostramos los resultados en consola
    print("Cantidad por nivel educativo de padres o tutores:\n", edu_counts, "\n")

    # Creamos un gráfico de barras para visualizar la distribución de niveles educativos
    plt.figure(figsize=(8, 5))  # Tamaño del gráfico
    edu_counts.plot(kind='bar', color='green')  # Tipo de gráfico y color
    plt.title('Nivel Educativo de Padres o Tutores', fontsize=14, fontweight='bold')  # Título del gráfico
    plt.xlabel('Nivel Educativo')  # Etiqueta del eje X
    plt.ylabel('Cantidad de Personas')  # Etiqueta del eje Y
    plt.xticks(rotation=30, ha='right')  # Rotación de etiquetas para mejor lectura
    plt.tight_layout()  # Ajuste automático del layout
    plt.show()  # Mostramos el gráfico
else:
    # Si la columna no existe, mostramos un mensaje de error
    print("No se encontró la columna del nivel educativo de padres o tutores.")
