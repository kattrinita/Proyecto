from analizador_drx import IdentificarPicos

def deteccion_maximos(df, pct_altura=0.08, pct_prominencia=0.06):
    picos = IdentificarPicos(df, pct_altura=pct_altura, pct_prominencia=pct_prominencia)
    return picos.rename(columns={"Angulo_2Theta": "2Theta"})
