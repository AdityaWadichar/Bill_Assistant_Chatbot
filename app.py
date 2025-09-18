import os
import json
import pdfplumber
import openai
from flask import Flask, request, jsonify, render_template
import webbrowser
from threading import Timer
from pydantic import BaseModel
import instructor

# Flask Config
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
JSON_FOLDER = "json_storage"
API_KEY_FILE = "api_key.txt"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["JSON_FOLDER"] = JSON_FOLDER

class ItemDetails(BaseModel):
    item: str | None
    unit_price: float | None
    quantity: int | None
    net_amount: float | None
    discount: float | None
    total_tax: float | None
    total_amount: float | None

class BillDetails(BaseModel):
    seller_name: str | None
    seller_address: str | None
    buyer_name: str | None
    buyer_address: str | None
    invoice_number: str | None
    order_id: str | None
    order_date: str | None
    items: list[ItemDetails] | None
    other_charges: float | None
    other_discounts: float | None
    final_amount: float | None

# Ensure upload & storage folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(JSON_FOLDER, exist_ok=True)

extracted_json = {}

chat_history = [{"role": "system", "content": "You are an AI assistant helping a user understand their bill."}]

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

# Function to Load API Key Persistently
def load_api_key():
    try:
        with open(API_KEY_FILE, "r") as key_file:
            return key_file.read().strip()
    except FileNotFoundError:
        return None

# Set API Key for OpenAI
openai.api_key = load_api_key()

# Home Route - Asks for API Key if Not Set
@app.route("/")
def home():
    if not openai.api_key or openai.api_key == "your_secret_key":
        return render_template("api_key.html")  # Prompt user for API key
    return render_template("index.html")  # Proceed to main page

# Store API Key Temporarily and Persistently
@app.route("/set_api_key", methods=["POST"])
def set_api_key():
    api_key = request.json.get("api_key")
    if not api_key:
        return jsonify({"error": "API Key is required"}), 400

    openai.api_key = api_key  # Set OpenAI API key dynamically

    # Save API key to file
    with open(API_KEY_FILE, "w") as key_file:
        key_file.write(api_key)

    return jsonify({"message": "API Key saved, proceeding to main app"})

# Upload PDF (Requires API Key)
@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    extracted_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() + "\n"

    messages = [
        {"role": "system", "content": "Extract structured data from this bill in JSON format."},
        {"role": "user", "content": extracted_text}
    ]
    chat_history.extend(messages)

    instruct_client = instructor.patch(openai.OpenAI(api_key=openai.api_key))
    response = instruct_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_model=BillDetails,
        max_tokens=None
    )
    processed_data = response.dict()

    chat_history.append({"role": "assistant", "content": str(processed_data)})
    global extracted_json
    extracted_json = processed_data  # Store in memory but don't save yet

    return jsonify({"message": "File uploaded!", "json_data": processed_data})

@app.route("/save_data", methods=["POST"])
def save_data():
    global extracted_json
    if not extracted_json:
        return jsonify({"error": "No data to save"}), 400

    file_name = "saved_data.json"
    with open(os.path.join(JSON_FOLDER, file_name), "w") as json_file:
        json.dump(extracted_json, json_file, indent=4)

    return jsonify({"message": "Data saved successfully!"})


# Ask Questions (Requires API Key)
@app.route("/ask_question", methods=["POST"])
def ask_question():
    if not openai.api_key or openai.api_key == "your_secret_key":
        return jsonify({"error": "API Key not set. Please refresh and enter it."}), 403

    query = request.json.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    messages = [
        {"role": "system", "content": "You are an AI assistant helping with the bill."},
        {"role": "user", "content": query}
    ]
    chat_history.extend(messages)
    standard_client = openai.OpenAI(api_key=openai.api_key)
    response = standard_client.chat.completions.create(model="gpt-4o-mini", messages=chat_history)
    answer = response.choices[0].message.content.strip()
    chat_history.append({"role": "assistant", "content": answer})

    return jsonify({"answer": answer})

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True)