import pandas as pd
from tkinter import Tk, filedialog

def cargar_archivo():
    # Creo ventana pa que el user pueda seleccionar el archivo
    root = Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter
    file_path = filedialog.askopenfilename(title="Selecciona un archivo DRX", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    
    if not file_path:
        print("No se seleccionó ningún archivo.")
        return None
    try:
        # sep='\s+' detecta cualquier cantidad de espacios o tabulaciones como separador
        df = pd.read_csv(file_path, sep='\\s+', engine='python')

        # me quedo nada mas con 2Theta e Iobs
        columna_theta = [c for c in df.columns if 'Pos' in c][0]
        columna_intensidad = [c for c in df.columns if 'Iobs' in c][0]

        df = df[[columna_theta, columna_intensidad]].copy() #creo tabla nueva con lo que me interesa
        df.columns = ['2Theta', 'Iobs']  # renombro las columnas

        # convierto a float los valores de la tabla (antes python los tomaba como strings)
        for col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

        print(f"Archivo {file_path} cargado exitosamente.")
        return df
    
    except Exception as e:
        print(f"Error al cargar el archivo: {e}") # e siempre me dice por que el archivo falló 
        return None