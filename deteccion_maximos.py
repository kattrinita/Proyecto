import numpy as np
import pandas as pd
from scipy.signal import find_peaks

def deteccion_maximos(df, pct_altura=0.02, pct_prominencia=0.01):

    x=df['2Theta'].values       #extraigo del df todas las posiciones en 2theta
    y=df['Iobs_Limpia'].values     #extraigo del df todos la valores de la Iobs limpios
    
    int_max_ref = np.max(y)
    alturamax = int_max_ref * pct_altura
    prominencia_min = int_max_ref * pct_prominencia

    indices_maximos, _ = find_peaks(y, prominence=prominencia_min, height=alturamax)   #obtengo todo los indices donde hay un pico en x=1,2,3,etc
                                                      
    maximos_df = pd.DataFrame({                
        '2Theta': x[indices_maximos],           #indexo en la col 2theta el angulo del pico que se encontro un maximo
        'Iobs_maxima': y[indices_maximos]       #indexo las Iobs maximas
    })

    

    return maximos_df