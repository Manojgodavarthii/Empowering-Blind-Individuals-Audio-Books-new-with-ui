import os
import re
import tempfile
import numpy as np
import pymupdf as fitz
import torch
import gradio as gr
from PIL import Image
from gtts import gTTS
from deep_translator import GoogleTranslator
from transformers import AutoModelForCausalLM, AutoTokenizer
from rapidocr_onnxruntime import RapidOCR

# =====================================================================
# 1. INITIALIZE ENGINES
# =====================================================================
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

print("[STATUS] Initializing RapidOCR (CPU/ONNX optimized)...")
ocr_engine = RapidOCR()

print(f"[STATUS] Loading {MODEL_NAME} on {DEVICE.upper()}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    device_map="auto" if DEVICE == "cuda" else None,
    low_cpu_mem_usage=True
).to(DEVICE).eval()

print("[STATUS] Engines loaded successfully.")

# =====================================================================
# 2. DOCUMENT INGESTION & OCR ENGINE
# =====================================================================
def extract_text_robust(file_obj):
    if file_obj is None:
        return ""

    filepath = file_obj.name if hasattr(file_obj, "name") else str(file_obj)
    extracted_text = ""

    if filepath.lower().endswith(".pdf"):
        doc = fitz.open(filepath)
        max_pages = min(len(doc), 6)

        for page_idx in range(max_pages):
            page = doc[page_idx]
            page_text = page.get_text().strip()

            if len(page_text) < 40:
                pix = page.get_pixmap(dpi=140)
                img_bytes = pix.tobytes("png")
                result, _ = ocr_engine(img_bytes)
                if result:
                    page_text = "\n".join([line[1] for line in result])

            if page_text:
                extracted_text += f"\n--- Page {page_idx + 1} ---\n{page_text}\n"

        doc.close()
    else:
        img = Image.open(filepath).convert("RGB")
        img_np = np.array(img)
        result, _ = ocr_engine(img_np)
        if result:
            extracted_text = "\n".join([line[1] for line in result])

    return extracted_text.strip()


def run_llm_inference(prompt, max_new_tokens=650):
    messages = [
        {"role": "system", "content": "You are an analytical document specialist. Be thorough, clear, and follow exact structural tags."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to(DEVICE)

    with torch.inference_mode():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=None,
            top_p=None
        )

    out_ids = generated_ids[0][len(inputs.input_ids[0]):]
    return tokenizer.decode(out_ids, skip_special_tokens=True).strip()


def parse_llm_output(raw_text):
    sections = {
        "summary": "",
        "action_items": "",
        "keywords": "",
        "flashcards": "",
        "quiz": ""
    }

    patterns = {
        "summary": r"###\s*SUMMARY\s*([\s\S]*?)(?=###\s*ACTION_ITEMS|$)",
        "action_items": r"###\s*ACTION_ITEMS\s*([\s\S]*?)(?=###\s*KEYWORDS|$)",
        "keywords": r"###\s*KEYWORDS\s*([\s\S]*?)(?=###\s*FLASHCARDS|$)",
        "flashcards": r"###\s*FLASHCARDS\s*([\s\S]*?)(?=###\s*QUIZ|$)",
        "quiz": r"###\s*QUIZ\s*([\s\S]*?)$"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, raw_text, re.I)
        if match and match.group(1).strip():
            sections[key] = match.group(1).strip()

    if not sections["summary"]:
        sections["summary"] = raw_text

    return (
        str(sections["summary"]),
        str(sections["action_items"] or "No direct action items identified."),
        str(sections["keywords"] or "No keywords found."),
        str(sections["flashcards"] or "No flashcards generated."),
        str(sections["quiz"] or "No quiz generated.")
    )

# =====================================================================
# 3. GRADIO CONTROLLER FUNCTIONS
# =====================================================================
def process_document(file_obj):
    if file_obj is None:
        return "No file uploaded.", "No file uploaded.", "None", "None", "None", "None"

    extracted = extract_text_robust(file_obj)
    if not extracted:
        return "No text or readable characters found in the document.", "Empty document.", "", "", "", ""

    context = extracted[:4000]

    prompt = f"""Examine this document content:

{context}

Generate an exhaustive, highly structured kit formatted strictly with these exact markdown headers:

### SUMMARY
- (Core purpose and high-level premise)
- (Critical findings, data points, or key methodologies)
- (Final takeaway or conclusion)

### ACTION_ITEMS
- [ ] (Action item or next step 1)
- [ ] (Action item or next step 2)
- [ ] (Action item or next step 3)

### KEYWORDS
(Provide 6-8 core technical terms separated by commas)

### FLASHCARDS
Q1: ...
A1: ...
Q2: ...
A2: ...

### QUIZ
Q1: [Multiple Choice Question]
A) ...
B) ...
C) ...
D) ...
Answer: [Letter] - [Brief rationale]

Q2: [Multiple Choice Question]
A) ...
B) ...
C) ...
D) ...
Answer: [Letter] - [Brief rationale]"""

    raw_response = run_llm_inference(prompt, max_new_tokens=750)
    summary, actions, keywords, flashcards, quiz = parse_llm_output(raw_response)

    return (
        str(extracted),
        str(summary),
        str(actions),
        str(keywords),
        str(flashcards),
        str(quiz)
    )


def run_qa(question, context):
    if not question.strip():
        return "Please type a question."
    if not context or "No file" in context or "No text" in context:
        return "Please upload and analyze a document first."

    prompt = (
        f"Context from document:\n{context[:3500]}\n\n"
        f"Question: {question}\n\n"
        "Provide a comprehensive, clear, and direct answer based strictly on the context above. "
        "Include relevant facts, numbers, and bullet points where appropriate."
    )
    return run_llm_inference(prompt, max_new_tokens=550)


def generate_audio_file(source_text, lang):
    if not source_text or "No file" in source_text:
        return None
    speech_text = source_text[:1200]
    if lang != "en":
        try:
            speech_text = GoogleTranslator(source="auto", target=lang).translate(speech_text)
        except Exception as e:
            print(f"[Translation Warning] {e}")

    audio_path = os.path.join(tempfile.gettempdir(), "docsense_speech.mp3")
    tts = gTTS(text=speech_text, lang=lang)
    tts.save(audio_path)
    return audio_path


def export_study_kit(extracted, summary, actions, keywords, flashcards, quiz):
    if not summary or "No file" in summary:
        return None

    content = f"""# DocSense Analysis & Study Kit

## Executive Summary
{summary}

## Action Items & Next Steps
{actions}

## Key Technical Concepts
{keywords}

## Flashcards
{flashcards}

## Practice Quiz
{quiz}

---
## Raw Document Content
{extracted}
"""
    export_path = os.path.join(tempfile.gettempdir(), "DocSense_Analysis_Kit.md")
    with open(export_path, "w", encoding="utf-8") as f:
        f.write(content)

    return export_path

# =====================================================================
# 4. GRADIO INTERFACE
# =====================================================================
with gr.Blocks(title="DocSense Fast OCR & Analysis") as demo:
    gr.Markdown("# ⚡ DocSense Document Intelligence Suite")
    gr.Markdown("Fast two-tier OCR extraction, deep analytical synthesis, and study kit generation.")

    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(
                label="Upload Document (PDF, PNG, JPG)",
                file_types=[".pdf", ".png", ".jpg", ".jpeg"]
            )
            process_btn = gr.Button("🚀 Analyze Document", variant="primary")

            gr.Markdown("---")
            gr.Markdown("### 💾 Export & Download")
            export_btn = gr.Button("📥 Download Complete Kit (.md)")
            download_file = gr.File(label="Ready for Download", interactive=False)

            gr.Markdown("---")
            gr.Markdown("### 🔊 Audio Synthesis")
            audio_source_select = gr.Radio(
                choices=["Summary", "Flashcards", "QA Answer", "Extracted Text"],
                value="Summary",
                label="Voice Readout Source"
            )
            lang_selector = gr.Dropdown(
                choices=[("English", "en"), ("Spanish", "es"), ("French", "fr"), ("German", "de"), ("Hindi", "hi")],
                value="en",
                label="Language"
            )
            audio_btn = gr.Button("Generate Speech")
            audio_player = gr.Audio(label="Audio Player", type="filepath")

        with gr.Column(scale=2):
            with gr.Tabs():
                with gr.Tab("📌 Summary & Topics"):
                    summary_box = gr.Textbox(label="Executive Takeaways", lines=6)
                    keywords_box = gr.Textbox(label="Keywords & Key Terms", lines=2)

                with gr.Tab("✅ Action Items"):
                    actions_box = gr.Textbox(label="Checklist & To-Dos", lines=8)

                with gr.Tab("🃏 Flashcards"):
                    flashcards_box = gr.Textbox(label="Study Flashcards (Q&A)", lines=10)

                with gr.Tab("📝 Practice Quiz"):
                    quiz_box = gr.Textbox(label="Self-Assessment Multiple Choice Questions", lines=12)

                with gr.Tab("💬 Ask Document"):
                    qa_input = gr.Textbox(label="Your Question", placeholder="e.g. Elaborate on the experimental results...")
                    qa_btn = gr.Button("Ask", variant="primary")
                    # Expanded viewport: 14 lines tall, expands up to 35 lines without cutoff
                    qa_output = gr.Textbox(
                        label="Detailed Answer",
                        lines=14,
                        max_lines=35,
                        autoscroll=False
                    )

                with gr.Tab("📄 Extracted Content"):
                    raw_text_box = gr.Textbox(label="Extracted Content (Digital + OCR)", lines=14)

    # Document processing binding
    process_btn.click(
        fn=process_document,
        inputs=[file_input],
        outputs=[raw_text_box, summary_box, actions_box, keywords_box, flashcards_box, quiz_box]
    )

    # QA binding
    qa_btn.click(
        fn=run_qa,
        inputs=[qa_input, raw_text_box],
        outputs=[qa_output]
    )

    # Audio generation dispatcher
    def dispatch_audio(source_choice, sum_text, flash_text, qa_text, raw_text, lang):
        source_map = {
            "Summary": sum_text,
            "Flashcards": flash_text,
            "QA Answer": qa_text,
            "Extracted Text": raw_text
        }
        selected_text = source_map.get(source_choice, sum_text)
        return generate_audio_file(selected_text, lang)

    audio_btn.click(
        fn=dispatch_audio,
        inputs=[audio_source_select, summary_box, flashcards_box, qa_output, raw_text_box, lang_selector],
        outputs=[audio_player]
    )

    # Export kit to file
    export_btn.click(
        fn=export_study_kit,
        inputs=[raw_text_box, summary_box, actions_box, keywords_box, flashcards_box, quiz_box],
        outputs=[download_file]
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft(), inbrowser=True)