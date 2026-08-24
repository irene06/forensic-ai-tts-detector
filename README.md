# 🛡️ Forensic AI & TTS Detector

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Librosa](https://img.shields.io/badge/Librosa-Audio%20Analysis-orange.svg)](https://librosa.org/)
[![Status](https://img.shields.io/badge/Status-En%20Desarrollo%20%2F%20Fase%20Beta-yellow.svg)](#)

Aplicación web interactiva para el análisis acústico-forense y la detección preliminar de muestras de voz sintética (Text-to-Speech / Clonación con Inteligencia Artificial).

El sistema procesa la señal de audio en busca de discontinuidades espectrales, anomalías en la frecuencia fundamental ($F_0$), micro-variaciones timbrales (MFCC) y artefactos característicos de vocoders neurales.

---

## 🚧 Estado del Proyecto y Mejoras en Proceso (Roadmap)

Este proyecto se encuentra actualmente en **fase de desarrollo y calibración activa (Beta)**.

* **Fase Actual (V1 - Heurística basada en DSP):** Implementación de análisis acústico estático con Librosa (Pitch, MFCC, RMS, Energía Espectral).
* **Calibración en Proceso:** Se está trabajando en el ajuste de umbrales para reducir los **falsos positivos** generados por voces humanas monótonas, compresión de micrófonos integrados o algoritmos de cancelación de ruido.
* **Próximas Actualizaciones (V2 - Aprendizaje Automático):**
  * [ ] Entrenamiento e integración de un clasificador de Machine Learning / Deep Learning (ej. *ASVspoof / AASIST*).
  * [ ] Soporte para análisis batch de múltiples archivos de audio.
  * [ ] Comparativa directa entre perfiles de audio humano y sintético en la interfaz.

---

## 🚀 Características Principales

* **Carga de Archivos Flexible:** Soporte para formatos `.wav` y `.mp3` con procesamiento del fragmento de análisis.
* **Análisis Forense en Tiempo Real:**
  * **Pitch ($F_0$):** Medición del contorno de entonación y variabilidad espectral en Hz.
  * **Varianza MFCC:** Análisis tímbrico para evaluar la homogeneidad espectral del audio.
  * **Energía de Altas Frecuencias:** Evaluación del rango espectral ($>8\text{ kHz}$) para detectar artefactos de síntesis.
  * **Variabilidad RMS:** Chequeo de homogeneidad en la dinámica de volumen.
* **Integridad de Datos:** Generación automática del hash **SHA-256** del archivo analizado.
* **Visualización de Datos:** Espectrograma STFT (Short-Time Fourier Transform) y curvas del contorno de entonación.
* **Exportación de Informes:** Descarga del reporte estructurado en **JSON** y **PDF**.

---

## 🛠️ Requisitos del Sistema

* Python 3.9 o superior
* `ffmpeg` instalado en el sistema

---

## 📦 Instalación

1. **Clonar el repositorio:**  
   `git clone https://github.com/irene06/forensic-ai-tts-detector.git`  
   `cd forensic-ai-tts-detector`

2. **Crear y activar entorno virtual:**  
   `python -m venv venv`  
   `venv\Scripts\activate`

3. **Instalar dependencias:**  
   `pip install streamlit librosa numpy matplotlib reportlab`

---

## ⚡ Uso

Inicia la aplicación ejecutando el siguiente comando en tu terminal:

`streamlit run app.py`

---

## 📁 Estructura del Proyecto

* **app.py** — Interfaz de usuario con Streamlit
* **analizador.py** — Algoritmo forense y generación de reportes
* **README.md** — Documentación del proyecto

---

## ⚠️ Exención de Responsabilidad

Prototipo educativo y de demostración analítica basado en procesamiento de señales estático. No debe utilizarse como evidencia para peritajes judiciales formales.
