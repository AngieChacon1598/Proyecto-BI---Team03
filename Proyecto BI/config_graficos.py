"""
Configuración de estilos y parámetros visuales para los gráficos
Este módulo centraliza todas las configuraciones de matplotlib
"""

import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================================
# CONFIGURACIÓN GLOBAL DE MATPLOTLIB
# ============================================================================

def configurar_estilo_global():
    """Configura el estilo global de matplotlib con tema oscuro"""
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette("viridis")
    
    plt.rcParams.update({
        'figure.facecolor': 'black',
        'axes.facecolor': 'black',
        'axes.edgecolor': '#BDC3C7',
        'axes.linewidth': 1.2,
        'grid.color': '#555555',
        'grid.alpha': 0.3,
        'text.color': 'white',
        'xtick.color': 'white',
        'ytick.color': 'white',
        'font.size': 10,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16
    })


# ============================================================================
# PALETAS DE COLORES
# ============================================================================

# Paleta de colores profesional para gráficos generales
COLORES_PROFESIONALES = ['#3498DB', '#E74C3C', '#2ECC71', '#F39C12', '#9B59B6', '#1ABC9C']

# Colores para gráficos comparativos
COLORES_COMPARATIVO = ['#3498DB', '#E74C3C', '#2ECC71', '#F39C12']

# Colores para gráficos por grado
COLORES_GRADOS = ['#3498DB', '#E74C3C', '#2ECC71', '#F39C12']


# ============================================================================
# TAMAÑOS DE FIGURAS
# ============================================================================

TAMANO_BARRAS = (10, 6)
TAMANO_PASTEL = (8, 8)
TAMANO_BARRAS_HORIZONTALES = (12, 8)
TAMANO_COMPARATIVO = (16, 8)
TAMANO_DASHBOARD = (20, 12)


# ============================================================================
# PARÁMETROS DE ESTILO
# ============================================================================

# Colores de texto y bordes
COLOR_TEXTO = 'white'
COLOR_BORDE = '#BDC3C7'
COLOR_GRID = '#555555'

# Configuración de barras
GROSOR_BORDE_BARRAS = 1.5
ALPHA_BARRAS = 0.8

# Configuración de spines (ejes)
GROSOR_SPINE = 1.2

# Configuración de grid
ALPHA_GRID = 0.3
ESTILO_GRID = '--'

# Configuración de títulos
TAMANO_TITULO_PRINCIPAL = 16
TAMANO_TITULO_SECUNDARIO = 14
TAMANO_TITULO_DASHBOARD = 18
PADDING_TITULO = 20

# Configuración de etiquetas
TAMANO_ETIQUETA = 12
TAMANO_TICK = 10
TAMANO_LEYENDA = 11

# Configuración de texto en gráficos
TAMANO_TEXTO_BARRAS = 12
TAMANO_TEXTO_PASTEL = 11
TAMANO_TEXTO_PORCENTAJES = 10


# ============================================================================
# FUNCIONES HELPER PARA APLICAR ESTILOS
# ============================================================================

def aplicar_estilo_ejes(ax):
    """Aplica el estilo estándar a los ejes de un gráfico"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLOR_BORDE)
    ax.spines['bottom'].set_color(COLOR_BORDE)


def aplicar_grid(ax, eje='y'):
    """Aplica grid a un eje específico"""
    ax.grid(axis=eje, alpha=ALPHA_GRID, linestyle=ESTILO_GRID, color=COLOR_GRID)


def aplicar_titulo(ax, titulo, tamano=TAMANO_TITULO_PRINCIPAL, color=COLOR_TEXTO):
    """Aplica un título con el estilo estándar"""
    ax.set_title(titulo, fontsize=tamano, fontweight='bold', color=color, pad=PADDING_TITULO)


def aplicar_etiquetas(ax, xlabel=None, ylabel=None, color=COLOR_TEXTO):
    """Aplica etiquetas a los ejes con el estilo estándar"""
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=TAMANO_ETIQUETA, fontweight='bold', color=color)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=TAMANO_ETIQUETA, fontweight='bold', color=color)

