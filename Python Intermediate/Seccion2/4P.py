import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import menu_filtro_grado

# ==================== PREGUNTA 4 — Factor que influye más en la elección de carrera ====================
# Conceptos aplicados: funciones + diccionarios + pandas + gráficos

# Cargar datos del archivo correcto
archivo = '../../data/RecopilaciónDeDatos-BI(respuestas).xlsx'
df = pd.read_excel(archivo)

# Menú interactivo para filtrar por grado
df = menu_filtro_grado(df)

# Función para contar frecuencias
def contar_frecuencias(serie):
    return dict(serie.value_counts())

# Aplicar función
col_eleccion = "¿Qué factor influye más en tu elección de carrera?"
resultado_p3 = contar_frecuencias(df[col_eleccion])

print("=" * 80)
print("PREGUNTA 3 — Factor que influye más en la elección de carrera")
print("=" * 80)
print("\nFactores que influyen en la elección de carrera:")
for factor, cantidad in resultado_p3.items():
    print(f"  - {factor}: {cantidad}")

# Crear gráfico de barras horizontal
serie_p3 = df[col_eleccion].value_counts()
plt.figure(figsize=(10, 6))
serie_p3.plot(kind='barh', color='coral', edgecolor='black', alpha=0.7)
plt.title('Factores que Influyen en la Elección de Carrera', fontsize=14, fontweight='bold')
plt.xlabel('Cantidad de Estudiantes', fontsize=12)
plt.ylabel('Factor', fontsize=12)
plt.grid(axis='x', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()

# Crear gráfico de pastel
plt.figure(figsize=(8, 8))
serie_p3.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
plt.title('Distribución de Factores de Influencia', fontsize=14, fontweight='bold')
plt.ylabel('')
plt.tight_layout()
plt.show()
