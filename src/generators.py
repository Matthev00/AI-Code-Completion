from transformers import AutoModelForCausalLM, AutoTokenizer
from dataloader import CodeCopletionDataset, CodeCompletionDataLoader
import json


MODELS = {
    "starcoder": "bigcode/tiny_starcoder_py",
}

TOKNIZERS = {name: AutoTokenizer.from_pretrained(model) for name, model in MODELS.items()}
LOADED_MODELS = {name: AutoModelForCausalLM.from_pretrained(model) for name, model in MODELS.items()}

def process_with_model(model_name, prefix, suffix):
    model = LOADED_MODELS[model_name]
    tokenizer = TOKNIZERS[model_name]
    
    input_text = prefix + "[MASK]" + suffix
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=50)
    
    completion = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return completion.replace(prefix, "").replace(suffix, "")


def main():
    dataset = CodeCopletionDataset()[:50]
    dataloader = CodeCompletionDataLoader(dataset)
    output_file = "data/rewiev/preds.json"

    data = []
    for sample in dataloader:
        prefix, middle, suffix = sample
        outputs = {
            "starcoder": process_with_model("starcoder", prefix, suffix),
        }
        data.append({
            "prefix": prefix,
            "middle": middle,
            "suffix": suffix,
            "outputs": outputs
        })

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
