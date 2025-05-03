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

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <URL-del-repo>
   cd excel_pandas_proyecto
   ```
2. Crea el ambiente virtual
    ```python
    pyenv install 3.10.14  
    pyenv virtualenv 3.10.14 excel-pandas-env
    pyenv activate excel-pandas-env
    ```
3. Instala las dependencias
    ```python
    pip install -r requirements.txt
    ``
