import numpy as np

def aplicar_scherrer(df_resultados, longitud_onda=0.15406, K=0.9):
  
    # 1. Conversión geométrica: De 2Theta (grados) a Theta (radianes)
    theta_radianes = np.radians(df_resultados['Angulo_2Theta'] / 2)
    
    # 2. Conversión del ancho: De FWHM (grados) a Beta (radianes)
    beta_radianes = np.radians(df_resultados['FWHM_grados'])
    
    # 3. La Física: D = (K * lambda) / (beta * cos(theta))
    tamano_cristalito = (K * longitud_onda) / (beta_radianes * np.cos(theta_radianes))
    
    # 4. Inyectamos la nueva columna en nuestra tabla (redondeada a 2 decimales)
    df_resultados['Tamaño_Cristal_nm'] = tamano_cristalito.round(2)
    
    return df_resultados