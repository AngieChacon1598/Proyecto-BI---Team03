import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import menu_filtro_grado

# ==================== PREGUNTA 2 — Importancia de la tecnología ====================
# Conceptos aplicados: filtrado booleano + NumPy + conteo + gráficos

# Cargar datos del archivo correcto
archivo = '../../data/RecopilaciónDeDatos-BI(respuestas).xlsx'
df = pd.read_excel(archivo)

# Menú interactivo para filtrar por grado
df = menu_filtro_grado(df)

# Convertir columna a array de NumPy
col_tech = "¿Qué tan importante consideras la tecnología (computadoras, internet, apps) para tu educación futura?"
col_grado = "  ¿En qué grado estás actualmente?   "

tech_array = np.array(df[col_tech])

# Filtrar quienes dijeron "Muy importante."
muy_importante = tech_array[tech_array == "Muy importante."]

print("=" * 80)
print("PREGUNTA 2 — Importancia de la tecnología")
print("=" * 80)
print(f"\nTotal de estudiantes analizados: {len(df)}")

# Filtrar quienes dijeron "Muy importante."
muy_importante = tech_array[tech_array == "Muy importante."]
print(f"\nTotal que consideran MUY importante la tecnología: {len(muy_importante)}")

# Conteo completo de todas las respuestas
tech_counts = df[col_tech].value_counts()
print("\nDistribución completa:")
print(tech_counts)

# Crear gráfico de barras
plt.figure(figsize=(10, 6))
tech_counts.plot(kind='bar', color=['#2ecc71', '#3498db', '#e74c3c', '#f39c12'], edgecolor='black', alpha=0.7)
plt.title('Importancia de la Tecnología para la Educación Futura', fontsize=14, fontweight='bold')
plt.xlabel('Nivel de Importancia', fontsize=12)
plt.ylabel('Cantidad de Estudiantes', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()
