import gradio as gr

def change_audio(audio_path):
    print("Audio path:", audio_path)
    return "done"

with gr.Blocks() as demo:
    input_mic = gr.Audio(
        label="마이크 입력", sources=["microphone"], type="filepath"
    )
    output_textbox = gr.Textbox(label="텍스트")
    input_mic.change(fn=change_audio, inputs=[input_mic], outputs=[output_textbox])

demo.launch(prevent_thread_lock=True)
