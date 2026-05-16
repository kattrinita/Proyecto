import pandas as pd
import numpy as np

def asignar_indices_miller(df_resultados, df_referencia, tolerancia=0.3):
   
    etiquetas_hkl = []
    
    for angulo_exp in df_resultados['Angulo_2Theta']:
        # 1. Calculamos la distancia absoluta entre el pico experimental y TODOS los teóricos
        distancias = np.abs(df_referencia['2Theta'] - angulo_exp)
        
        # 2. Encontramos la distancia más pequeña y su posición (índice) en la tabla
        menor_distancia = distancias.min()
        indice_del_mas_cercano = distancias.idxmin()
        
        # 3. Regla de decisión: ¿Está dentro de nuestro margen de error?
        if menor_distancia <= tolerancia:
            # ¡Match exitoso! Extraemos el string del plano (ej. "(111)")
            plano = df_referencia.loc[indice_del_mas_cercano, 'Indice']
            etiquetas_hkl.append(plano)
        else:
            # Si el pico está muy lejos de cualquier plano teórico, es una impureza
            etiquetas_hkl.append("* Impureza")
            
    # 4. Agregamos esta nueva lista como la primera columna de nuestro DataFrame final
    df_resultados.insert(0, 'Plano_hkl', etiquetas_hkl)
    
    return df_resultados