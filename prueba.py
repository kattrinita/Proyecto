import seaborn as sns
import pandas as pd
import numpy as np
from tkinter import Tk, filedialog 

# Importaciones de tus módulos actuales
from sustraccion_fondo import sustraccion_fondo
from deteccion_maximos import deteccion_maximos
from visualizador import visualizador
from script_mod import cargar_archivo

# ---> NUEVAS IMPORTACIONES <---
from ajuste import calcular_FWHM_exacto
from scherrer import aplicar_scherrer

if __name__ == "__main__":
    print("Iniciando sistema de análisis DRX...")
    
    # 1. Se abre la ventana para que el usuario elija el .txt
    df_experimental = cargar_archivo()
    
    # Verificación de seguridad: solo avanza si el usuario seleccionó un archivo
    if df_experimental is not None:
        
        # 2. Ajuste de Línea Base
        print("Limpiando señal y sustrayendo fondo amorfo...")
        df_limpio = sustraccion_fondo(df_experimental, grado_base=2)
        
        # 3. Detección de Máximos
        print("Extrayendo picos característicos...")
        maximos_df = deteccion_maximos(df_limpio, pct_altura=0.1, pct_prominencia=0.11)
        print(f"Se encontraron {len(maximos_df)} picos en la muestra.")

        # =========================================================
        # NUEVA FASE: ANÁLISIS FÍSICO (FWHM y Ecuación de Scherrer)
        # =========================================================
        print("Calculando FWHM mediante ajuste de perfiles Lorentzianos...")
        resultados_analisis = []
        
        # Extraemos los datos como arreglos de NumPy (Ajusta 'Iobs' al nombre de tu columna limpia)
        angulos = df_limpio['2Theta'].values
        intensidades_limpias = df_limpio['Iobs'].values 
        
        # Iteramos sobre los centros encontrados por tu Función 3
        for centro in maximos_df['2Theta']:
            fwhm, parametros = calcular_FWHM_exacto(angulos, intensidades_limpias, centro_detectado=centro)
            if fwhm is not None:
                resultados_analisis.append({
                    'Angulo_2Theta': centro,
                    'FWHM_grados': fwhm
                })
        
        # Convertimos la lista de resultados a un DataFrame de Pandas
        df_resultados = pd.DataFrame(resultados_analisis)
        
        # Aplicamos la matemática vectorizada de Scherrer a todos los picos
        print("Aplicando ecuación de Scherrer...")
        df_resultados = aplicar_scherrer(df_resultados)
        
        # Mostramos la tabla final en consola
        print("\n--- TABLA DE RESULTADOS FÍSICOS ---")
        print(df_resultados)
        print("-----------------------------------\n")
        # =========================================================

        # 4. Visualización Final
        print("Generando gráfico del difractograma...")
        # Llama a la función gráfica pasándole la curva original, la limpia y los puntos de los picos
        visualizador(df_limpio, maximos_df)
        
        print("Análisis experimental completado.")
        
    else:
        # Cerramos el if que dejaste abierto
        print("Operación cancelada: No se seleccionó ningún archivo.")