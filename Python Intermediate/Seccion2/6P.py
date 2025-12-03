import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import menu_filtro_grado

# ==================== PREGUNTA 6 — ¿Dónde se imaginan trabajando? ====================
# Conceptos aplicados: groupby, comprensión de listas, gráficos

# Cargar datos del archivo correcto
archivo = '../../data/RecopilaciónDeDatos-BI(respuestas).xlsx'
df = pd.read_excel(archivo)

# Menú interactivo para filtrar por grado
df = menu_filtro_grado(df)

col_lugar = "¿Dónde te imaginas trabajando en el futuro?"
lugares = df[col_lugar]

print("=" * 80)
print("PREGUNTA 5 — ¿Dónde te imaginas trabajando en el futuro?")
print("=" * 80)
print("\nDistribución de respuestas:")

# Usando comprensión de listas y unique()
for val in lugares.unique():
    cantidad = len(lugares[lugares == val])
    print(f"  - {val}: {cantidad} respuestas")

# Usando value_counts para mejor visualización
conteos_lugares = lugares.value_counts()
print("\nResumen ordenado:")
print(conteos_lugares)

# Crear gráfico de barras
plt.figure(figsize=(12, 6))
conteos_lugares.plot(kind='bar', color='teal', edgecolor='black', alpha=0.7)
plt.title('Lugares Donde los Estudiantes se Imaginan Trabajando', fontsize=14, fontweight='bold')
plt.xlabel('Lugar de Trabajo', fontsize=12)
plt.ylabel('Cantidad de Estudiantes', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()

# Crear gráfico de pastel
plt.figure(figsize=(10, 10))
conteos_lugares.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.tab20.colors)
plt.title('Distribución de Lugares de Trabajo Preferidos', fontsize=14, fontweight='bold')
plt.ylabel('')
plt.tight_layout()
plt.show()

