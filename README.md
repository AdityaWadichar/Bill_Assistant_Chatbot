# 🧾 Bill Assistant

A Flask-based app to extract and interact with structured data from bill PDFs using OpenAI's GPT models.

---

## 🖼️ Sample Screenshot

![App Screenshot](/images/Screenshot_Bill_Assistant.png)

## 🚀 How to Run This App

### 🪟 For Windows (Recommended)
Simply double-click the `run_app.bat` file.

> This script will:
- Check and install Python and pip (if not already installed)
- Create a virtual environment (if not already created)
- Install dependencies from `requirements.txt`
- Launch the app via `app.py`

No manual setup needed!

---

### 🐧 For Manual Setup (Linux/macOS/Windows)

1. **Create and activate a virtual environment** (optional but recommended)  
   Follow instructions for your OS here:  
   👉 [Python Virtual Environments Documentation](https://docs.python.org/3/library/venv.html)

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. Run the app
```bash
python app.py
```

## 🛡️ API Key Required

You must provide your OpenAI API key via the UI (prompted on first run) or by saving it to a file named `api_key.txt`.

### 👉 [Get your OpenAI API Key here](https://platform.openai.com/account/api-keys)

Example format for `api_key.txt`:



```
sk-...
```

## 📄 How to Use
Upload a PDF bill via the interface.

The app will extract structured data using GPT.

Click “Save Data” to save the extracted information as a JSON file.

Use the chatbox to ask any questions about the bill.
