import seaborn as sns
import pandas as pd
import numpy as np
from tkinter import Tk, filedialog 
from sustraccion_fondo import sustraccion_fondo
from deteccion_maximos import deteccion_maximos
from visualizador import visualizador
from ppp import cargar_archivo

if __name__ == "__main__":
    print("Iniciando sistema de análisis DRX...")
    
    # Se abre la ventana para que el usuario elija el .txt
    df_experimental = cargar_archivo()
    
    # Verificación de seguridad: solo avanza si el usuario seleccionó un archivo
    if df_experimental is not None:
        
        # 2. Ajuste de Línea Base
        print("Limpiando señal y sustrayendo fondo amorfo...")
        df_limpio = sustraccion_fondo(df_experimental, grado_base=2)
        
        # 3. Detección de Máximos
        print("Extrayendo picos característicos...")
        maximos_df = deteccion_maximos(df_limpio, pct_altura=0.1, pct_prominencia=0.11)
        
        # 4. Visualización Final
        print("Generando gráfico del difractograma...")
        # Llama a la función gráfica pasándole la curva original, la limpia y los puntos de los picos
        visualizador(df_limpio, maximos_df)
        
        print("Análisis experimental completado.")
    else:
        print("Operación cancelada por el usuario.")