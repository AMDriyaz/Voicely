import gradio as gr
from TTS.api import TTS

# Voice options
voice_options = {
    "tts_models/en/ljspeech/tacotron2-DDC": "English - Female (LJSpeech)",
    "tts_models/en/vctk/vits": "English - Multi-Speaker (VCTK)"
}

label_to_model = {v: k for k, v in voice_options.items()}

# Cache for TTS models
tts_models_cache = {}

def get_tts_model(model_name):
    """Load TTS model only once and reuse it."""
    if model_name not in tts_models_cache:
        print(f"🔄 Loading model: {model_name}")
        tts_models_cache[model_name] = TTS(model_name=model_name, progress_bar=False, gpu=False)
    return tts_models_cache[model_name]

def get_speakers(voice_label):
    model_name = label_to_model[voice_label]
    tts = get_tts_model(model_name)

    if hasattr(tts, "speakers") and tts.speakers:
        speakers = tts.speakers
        return gr.Dropdown.update(choices=speakers, value=speakers[0])
    else:
        return gr.Dropdown.update(choices=["Default"], value="Default")

def generate_speech(text, voice_label, speaker_label):
    if not text.strip():
        text = "Hello world"

    model_name = label_to_model[voice_label]
    tts = get_tts_model(model_name)

    if hasattr(tts, "speakers") and tts.speakers:
        if speaker_label not in tts.speakers:
            speaker_label = tts.speakers[0]
        tts.tts_to_file(text=text, file_path="output.wav", speaker=speaker_label)
    else:
        tts.tts_to_file(text=text, file_path="output.wav")

    return "output.wav"

# --------------------------
# UI (footer removed ✅)
# --------------------------
with gr.Blocks(theme=gr.themes.Default(), analytics_enabled=False) as demo:
    gr.HTML("""
        <style>
            footer, .svelte-1ipelgc {display: none !important;}
        </style>
    """)
    gr.Markdown("## Coqui TTS Web UI")

    text_input = gr.Textbox(lines=4, placeholder="Enter text here...", label="Text to Speak")
    voice_dropdown = gr.Dropdown(choices=list(voice_options.values()), label="Select Voice / Language")
    speaker_dropdown = gr.Dropdown(choices=["Default"], label="Select Speaker", allow_custom_value=True)
    output_audio = gr.Audio(type="filepath")

    voice_dropdown.change(fn=get_speakers, inputs=voice_dropdown, outputs=speaker_dropdown)

    generate_btn = gr.Button("Generate Speech")
    generate_btn.click(fn=generate_speech,
                       inputs=[text_input, voice_dropdown, speaker_dropdown],
                       outputs=output_audio)

demo.launch()
