import seaborn as sns
import pandas as pd
import numpy as np
from tkinter import Tk, filedialog 

# --- TUS MÓDULOS DE PREPROCESAMIENTO ---
from script_mod import cargar_archivo
from sustraccion_fondo import sustraccion_fondo
from deteccion_maximos import deteccion_maximos

# --- NUESTROS NUEVOS MÓDULOS (FÍSICA Y CRUCE) ---
from ajuste import calcular_FWHM_exacto
from scherrer import aplicar_scherrer
from search import asignar_indices_miller
from visualizador import visualizador_search_match # El visualizador indexado

if __name__ == "__main__":
    print("Iniciando sistema de análisis DRX - Sprint 1...")
    
    # =========================================================
    # FASE 1 y 2: DATOS EXPERIMENTALES Y LIMPIEZA
    # =========================================================
    print("\n[1/5] Seleccione el difractograma experimental...")
    df_experimental = cargar_archivo()
    
    if df_experimental is not None:
        
        print("[2/5] Limpiando señal y sustrayendo fondo amorfo...")
        df_limpio = sustraccion_fondo(df_experimental, grado_base=2)
        
        print("      Extrayendo picos característicos...")
        maximos_df = deteccion_maximos(df_limpio, pct_altura=0.02, pct_prominencia=0.03)
        print(f"      -> Se encontraron {len(maximos_df)} picos en la muestra.")

        # =========================================================
        # FASE 3: ANÁLISIS FÍSICO (FWHM y SCHERRER)
        # =========================================================
        print("\n[3/5] Calculando FWHM mediante ajuste de perfiles Lorentzianos...")
        resultados_analisis = []
        
        # Extraemos las columnas limpias como vectores
        angulos = df_limpio['2Theta'].values
        intensidades_limpias = df_limpio['Iobs'].values 
        
        # Iteramos solo sobre los máximos encontrados
        for centro in maximos_df['2Theta']:
            fwhm, parametros = calcular_FWHM_exacto(angulos, intensidades_limpias, centro_detectado=centro)
            if fwhm is not None:
                resultados_analisis.append({
                    'Angulo_2Theta': centro,
                    'FWHM_grados': fwhm
                })
        
        df_resultados = pd.DataFrame(resultados_analisis)
        
        print("      Aplicando ecuación de Scherrer (Ánodo Cu, K=0.9)...")
        df_resultados = aplicar_scherrer(df_resultados, longitud_onda=0.15406, K=0.9)

        # =========================================================
        # FASE 4: SEARCH-MATCH (INDEXACIÓN)
        # =========================================================
        print("\n[4/5] Seleccione el archivo teórico 'Referencia.txt'...")
        
        # Abrimos un selector de archivos específicamente para la referencia
        root = Tk()
        root.withdraw() 
        ruta_ref = filedialog.askopenfilename(
            title="Selecciona el archivo de Referencia",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if ruta_ref:
            # Cargamos la base de datos teórica
            df_referencia = pd.read_csv(ruta_ref, sep=r'\s+', engine='python', decimal='.')
            
            print("      Cruzando datos experimentales con base teórica...")
            df_resultados = asignar_indices_miller(df_resultados, df_referencia, tolerancia=0.3)
            
            # Imprimimos el reporte final de forma elegante en la consola
            print("\n========================================================")
            print("            REPORTE CRISTALOGRÁFICO FINAL               ")
            print("========================================================")
            print(df_resultados.to_string(index=False))
            print("========================================================\n")

            # =========================================================
            # FASE 5: VISUALIZACIÓN
            # =========================================================
            print("[5/5] Generando difractograma indexado...")
            visualizador_search_match(df_experimental, df_resultados)
            
            print("\n¡Análisis completado con éxito!")
            
        else:
            print("\n[!] Operación cancelada: No se seleccionó archivo de referencia.")
            
    else:
        print("\n[!] Operación cancelada: No se seleccionó archivo experimental.")