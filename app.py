from flask import Flask, render_template, request
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

# Model mapping (only loads when needed)
MODEL_MAP = {
    "hi": "Helsinki-NLP/opus-mt-en-hi",
    "fr": "Helsinki-NLP/opus-mt-en-fr",
    "de": "Helsinki-NLP/opus-mt-en-de"
}

# Cache loaded models (so it doesn’t reload every time)
loaded_models = {}

def load_model(lang):
    if lang not in loaded_models:
        model_name = MODEL_MAP[lang]
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        loaded_models[lang] = (tokenizer, model)
    return loaded_models[lang]

@app.route("/", methods=["GET", "POST"])
def index():
    translation = ""

    if request.method == "POST":
        text = request.form["text"]
        lang = request.form["lang"]

        try:
            tokenizer, model = load_model(lang)

            inputs = tokenizer(text, return_tensors="pt", padding=True)
            outputs = model.generate(**inputs)

            translation = tokenizer.decode(outputs[0], skip_special_tokens=True)

        except Exception as e:
            translation = "Translation error. Try again."

    return render_template("index.html", translation=translation)

if __name__ == "__main__":
    app.run(debug=True)