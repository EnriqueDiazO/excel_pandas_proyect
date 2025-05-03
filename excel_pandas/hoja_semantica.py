from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from .hoja import HojaPandas

class HojaSemantica(HojaPandas):
    def __init__(self, data=None, nombre="Semantica", **kwargs):
        super().__init__(data, nombre=nombre, **kwargs)
        self.vectorizer = None
        self.model = None
        self.X_tfidf = None
        self.clusters = None
        self.pca_coords = None

    def analizar_texto(self, columna="Abstract", n_clusters=4, max_df=0.8, min_df=3, stop_words="english") -> None:
        """
        Ejecuta análisis semántico: TF-IDF + KMeans + PCA.

        Parámetros:
        -----------
        columna : str
            Columna de texto a analizar.
        n_clusters : int
            Número de clusters KMeans.
        """
        textos = self[columna].dropna().astype(str)
        self.vectorizer = TfidfVectorizer(stop_words=stop_words, max_df=max_df, min_df=min_df)
        self.X_tfidf = self.vectorizer.fit_transform(textos)

        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        self.clusters = self.model.fit_predict(self.X_tfidf)

        # Guardar resultados
        self.loc[textos.index, "Cluster"] = self.clusters

        pca = PCA(n_components=2)
        self.pca_coords = pca.fit_transform(self.X_tfidf.toarray())
        self.loc[textos.index, "PCA1"] = self.pca_coords[:, 0]
        self.loc[textos.index, "PCA2"] = self.pca_coords[:, 1]

    def graficar_clusters(self, etiqueta="ID", guardar="clusters.png") -> None:
        """
        Muestra y guarda gráfico PCA con clusters.

        Parámetros:
        -----------
        etiqueta : str
            Columna a mostrar como etiqueta en el gráfico.
        guardar : str
            Ruta para guardar la imagen.
        """
        if self.pca_coords is None or self.clusters is None:
            raise ValueError("Primero ejecuta `analizar_texto(...)`.")

        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(self["PCA1"], self["PCA2"], c=self["Cluster"], cmap="tab10")

        for i, txt in enumerate(self[etiqueta]):
            plt.annotate(txt, (self["PCA1"].iloc[i], self["PCA2"].iloc[i]), fontsize=8, color="black", alpha=0.8)

        plt.title("Agrupación de documentos (TF-IDF + KMeans)")
        plt.xlabel("Componente Principal 1")
        plt.ylabel("Componente Principal 2")
        plt.grid(True)
        plt.legend(*scatter.legend_elements(), title="Cluster")
        plt.tight_layout()
        plt.savefig(guardar)
        plt.show()

    def nube_palabras(self, columna="Abstract", guardar="wordcloud.png") -> None:
        """
        Genera y guarda una nube de palabras.

        Parámetros:
        -----------
        columna : str
            Columna de texto base.
        guardar : str
            Ruta de imagen para guardar.
        """
        textos = " ".join(self[columna].dropna().astype(str))
        nube = WordCloud(width=1000, height=600, background_color="white", colormap="viridis").generate(textos)
        plt.figure(figsize=(12, 6))
        plt.imshow(nube, interpolation="bilinear")
        plt.axis("off")
        plt.title(f"Nube de palabras de columna '{columna}'")
        plt.tight_layout()
        plt.savefig(guardar)
        plt.show()
    
    def graficar_articulos_por_anio(self, columna="Year") -> None:
        """
        -> Gráfico de barras con el número de artículos por año.
        Parámetros:
        -----------
        columna : str
            Columna de año.
        """
        self[columna] = pd.to_numeric(self[columna], errors="coerce")
        conteo = self[columna].dropna().astype(int).value_counts().sort_index()
        conteo.plot(kind="bar", figsize=(10, 4))
        plt.title("Número de artículos por año")
        plt.xlabel("Año")
        plt.ylabel("Cantidad")
        plt.grid(axis="y")
        plt.tight_layout()
        plt.show()
    
    def graficar_autores_frecuentes(self, columna="Author(s)", top_n=3) -> None:
        """
        -> Muestra autores más frecuentes en los artículos.
        Parámetros:
        -----------
        columna : str
            Columna de Autor.
        top_n: int
            Los primeros top_n autores.
        """
        todos = ", ".join(self[columna].dropna().astype(str).tolist()).split(" and ")
        conteo = Counter(a.strip() for a in todos if a.strip())
        mas_comunes = dict(conteo.most_common(top_n))

        pd.Series(mas_comunes).plot(kind="barh", figsize=(8, 6))
        plt.title("Autores más frecuentes")
        plt.xlabel("Número de artículos")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()
    
    def graficar_frecuencia_keywords(self, columna="Keywords") -> None:
        """
        -> Muestra frecuencia de las palabras clave más comunes.
        """
        todos = ", ".join(self[columna].dropna().astype(str).tolist()).split(",")
        conteo = Counter(k.strip() for k in todos if k.strip())
        top_keywords = dict(conteo.most_common(20))

        pd.Series(top_keywords).plot(kind="barh", figsize=(10, 6), color="skyblue")
        plt.title("Palabras clave más frecuentes")
        plt.xlabel("Frecuencia")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()


