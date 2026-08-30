import numpy as np
import pandas as pd

from analizador_drx import CalcularFWHM


def ecuacion_lorentziana(x, amplitud, centro, gamma):

    return (amplitud / np.pi) * (gamma / ((x - centro)**2 + gamma**2))


def calcular_FWHM_exacto(angulos, intensidades, centro_detectado, ventana_grados=0.4):
    df = pd.DataFrame({"2Theta": angulos, "Iobs_Limpia": intensidades})
    df_pico = pd.DataFrame({"Angulo_2Theta": [centro_detectado]})
    resultado = CalcularFWHM(df, df_pico, ventana_grados=ventana_grados)
    if resultado.empty:
        print(f"No se pudo medir FWHM del pico en {centro_detectado}°")
        return None, None
    return float(resultado.iloc[0]["FWHM_grados"]), None
