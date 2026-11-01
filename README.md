# 🌊 ONDAS, OLEAJE Y NIVEL DEL MAR

**Geomatics and Ocean Engineering Group** · E.T.S. Ingenieros de Caminos, Canales y Puertos · Universidad de Cantabria

**Profesores**

- Fernando J. Méndez · fernando.mendez@unican.es
- Pablo Alonso · pablo.alonsoalguacil@unican.es
- Laura Cagigal · laura.cagigal@unican.es
- Jared Ortiz-Angulo · jared.ortizangulo@unican.es

---

## ¿Qué vas a encontrar aquí?

Material práctico de la asignatura en forma de notebooks de Python (Jupyter). Con ellos aprenderás a:

- **Propagar el oleaje** desde aguas profundas hasta la costa con la ley de Snell (dispersión, refracción y asomeramiento).
- **Calcular dónde y cómo rompe el oleaje**, comparando distintos criterios de rotura (McCowan, Miche, Goda, Weggel, Kaminsky–Kraus).
- **Analizar el clima marítimo** de una playa real a partir de 40 años de datos horarios de oleaje y nivel del mar.
- **Calcular el flujo medio de energía** del oleaje en rotura y su variabilidad anual, mensual y estacional.

No necesitas instalar nada en tu ordenador: todo se ejecuta en el navegador con **GitHub Codespaces** (ver [Cómo ejecutar los notebooks](#-cómo-ejecutar-los-notebooks)).

---

## 📚 Notebooks

Están en la carpeta [`notebooks/`](notebooks) y conviene seguirlos **en orden**.

### Teoría con ejemplos

| # | Notebook | Qué aprenderás |
|---|---|---|
| 00 | [Snell: propagación entre dos puntos](notebooks/00_Snell_propagacion_entre_dos_puntos.ipynb) | Qué le pasa a una ola entre dos profundidades, paso a paso: longitud de onda, celeridad, dirección y altura. Uso de la función `snell_propagation`. |
| 01 | [Propagación con Snell y criterios de rotura](notebooks/01_Propagacion_Snell_didactica.ipynb) | Un tren de ondas sobre una playa recta: cómo refracta, asomera y rompe; comparación de criterios de rotura; crestas y rayos en planta y animación de la superficie libre. |

### Ejercicios

Cada ejercicio tiene dos versiones:

- **`_enunciado`**: el enunciado y las celdas vacías para que lo resuelvas tú. **Empieza siempre por aquí.**
- **`_solucion`**: el ejercicio resuelto paso a paso, para comprobar tus resultados.

| # | Ejercicio | Enunciado | Solución |
|---|---|---|---|
| 02 | Ejercicio 1 · Propagación desde indefinidas y rotura (Kaminsky–Kraus) | [enunciado](notebooks/02_Ejercicio1_Propagacion_y_rotura_enunciado.ipynb) | [solución](notebooks/02_Ejercicio1_Propagacion_y_rotura_solucion.ipynb) |
| 03 | Ejercicio 2 · Propagación inversa desde la rotura | [enunciado](notebooks/03_Ejercicio2_Propagacion_inversa_enunciado.ipynb) | [solución](notebooks/03_Ejercicio2_Propagacion_inversa_solucion.ipynb) |
| 04 | Ejercicio 3 · Profundidad de rotura con el criterio de Goda | [enunciado](notebooks/04_Ejercicio3_Rotura_Goda_enunciado.ipynb) | [solución](notebooks/04_Ejercicio3_Rotura_Goda_solucion.ipynb) |

### Práctica

| # | Notebook | Qué harás |
|---|---|---|
| 05 | [Clima marítimo, propagación y flujo de energía](notebooks/05_Clima_maritimo_y_propagacion.ipynb) | Elegir una estación, analizar sus series de nivel del mar y oleaje, propagar 40 años de oleaje hasta la costa y calcular el flujo medio de energía. |
| 05aux | [Pendientes globales](notebooks/05aux_Pendientes_globales.ipynb) | Consultar la pendiente aproximada de una playa a partir de sus coordenadas. |

> ✏️ En cada notebook, las celdas marcadas como **INPUTS** son las que puedes modificar (por ejemplo, la estación, la pendiente o la orientación de tu playa). El resto se ejecuta tal cual, de arriba a abajo.

---

## 🚀 Cómo ejecutar los notebooks

Usaremos **GitHub Codespaces**: un ordenador en la nube con todo ya instalado, que se abre en el navegador con VS Code.

### 1. Crea tu Codespace (solo la primera vez)

1. Inicia sesión en [GitHub](https://github.com) (si no tienes cuenta, créala; es gratuita).
2. En la página de este repositorio, pulsa el botón verde **`<> Code`** → pestaña **Codespaces** → **Create codespace on main**.
3. Espera a que termine de prepararse (la primera vez tarda unos minutos). Se abrirá VS Code en el navegador.

### 2. Abre y ejecuta un notebook

1. En el panel de la izquierda (explorador de archivos), entra en la carpeta `notebooks/` y abre el notebook que quieras.
2. Arriba a la derecha, pulsa **Select Kernel** y elige el entorno de Python que te ofrezca (*Python Environments* → el que aparece recomendado).
3. Ejecuta las celdas en orden con **Shift + Enter**, o todas a la vez con **Run All**.

### 3. Vuelve otro día

Tu Codespace se guarda con tus cambios. Para volver a él: **`<> Code`** → **Codespaces** → elige tu Codespace de la lista (no crees uno nuevo cada vez).

> ⚠️ **Importante**
> - GitHub ofrece un número limitado de **horas gratuitas al mes**. Cuando termines, **detén el Codespace**: menú ☰ (arriba a la izquierda) → *Codespaces: Stop Current Codespace*, o desde [github.com/codespaces](https://github.com/codespaces).
> - Los Codespaces que no se usan durante un tiempo se borran automáticamente. Si quieres conservar tu trabajo, **descarga tus notebooks** (clic derecho sobre el archivo → *Download*).

---

## 📁 Estructura del repositorio

```
Ondas/
├── notebooks/        # Notebooks de la asignatura (seguir en orden)
├── functions/        # Funciones de Python que usan los notebooks (propagación, rotura, gráficas…)
├── data/             # Datos de las estaciones (.nc) y pendientes globales (.csv)
├── images/           # Figuras de los notebooks
├── environment.yml   # Librerías necesarias
└── .devcontainer/    # Configuración del Codespace
```

---

## ❓ Problemas frecuentes

- **`ModuleNotFoundError: No module named 'functions'`**: abre los notebooks desde la carpeta `notebooks/` (no los muevas de sitio), ya que buscan las funciones en la carpeta superior.
- **Una celda da error porque falta una variable**: probablemente no has ejecutado las celdas anteriores. Usa **Run All** o ejecuta el notebook desde el principio.
- **El notebook va lento o se queda colgado**: reinicia el kernel (**Restart**) y vuelve a ejecutarlo.
