# Exploración y filtrado de metadatos de mamografías

**Autor:** Jhon Jaime Vaca Hincapié  
**Correo:** jjvacah@libertadores.edu.co  
**ORCID:** [0009-0007-7994-3130](https://orcid.org/0009-0007-7994-3130)  
**Programa:** Maestría en Ingeniería – Énfasis en Ingeniería Automática  
**Institución:** Fundación Universitaria Los Libertadores  
**Año:** 2025  


## Descripción del proyecto

Este repositorio contiene los scripts utilizados para la **exploración, validación y filtrado inicial de metadatos** de tres bases de datos públicas de mamografías:

1. **CBIS-DDSM** – Cancer Imaging Archive (TCIA)  
2. **INbreast** – Breast Cancer Digital Repository (Hospital de São João, Portugal)  
3. **VINDr-Mammo (DrMammo)** – VinBigData (Vietnam)

El objetivo de esta etapa es unificar los metadatos relevantes de cada base para construir un **dataset maestro estandarizado**, que sirva como punto de partida para la conversión de imágenes médicas en formato **DICOM → TIFF**, cumpliendo con los principios **FAIR (Findable, Accessible, Interoperable, Reusable)**.

El filtrado se centra en los parámetros más relevantes para el diagnóstico automatizado:  
**densidad mamaria (A–D)** y **categoría BI-RADS (0–6)**.  
De esta forma, se garantiza la compatibilidad entre datasets y la calidad de los registros que se utilizarán en el modelo de clasificación.

---

## Licencia

Este trabajo y los scripts contenidos en este repositorio están bajo licencia:

**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**  
[https://creativecommons.org/licenses/by-nc/4.0/](https://creativecommons.org/licenses/by-nc/4.0/)

Esto significa que:
- Se permite **copiar, redistribuir y adaptar** el contenido.  
- Se debe otorgar **crédito adecuado** al autor.  
- **No está permitido el uso comercial** del material.

---


## Descripción general

Este repositorio documenta el proceso de **exploración, análisis y filtrado inicial de metadatos** de tres bases de datos públicas de mamografías digitales:

1. **INbreast** (Universidad de Oporto)  
2. **CBIS-DDSM** (The Cancer Imaging Archive - TCIA)  
3. **VINDr-Mammo (DrMammo)** (Vietnam National Digital Radiology Dataset)

El propósito de esta etapa es generar una base de metadatos unificada y limpia que permita posteriormente **la conversión y organización de las imágenes DICOM** en un dataset maestro estructurado por **densidad mamaria (A–D)** y **categoría BI-RADS (0–6)**.


## Objetivos

1. Analizar la estructura y los campos disponibles en los metadatos originales de cada dataset.  
2. Filtrar únicamente los registros relevantes para la investigación.  
3. Unificar los formatos y nombres de columnas entre las tres fuentes.  
4. Exportar tres CSV filtrados (uno por dataset) y un CSV final unificado.


## 1. Fuentes de datos y descarga

| Dataset | Fuente | Formato | Enlace oficial |
|----------|---------|----------|----------------|
| **INbreast** | Breast Research Group, University of Porto | CSV + DICOM | [https://biokeanos.com/source/INbreast](https://biokeanos.com/source/INbreast) |
| **CBIS-DDSM** | The Cancer Imaging Archive (TCIA) | XML + CSV + DICOM | [https://www.cancerimagingarchive.net/collection/cbis-ddsm/](https://www.cancerimagingarchive.net/collection/cbis-ddsm/) |
| **VINDr-Mammo (DrMammo)** | Vietnam National Digital Radiology Dataset | JSON + CSV + DICOM | [https://vindr.ai/datasets/mammo](https://vindr.ai/datasets/mammo) |

Todos los archivos fueron convertidos a formato **CSV** y analizados localmente usando Python (pandas).


## 2. Criterios de filtrado aplicados

Se eliminaron registros duplicados, inconsistentes o con valores ausentes en los siguientes campos críticos:

| Campo estándar | Descripción | Condición mínima |
|----------------|-------------|------------------|
| `densidad_mamaria` | Nivel de densidad (A–D) | No nulo |
| `categoria_birads` | Valor numérico 0–6 | No nulo |
| `lateralidad` | Lado de la mama (`Izquierda` o `Derecha`) | No nulo |
| `vista` | Proyección (`CC` o `MLO`) | No nulo |

Los campos se homogenizaron en nombres y formato antes de la unificación.

## 3. Scripts incluidos y parámetros estandarizados

A continuación se describen los scripts de exploración y filtrado de metadatos aplicados a cada una de las tres bases de datos, junto con las variables que fueron seleccionadas para conservar en el proceso de integración.


### exploracion_INbreast_metadata.py

Este script explora el archivo `INbreast.csv` y valida los campos correspondientes a **densidad mamaria (ACR)** y **categoría BI-RADS**.  
Se normalizan los nombres de las columnas y se genera un nuevo CSV con los siguientes campos:

| Campo | Descripción | Fuente original |
|--------|--------------|----------------|
| `id_paciente` | Identificador anónimo del paciente | Patient ID |
| `id_imagen` | Nombre del archivo de imagen | File Name |
| `lateralidad` | Lado de la mama (`L` o `R`) | Laterality |
| `vista` | Proyección de la imagen (`CC` o `MLO`) | View |
| `densidad_mamaria` | Valor ACR (1–4) convertido a letras (A–D) | ACR |
| `categoria_birads` | Clasificación BI-RADS numérica (1–5) | Bi-Rads |
| `fuente_datos` | Nombre de la base de datos | INbreast |

En este dataset la densidad no se encuentra directamente etiquetada como A–D, sino como valores **numéricos del 1 al 4**, equivalentes a:

| Código original | Densidad final |
|-----------------|----------------|
| 1 | A |
| 2 | B |
| 3 | C |
| 4 | D |


### exploracion_CBIS_metadata.py

El script lee los metadatos del conjunto **CBIS-DDSM**, seleccionando únicamente las imágenes que tienen registros completos de densidad, tipo de lesión y categoría BI-RADS.  
Los campos conservados fueron:

| Campo | Descripción | Fuente original |
|--------|--------------|----------------|
| `id_paciente` | Identificador anónimo del paciente | Patient ID |
| `ruta_imagen` | Ruta relativa al archivo DICOM | Image Path |
| `densidad_mamaria` | Nivel de densidad (A–D) | Breast Density |
| `tipo_lesion` | Clasificación general (Maligna, Benigna, etc.) | Pathology |
| `id_anormalidad` | Identificador del hallazgo | Abnormality ID |
| `tipo_anormalidad` | Tipo de anormalidad (masa, calcificación) | Abnormality Type |
| `categoria_birads` | Categoría BI-RADS (1–5) | Assessment |
| `fuente_datos` | Nombre del dataset | CBIS-DDSM |

En este caso, la densidad mamaria ya viene expresada como letras **A–D** en los metadatos originales.


### exploracion_VINDr_metadata.py

Este script procesa los metadatos de **VINDr-Mammo (DrMammo)**, normalizando la codificación de texto y los formatos de los campos.  
Las variables seleccionadas fueron:

| Campo | Descripción | Fuente original |
|--------|--------------|----------------|
| `id_estudio` | Identificador del estudio | study_id |
| `id_imagen` | Identificador único de la imagen | image_id |
| `lateralidad` | Lado de la mama (`Izquierda`, `Derecha`) | laterality |
| `vista` | Proyección de la imagen (`Craneocaudal`, `Oblicua mediolateral`) | view_position |
| `densidad_mamaria` | Valor original en texto (e.g. "DENSITY C") simplificado a `C` | breast_density |
| `categoria_birads` | Valor original en texto (e.g. "BI-RADS 3") convertido a número `3` | breast_birads |
| `fuente_datos` | Nombre de la base de datos | VINDr-Mammo |

**Nota importante:**  
En esta base, los campos de densidad y BI-RADS vienen como cadenas de texto completas (`"DENSITY C"`, `"BI-RADS 2"`).  
Durante el filtrado, se extrajo únicamente el carácter representativo (A–D o el número de 0–6) para estandarizarlo con los otros datasets.

### combinacion_filtered_metadata.py

Finalmente, este script une los tres CSV filtrados en un solo archivo:

metadata_unificada_CBIS_VINDr_INbreast.csv


La estructura final de columnas es:

| Campo | Descripción | Presente en |
|--------|--------------|-------------|
| `id_registro` | ID único (paciente o estudio) | Todos |
| `imagen_id` | Nombre o hash de la imagen | Todos |
| `lateralidad` | Lado de la mama | INbreast, VINDr |
| `vista` | Tipo de proyección | INbreast, VINDr |
| `densidad_mamaria` | Densidad estandarizada (A–D) | Todos |
| `categoria_birads` | BI-RADS numérico (0–6) | Todos |
| `tipo_lesion` | (solo CBIS) | CBIS-DDSM |
| `tipo_anormalidad` | (solo CBIS) | CBIS-DDSM |
| `fuente_datos` | Nombre del dataset original | Todos |

La salida de este script es el **dataset maestro de metadatos**, usado posteriormente para buscar, convertir y organizar las imágenes DICOM en formato TIFF.


**Resumen de equivalencias aplicadas durante la estandarización:**

| Atributo | INbreast | CBIS-DDSM | VINDr-Mammo | Estandarización final |
|-----------|-----------|------------|---------------|------------------------|
| Densidad mamaria | Numérica (1–4) | Letras (A–D) | Texto ("DENSITY X") | Letras (A–D) |
| Categoría BI-RADS | Numérica (1–5) | Numérica (1–5) | Texto ("BI-RADS X") | Numérica (0–6) |
| Lateralidad | R/L | variable | Left/Right | Izquierda/Derecha |
| Vista | CC/MLO | variable | CC/MLO | Craneocaudal / Oblicua mediolateral |


Este proceso permitió garantizar que las tres fuentes tuvieran una estructura uniforme de metadatos, condición necesaria antes de pasar a la fase de **conversión DICOM–TIFF y organización estructurada por categorías BI-RADS y densidad mamaria.**


