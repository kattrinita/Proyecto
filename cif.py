from analizador_drx import CargarCIF


def cargar_cif(ruta_archivo=None):
    """
    Devuelve un dict con: celda (a,b,c,alpha,beta,gamma,volumen),
    grupo_espacial y atomos (DataFrame con las posiciones atomicas).
    """
    return CargarCIF(ruta_archivo)
