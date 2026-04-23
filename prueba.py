import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from tkinter import Tk, filedialog

# === CONFIGURACIÓN ===
TOLERANCIA = 0.37
COLOR_PICOS = 'skyblue'
LABEL_FONDO_ALPHA = 0.6
LABEL_FONDO_COLOR = 'white'
LABEL_FONDO_BORDE = 'none'
FUENTE_LABEL = 8

# Agregar picos que querés marcar con asterisco
BANDAS_CON_ASTERISCO = [37.3200, 43.4810]  # <--- Editar con tus 2θ deseados

def _to_float_series(s):
    return (
        s.astype(str)
         .str.strip()
         .str.replace(',', '.', regex=False)
         .replace(['', 'nan', 'None'], np.nan)
         .astype(float)
    )

def leer_drx_completo():
    Tk().withdraw()
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de DRX experimental completo")
    if not archivo:
        raise FileNotFoundError("No se seleccionó archivo de DRX completo.")
    try:
        df = pd.read_csv(archivo, sep='\t', engine='python')
    except Exception:
        df = pd.read_csv(archivo, sep=None, engine='python')
    colmap = {c.lower(): c for c in df.columns}
    theta_col = next((colmap[c] for c in colmap if '2th' in c or 'pos' in c), None)
    inten_col = next((colmap[c] for c in colmap if 'iobs' in c or 'int' in c), None)
    if theta_col is None or inten_col is None:
        raise KeyError(f"No se encontraron columnas 2θ/intensidad en: {list(df.columns)}")
    df = df[[theta_col, inten_col]].copy()
    df.columns = ['2Theta', 'Intensidad']
    df['2Theta'] = _to_float_series(df['2Theta'])
    df['Intensidad'] = _to_float_series(df['Intensidad'])
    df.dropna(subset=['2Theta', 'Intensidad'], inplace=True)
    return df.reset_index(drop=True)

def leer_picos_detectados():
    Tk().withdraw()
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de picos detectados")
    if not archivo:
        raise FileNotFoundError("No se seleccionó archivo de picos detectados.")
    try:
        df = pd.read_csv(archivo, sep=None, engine='python', header=None)
        numeric = df.apply(lambda col: pd.to_numeric(col.astype(str).str.replace(',', '.', regex=False), errors='coerce'))
        valid_cols = [c for c in numeric.columns if numeric[c].notna().any()]
        if len(valid_cols) == 0:
            raise ValueError("No se detectaron números.")
        if len(valid_cols) == 1:
            df_out = pd.DataFrame({'2Theta': numeric[valid_cols[0]]})
        else:
            df_out = pd.DataFrame({'2Theta': numeric[valid_cols[0]], 'Intensidad': numeric[valid_cols[1]]})
        df_out['2Theta'] = df_out['2Theta'].astype(float)
        df_out.dropna(subset=['2Theta'], inplace=True)
        return df_out.reset_index(drop=True)
    except Exception:
        thetas, intens = [], []
        pattern = re.compile(r'[-+]?\d*,?\d*(?:\.\d+)?(?:[eE][-+]?\d+)?')
        with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                nums = [n for n in re.findall(pattern, line) if any(ch.isdigit() for ch in n)]
                if len(nums) >= 1:
                    thetas.append(float(nums[0].replace(',', '.')))
                    intens.append(float(nums[1].replace(',', '.')) if len(nums) >= 2 else np.nan)
        return pd.DataFrame({'2Theta': thetas, 'Intensidad': intens})

def leer_referencia():
    Tk().withdraw()
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de referencia")
    if not archivo:
        raise FileNotFoundError("No se seleccionó archivo de referencia.")
    
    try:
        df = pd.read_csv(archivo, sep='\t', engine='python', on_bad_lines='skip')
    except Exception:
        df = pd.read_csv(archivo, sep=None, engine='python', on_bad_lines='skip')

    colmap = {c.lower(): c for c in df.columns}
    theta_col = next((colmap[c] for c in colmap if '2theta' in c or 'pos' in c), None)
    idx_col = next((colmap[c] for c in colmap if 'indice' in c or 'index' in c or 'hkl' in c), None)
    inten_col = next((colmap[c] for c in colmap if 'int' in c), None)

    if theta_col is None or idx_col is None:
        raise KeyError(f"No se encontraron columnas requeridas en: {list(df.columns)}")
    
    cols = [theta_col, idx_col] + ([inten_col] if inten_col else [])
    df = df[cols].copy()
    df.columns = ['2Theta', 'Indice'] + (['Intensidad_ref'] if inten_col else [])
    df['2Theta'] = _to_float_series(df['2Theta'])
    df.dropna(subset=['2Theta'], inplace=True)
    
    return df.reset_index(drop=True)

def asignar_indices(picos_df, ref_df, tolerancia=TOLERANCIA):
    asignaciones = []
    picos_sorted = picos_df.sort_values('2Theta').reset_index(drop=True)
    ref_sorted = ref_df.sort_values('2Theta').reset_index(drop=True)
    for _, pico in picos_sorted.iterrows():
        pa = pico['2Theta']
        mask = np.abs(ref_sorted['2Theta'] - pa) <= tolerancia
        matches = ref_sorted.loc[mask]
        if not matches.empty:
            etiqueta = ''.join(matches['Indice'].astype(str).tolist())
            asignaciones.append((pa, etiqueta))
    return asignaciones

def graficar_asignaciones(drx_df, asignaciones):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(drx_df['2Theta'], drx_df['Intensidad'], color='black', lw=1.5, label='DRX experimental completo')
    ymax = drx_df['Intensidad'].max()
    ax.set_ylim(top=ymax * 1.15)
    y_levels = [1.02, 1.06, 1.10, 1.14]
    last_positions = []
    asignaciones = sorted(asignaciones, key=lambda x: x[0])

    for x, hkl in asignaciones:
        ymin_abs, ymax_abs = ax.get_ylim()
        rel_ymin = (100 - ymin_abs) / (ymax_abs - ymin_abs)
        rel_ymax = (800 - ymin_abs) / (ymax_abs - ymin_abs)
        rel_ymin = max(0, min(1, rel_ymin))
        rel_ymax = max(0, min(1, rel_ymax))

        ax.axvline(x=x, color=COLOR_PICOS, linestyle='--', linewidth=1,
                   ymin=rel_ymin, ymax=rel_ymax)

        nivel = 0
        for prev_x in reversed(last_positions[-4:]):
            if abs(x - prev_x) < 0.25:
                nivel += 1
        nivel = min(nivel, len(y_levels) - 1)
        last_positions.append(x)
        y = ymax * y_levels[nivel]

        cerca_de_asterisco = any(abs(x - b) <= 0.1 for b in BANDAS_CON_ASTERISCO)
        etiqueta_final = hkl + ('*' if cerca_de_asterisco else '')
        # Si es impureza, subir un poco más la etiqueta
        if cerca_de_asterisco:
            y *= 0.82
        
        ax.text(
            x, y, etiqueta_final,
            rotation=90,
            ha='center',
            va='bottom',
            fontsize=FUENTE_LABEL,
            color='blue',
            bbox=dict(
                boxstyle='round,pad=0.2',
                edgecolor=LABEL_FONDO_BORDE,
                facecolor=LABEL_FONDO_COLOR,
                alpha=LABEL_FONDO_ALPHA,
            ),
            clip_on=False,
        )

    # Diccionario de impurezas conocidas
    LEYENDA_IMPUREZAS = {
        43.4810: "Li2CO3",
        37.3200: "MnO2"
    }

    # Crear entradas de leyenda específicas
    for angulo, nombre in LEYENDA_IMPUREZAS.items():
        ax.plot([], [], ' ', label=f"* {nombre}")

    # Entrada ficticia para que aparezca en la leyenda
    ax.set_xlabel("2θ [°]")
    ax.set_ylabel("Intensidad [u.a.]")
    ax.set_title("DRX LMNO con asignación de índices de Miller")
    ax.grid(True, linestyle=':', color='lightgray')
    ax.legend()
    fig.tight_layout()
    plt.xlim(5, 85)
    plt.ylim(80, 800)
    plt.show()

# === MAIN ===
if __name__ == "__main__":
    drx_df = leer_drx_completo()
    picos_df = leer_picos_detectados()
    ref_df = leer_referencia()
    asignaciones = asignar_indices(picos_df, ref_df, tolerancia=TOLERANCIA)
    graficar_asignaciones(drx_df, asignaciones)

