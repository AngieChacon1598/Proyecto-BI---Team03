import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
import glob

# ==================== GENERAR REPORTE PDF ====================

def generar_reporte_pdf():
    """Genera un reporte PDF completo con todos los resultados y gráficos"""
    
    # Cargar datos
    archivo = '../../data/RecopilaciónDeDatos-BI(respuestas).xlsx'
    df = pd.read_excel(archivo)
    
    # Crear el documento PDF
    nombre_pdf = f"Reporte_Analisis_Encuesta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(nombre_pdf, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    # Contenedor para los elementos del PDF
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#283593'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Título principal
    story.append(Paragraph("REPORTE DE ANÁLISIS DE ENCUESTA", title_style))
    story.append(Paragraph("Análisis de Preferencias y Expectativas de Estudiantes", 
                          styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"<b>Fecha de generación:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 
                          styles['Normal']))
    story.append(Paragraph(f"<b>Total de estudiantes encuestados:</b> {len(df)}", 
                          styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Columnas de las preguntas
    columnas_preguntas = {
        "Pregunta 1 - Preferencias de Aprendizaje": {
            "columna": "¿Cómo prefieres aprender cosas nuevas?",
            "descripcion": "Análisis de los métodos de aprendizaje preferidos por los estudiantes."
        },
        "Pregunta 2 - Importancia de la Tecnología": {
            "columna": "¿Qué tan importante consideras la tecnología (computadoras, internet, apps) para tu educación futura?",
            "descripcion": "Evaluación de la percepción sobre la importancia de la tecnología."
        },
        "Pregunta 3 - Factores de Elección de Carrera": {
            "columna": "¿Qué factor influye más en tu elección de carrera?",
            "descripcion": "Identificación de los principales factores que influyen en la elección de carrera."
        },
        "Pregunta 4 - Tipo de Estudios Preferidos": {
            "columna": "¿Qué tipo de estudios prefieres seguir después del colegio?",
            "descripcion": "Análisis de las preferencias sobre el tipo de estudios superiores."
        },
        "Pregunta 5 - Lugar de Trabajo Futuro": {
            "columna": "¿Dónde te imaginas trabajando en el futuro?",
            "descripcion": "Expectativas sobre los lugares donde los estudiantes se imaginan trabajando."
        }
    }
    
    # Procesar cada pregunta
    for idx, (titulo, info) in enumerate(columnas_preguntas.items(), 1):
        columna = info["columna"]
        descripcion = info["descripcion"]
        
        if columna not in df.columns:
            story.append(Paragraph(f"<b>{titulo}</b>", heading_style))
            story.append(Paragraph("[ADVERTENCIA] Columna no encontrada en los datos.", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            continue
        
        # Título de la pregunta
        story.append(PageBreak() if idx > 1 else Spacer(1, 0.2*inch))
        story.append(Paragraph(f"<b>{titulo}</b>", heading_style))
        story.append(Paragraph(descripcion, styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Columna de grado
        col_grado = "  ¿En qué grado estás actualmente?   "
        
        # Función auxiliar para crear tabla
        def crear_tabla_resultados(conteos, titulo_tabla=""):
            """Crea una tabla con los resultados"""
            # Crear estilo para encabezados con texto blanco
            header_style = ParagraphStyle(
                'HeaderStyle',
                parent=styles['Normal'],
                textColor=colors.white,
                fontName='Helvetica-Bold',
                fontSize=10,
                alignment=TA_LEFT
            )
            header_style_center = ParagraphStyle(
                'HeaderStyleCenter',
                parent=header_style,
                alignment=TA_CENTER
            )
            
            data = [[Paragraph('Opción', header_style), 
                     Paragraph('Cantidad', header_style_center), 
                     Paragraph('Porcentaje', header_style_center)]]
            total = conteos.sum() if len(conteos) > 0 else 0
            
            if total > 0:
                for opcion, cantidad in conteos.items():
                    porcentaje = (cantidad / total) * 100
                    data.append([
                        Paragraph(str(opcion)[:50] + ('...' if len(str(opcion)) > 50 else ''), styles['Normal']),
                        Paragraph(str(cantidad), styles['Normal']),
                        Paragraph(f"{porcentaje:.1f}%", styles['Normal'])
                    ])
                # Usar Paragraph para que el HTML se interprete correctamente
                data.append([
                    Paragraph('<b>TOTAL</b>', styles['Normal']), 
                    Paragraph(f'<b>{total}</b>', styles['Normal']), 
                    Paragraph('<b>100.0%</b>', styles['Normal'])
                ])
            else:
                data.append([
                    Paragraph('Sin datos', styles['Normal']), 
                    Paragraph('0', styles['Normal']), 
                    Paragraph('0.0%', styles['Normal'])
                ])
            
            tabla = Table(data, colWidths=[3.5*inch, 1*inch, 1*inch])
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#283593')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#c5cae9')),
            ]))
            return tabla
        
        # Mostrar resultados por grado si existe la columna
        if col_grado in df.columns:
            # Resultados de 4to año
            df_4to = df[df[col_grado] == '4°']
            if len(df_4to) > 0:
                conteos_4to = df_4to[columna].value_counts()
                story.append(Paragraph("<b>Resultados - 4to Año:</b>", styles['Normal']))
                story.append(Spacer(1, 0.05*inch))
                tabla_4to = crear_tabla_resultados(conteos_4to)
                story.append(tabla_4to)
                story.append(Spacer(1, 0.15*inch))
            
            # Resultados de 5to año
            df_5to = df[df[col_grado] == '5°']
            if len(df_5to) > 0:
                conteos_5to = df_5to[columna].value_counts()
                story.append(Paragraph("<b>Resultados - 5to Año:</b>", styles['Normal']))
                story.append(Spacer(1, 0.05*inch))
                tabla_5to = crear_tabla_resultados(conteos_5to)
                story.append(tabla_5to)
                story.append(Spacer(1, 0.15*inch))
        
        # Obtener conteos totales
        conteos = df[columna].value_counts()
        
        # Crear tabla con todos los resultados
        story.append(Paragraph("<b>Resultados - Total (4to + 5to Año):</b>", styles['Normal']))
        story.append(Spacer(1, 0.05*inch))
        tabla_total = crear_tabla_resultados(conteos)
        story.append(tabla_total)
        story.append(Spacer(1, 0.2*inch))
        
        # Intentar agregar gráfico si existe
        grafico_path = f'grafico_p{idx}_*.png'
        graficos = glob.glob(grafico_path)
        if graficos:
            # Tomar el primer gráfico encontrado (barras preferiblemente)
            grafico_barras = [g for g in graficos if 'pie' not in g]
            grafico_a_usar = grafico_barras[0] if grafico_barras else graficos[0]
            
            if os.path.exists(grafico_a_usar):
                try:
                    img = Image(grafico_a_usar, width=6*inch, height=3.5*inch)
                    story.append(img)
                    story.append(Spacer(1, 0.2*inch))
                except:
                    pass
    
    # Página de resumen final
    story.append(PageBreak())
    story.append(Paragraph("<b>RESUMEN EJECUTIVO</b>", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Estadísticas generales
    col_grado = "  ¿En qué grado estás actualmente?   "
    if col_grado in df.columns:
        conteo_grados = df[col_grado].value_counts()
        story.append(Paragraph("<b>Distribución por Grado:</b>", styles['Normal']))
        for grado, cantidad in conteo_grados.items():
            story.append(Paragraph(f"  • {grado}: {cantidad} estudiantes", styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    # Construir el PDF
    doc.build(story)
    print(f"\n[OK] Reporte PDF generado exitosamente: {nombre_pdf}")
    return nombre_pdf

if __name__ == "__main__":
    print("=" * 80)
    print("GENERANDO REPORTE PDF...")
    print("=" * 80)
    generar_reporte_pdf()
    print("\n[OK] Proceso completado!")

