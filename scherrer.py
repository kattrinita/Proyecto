from analizador_drx import AplicarScherrer

def aplicar_scherrer(df_resultados, longitud_onda=0.15406, K=0.9):
    return AplicarScherrer(df_resultados, longitud_onda=longitud_onda, K=K)
