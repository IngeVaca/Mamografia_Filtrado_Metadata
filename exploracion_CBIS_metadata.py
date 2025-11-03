"""
Scritp elaborado con la intención de recorrer los metadatos que entrega
CBIS-DDSM, verificar cuales son válidos para el proyecto y crear un nuevo CSV en el que se guarde la información prefiltrada
está pensado para ejecutarse en Colab, adicional al final entrega un resumen de los resultados y datos.
"""

import pandas as pd
import os
from google.colab import files

archivos_requeridos = [
    "calc_case_description_train_set.csv",
    "calc_case_description_test_set.csv",
    "mass_case_description_train_set.csv",
    "mass_case_description_test_set.csv"
]

faltantes = [f for f in archivos_requeridos if not os.path.exists(f)]

if faltantes:
    print("No se encontraron todos los archivos requeridos. Sube los CSV a continuación:")
    uploaded = files.upload()
else:
    print("Archivos ya presentes en el entorno. Continuando con la lectura...")

dfs = []
for name in archivos_requeridos:
    if os.path.exists(name):
        print(f"Leyendo: {name}")
        df = pd.read_csv(name)
        df["fuente_datos"] = "CBIS-DDSM"
        dfs.append(df)
    else:
        print(f"Advertencia: el archivo {name} no está disponible.")

data = pd.concat(dfs, ignore_index=True)
print(f"\nTotal de registros combinados: {len(data)}")

data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")
data = data.loc[:, ~data.columns.duplicated()]  # eliminar duplicados de nombre
data = data.rename(columns={
    "assessment": "birads",
    "breast_density": "densidad",
    "pathology": "patologia",
    "image_file_path": "ruta_imagen",
    "patient_id": "paciente_id"
})

requisitos = ["birads", "densidad", "ruta_imagen", "paciente_id"]
existentes = [c for c in requisitos if c in data.columns]

if not existentes:
    raise ValueError("No se encontraron las columnas requeridas en los CSV. Verifica los nombres.")

data_filtrada = data.dropna(subset=existentes)

for c in existentes:
    if c in data_filtrada.columns:
        serie = data_filtrada[c]
        if isinstance(serie, pd.DataFrame):
            serie = serie.iloc[:, 0]
        data_filtrada = data_filtrada[serie.astype(str).str.strip() != ""]

print(f"\nFiltrado completado. Registros válidos: {len(data_filtrada)}")

data_filtrada = data_filtrada.rename(columns={
    "paciente_id": "id_paciente",
    "ruta_imagen": "ruta_imagen",
    "densidad": "densidad_mamaria",
    "patologia": "tipo_lesion",
    "abnormality_id": "id_anormalidad",
    "abnormality_type": "tipo_anormalidad",
    "birads": "categoria_birads"
})

mapa_densidad = {1: "A", 2: "B", 3: "C", 4: "D"}
data_filtrada["densidad_mamaria"] = pd.to_numeric(
    data_filtrada["densidad_mamaria"], errors="coerce"
).map(mapa_densidad)

if "tipo_lesion" in data_filtrada.columns:
    data_filtrada["tipo_lesion"] = data_filtrada["tipo_lesion"].replace({
        "BENIGN": "Benigna",
        "MALIGNANT": "Maligna"
    })


columnas_finales = [
    "id_paciente",
    "ruta_imagen",
    "densidad_mamaria",
    "tipo_lesion",
    "id_anormalidad",
    "tipo_anormalidad",
    "categoria_birads",
    "fuente_datos"
]
columnas_existentes = [c for c in columnas_finales if c in data_filtrada.columns]
resultado = data_filtrada[columnas_existentes]

nombre_salida = "metadata_filtrado_CBIS_es.csv"
resultado.to_csv(nombre_salida, index=False)

print(f"\nArchivo final guardado como: {nombre_salida}")
print(f"Total de registros antes: {len(data)} → después del filtrado: {len(resultado)}")

from google.colab import files
files.download(nombre_salida)

archivo = "metadata_filtrado_CBIS_es.csv"
df = pd.read_csv(archivo)

print(f"\nArchivo cargado: {archivo}")
print(f"Total de registros: {len(df)}")
print(f"Total de columnas: {len(df.columns)}")

print("\n--- Columnas disponibles ---")
for i, col in enumerate(df.columns, start=1):
    print(f"{i}. {col}")
print("\n--- Tipos de datos ---")
print(df.dtypes)
print("\n--- Valores faltantes por columna ---")
print(df.isnull().sum())
if "categoria_birads" in df.columns:
    print("\n--- Distribución de categoría BI-RADS ---")
    print(df["categoria_birads"].value_counts(dropna=False))

if "densidad_mamaria" in df.columns:
    print("\n--- Distribución de densidad mamaria (A–D) ---")
    print(df["densidad_mamaria"].value_counts(dropna=False))

if "tipo_lesion" in df.columns:
    print("\n--- Distribución de tipo de lesión ---")
    print(df["tipo_lesion"].value_counts(dropna=False))

print("\n--- Estadísticas descriptivas (columnas numéricas) ---")
print(df.describe())
print("\n--- Resumen general ---")
resumen = {
    "Total de registros": len(df),
    "Pacientes únicos": df["id_paciente"].nunique() if "id_paciente" in df.columns else "No disponible",
    "Tipos de lesión": list(df["tipo_lesion"].unique()) if "tipo_lesion" in df.columns else "No disponible",
    "Rango de BI-RADS": (
        f"{df['categoria_birads'].min()}–{df['categoria_birads'].max()}"
        if "categoria_birads" in df.columns else "No disponible"
    ),
    "Densidades presentes": list(df["densidad_mamaria"].dropna().unique()) if "densidad_mamaria" in df.columns else "No disponible"
}
for k, v in resumen.items():
    print(f"{k}: {v}")
