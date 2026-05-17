import matplotlib.pyplot as plt
from analizador_drx import GenerarGrafica

def visualizador_search_match(df_curva, df_resultados):
    return GenerarGrafica(df_curva, df_resultados, mostrar=True)
