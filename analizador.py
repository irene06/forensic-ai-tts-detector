import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Tuple
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def calcular_hash(ruta_archivo: Path) -> str:
    sha256 = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def analizar_audio(ruta_audio: Path) -> Tuple[Dict[str, Any], np.ndarray, float, Any]:
    y, sr = librosa.load(ruta_audio, sr=None, duration=30.0)
    duracion = float(librosa.get_duration(y=y, sr=sr))
    
    # 1. Extracción de Pitch (F0)
    f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    f0_clean = f0[~np.isnan(f0)] if f0 is not None else np.array([])
    std_f0 = float(np.std(f0_clean)) if len(f0_clean) > 0 else 0.0

    # 2. Análisis del Espectro y Estructura Armónica
    S = np.abs(librosa.stft(y))
    
    # Inconsistencia en altas frecuencias (>8kHz / vocoders neurales)
    high_freq_energy = float(np.mean(S[int(S.shape[0]*0.7):, :]))
    
    # Varianza de los coeficientes MFCC (Las IA suelen tener una varianza inter-frame muy baja/suave)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_var = float(np.mean(np.var(mfccs, axis=1)))

    # Flatness espectral y varianza RMS
    flatness = float(np.mean(librosa.feature.spectral_flatness(y=y)))
    rms = librosa.feature.rms(y=y)
    std_rms = float(np.std(rms))

    # 3. Detección por Score Forense Sensible
    score_sintetico = 0
    motivos = []

    # Umbral de pitch elevado para capturar TTS expresivo pero sintético
    if std_f0 < 40.0:
        score_sintetico += 1.5
        motivos.append("Pitch / F0 con modulación sintética o excesivamente estructurada")

    # Si la varianza MFCC es baja, significa que el timbre es "demasiado perfecto"
    if mfcc_var < 150.0:
        score_sintetico += 1.5
        motivos.append("Varianza timbral reducida (patrón de generación neural homogéneo)")

    if high_freq_energy < 0.005:
        score_sintetico += 1.0
        motivos.append("Atenuación o distorsión de fase en altas frecuencias (>8kHz)")

    if std_rms < 0.05:
        score_sintetico += 1.0
        motivos.append("Dinámica de volumen/rms inusualmente uniforme")

    # Evaluación: Basta con sumar 1.5 puntos para marcarlo como sospechoso
    es_sintetico = score_sintetico >= 1.5
    hash_val = calcular_hash(ruta_audio)

    reporte = {
        "analisis_forense": {
            "integridad": {"algoritmo": "SHA-256", "hash": hash_val},
            "propiedades": {"duracion_analizada_seg": round(duracion, 2), "sample_rate_hz": sr, "canales": 1 if y.ndim == 1 else y.shape[0]},
            "diagnostico_tts": {"probabilidad_sintetico": es_sintetico, "anomalias": motivos},
            "metricas": {
                "f0_std_hz": round(std_f0, 2),
                "mfcc_varianza": round(mfcc_var, 2),
                "high_freq_energy": round(high_freq_energy, 6),
                "std_rms_dinamica": round(std_rms, 4)
            }
        }
    }
    
    return reporte, y, sr, f0

def generar_grafico(y: np.ndarray, sr: float, f0: Any) -> plt.Figure:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
    
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    img = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz', ax=ax1)
    ax1.set_title('Espectrograma STFT')
    fig.colorbar(img, ax=ax1, format='%+2.0f dB')

    times = librosa.times_like(f0, sr=sr)
    ax2.plot(times, f0, color='magenta', linewidth=1.5, label='F0 (Pitch)')
    ax2.set(xlabel='Tiempo (s)', ylabel='Hz', title='Contorno de Entonación')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc='upper right')

    plt.tight_layout()
    return fig