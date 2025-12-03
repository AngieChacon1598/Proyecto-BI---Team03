import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import menu_filtro_grado

# ==================== PREGUNTA 3 — ¿Te entusiasma diseñar programas, aplicaciones o inventos? ====================
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
col_pregunta = "¿Te entusiasma diseñar programas, aplicaciones o inventos?"
resultado_p3 = contar_frecuencias(df[col_pregunta])

print("=" * 80)
print("PREGUNTA 3 — ¿Te entusiasma diseñar programas, aplicaciones o inventos?")
print("=" * 80)
print("\nDistribución de respuestas:")
for respuesta, cantidad in resultado_p3.items():
    print(f"  - {respuesta}: {cantidad}")

# Crear gráfico de barras horizontal
serie_p3 = df[col_pregunta].value_counts()
plt.figure(figsize=(10, 6))
serie_p3.plot(kind='barh', color='coral', edgecolor='black', alpha=0.7)
plt.title('¿Te entusiasma diseñar programas, aplicaciones o inventos?', fontsize=14, fontweight='bold')
plt.xlabel('Cantidad de Estudiantes', fontsize=12)
plt.ylabel('Respuesta', fontsize=12)
plt.grid(axis='x', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()

# Crear gráfico de pastel
plt.figure(figsize=(8, 8))
serie_p3.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
plt.title('Distribución de Respuestas sobre Diseño de Programas', fontsize=14, fontweight='bold')
plt.ylabel('')
plt.tight_layout()
plt.show()

