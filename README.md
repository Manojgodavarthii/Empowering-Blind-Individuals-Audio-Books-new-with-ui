# 🎧 Audio Books: Empowering Blind People

### An AI-Powered Accessible Learning and Audiobook Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/UI-Gradio-orange?logo=gradio&logoColor=white" alt="Gradio">
  <img src="https://img.shields.io/badge/AI-Qwen2.5--1.5B--Instruct-purple" alt="Qwen2.5">
  <img src="https://img.shields.io/badge/OCR-RapidOCR-green" alt="RapidOCR">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
</p>

<p align="center">
  <a href="https://audiobooks-assist.hashnode.dev/audio-books-empowering-blind-people">📖 Read the Project Blog</a>
  ·
  <a href="https://github.com/Manojgodavarthii">👨‍💻 GitHub Profile</a>
  ·
  <a href="#-installation-and-setup">🚀 Get Started</a>
</p>

> **Audio Books** is an assistive Generative AI application designed to help blind and visually impaired learners access printed and digital educational materials. It converts PDFs, scanned documents, and book images into structured study resources, document-based answers, and multilingual spoken audio.

The project combines OCR, a locally run language model, prompt engineering, translation, and text-to-speech in an interactive Gradio application.

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Key Features](#-key-features)
- [Application Workflow](#-application-workflow)
- [Technology Stack](#-technology-stack)
- [Installation and Setup](#-installation-and-setup)
- [User Interface Overview](#-user-interface-overview)
- [Project Structure](#-project-structure)
- [Current Status and Limitations](#-current-status-and-limitations)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)
- [Author](#-author)
- [Project Blog](#-project-blog)
- [License](#-license)

---

## 💡 Project Overview

Educational materials are not always available in accessible digital formats. Students may receive physical textbooks, photocopied notes, photographs of printed pages, or scanned PDFs that contain no selectable text.

Audio Books aims to bridge this accessibility gap by combining document extraction and AI-powered learning assistance in one application.

Users can upload supported documents, extract their text, generate structured study materials, ask questions about the content, and convert selected information into spoken audio.

### 🎯 Project Objectives

- Improve access to printed and scanned educational materials.
- Convert extracted text into understandable summaries and revision resources.
- Provide question answering based on uploaded document content.
- Support multilingual audio generation.
- Explore lightweight, locally executed AI models to reduce dependence on paid cloud AI APIs.
- Create a foundation for more accessible and inclusive digital learning.

## 🚩 Problem Statement

Traditional screen readers are useful for accessible digital documents, but scanned textbook pages and photographed notes require additional text-recognition capabilities.

Even after text extraction, learners may need to organize lengthy chapters, understand difficult concepts, prepare for examinations, or listen to the content instead of reading it visually.

Audio Books addresses these challenges through a combined document-processing, language-model, and speech-generation workflow.

## 🌟 Key Features

### 📄 1. Dual-Tier Document Extraction

- Extracts selectable PDF text using **PyMuPDF (`fitz`)**.
- Uses **RapidOCR with ONNX Runtime** as an OCR fallback for scanned pages and images.
- Supports PDF, PNG, and JPG/JPEG input through the applicable interface components.
- Helps process both digital documents and image-based study materials.

### 🧠 2. Local Language-Model Processing

- Uses `Qwen/Qwen2.5-1.5B-Instruct` through Hugging Face Transformers.
- Generates structured responses using prompt templates.
- Supports local text analysis without requiring a paid LLM API subscription.
- Uses section markers to organize model responses into different application tabs.

*Actual performance depends on available RAM, CPU, model configuration, and document length.*

### 📚 3. AI-Generated Study Kits

Transforms extracted content into structured learning materials:

- **Summary and Topics:** Important concepts and main arguments.
- **Action Items:** Relevant tasks, methods, and points to review.
- **Keywords:** Important terms from the content.
- **Flashcards:** Question-and-answer pairs for revision.
- **Practice Quizzes:** Multiple-choice questions and explanations.

### 💬 4. Document-Based Question Answering

- Allows users to ask questions about uploaded content.
- Provides answers using the extracted document text as context.
- Helps users understand technical topics and specific passages.
- Can be extended with retrieval-based methods and page-level citations.

Document context helps reduce unsupported answers but cannot guarantee that every response is correct.

### 🌍 5. Multilingual Audio Generation

- Supports English, Hindi, Spanish, French, and German through the configured translation and speech pipeline.
- Uses `deep-translator` for translation where required.
- Uses `gTTS` to generate MP3 speech.
- Allows generated audio to be played in the browser or downloaded.

**Note:** The current gTTS and online translation workflow requires an internet connection.

### ♿ 6. Accessible Study-Material Export

- Exports available study content to Markdown (`.md`).
- Organizes generated sections into a readable document.
- Supports reuse with compatible Markdown editors and assistive reading tools.
- Provides a foundation for future Braille-friendly and screen-reader-focused improvements.

---

## 🏗️ Application Workflow

The application follows a pipeline that converts uploaded documents into structured learning resources and spoken audio.

```text
           DOCUMENT INPUT
        PDF / Scanned PDF / Image
                   |
                   v
       +--------------------------+
       |  Document Text Extraction|
       |       PyMuPDF            |
       +--------------------------+
                   |
          Text unavailable?
                   |
                   v
       +--------------------------+
       |      RapidOCR            |
       |   Scanned Page OCR       |
       +--------------------------+
                   |
                   v
          EXTRACTED TEXT
                   |
                   v
       +--------------------------+
       | Local Language Model     |
       | Qwen2.5-1.5B-Instruct    |
       +--------------------------+
                   |
           +-------+-------+
           |               |
           v               v
     STRUCTURED KIT    DOCUMENT Q&A
     Summary           User Question
     Keywords          + Document Text
     Action Items           |
     Flashcards             v
     Quiz              Text Answer
           |               |
           +-------+-------+
                   |
                   v
       +--------------------------+
       | Translation (Optional)   |
       | deep-translator          |
       +--------------------------+
                   |
                   v
       +--------------------------+
       | Speech Generation        |
       | gTTS                     |
       +--------------------------+
                   |
                   v
           MP3 AUDIO OUTPUT
```

The architecture separates extraction, language-model processing, study-kit generation, question answering, and audio generation. This makes the workflow easier to understand and provides clear areas for future optimization.

---

## 🛠️ Technology Stack

| Category | Technologies | Purpose |
|---|---|---|
| Programming Language | Python | Application logic and processing |
| PDF Processing | PyMuPDF (`fitz`) | Digital PDF text extraction |
| OCR | RapidOCR, ONNX Runtime | Text recognition from scanned pages |
| Image Processing | Pillow | Image loading and preprocessing |
| Language Model | Qwen2.5-1.5B-Instruct | Content analysis and study-kit generation |
| AI Framework | Hugging Face Transformers, PyTorch | Model loading and inference |
| Translation | deep-translator | Translating selected content |
| Text-to-Speech | gTTS | Generating spoken audio |
| Interface | Gradio Blocks | Interactive web application |
| Output Formats | Markdown, MP3 | Study notes and audio files |

---

## 🚀 Installation and Setup

Follow these steps to run the application locally.

### Prerequisites

- Python 3.10 or a compatible Python version supported by the selected dependencies.
- Git.
- An internet connection for installing dependencies and downloading model files.
- Sufficient memory and disk space for PyTorch and the language model.

The first model download may take time. Subsequent runs can reuse cached files, subject to the application's configuration.

### 1. Clone the Repository

Replace the placeholder repository URL with your actual GitHub repository URL.

```bash
git clone https://github.com/Manojgodavarthii/audiobooks-empowering-blind-people.git
cd audiobooks-empowering-blind-people
```

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the required libraries:

```bash
pip install pymupdf rapidocr-onnxruntime transformers torch torchvision gradio pillow gTTS deep-translator numpy
```

For a reproducible setup, consider adding a tested `requirements.txt` file with compatible package versions.

### 4. Download Model Files (Optional)

If your repository includes `download_models.py`, run:

```bash
python download_models.py
```

This step can download the required model files in advance. Check that the script saves them to the expected cache or local directory.

**Offline-use note:** Pre-downloading model weights does not make every feature offline. Local model inference may work without internet once setup is complete, but gTTS and online translation still require connectivity.

### 5. Launch the Application

Run:

```bash
python app.py
```

Open your browser and navigate to:

```text
http://localhost:7860
```

The Gradio interface should be available if the application starts successfully and uses the default port.

---

## 🖥️ User Interface Overview

| Feature / Tab | Purpose |
|---|---|
| Summary & Topics | Presents summaries, main arguments, and key concepts |
| Action Items | Organizes relevant tasks and points to review |
| Flashcards | Supports active recall with questions and answers |
| Practice Quiz | Generates multiple-choice questions and answer explanations |
| Ask Document | Answers questions using extracted document context |
| Extracted Content | Displays extracted digital text and OCR results |
| Audio Synthesis | Generates and plays speech in a selected language |
| Export | Saves available learning material as a Markdown document |

The exact tabs and their availability depend on the current implementation of `app.py`.

---

## 📂 Suggested Project Structure

```text
audiobooks-empowering-blind-people/
│
├── app.py
├── download_models.py
├── requirements.txt
├── README.md
├── LICENSE
│
├── models/
│   └── (Optional local model files)
│
├── uploads/
│   └── (Temporary uploaded documents)
│
├── outputs/
│   ├── (Generated audio files)
│   └── (Exported study notes)
│
└── images/
    └── (Project screenshots and documentation images)
```

This is a suggested structure. Keep only the folders and files used by your actual application, and avoid committing large model weights, private documents, generated audio, or temporary uploads to Git.

---

## ⚠️ Current Status and Known Limitations

Audio Books is an assistive technology prototype under active development. Its current capabilities have several limitations.

### 1. Complex Page Layouts

Multi-column layouts, tables, sidebars, and irregular formatting may affect text extraction and reading order.

**Planned improvement:** Add layout detection, better preprocessing, and reading-order correction.

### 2. Long-Document Processing

Passing a complete, multi-hundred-page textbook to a small language model at once is impractical because of context-window and memory constraints.

**Planned improvement:** Introduce document chunking, embeddings, vector search, and Retrieval-Augmented Generation (RAG).

### 3. Diagrams and Scientific Charts

OCR can recognize many visible labels, but it cannot reliably explain every diagram, arrow, graph, or spatial relationship.

**Planned improvement:** Evaluate vision-language models for diagram description and visual question answering.

### 4. Internet Dependency for Speech

The current gTTS and translation integrations require internet connectivity.

**Planned improvement:** Integrate a suitable local text-to-speech engine for offline speech generation.

### 5. Answer Reliability

The language model may misunderstand extracted text or generate unsupported statements.

**Planned improvement:** Improve context selection, output validation, source references, and testing against known document answers.

### 6. Accessibility Validation

An interface designed for accessibility still requires practical testing with assistive technologies and users.

**Planned improvement:** Improve keyboard navigation, screen-reader labels, speech controls, and feedback from visually impaired learners.

---

## 🔮 Future Roadmap

The following improvements are planned for future versions.

- [ ] **RAG Integration:** Add document chunking, embeddings, and FAISS vector search for large textbooks.
- [ ] **Vision-Language Models:** Evaluate BLIP, Florence-2, or other compatible models for describing diagrams and charts.
- [ ] **Offline Neural TTS:** Evaluate Piper or Kokoro for local speech synthesis and adjustable playback speed.
- [ ] **Voice Commands:** Enable hands-free navigation using microphone input and speech recognition.
- [ ] **Improved PDF Layout Handling:** Preserve reading order across multi-column pages and tables.
- [ ] **Source References:** Display relevant page numbers or document passages alongside answers.
- [ ] **Accessibility Testing:** Improve screen-reader compatibility, keyboard navigation, and usability.
- [ ] **Performance Optimization:** Reduce model-loading overhead, memory consumption, and processing time on CPU-only systems.

These are planned enhancements, not claims that the features are already implemented.

---

## 🤝 Contributing

Suggestions, bug reports, and contributions are welcome.

If you have experience with OCR, document processing, language models, accessibility, or speech technology, you can help improve the project.

### How to Contribute

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and test them.
4. Commit your changes.
5. Push the branch to your fork.
6. Open a pull request describing your contribution.

Example commands:

```bash
git checkout -b feature/improve-document-extraction
git add .
git commit -m "Improve document text extraction"
git push origin feature/improve-document-extraction
```

Then open a pull request on GitHub.

### Reporting Issues

When reporting an issue, include:

- A short description of the problem.
- Steps to reproduce it.
- Relevant error messages.
- Python and dependency versions.
- A small sample document, if safe and appropriate to share.

Please do not upload private, sensitive, or copyrighted documents without permission.

---

## 👤 Author

**Godavarthi Naga Manoj Balaji**

*Computer Engineering Graduate (AI & ML) | Python | Machine Learning | Generative AI*

I am interested in developing practical applications using Artificial Intelligence, Machine Learning, and Generative AI. My focus is on combining AI models and software development to solve real-world problems through accessible, useful, and resource-conscious applications.

Audio Books reflects my interest in assistive technology, document intelligence, and making educational content easier to access.

- **GitHub:** [Manojgodavarthii](https://github.com/Manojgodavarthii)
- **LinkedIn:** [Godavarthi Naga Manoj Balaji](https://www.linkedin.com/in/godavarthi-naga-manoj-balaji/)
- **Project Blog:** [Read the Audio Books Project Story](https://audiobooks-assist.hashnode.dev/audio-books-empowering-blind-people)

---

## 📖 Project Blog

I have also written a blog explaining the motivation behind this project, its workflow, the technologies used, the challenges encountered, and the improvements planned for future versions.

**Read the full article:** [Audio Books: Empowering Blind People](https://audiobooks-assist.hashnode.dev/audio-books-empowering-blind-people)

The article provides additional context about how an assistive idea developed into an AI-powered document and audiobook assistant.

---
## 🚧 Project Status

**Audio Books: Empowering Blind People** is currently under active development. New features, performance improvements, and accessibility enhancements are being worked on. Some features may change as development continues.

Your feedback and suggestions are always welcome as I continue improving this project.

## 🤝 Support & Suggestions

If you have any suggestions, ideas, feedback, or recommendations to improve this project, you are always welcome to share them.

- 💡 Suggest new features or improvements.
- 🐛 Report bugs or issues.
- ♿ Recommend accessibility enhancements.
- 📩 Contact me through [GitHub](https://github.com/Manojgodavarthii) or [LinkedIn](https://www.linkedin.com/in/godavarthi-naga-manoj-balaji/).

Every suggestion is appreciated and can help make this project better.

## 📜 License & Usage Terms

**Copyright © 2026 Godavarthi Naga Manoj Balaji. All rights reserved.**

This project is a personal development project and is **not released under an open-source license**.

- You may view the repository for learning and reference purposes.
- You may not copy, modify, redistribute, publish, or use this project's code or its components in another project without obtaining prior written permission from the author.
- Commercial use or redistribution requires explicit permission from the author.

If you would like to use, adapt, or collaborate on this project, please contact the author and request permission first.

**Please do not assume that publicly available code is free to reuse.** All rights not expressly granted are reserved by the author.

## 👨‍💻 Author

**Godavarthi Naga Manoj Balaji**

Computer Engineering Graduate — AI & ML

- GitHub: [Manojgodavarthii](https://github.com/Manojgodavarthii)
- LinkedIn: [Connect with me](https://www.linkedin.com/in/godavarthi-naga-manoj-balaji/)
- Project Blog: [Audio Books: Empowering Blind People](https://audiobooks-assist.hashnode.dev/audio-books-empowering-blind-people)

---

*This project is still under development. More features and improvements are planned. Thank you for your interest, feedback, and suggestions!*
