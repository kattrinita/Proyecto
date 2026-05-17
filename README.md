# Proyecto DRX

Herramienta en **Python** para procesar datos de Difraccion de Rayos X (DRX),
indexar picos y calcular el tamano de cristalito con la ecuacion de Scherrer.

## Como ejecutar

```bash
python prueba.py
```

Se abre una interfaz grafica donde se seleccionan:

- archivo experimental DRX (`.txt`, `.xy`, `.dat`, `.csv`);
- archivo de referencia con angulos teoricos e indices hkl;
- tolerancia de search-match;
- longitud de onda y constante K.

La interfaz permite ver la tabla final, visualizar el difractograma indexado,
exportar el reporte a `.csv` y guardar la grafica.

## Funciones principales

- `CargarDatos`: lee archivos experimentales, ignora encabezados y normaliza comas decimales.
- `RemoverBackground`: estima y resta la linea base del difractograma.
- `IdentificarPicos`: encuentra maximos de Bragg por altura, prominencia y distancia minima.
- `CompararConReferencia`: asigna el indice hkl mas cercano dentro de una tolerancia.
- `CalcularFWHM`: mide el ancho a media altura por interpolacion.
- `AplicarScherrer`: calcula `D = K*lambda / (beta*cos(theta))`.
- `GenerarGrafica`: dibuja la curva y marca los picos indexados.
- `GenerarReporte`: crea una tabla final y puede exportarla como CSV.

Todas estan centralizadas en `analizador_drx.py`. Los modulos anteriores siguen
existiendo como adaptadores para no romper imports viejos.
