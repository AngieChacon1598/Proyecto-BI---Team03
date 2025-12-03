# pandas: se utiliza para la manipulación y análisis de datos estructurados, como hojas de Excel o archivos CSV
# numpy: se emplea para realizar cálculos numéricos eficientes, como contar valores únicos y calcular porcentajes
# matplotlib.pyplot: se usa para crear gráficos y visualizaciones, como gráficos de pastel, barras, líneas, etc.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargamos el archivo Excel en un DataFrame de pandas
df = pd.read_excel("RecopilacionDeDatos.xlsx")

# Definimos el nombre exacto de la columna que queremos analizar
col = '¿Con cuántas personas vive actualmente en tu hogar?'

# Verificamos si la columna existe en el DataFrame
if col in df.columns:
    # Eliminamos valores nulos y extraemos los datos como un array de NumPy
    data = df[col].dropna().values

    # Obtenemos los valores únicos y la cantidad de veces que aparecen
    unique, counts = np.unique(data, return_counts=True)

    # Calculamos el total de respuestas válidas
    total = np.sum(counts)

    # Calculamos el porcentaje que representa cada respuesta
    percentages = np.round((counts / total) * 100, 2)

    # Mostramos los resultados en consola con formato amigable
    print("Personas en el hogar:")
    for val, c, pct in zip(unique, counts, percentages):
        print(f"{val}: {c} ({pct}%)")

    # Creamos un gráfico de pastel para visualizar la distribución de respuestas
    plt.figure(figsize=(7,7))  # Tamaño del gráfico
    plt.pie(counts, labels=unique, autopct='%1.1f%%', startangle=140)  # Gráfico circular con porcentajes
    plt.title('Personas con las que vive actualmente', fontsize=14, fontweight='bold')  # Título del gráfico
    plt.tight_layout()  # Ajuste automático del layout
    plt.show()  # Mostramos el gráfico
else:
    # Si la columna no existe, mostramos un mensaje de error
    print("No se encontró la columna:", col)
