from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.chrf_score import sentence_chrf
from nltk.metrics import edit_distance

import json
import mlflow


with open("data/review/preds.json") as f:
    EXAMPLES = json.load(f)


with open("data/review/ratings.json") as f:
    RATINGS = json.load(f)


def calculate_metrics(generated: str, actual: str):
    return {
        "exact match": int(generated == actual),
        "bleu": sentence_bleu([actual.split()], generated.split()),
        "chrf": sentence_chrf(generated, actual),
        "edit_distance": edit_distance(generated, actual),
    }


def get_rating(example_id):
    for rating in RATINGS:
        if rating["example_id"] == example_id:
            answear = rating["rating"]
            if answear == "correct":
                return 2
            elif answear == "partially_correct":
                return 1
            elif answear == "incorrect":
                return 0
    return None


def evaluate():
    for example_id, example in enumerate(EXAMPLES):
        prefix = example["prefix"]
        middle = example["middle"]
        suffix = example["suffix"]

        for model_name, generated in example["outputs"].items():
            metrics = calculate_metrics(generated, middle)

            rating = get_rating(example_id)
            if rating is not None:
                metrics["Manual Rating"] = rating
            else:
                metrics["Manual Rating"] = "N/A"

            with mlflow.start_run(run_name=f"{model_name}_example_{example_id}"):
                mlflow.log_param("Model", model_name)
                mlflow.log_param("Example ID", example_id)
                mlflow.log_metric("Manual Rating", metrics["Manual Rating"])
                mlflow.log_metrics(calculate_metrics(generated, middle))


if __name__ == "__main__":
    evaluate()
