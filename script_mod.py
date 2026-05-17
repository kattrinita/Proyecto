from analizador_drx import CargarDatos

def cargar_archivo():
    try:
        df = CargarDatos()
        if df is not None:
            print(f"Archivo cargado exitosamente. Filas detectadas: {len(df)}")
        return df
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None
