import numpy as np
import pandas as pd
import peakutils

def sustraccion_fondo(df, grado_base=2):

    y = df['Iobs'].values   #Extraigo del data frame intensidades brutas con fondo amorfo pasadas a numeros

    fondo = peakutils.baseline(y, deg=grado_base)     #guardo la linea de base con ruido
    
    y_limpia = y - fondo      #le quito a la intensidad el fondo amorfo inicial 
    y_limpia = np.maximum(y_limpia,0)

    df['Linea_Base'] = fondo                #creo nueva col en el df con la linea base debajo de toda la funcion
    df['Iobs_Limpia'] = y_limpia            #creo nueva col en el df con las Iobs aplanadas sobre la linea base

    return df
   

