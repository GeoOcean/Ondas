# 🌊 ONDAS, OLEAJE Y NIVEL DEL MAR

Geomatics and Ocean Engineering Group · Universidad de Cantabria

Fernando J. Méndez (fernando.mendez@unican.es)\
Laura Cagigal (laura.cagigal@unican.es)\
Jared Ortiz-Angulo (jared.ortizangulo@unican.es)

## Notebooks

| Notebook | Contenido |
|---|---|
| [`00_Snell_propagacion_entre_dos_puntos.ipynb`](notebooks/00_Snell_propagacion_entre_dos_puntos.ipynb) | Introducción: propagación de un oleaje monocromático entre dos profundidades paso a paso (dispersión, Snell, asomeramiento, refracción) y uso de la función `snell_propagation`, incluida la propagación hacia y desde indefinidas. |
| [`01_Propagacion_Snell_didactica.ipynb`](notebooks/01_Propagacion_Snell_didactica.ipynb) | Ejemplo didáctico: propagación con la ley de Snell de un oleaje monocromático sobre una playa recta orientada al norte, con las mismas funciones del curso (dispersión, refracción, asomeramiento), comparación de criterios de rotura (McCowan, Miche, Goda, Weggel, Kaminsky–Kraus), crestas y rayos en planta y animación de la superficie libre. |
| [`02_Ejercicio1_Propagacion_y_rotura_enunciado.ipynb`](notebooks/02_Ejercicio1_Propagacion_y_rotura_enunciado.ipynb) | Ejercicio 1 (enunciado): propagación desde indefinidas a profundidades intermedias y someras, y rotura con el criterio de Kaminsky–Kraus. |
| [`02_Ejercicio1_Propagacion_y_rotura_solucion.ipynb`](notebooks/02_Ejercicio1_Propagacion_y_rotura_solucion.ipynb) | Ejercicio 1 (solución): iteración a mano y dispersión completa. |
| [`03_Ejercicio2_Propagacion_inversa_enunciado.ipynb`](notebooks/03_Ejercicio2_Propagacion_inversa_enunciado.ipynb) | Ejercicio 2 (enunciado): propagación inversa desde el punto de rotura hasta indefinidas y una batimétrica intermedia. |
| [`03_Ejercicio2_Propagacion_inversa_solucion.ipynb`](notebooks/03_Ejercicio2_Propagacion_inversa_solucion.ipynb) | Ejercicio 2 (solución). |
| [`04_Ejercicio3_Rotura_Goda_enunciado.ipynb`](notebooks/04_Ejercicio3_Rotura_Goda_enunciado.ipynb) | Ejercicio 3 (enunciado): profundidad de rotura despejada del criterio de Goda y propagación inversa a indefinidas. |
| [`04_Ejercicio3_Rotura_Goda_solucion.ipynb`](notebooks/04_Ejercicio3_Rotura_Goda_solucion.ipynb) | Ejercicio 3 (solución). |
| [`05_Clima_maritimo_y_propagacion.ipynb`](notebooks/05_Clima_maritimo_y_propagacion.ipynb) | Selección de estación, análisis de nivel del mar y oleaje, propagación con la ley de Snell (profundidad objetivo y rotura), comparación offshore–nearshore y flujo medio de energía (total, anual, mensual y estacional). |
| [`05aux_Pendientes_globales.ipynb`](notebooks/05aux_Pendientes_globales.ipynb) | Notebook auxiliar del 05: mapa de la base de datos global de pendientes nearshore y búsqueda de la pendiente más cercana a una playa. |

### Ejercicios adicionales (`new_exercises/`)

| Notebook | Contenido |
|---|---|
| [`Ejercicio4_Boya_y_rotura.ipynb`](new_exercises/Ejercicio4_Boya_y_rotura.ipynb) | Propagación desde una boya en h = 20 m a indefinidas y rotura con McCowan y Goda. |
| [`Ejercicio5_Direcciones_y_flujo.ipynb`](new_exercises/Ejercicio5_Direcciones_y_flujo.ipynb) | Direcciones absolutas con la orientación de la playa, rotura con Miche y flujo de energía en rotura. |
| [`Ejercicio6_Comparacion_criterios_rotura.ipynb`](new_exercises/Ejercicio6_Comparacion_criterios_rotura.ipynb) | Comparación de los criterios de McCowan, Kaminsky–Kraus y Goda e influencia de la pendiente. |

## Estructura del repositorio

```
Ondas/
├── notebooks/        # Notebooks de la asignatura (ejecutar en orden)
├── new_exercises/    # Ejercicios adicionales (solo enunciado)
├── functions/        # Funciones Python usadas por los notebooks
├── data/             # Datos de las estaciones (.nc) y pendientes globales (.csv)
├── images/           # Figuras usadas en los notebooks
├── environment.yml   # Entorno conda
└── .devcontainer/    # Configuración para VS Code / Codespaces
```

## Instalación

- Descarga el repositorio
- Abre Anaconda Prompt (o una terminal)
- Ve a la carpeta descargada: `cd <ruta>/Ondas`
- Crea el entorno conda a partir de `environment.yml`:
  - `conda env create -f environment.yml`
- Activa el entorno:
  - `conda activate ondas2`
- Lanza Jupyter Lab y abre los notebooks de la carpeta `notebooks/`:
  - `jupyter lab`
