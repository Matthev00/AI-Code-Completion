from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import signal

app = Flask(__name__)

with open("data/review/preds.json") as f:
    examples = json.load(f)

ratings = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        example_id = int(request.form["example_id"])
        for i, model in enumerate(examples[example_id]["outputs"]):
            rating = request.form.get(f"rating_{i+1}")
            model_name = request.form.get(f"model_{i+1}")
            if rating and model_name:
                ratings.append({"example_id": example_id, "model": model_name, "rating": rating})
        
        return redirect(url_for("index"))

    example_id = len(ratings)
    if example_id >= len(examples):
        save_and_exit()

    example = examples[example_id]
    return render_template("index.html", example=example, example_id=example_id, models=example["outputs"])

def save_and_exit():
    with open("data/review/ratings.json", "w") as f:
        json.dump(ratings, f, indent=4)
    os.kill(os.getpid(), signal.SIGINT)

if __name__ == "__main__":
    app.run(debug=True)