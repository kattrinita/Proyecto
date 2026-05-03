import pandas as pd
from tkinter import Tk, filedialog

def cargar_archivo():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo DRX", 
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    
    if not file_path:
        return None
        
    try:
        # 1. LECTURA DIRECTA: 'sep=\t' lee tabulaciones, 'decimal=,' convierte los números automáticamente
        df = pd.read_csv(file_path, sep='\t', decimal=',')
        
        # 2. Búsqueda de columnas robusta
        colmap = {c.lower(): c for c in df.columns} 
        theta_col = next((colmap[c] for c in colmap if 'pos' in c or '2th' in c), None)
        inten_col = next((colmap[c] for c in colmap if 'iobs' in c), None)
        
        if theta_col is None or inten_col is None:
            print(f"Error: Columnas no reconocidas. Encontradas: {list(df.columns)}")
            return None

        # 3. Aislar y estandarizar nombres
        df = df[[theta_col, inten_col]].copy()
        df.columns = ['2Theta', 'Iobs']
                
        print(f"Archivo cargado exitosamente. Filas detectadas: {len(df)}")
        return df
        
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None