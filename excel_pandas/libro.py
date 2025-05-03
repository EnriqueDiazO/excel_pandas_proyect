from typing import Dict
import pandas as pd
from .hoja import HojaPandas
import bibtexparser
import fitz 
import os

class LibroPandas:
    def __init__(self, nombre: str):
        """
        Representa un libro que contiene múltiples hojas basadas en pandas.

        Parámetros:
        -----------
        nombre : str
            Nombre del libro.
        """
        self.nombre: str = nombre
        self.hojas: Dict[str, HojaPandas] = {}

    def agregar_hoja(self, nombre_hoja: str, dataframe: pd.DataFrame) -> None:
        """
        Agrega una hoja al libro a partir de un DataFrame.

        Parámetros:
        -----------
        nombre_hoja : str
            Nombre identificador de la hoja.
        dataframe : pd.DataFrame
            Objeto DataFrame base para la hoja.
        """
        self.hojas[nombre_hoja] = HojaPandas(dataframe, nombre=nombre_hoja)

    def obtener_hoja(self, nombre_hoja: str) -> "HojaPandas | None":
        """
        Devuelve la hoja correspondiente al nombre proporcionado.

        Parámetros:
        -----------
        nombre_hoja : str

        Retorna:
        --------
        HojaPandas o None
        """
        return self.hojas.get(nombre_hoja)
    
    def copiar_hoja(self, nombre_hoja: str, nuevo_nombre: str) -> HojaPandas:
        """
        Crea una copia independiente de una hoja del libro con otro nombre.
    
        Parámetros:
        -----------
        nombre_hoja : str
           Nombre de la hoja original.
        nuevo_nombre : str
           Nombre para la nueva hoja clonada.

        Retorna:
        --------
        HojaPandas (la copia)
        """
        hoja = self.obtener_hoja(nombre_hoja)
        if hoja is None:
            raise ValueError(f"No existe la hoja '{nombre_hoja}' en el libro.")
    
        copia = hoja.copy(deep=True)
        copia.nombre = nuevo_nombre
        self.hojas[nuevo_nombre] = copia
        return copia
    
    def eliminar_hoja(self, nombre_hoja: str) -> None:
        """
        Elimina una hoja del libro por su nombre.

        Parámetros:
        -----------
        nombre_hoja : str
            Nombre de la hoja a eliminar.
        """
        if nombre_hoja in self.hojas:
            del self.hojas[nombre_hoja]
        else:
            raise ValueError(f"La hoja '{nombre_hoja}' no existe en el libro.")
        
    
    def renombrar_hoja(self, nombre_actual: str, nuevo_nombre: str) -> None:
        """
        Renombra una hoja del libro.
        
        Parámetros:
        -----------
        nombre_actual : str
            Nombre actual de la hoja.
        nuevo_nombre : str
            Nuevo nombre que se desea asignar.
        """
        if nombre_actual not in self.hojas:
            raise ValueError(f"La hoja '{nombre_actual}' no existe.")
        if nuevo_nombre in self.hojas:
            raise ValueError(f"Ya existe una hoja con el nombre '{nuevo_nombre}'.")

        self.hojas[nuevo_nombre] = self.hojas.pop(nombre_actual)
        self.hojas[nuevo_nombre].nombre = nuevo_nombre




    def __str__(self) -> str:
        """
        Representación en cadena del libro.

        Retorna:
        --------
        str
        """
        return f" Libro: {self.nombre}, hojas: {list(self.hojas.keys())}"

    @classmethod
    def desde_excel(cls, path: str, hojas: str = None) -> "LibroPandas":
        """
        Crea un libro a partir de un archivo Excel con múltiples hojas.

        Parámetros:
        -----------
        path : str
            Ruta al archivo Excel (.xlsx)
        hojas : str, opcional
            Rango de hojas a importar al estilo de impresora. Ej: "1-3,5"

        Retorna:
        --------
        LibroPandas
        """
        nombre_libro = path.split("/")[-1].replace(".xlsx", "")
        xls = pd.read_excel(path, sheet_name=None)
        nombres = list(xls.keys())

        if hojas is None:
            indices_seleccionados = list(range(len(nombres)))
        else:
            indices_seleccionados = _parsear_rango_hojas(hojas)

        libro = cls(nombre_libro)

        for i in indices_seleccionados:
            if i < len(nombres):
                nombre_hoja = nombres[i]
                libro.agregar_hoja(nombre_hoja, xls[nombre_hoja])

        return libro

    def agregar_hoja_desde_archivo(self, path: str, nombre_hoja: str = None, sep: str = ",", hojas: str = None) -> None:
        """
        Agrega una hoja o varias desde un archivo CSV, TSV o Excel (.xlsx).

        Parámetros:
        -----------
        path : str
            Ruta del archivo.
        nombre_hoja : str, opcional
            Nombre personalizado para la hoja (solo válido si se importa una sola).
        sep : str
            Separador para CSV o TSV ("," o "\\t").
        hojas : str, opcional
            Rango de hojas a importar (solo para archivos .xlsx). Ej: "1-2,4"
        """
        ext = path.split(".")[-1].lower()

        if ext == "csv":
            df = pd.read_csv(path, sep=sep)
            nombre = nombre_hoja or path.split("/")[-1].split(".")[0]
            self.agregar_hoja(nombre, df)

        elif ext == "tsv":
            df = pd.read_csv(path, sep="\t")
            nombre = nombre_hoja or path.split("/")[-1].split(".")[0]
            self.agregar_hoja(nombre, df)

        elif ext == "xlsx":
            xls = pd.read_excel(path, sheet_name=None)
            nombres = list(xls.keys())
            indices_seleccionados = (
                list(range(len(nombres))) if hojas is None
                else _parsear_rango_hojas(hojas)
            )

            if len(indices_seleccionados) == 1 and nombre_hoja:
                index = indices_seleccionados[0]
                self.agregar_hoja(nombre_hoja, xls[nombres[index]])
            else:
                for i in indices_seleccionados:
                    if i < len(nombres):
                        nombre = nombres[i]
                        self.agregar_hoja(nombre, xls[nombre])
        else:
            raise ValueError("Formato no soportado. Usa .csv, .tsv o .xlsx")
    
    @staticmethod
    def _contar_paginas(pages: str, file_path: str = "") -> int | str:
        """
         Intenta contar páginas a partir del campo 'pages' (e.g. '134--154') o, si no es posible,
         leyendo directamente el archivo PDF especificado en 'file_path'.

         Parámetros:
         ------------
         pages : str
            Rango de páginas como 'x--y', si está disponible en el registro BibTeX.
         file_path : str
            Ruta del archivo PDF (puede incluir rutas tipo Mendeley como ':C:/.../file.pdf:pdf').

        Retorna:
        --------
        int | str
           Número de páginas como entero, o cadena vacía si no puede determinarse.
        """
        # 1. Intentar con rango tipo '134--154'
        if pages and "--" in pages:
            try:
                inicio, fin = pages.split("--")
                return int(fin) - int(inicio) + 1
            except:
                pass  # sigue con intento por PDF

        # 2. Intentar con archivo PDF
        if file_path and ".pdf" in file_path.lower():
            try:
                # Extraer ruta válida de formatos tipo Mendeley
                # Ej: ':C:/path/to/file.pdf:pdf' → 'C:/path/to/file.pdf'
                partes = file_path.split(":")
                pdfs = [p for p in partes if p.strip().lower().endswith(".pdf")]

                if not pdfs:
                    return ""

                ruta_pdf = os.path.normpath(pdfs[0].strip())

                # Verificación robusta
                if os.path.exists(ruta_pdf):
                    doc = fitz.open(ruta_pdf)
                    return len(doc)
                else:
                    print(f"⚠️ Archivo no encontrado: '{ruta_pdf}'")
            except Exception as e:
                print(f"⚠️ Error al leer PDF '{file_path}': {e}")
        return ""


    

    @classmethod
    def desde_bib(cls, path_bib: str, nombre_hoja: str = "BibTeX") -> "LibroPandas":
        """ Crea un LibroPandas a partir de un archivo .bib de artículos académicos. 
        Convierte cada entrada en una fila del DataFrame.
        Parámetros:
        -----------
        path_bib : str
        Ruta al archivo .bib.
        nombre_hoja : str
        Nombre de la hoja en el libro resultante.

        Retorna:
        --------
        LibroPandas
       """
        with open(path_bib, encoding="utf-8") as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)

        registros = []
        for entry in bib_database.entries:
            paginas = entry.get("pages", "")
            archivo_pdf = entry.get("file", "")
            registros.append({
                "ID": entry.get("ID", ""),
                "Type": entry.get("ENTRYTYPE", ""),
                "Title": entry.get("title", ""),
                "Author(s)": entry.get("author", ""),
                "Year": entry.get("year", ""),
                "Journal": entry.get("journal", ""),
                "Volume": entry.get("volume", ""),
                "Number": entry.get("number", ""),
                "Pages": paginas,
                "Page Count": cls._contar_paginas(paginas, archivo_pdf),
                "DOI": entry.get("doi", ""),
                "URL": entry.get("url", ""),
                "Keywords": entry.get("keywords", ""),
                "Abstract": entry.get("abstract", ""),
                "Publisher": entry.get("publisher", ""),
                "ISSN": entry.get("issn", ""),
                "File": archivo_pdf,
                })

        df = pd.DataFrame(registros)
        hoja = HojaPandas(df, nombre=nombre_hoja)
        hoja.limpiar_columnas_latex()  # Aplica limpieza automática

        libro = cls(nombre="articulos_bib")
        libro.hojas[nombre_hoja] = hoja
        return libro

    def guardar_como_excel(self, path: str) -> None:
        """
        Exporta el libro actual como un archivo Excel con todas las hojas.
        
        Parámetros:
        -----------
        path : str
        Ruta de salida para el archivo .xlsx
        """
        with pd.ExcelWriter(path) as writer:
            for nombre, hoja in self.hojas.items():
                hoja.to_excel(writer, sheet_name=nombre, index=False)
    

 

# ╭────────────────────────────────────────────╮
# │ Función auxiliar para rangos estilo impresora
# ╰────────────────────────────────────────────╯
def _parsear_rango_hojas(rango: str) -> list[int]:
    """
    Convierte un string tipo "1-3,5,7-9" en una lista de índices (base 0): [0, 1, 2, 4, 6, 7, 8]

    Parámetros:
    -----------
    rango : str

    Retorna:
    --------
    list[int]
    """
    indices = set()
    partes = rango.split(",")
    for parte in partes:
        if "-" in parte:
            inicio, fin = map(int, parte.split("-"))
            indices.update(range(inicio - 1, fin))
        else:
            indices.add(int(parte) - 1)
    return sorted(indices)
