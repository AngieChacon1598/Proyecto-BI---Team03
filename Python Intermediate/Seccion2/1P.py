import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import menu_filtro_grado

# ==================== PREGUNTA 1 — ¿Cómo prefieres aprender cosas nuevas? ====================
# Conceptos aplicados: value_counts(), filtrado, diccionarios, gráficos

# Cargar datos del archivo correcto
archivo = '../../data/RecopilaciónDeDatos-BI(respuestas).xlsx'
df = pd.read_excel(archivo)

# Menú interactivo para filtrar por grado
df = menu_filtro_grado(df)

# Conteo de respuestas
col_aprendizaje = "¿Cómo prefieres aprender cosas nuevas?"
res_p1 = df[col_aprendizaje].value_counts()

print("=" * 80)
print("PREGUNTA 1 — ¿Cómo prefieres aprender cosas nuevas?")
print("=" * 80)
print("\nResultados:")
print(res_p1)
print(f"\nTotal de respuestas: {len(df)}")

# Crear gráfico de barras
plt.figure(figsize=(10, 6))
res_p1.plot(kind='bar', color='steelblue', edgecolor='black', alpha=0.7)
plt.title('Preferencias de Aprendizaje de los Estudiantes', fontsize=14, fontweight='bold')
plt.xlabel('Método de Aprendizaje', fontsize=12)
plt.ylabel('Cantidad de Estudiantes', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()

# Crear gráfico de pastel
plt.figure(figsize=(8, 8))
res_p1.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
plt.title('Distribución de Preferencias de Aprendizaje', fontsize=14, fontweight='bold')
plt.ylabel('')
plt.tight_layout()
plt.show()
