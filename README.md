# Proyecto DRX

Herramienta en **Python** para procesar datos de Difraccion de Rayos X (DRX),
indexar picos y calcular el tamano de cristalito con la ecuacion de Scherrer.

## Como ejecutar

```bash
python prueba.py
```

Se abre una interfaz grafica donde se seleccionan:

- archivo experimental DRX 1 (`.txt`, `.xy`, `.dat`, `.csv`, u otros formatos de texto);
- archivo experimental DRX 2 (**opcional**) para comparar dos ensayos en la misma grafica;
- archivo de referencia con angulos teoricos e indices hkl;
- tolerancia de search-match;
- longitud de onda y constante K.

La interfaz permite ver la tabla final, visualizar el difractograma indexado
(o la comparacion de dos ensayos si se cargo un segundo archivo), exportar el
reporte a `.csv` / `.html` / `.xlsx`, guardar la grafica y consultar
informacion basica de un archivo `.cif` (parametros de celda, grupo espacial
y cantidad de atomos leidos).

## Novedades de esta version

- **Dos curvas en la misma grafica**: si se carga un segundo archivo
  experimental, `GenerarGraficaComparativa` dibuja ambos ensayos superpuestos
  (uno arriba, uno abajo, normalizados y con offset) para ver de un vistazo
  si aparecen las mismas señales en los dos casos.
- **Lectura de datos mas robusta**: `CargarDatos` ahora prueba varias
  combinaciones de separador y decimal (tab, coma, punto y coma, espacios,
  autodeteccion) antes de caer al modo de extraccion por expresiones
  regulares, para cubrir mas formatos de exportacion sin tener que tocar el
  codigo cada vez.
- **Lectura basica de `.cif`**: `CargarCIF` extrae parametros de celda
  (a, b, c, angulos, volumen), grupo espacial y la tabla de posiciones
  atomicas de un archivo `.cif` estandar, sin depender de librerias externas.
- **Calculo de parametros de red**: no se encontro ninguna funcion de este
  tipo en el codigo original (solo estaba el tamano de cristalito via
  Scherrer), asi que no hubo nada que quitar. Si en algun momento se agrega,
  conviene aislarla en su propia funcion para poder sacarla facil de nuevo.

## Funciones principales

- `CargarDatos`: lee archivos experimentales con varios formatos de
  separador/decimal, ignora encabezados y normaliza comas decimales.
- `CargarReferencia`: lee el archivo de picos teoricos e indices hkl.
- `CargarCIF`: lee parametros de celda, grupo espacial y atomos de un `.cif`.
- `RemoverBackground`: estima y resta la linea base del difractograma.
- `IdentificarPicos`: encuentra maximos de Bragg por altura, prominencia y distancia minima.
- `CompararConReferencia`: asigna el indice hkl mas cercano dentro de una tolerancia.
- `CalcularFWHM`: mide el ancho a media altura por interpolacion.
- `AplicarScherrer`: calcula `D = K*lambda / (beta*cos(theta))`.
- `GenerarGrafica`: dibuja la curva de un solo ensayo y marca los picos indexados.
- `GenerarGraficaComparativa`: dibuja dos ensayos superpuestos para comparar señales.
- `GenerarReporte`: crea una tabla final y puede exportarla como CSV, HTML o XLSX.

Todas estan centralizadas en `analizador_drx.py`. Los modulos anteriores
(`scherrer.py`, `visualizador.py`, `search.py`, `script_mod.py`,
`deteccion_maximos.py`, `ajuste.py`, `sustraccion_fondo.py`) siguen
existiendo como adaptadores para no romper imports viejos, y se sumo
`cif.py` como adaptador nuevo para la lectura de archivos `.cif`.
