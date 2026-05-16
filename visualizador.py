import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def visualizador_search_match(df_curva, df_resultados):
    """
    Dibuja el difractograma imitando el estilo de publicación de referencia,
    con leyendas personalizadas, líneas guía y cajas de texto de colores.
    """
    fig, ax = plt.subplots(figsize=(13, 7))
    
    # 1. Trazamos la curva experimental original
    ax.plot(df_curva['2Theta'], df_curva['Iobs'], color='black', lw=1.2)
    
    # Ajustamos los límites de la ventana
    ymax = df_curva['Iobs'].max()
    ax.set_ylim(0, ymax * 1.35) # Damos un 35% de espacio arriba para textos
    ax.set_xlim(df_curva['2Theta'].min(), df_curva['2Theta'].max())
    
    # 2. Lógica de Escalera Anticolisión
    y_levels = [1.05, 1.12, 1.19, 1.26] 
    last_positions = []
    
    # Diccionario para rastrear qué fases encontramos y armar la leyenda después
    fases_detectadas = {'Fase Principal (LMNO)': 'black'}

    # 3. Iteramos sobre los resultados para estampar marcas
    for _, fila in df_resultados.iterrows():
        x_pico = fila['Angulo_2Theta']
        etiqueta = str(fila['Plano_hkl'])
        
        # --- LÓGICA DE DETECCIÓN DE COLORES ---
        color_texto = 'black'
        color_borde = 'gray'
        
        if "Impureza" in etiqueta or "*" in etiqueta:
            # Simulamos la separación de impurezas (Ajusten los strings según su Referencia.txt)
            if "101" in etiqueta or "MnO2" in etiqueta:
                color_texto = 'darkred'
                color_borde = 'darkred'
                fases_detectadas['Impureza: MnO2'] = 'darkred'
            else:
                color_texto = 'green'
                color_borde = 'green'
                fases_detectadas['Impureza: Li2CO3'] = 'green'
        
        # Algoritmo anticolisión
        nivel = 0
        for prev_x in reversed(last_positions[-4:]):
            if abs(x_pico - prev_x) < 2.5:
                nivel += 1
        nivel = min(nivel, len(y_levels) - 1)
        last_positions.append(x_pico)
        
        y_texto = ymax * y_levels[nivel]
        
        # --- LÍNEA VERTICAL GUÍA ---
        ax.axvline(x=x_pico, ymin=0, ymax=y_levels[nivel] / 1.35, 
                   color=color_borde if color_texto != 'black' else 'silver', 
                   linestyle='--', linewidth=0.8)
        
        # --- CAJA DE TEXTO (BBOX) ---
        ax.text(x_pico, y_texto, etiqueta, 
                rotation=90, ha='center', va='bottom',
                fontsize=9, color=color_texto, fontweight='bold',
                bbox=dict(boxstyle='square,pad=0.2', facecolor='white', 
                          edgecolor=color_borde, alpha=1))

    # 4. Construcción de la Leyenda Personalizada (Los cuadritos de colores)
    leyenda_patches = []
    for nombre, color in fases_detectadas.items():
        leyenda_patches.append(mpatches.Patch(color=color, label=nombre))
        
    ax.legend(handles=leyenda_patches, loc='upper right', 
              frameon=True, shadow=True, fontsize=10)

    # 5. Estética y Títulos
    ax.set_xlabel("2θ (°)", fontsize=12)
    ax.set_ylabel("Intensidad (u.a.)", fontsize=12)
    ax.set_title("DRX LMNOA3 - Análisis de Fases e Impurezas", fontsize=14, fontweight='bold')
    
    # Cuadrícula muy tenue como en la referencia
    ax.grid(True, linestyle=':', alpha=0.3)
    
    plt.tight_layout()
    plt.show()