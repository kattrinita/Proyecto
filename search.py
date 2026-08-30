from analizador_drx import CompararConReferencia

def asignar_indices_miller(df_resultados, df_referencia, tolerancia=0.3):
    return CompararConReferencia(df_resultados, df_referencia, tolerancia=tolerancia)
