"""
Script de prueba rapida para el proyecto DRX.

No necesita archivos reales: genera datos sinteticos (dos ensayos con picos
parecidos + un poco de ruido), corre todo el pipeline (lectura, resta de
fondo, deteccion de picos, FWHM, Scherrer, comparacion con referencia),
prueba la lectura de distintos formatos de archivo, prueba la lectura de un
.cif de ejemplo, y genera la grafica comparativa como PNG.

Como correrlo:
    python probar_todo.py

Al final va a quedar un archivo "prueba_comparativa.png" con la grafica de
los dos ensayos superpuestos, para que lo abran y vean que se ve bien.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # no abre ventana, solo genera el PNG

from analizador_drx import (
    CargarDatos,
    RemoverBackground,
    IdentificarPicos,
    CalcularFWHM,
    AplicarScherrer,
    CompararConReferencia,
    GenerarGraficaComparativa,
    CargarCIF,
)


def _gauss(x, centro, amplitud, ancho):
    return amplitud * np.exp(-((x - centro) ** 2) / (2 * ancho ** 2))


def generar_datos_sinteticos():
    """Crea dos 'ensayos' con picos en angulos parecidos pero distinta intensidad."""
    x = np.linspace(5, 85, 4000)
    ruido = lambda: 0.05 * np.random.rand(len(x))

    y1 = (
        ruido()
        + _gauss(x, 18.7, 2.1, 0.15)
        + _gauss(x, 37.0, 0.30, 0.20)
        + _gauss(x, 43.3, 0.30, 0.15)
    )
    y2 = (
        ruido()
        + _gauss(x, 18.7, 1.0, 0.15)
        + _gauss(x, 37.0, 0.15, 0.20)
    )
    return pd.DataFrame({"2Theta": x, "Iobs": y1}), pd.DataFrame({"2Theta": x, "Iobs": y2})


def probar_lectura_formatos(df1, df2):
    print("\n== 1) Lectura de datos en distintos formatos ==")
    df1.to_csv("prueba_exp1.csv", sep=";", decimal=",", index=False)   # como Excel en español
    df2.to_csv("prueba_exp2.txt", sep=" ", index=False)                # espacios, punto decimal

    cargado1 = CargarDatos("prueba_exp1.csv")
    cargado2 = CargarDatos("prueba_exp2.txt")
    print(f"  prueba_exp1.csv (';' y coma decimal) -> {len(cargado1)} filas leidas")
    print(f"  prueba_exp2.txt (espacios)            -> {len(cargado2)} filas leidas")
    return cargado1, cargado2


def probar_pipeline_completo(cargado1, cargado2):
    print("\n== 2) Pipeline completo (fondo, picos, FWHM, Scherrer, comparacion) ==")
    limpio1 = RemoverBackground(cargado1)
    limpio2 = RemoverBackground(cargado2)

    picos1 = IdentificarPicos(limpio1)
    resultados = CalcularFWHM(limpio1, picos1)
    resultados = AplicarScherrer(resultados)

    referencia = pd.DataFrame({
        "2Theta": [18.7, 37.0, 43.3],
        "Indice": ["(111)", "(311)", "(400)"],
    })
    resultados = CompararConReferencia(resultados, referencia, tolerancia=0.3)

    print(resultados[["Plano_hkl", "Angulo_2Theta", "FWHM_grados", "Tamaño_Cristal_nm"]].to_string(index=False))
    return limpio1, limpio2, resultados, referencia


def probar_grafica_comparativa(limpio1, resultados, limpio2, referencia):
    print("\n== 3) Grafica comparativa de dos ensayos ==")
    GenerarGraficaComparativa(
        limpio1, resultados, limpio2,
        etiqueta_1="Ensayo 1 (sintetico)",
        etiqueta_2="Ensayo 2 (sintetico)",
        df_referencia=referencia,
        guardar_en="prueba_comparativa.png",
        mostrar=False,
    )
    print("  Grafica guardada en prueba_comparativa.png")


def probar_cif():
    print("\n== 4) Lectura de archivo .cif ==")
    contenido_cif = """
data_ejemplo
_cell_length_a    8.2000(3)
_cell_length_b    8.2000
_cell_length_c    8.2000
_cell_angle_alpha 90.00
_cell_angle_beta  90.00
_cell_angle_gamma 90.00
_cell_volume      551.37
_symmetry_space_group_name_H-M  'F d -3 m'
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
Li1 Li 0.1250 0.1250 0.1250
Mn1 Mn 0.5000 0.5000 0.5000
O1 O 0.2600 0.2600 0.2600
"""
    with open("prueba_ejemplo.cif", "w") as archivo:
        archivo.write(contenido_cif)

    info = CargarCIF("prueba_ejemplo.cif")
    print(f"  Celda: {info['celda']}")
    print(f"  Grupo espacial: {info['grupo_espacial']}")
    print(f"  Atomos leidos: {len(info['atomos'])}")
    print(info["atomos"].to_string(index=False))


if __name__ == "__main__":
    df1, df2 = generar_datos_sinteticos()
    cargado1, cargado2 = probar_lectura_formatos(df1, df2)
    limpio1, limpio2, resultados, referencia = probar_pipeline_completo(cargado1, cargado2)
    probar_grafica_comparativa(limpio1, resultados, limpio2, referencia)
    probar_cif()
    print("\nTodo OK. Revisa prueba_comparativa.png para ver la grafica generada.")
