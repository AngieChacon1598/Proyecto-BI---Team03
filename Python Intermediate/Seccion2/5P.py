import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import menu_filtro_grado

# ==================== PREGUNTA 5 — Tipo de estudios preferidos después del colegio ====================
# Conceptos aplicados: NumPy + boolean indexing + value_counts + gráficos

# Cargar datos del archivo correcto
archivo = '../../data/RecopilaciónDeDatos-BI(respuestas).xlsx'
df = pd.read_excel(archivo)

# Menú interactivo para filtrar por grado
df = menu_filtro_grado(df)

# Convertir a array de NumPy
col_tipo_estudios = "¿Qué tipo de estudios prefieres seguir después del colegio?"
tipo_estudios = np.array(df[col_tipo_estudios])

# Filtrar quienes prefieren "carrera corta" (verificar el valor exacto primero)
print("=" * 80)
print("PREGUNTA 4 — Tipo de estudios preferidos después del colegio")
print("=" * 80)

# Ver valores únicos para encontrar el correcto
valores_unicos = np.unique(tipo_estudios)
print("\nValores únicos encontrados:")
for val in valores_unicos:
    print(f"  - {repr(val)}")

# Buscar variaciones de "carrera corta"
for val in valores_unicos:
    if 'corta' in str(val).lower() or 'técnico' in str(val).lower() or 'técnica' in str(val).lower():
        pref_corta = tipo_estudios[tipo_estudios == val]
        print(f"\nEstudiantes que prefieren '{val}': {len(pref_corta)}")
        break

# Mostrar todos los conteos
conteos = df[col_tipo_estudios].value_counts()
print("\nDistribución completa:")
print(conteos)

# Crear gráfico de barras
plt.figure(figsize=(10, 6))
conteos.plot(kind='bar', color='mediumpurple', edgecolor='black', alpha=0.7)
plt.title('Tipo de Estudios Preferidos Después del Colegio', fontsize=14, fontweight='bold')
plt.xlabel('Tipo de Estudios', fontsize=12)
plt.ylabel('Cantidad de Estudiantes', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()

# Crear gráfico de pastel
plt.figure(figsize=(8, 8))
conteos.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Set2.colors)
plt.title('Distribución de Preferencias de Estudios', fontsize=14, fontweight='bold')
plt.ylabel('')
plt.tight_layout()
plt.show()

