# Code Completion Model Experiment Report

## Data Description
For this experiment, I used data from my GitHub repository, which is a PyTorch project focused on animal classification <https://github.com/Matthev00/Oxford_Pet_Recognition>. 

### Data Preparation
A key consideration in creating these examples was extracting code from within functions or classes to provide a realistic context. Each example includes:

## Reproducing the Experiment
To reproduce this experiment, follow these steps:
1. **Install Required Libraries**:
   ```bash
   pip install -r requirements.txt
    ```
2. Download Data: Run the **data_download.py** script to download and prepare the data for processing.

3. Generate Model Predictions: The **generators.py** script uses a selected model to generate code completions for each example based on the prefix and suffix.
 -  *I also planned to test the CodeLlama-7b-hf model for this experiment. However, it turned out to be too large for my local hardware and the free tier of Google Colab, which limited my ability to fully evaluate it.*

3. Manual Evaluation of Results: **app.py** is a simple Flask application that allows for manual assessment of generated code. For each example, you can select one of three labels: correct, partially correct, or incorrect.

3. Automatic Evaluation: The **evaluate.py** script computes automatic metrics for each generated completion and compares it with the actual middle segment.

4. Analyze Results in **MLflow**: After running the evaluation script, start the MLflow UI to analyze metrics and experiment results:

    ```bash
    mlflow ui
    ```
## Applied Automatic Metrics
For automatic evaluation of the model’s generated completions, the following metrics were used:

 - Exact Match: Checks if the generated fragment is identical to the actual middle. 

 - BLEU: Measures n-gram overlap between the generated code and the actual middle. 

 - CHRF: Measures character-level similarity by comparing character n-grams between the generated code and the actual code. This metric is more flexible than BLEU and more precise for code.
- Levenshtein Distance: Measures the number of edits (insertions, deletions, substitutions) needed to transform the generated fragment into the actual middle. A smaller distance indicates closer resemblance to the original.
  
## Which Auto-metrisc is the best
1. Exact Match as the Primary Metric for "Correct" (Rating 2):

   - Exact Match is ideal for identifying "correct" completions because it strictly requires the generated code to match the original exactly. However, it's too strict for partially correct cases, where even minor differences lead to a score of zero.
2. CHRF as the Best Metric for "Partially Correct" (Rating 1):

   - CHRF measures character-level similarity, making it sensitive to small variations in code. We see higher CHRF scores with increasing manual ratings, which suggests it’s effective at capturing "partially correct" cases where the generated code is close but not identical to the original.
3. Edit Distance BLEU are very random and unusfull in this case

**All 3 metrics are far from perfect but the CHRF is the most accurate.**

## Ideas for Alternative Approaches
- **Vary Dataset Splits**: Experiment with different proportions for prefix, middle, and suffix segments.
- **Randomize Starting Points**: Instead of always starting the prefix from the beginning of a function or class, try using random positions.
- **Test on Unrelated Domains**: Evaluate the model on datasets that are not related to ML/DL.
