import json
from pathlib import Path
import tempfile
import streamlit as st
from analizador import analizar_audio, generar_grafico

st.set_page_config(page_title="Forensic Detector", page_icon="🛡️", layout="wide")
st.title("🛡️ Forensic Audio & TTS Detector")

file_up = st.file_uploader("Cargar muestra (.wav, .mp3)", type=["wav", "mp3"])

if file_up:
    if st.button("🔍 Analizar Muestra", type="primary"):
        suffix = Path(file_up.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_up.getbuffer())
            tmp_path = Path(tmp.name)

        try:
            with st.spinner("Procesando espectrogramas y extracción de métricas forenses..."):
                reporte, y, sr, f0 = analizar_audio(tmp_path)
            
            diag = reporte["analisis_forense"]["diagnostico_tts"]
            metrics = reporte["analisis_forense"]["metricas"]
            props = reporte["analisis_forense"]["propiedades"]
            json_str = json.dumps(reporte, indent=2, ensure_ascii=False)

            tab1, tab2, tab3 = st.tabs(["📊 Métricas", "📄 JSON Report", "📈 Espectrograma"])

            with tab1:
                st.audio(file_up)
                if diag["probabilidad_sintetico"]:
                    st.error("⚠️ Muestra Sospechosa (Posible TTS / Voz Sintética IA)")
                    for a in diag["anomalias"]:
                        st.write(f"- {a}")
                else:
                    st.success("✅ Estructura Acústica Natural")

                c1, c2, c3 = st.columns(3)
                c1.metric("Duración Muestra", f'{props["duracion_analizada_seg"]} s')
                c2.metric("Pitch Std (F0)", f'{metrics["f0_std_hz"]} Hz')
                c3.metric("Varianza MFCC", metrics["mfcc_varianza"])

            with tab2:
                st.download_button("📥 Descargar JSON", json_str, f"reporte_{file_up.name}.json", "application/json")
                st.json(reporte)

            with tab3:
                st.pyplot(generar_grafico(y, sr, f0))

        finally:
            if tmp_path.exists():
                tmp_path.unlink()