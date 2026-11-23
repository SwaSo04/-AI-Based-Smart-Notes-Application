# AI-Based Smart Notes Application (ZCOER)
**Department of Electronics & Computer Engineering, Zeal College of Engineering & Research**

---

## 🚀 Quick Setup Instructions (Running in 2 Minutes)

### 1. Open Terminal / PowerShell in this directory
```bash
cd c:\Users\Admin\Documents\AntiGravity
```

### 2. Install Required Python Packages
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
streamlit run app.py
```
Your browser will automatically open at: `http://localhost:8501`.

---

## 👥 Team Work Allocation (For Tuesday Evaluation)
* **Snehalish Zode (EC3347):** AI prompt pipeline (`ai_service.py`), structured summary generation, and flashcard extraction logic.
* **Swayam Sonawane (EC3331):** Document parser (`extractor.py`), PyMuPDF pipeline, text cleaning, and whitespace preprocessing.
* **Krishna Wajage (EC3341):** Relational schema (`database.py`), SQLite storage, and Streamlit user interface (`app.py`).

---

## 🎯 Tuesday 50% Demo Checklist
1. **Have 2 sample PDFs ready on your desktop** (e.g., one on *Digital Signal Processing* or *Linear Algebra*, and one on *Machine Learning*).
2. **Launch `streamlit run app.py`** before entering the viva room so it is already running.
3. If you have an active Google Gemini API key from [aistudio.google.com](https://aistudio.google.com/), paste it in the sidebar. If not, the application has an automatic safe fallback demo mode that will still generate structured notes and flashcards without crashing.
