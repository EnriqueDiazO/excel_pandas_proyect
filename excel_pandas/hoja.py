import pandas as pd
import re
from typing import List

class HojaPandas(pd.DataFrame):
    """
    Subclase de pandas.DataFrame que representa una hoja de cálculo con funciones personalizadas.
    Incluye un atributo 'nombre' para identificar la hoja.
    """

    def __init__(self, data=None, nombre: str = "Hoja", **kwargs):
        """
        Inicializa una hoja de cálculo a partir de un DataFrame.

        Parámetros:
        -----------
        data : cualquier tipo válido para pd.DataFrame
        nombre : str
            Nombre identificador de la hoja
        kwargs : dict
            Argumentos adicionales para pd.DataFrame
        """
        super().__init__(data, **kwargs)
        self.nombre: str = nombre

    @property
    def _constructor(self):
        # Esto asegura que las operaciones devuelvan HojaPandas y conserven el nombre
        def _c(*args, **kwargs):
            result = HojaPandas(*args, **kwargs)
            result.nombre = getattr(self, "nombre", "Hoja")
            return result
        return _c

    def insertar_fila(self, valores: dict, index: int = None) -> "HojaPandas":
        nueva_fila = pd.Series(valores, index=self.columns)
        nueva_hoja = (pd.concat([self, nueva_fila.to_frame().T], ignore_index=True)
                      if index is None else
                      pd.concat([self.iloc[:index], nueva_fila.to_frame().T, self.iloc[index:]]).reset_index(drop=True))
        return HojaPandas(nueva_hoja, nombre=self.nombre)
    
    def limpiar_columnas_latex(self, columnas: List[str] = None) -> None:
        """
        Limpia caracteres LaTeX de columnas seleccionadas.
        Si no se especifica ninguna, se limpia todo texto del DataFrame.
        """
        def latex_to_unicode(text):
            if not isinstance(text, str):
                return text
            replacements = {
                r"\'a": "á", r'\"a': "ä", r"\`a": "à", r"\~a": "ã",
                r"\'e": "é", r'\"e': "ë", r"\`e": "è",
                r"\'i": "í", r'\"i': "ï", r"\`i": "ì",
                r"\'o": "ó", r'\"o': "ö", r"\`o": "ò", r"\~o": "õ",
                r"\'u": "ú", r'\"u': "ü", r"\`u": "ù",
                r"\'A": "Á", r'\"A': "Ä", r"\`A": "À", r"\~A": "Ã",
                r"\'E": "É", r'\"E': "Ë", r"\`E": "È",
                r"\'I": "Í", r'\"I': "Ï", r"\`I": "Ì",
                r"\'O": "Ó", r'\"O': "Ö", r"\`O": "Ò", r"\~O": "Õ",
                r"\'U": "Ú", r'\"U': "Ü", r"\`U": "Ù",
                r"\~n": "ñ", r"\~N": "Ñ",
                r"\c{c}": "ç", r"\c{C}": "Ç",
                r"\\ss": "ß", r"\'y": "ý", r"\'Y": "Ý"
            }
            for latex, char in replacements.items():
                text = text.replace(latex, char)
            return re.sub(r"[{}]", "", text)

        if columnas is None:
            columnas = self.select_dtypes(include="object").columns.tolist()

        for col in columnas:
            if col in self.columns:
                self[col] = self[col].apply(latex_to_unicode)
    
    def tipificar_columnas(self) -> None:
        """ Convierte columnas comunes del modelo de artículos (.bib) a tipos más adecuados:
        - Year y Page Count como enteros.
        - Keywords como listas.
        """
        # Asegurar existencia antes de convertir
        if "Year" in self.columns:
            self["Year"] = pd.to_numeric(self["Year"], errors="coerce").astype("Int64")
        if "Page Count" in self.columns:
            self["Page Count"] = pd.to_numeric(self["Page Count"], errors="coerce").astype("Int64")
        if "Keywords" in self.columns:
            self["KeywordList"] = self["Keywords"].fillna("").apply(lambda x: [k.strip() for k in x.split(",") if k.strip()])



    def __str__(self) -> str:
        return f" Hoja: '{self.nombre}'\n{super().__str__()}"
