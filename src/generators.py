from transformers import AutoModelForCausalLM, AutoTokenizer
from dataloader import CodeCopletionDataset, CodeCompletionDataLoader
import json
import torch


MODELS = {
    "starcoder": "bigcode/tiny_starcoder_py",
}

TOKNIZERS = {name: AutoTokenizer.from_pretrained(model) for name, model in MODELS.items()}
LOADED_MODELS = {name: AutoModelForCausalLM.from_pretrained(model) for name, model in MODELS.items()}
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def process_with_model(model_name, prefix, suffix):
    model = LOADED_MODELS[model_name]
    tokenizer = TOKNIZERS[model_name]
    
    input_text = f"<fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>"
    inputs = tokenizer.encode(input_text, return_tensors="pt").to(DEVICE)
    outputs = model.generate(inputs, max_new_tokens=50)
    
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


if __name__ == "__main__":
    main()
