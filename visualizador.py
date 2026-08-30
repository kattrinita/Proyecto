import matplotlib.pyplot as plt
from analizador_drx import GenerarGrafica, GenerarGraficaComparativa


def visualizador_search_match(df_curva, df_resultados):
    """Grafica de un solo ensayo (comportamiento original, sin cambios)."""
    return GenerarGrafica(df_curva, df_resultados, mostrar=True)


def visualizador_comparativo(df_curva_1, df_resultados_1, df_curva_2,
                              etiqueta_1="Ensayo 1", etiqueta_2="Ensayo 2",
                              df_referencia=None):
    """
    Grafica dos ensayos experimentales superpuestos (con offset vertical)
    para comparar visualmente si aparecen las mismas señales en ambos.
    """
    return GenerarGraficaComparativa(
        df_curva_1, df_resultados_1, df_curva_2,
        etiqueta_1=etiqueta_1, etiqueta_2=etiqueta_2,
        df_referencia=df_referencia, mostrar=True,
    )
