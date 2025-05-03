from excel_pandas.libro import LibroPandas
from excel_pandas.hoja import HojaPandas
import pandas as pd

# ╭─────────────────────────────────────────────╮
# │ Ejemplo 1: Cargar un Excel con múltiples hojas
# ╰─────────────────────────────────────────────╯

print("\n Ejemplo 1: Cargar Excel completo")
libro_excel = LibroPandas.desde_excel("/home/enrique/datos_acciones.xlsx")
print(libro_excel)

# Mostrar una hoja específica
print(libro_excel.obtener_hoja("V"))

# Mostrar resumen de todas las hojas
for nombre, hoja in libro_excel.hojas.items():
    print(f" Hoja: {nombre} — {len(hoja)} filas")

# ╭─────────────────────────────────────────────╮
# │ Ejemplo 2: Cargar solo ciertas hojas (1, 3-4)
# ╰─────────────────────────────────────────────╯

print("\n Ejemplo 2: Solo algunas hojas del Excel")
libro_rango = LibroPandas.desde_excel(
    "/home/enrique/datos_acciones.xlsx",
    hojas="1,3-4"
)
print(libro_rango)

# Mostrar resumen de las hojas seleccionadas
for nombre, hoja in libro_rango.hojas.items():
    print(f" Hoja: {nombre} — {len(hoja)} filas")

# ╭─────────────────────────────────────────────╮
# │ Ejemplo 3: Crear libro desde cero e importar CSV / Excel
# ╰─────────────────────────────────────────────╯

print("\n Ejemplo 3: Libro creado desde cero con archivos CSV y Excel")

libro_csv = LibroPandas("DatosImportados")

# Agregar hojas desde archivos CSV individuales
libro_csv.agregar_hoja_desde_archivo("/home/enrique/list_excels/insurance_claims.csv", sep=",")
libro_csv.agregar_hoja_desde_archivo("/home/enrique/list_excels/oral_cancer_prediction_dataset.csv", sep=",")
libro_csv.agregar_hoja_desde_archivo("/home/enrique/list_excels/education_career_success.csv", sep=",")

# Agregar todas las hojas de un Excel (como archivo fuente adicional)
libro_csv.agregar_hoja_desde_archivo("/home/enrique/datos_acciones.xlsx")

# Agregar solo hoja 2 con nombre personalizado
libro_csv.agregar_hoja_desde_archivo(
    "/home/enrique/datos_acciones.xlsx",
    hojas="2",
)

# Agregar solo hojas 1 y 4 del mismo archivo
libro_csv.agregar_hoja_desde_archivo(
    "/home/enrique/datos_acciones.xlsx",
    hojas="1,2"
)

# Mostrar resumen de todas las hojas importadas
print("\n Resumen final del libro")
for nombre, hoja in libro_csv.hojas.items():
    print(f" Hoja: {nombre} — {len(hoja)} filas")


# ╭─────────────────────────────────────────────╮
# │ Ejemplo 4: Guardar libro a  Excel
# ╰─────────────────────────────────────────────╯

libro_csv.guardar_como_excel("salida.xlsx")
