# Proyecto: Excel y Pandas para Análisis de Datos

Este repositorio contiene un conjunto de notebooks y scripts diseñados para transformar y analizar datos desde hojas de cálculo, utilizando la biblioteca `pandas` y herramientas complementarias como `scikit-learn` y `wordcloud`.

## Estructura

- `excel_pandas/`: Módulo con clases como `Libro`, `Hoja`, `HojaSemantica`.
- `run.py`: Script principal para ejecutar el procesamiento.
- `notebooks/`: Ejemplos de uso:
  - Lectura de archivos
  - Análisis bibliométrico
  - Comparación de sensores
- `data/`: Datos de entrada en Excel, CSV y BibTeX.
- `static/`: Carpeta para frontend

---

## Instalación en Windows

1. Crea el ambiente virtual mediante consola (debes tener instalado `pyenv`):
    ```bash
    pyenv install 3.10.11
    pyenv local 3.10.11
    python -m virtualenv excel-pandas-env    
    ```

2. Descarga el repositorio, descomprime el proyecto (la carpeta descomprimida es **excel_pandas_proyect-main**) y colócala dentro de **excel-pandas-env**.

3. Abre una terminal en la carpeta donde está contenido el proyecto y el ambiente. Activa el ambiente virtual:
    ```bash
    .\Scripts\activate
    ```

4. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

---

## Instalación en Google Colab

1. Clona el repositorio directamente desde Colab:
    ```python
    !git clone https://github.com/EnriqueDiazO/excel_pandas_proyect.git
    %cd excel_pandas_proyect
    ```

2. Instala las dependencias necesarias:
    ```python
    !pip install -r requirements.txt
    ```

3. Importa y usa las clases:
    ```python
    from excel_pandas.libro import LibroPandas
    libro = LibroPandas("MiLibro")
    ```

---

## Uso básico

```python
from excel_pandas.libro import LibroPandas

# Crear un libro desde archivo Excel
libro = LibroPandas.desde_excel("data/dataset.xlsx")

# Acceder a una hoja
hoja = libro.obtener_hoja("Hoja1")

# Ver las primeras filas
print(hoja.head())

# Analizar texto con HojaSemantica
from excel_pandas.hoja_semantica import HojaSemantica
hoja_sem = HojaSemantica(hoja)
hoja_sem.analizar_texto("Resumen")
hoja_sem.graficar_clusters()
