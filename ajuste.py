import numpy as np
from scipy.optimize import curve_fit


def ecuacion_lorentziana(x, amplitud, centro, gamma):

    return (amplitud / np.pi) * (gamma / ((x - centro)**2 + gamma**2))


def calcular_FWHM_exacto(angulos, intensidades, centro_detectado, ventana_grados=0.4):
    
  
    mascara = (angulos >= centro_detectado - ventana_grados) & (angulos <= centro_detectado + ventana_grados)
    x_pico = angulos[mascara]
    y_pico = intensidades[mascara]
    
    
    if len(x_pico) < 5:
        return None, None
        
    amplitud_estimada = np.max(y_pico) * np.pi * 0.1 
    gamma_estimado = 0.1 
    estimaciones_iniciales = [amplitud_estimada, centro_detectado, gamma_estimado]
    
    try:
       
        parametros_optimos, _ = curve_fit(
            f=ecuacion_lorentziana, 
            xdata=x_pico, 
            ydata=y_pico, 
            p0=estimaciones_iniciales
        )
        
       
        gamma_optimo = parametros_optimos[2]
        fwhm_calculado = 2 * abs(gamma_optimo)
        
       
        return fwhm_calculado, parametros_optimos
        
    except RuntimeError:
        
        print(f"No se pudo ajustar matemáticamente el pico en {centro_detectado}°")
        return None, None