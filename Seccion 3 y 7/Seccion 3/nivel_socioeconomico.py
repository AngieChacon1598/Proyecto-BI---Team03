# pandas: se utiliza para la manipulación y análisis de datos estructurados, como hojas de Excel o archivos CSV
# matplotlib.pyplot: se usa para crear gráficos y visualizaciones, como gráficos de pastel, barras, líneas, etc.
import pandas as pd
import matplotlib.pyplot as plt

# Cargamos el archivo Excel en un DataFrame de pandas
df = pd.read_excel("RecopilacionDeDatos.xlsx")

# Definimos el nombre exacto de la columna que contiene la pregunta
col_nivel = "¿A qué nivel socioeconómico considera que pertenece su familia?"

# Verificamos que la columna exista en el DataFrame
if col_nivel not in df.columns:
    print(f"No se encontró la columna '{col_nivel}'")
    exit()

# Eliminamos valores nulos y contamos la frecuencia de cada respuesta
respuestas = df[col_nivel].dropna()
conteo = respuestas.value_counts()

# Calculamos el porcentaje que representa cada respuesta
porcentajes = round((conteo / conteo.sum()) * 100, 2)

# Mostramos los resultados en consola
print("Distribución de nivel socioeconómico:")
for nivel, cantidad in conteo.items():
    print(f"- {nivel}: {cantidad} respuestas ({porcentajes[nivel]}%)")

# Creamos un gráfico de pastel para visualizar la distribución de respuestas
plt.figure(figsize=(8,8))  # Tamaño del gráfico
plt.pie(conteo, labels=conteo.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)  # Gráfico circular con colores predefinidos
plt.title("Nivel Socioeconómico Familiar", fontsize=14, fontweight='bold')  # Título del gráfico
plt.tight_layout()  # Ajuste automático del layout
plt.show()  # Mostramos el gráfico
