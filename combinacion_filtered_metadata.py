"""
Scritp diseñado para mezclar los 3 CSV filtrados de CBIS, Dr Mammo e INbreast, los archivos estan públicos en mi drive personal, al finalizar entrega un análisis
exploratorio de los datos útiles, adicional permite descargar las gráficas en alta calidad para su uso en documentos formales
"""




# Librerías requeridas
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import files

# Traer los CSV desde Drive
archivos_drive = {
    "CBIS": "https://drive.google.com/uc?id=1SEo3k-KoH-4K3V7BWDlKoeunm1mIibz7",
    "VINDr": "https://drive.google.com/uc?id=1gLoNbqzW8nijwOJHJN-UYSLTLTdPqa-M",
    "INbreast": "https://drive.google.com/uc?id=1wKQfbU3OZZloOtjz3ecExAVc17DtsUbD"
}

datasets = {}
for nombre, url in archivos_drive.items():
    nombre_local = f"metadata_filtrado_{nombre}.csv"
    if not os.path.exists(nombre_local):
        print(f"Descargando {nombre} desde Drive...")
        datasets[nombre] = pd.read_csv(url)
        datasets[nombre].to_csv(nombre_local, index=False)
        print(f"{nombre} descargado y guardado como {nombre_local} → {len(datasets[nombre])} filas")
    else:
        print(f"Archivo {nombre_local} ya existe. Cargando localmente...")
        datasets[nombre] = pd.read_csv(nombre_local)
        print(f"{nombre_local} cargado → {len(datasets[nombre])} filas")

# Recorrer los archivos y crear un solo CSV con la combinación de los 3

df_total = pd.concat(datasets.values(), ignore_index=True)
nombre_salida = "metadata_unificada_CBIS_VINDr_INbreast.csv"
df_total.to_csv(nombre_salida, index=False)
print(f"\nArchivo unificado guardado como: {nombre_salida}")
print(f"Total de registros combinados: {len(df_total)}")
print(f"Total de columnas: {len(df_total.columns)}")
print(f"Columnas: {list(df_total.columns)}")

# Describir los valores

print("\n--- Distribución por fuente de datos ---")
print(df_total["fuente_datos"].value_counts(), "\n")

print("--- Distribución de categoría BI-RADS ---")
print(df_total["categoria_birads"].value_counts().sort_index(), "\n")

print("--- Distribución de densidad mamaria ---")
print(df_total["densidad_mamaria"].value_counts().sort_index(), "\n")

if "lateralidad" in df_total.columns:
    print("--- Distribución por lateralidad ---")
    print(df_total["lateralidad"].value_counts(), "\n")

if "vista" in df_total.columns:
    print("--- Distribución por vista ---")
    print(df_total["vista"].value_counts(), "\n")

plt.figure(figsize=(10, 24))
plt.suptitle("Distribuciones Globales — Dataset Unificado", fontsize=18, fontweight='bold')

# Indicar la fuente de datos
plt.subplot(5,1,1)
df_total["fuente_datos"].value_counts().plot(kind="bar", color='steelblue')
plt.title("Distribución por Fuente de Datos")
plt.xlabel("Fuente")
plt.ylabel("Cantidad de registros")
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Indicar la densidad mamaria
plt.subplot(5,1,2)
df_total["densidad_mamaria"].value_counts().sort_index().plot(kind="bar", color='indianred')
plt.title("Distribución de Densidades Mamarias (A–D)")
plt.xlabel("Densidad Mamaria")
plt.ylabel("Cantidad")
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Indicar la categoria de BI-RADS
plt.subplot(5,1,3)
df_total["categoria_birads"].value_counts().sort_index().plot(kind="bar", color='seagreen')
plt.title("Distribución de Categorías BI-RADS")
plt.xlabel("Categoría BI-RADS")
plt.ylabel("Cantidad")
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Fuente × BI-RADS
plt.subplot(5,1,4)
pd.crosstab(df_total["fuente_datos"], df_total["categoria_birads"]).plot(
    kind='bar', stacked=True, ax=plt.gca(), colormap='Set2'
)
plt.title("Comparativa por Fuente y Categoría BI-RADS")
plt.xlabel("Fuente de Datos")
plt.ylabel("Cantidad")
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Mapa de calor BI-RADS × Densidad
plt.subplot(5,1,5)
ct = pd.crosstab(df_total["categoria_birads"], df_total["densidad_mamaria"])
sns.heatmap(ct, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Mapa de Calor: BI-RADS vs Densidad Mamaria")
plt.xlabel("Densidad Mamaria")
plt.ylabel("Categoría BI-RADS")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Descargar el CSV unido
files.download(nombre_salida)

# 7. Estádisticas generales
print("\n--- Resumen Global ---")
print(f"Fuentes incluidas: {list(datasets.keys())}")
print(f"Total de registros combinados: {len(df_total)}")
print(f"Rango de BI-RADS: {df_total['categoria_birads'].min()} – {df_total['categoria_birads'].max()}")
print(f"Densidades presentes: {sorted(df_total['densidad_mamaria'].dropna().unique())}")



#-------------------------------Opcional: descargar gráficas ------------------------------


# Configuración general de alta resolución

dpi = 300  # alta resolución
figsize = (12, 8)

# Lista de gráficos a generar
graficos = [
    {
        "nombre": "grafico_fuente_datos.png",
        "titulo": "Distribución por Fuente de Datos",
        "plot_func": lambda: df_total["fuente_datos"].value_counts().plot(kind="bar", color='steelblue')
    },
    {
        "nombre": "grafico_densidad.png",
        "titulo": "Distribución de Densidades Mamarias (A–D)",
        "plot_func": lambda: df_total["densidad_mamaria"].value_counts().sort_index().plot(kind="bar", color='indianred')
    },
    {
        "nombre": "grafico_birads.png",
        "titulo": "Distribución de Categorías BI-RADS",
        "plot_func": lambda: df_total["categoria_birads"].value_counts().sort_index().plot(kind="bar", color='seagreen')
    },
    {
        "nombre": "grafico_fuente_birads.png",
        "titulo": "Comparativa Fuente × BI-RADS",
        "plot_func": lambda: pd.crosstab(df_total["fuente_datos"], df_total["categoria_birads"]).plot(
            kind='bar', stacked=True, colormap='Set2', ax=plt.gca()
        )
    },
    {
        "nombre": "grafico_mapa_calor.png",
        "titulo": "Mapa de Calor: BI-RADS vs Densidad Mamaria",
        "plot_func": lambda: sns.heatmap(
            pd.crosstab(df_total["categoria_birads"], df_total["densidad_mamaria"]),
            annot=True, fmt="d", cmap="YlGnBu"
        )
    }
]

# Generar y descargar cada gráfico
for g in graficos:
    plt.figure(figsize=figsize, dpi=dpi)
    g["plot_func"]()
    plt.title(g["titulo"], fontsize=16)
    plt.xlabel("")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(g["nombre"], dpi=dpi)
    plt.close()
    files.download(g["nombre"])

print("Todos los gráficos se han generado en alta calidad y se han descargado automáticamente.")
