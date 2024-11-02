# Code Completion Model Experiment Report

## Data Description

For this experiment, I used data from my GitHub repository, which is a PyTorch project focused on animal classification. To adapt the data for code completion, I created code examples with missing segments to simulate real-world coding tasks.

### Data Preparation

A key consideration in creating these examples was extracting code from within functions or classes to provide a realistic context. Each example includes:
- **Prefix**:
- **Middle**
- **Suffix**

This approach ensures that the generated examples aren’t completely random, as each snippet retains a structure resembling practical code completion scenarios.

## Reproducing the Experiment

To reproduce this experiment, follow these steps:

1. **Install Required Libraries**:
   ```bash
   pip install -r requirements.txt
    ```
2. Download Data: Run the data_download.py script to download and prepare the data for processing.

3. Generate Model Predictions: The generators.py script uses a selected model to generate code completions for each example based on the prefix and suffix.

3. Manual Evaluation of Results: app.py is a simple Flask application that allows for manual assessment of generated code. For each example, you can select one of three labels: correct, partially correct, or incorrect.

3. Automatic Evaluation: The evaluate.py script computes automatic metrics for each generated completion and compares it with the actual middle segment.

4. Analyze Results in MLflow: After running the evaluation script, start the MLflow UI to analyze metrics and experiment results:

    ```bash
    mlflow ui
    ```
## Applied Automatic Metrics
For automatic evaluation of the model’s generated completions, the following metrics were used:

 - Exact Match: Checks if the generated fragment is identical to the actual middle. This is a strict metric that verifies exact matches.

 - BLEU: Measures n-gram overlap between the generated code and the actual middle. Although primarily used for text translation, it can provide insight into code fragment similarity.

 - CHRF: Measures character-level similarity by comparing character n-grams between the generated code and the actual code. This metric is more flexible than BLEU and more precise for code.

-  Levenshtein Distance: Measures the number of edits (insertions, deletions, substitutions) needed to transform the generated fragment into the actual middle. A smaller distance indicates closer resemblance to the original.
  
## Which Auto-metrisc is the best

1. Exact Match as the Primary Metric for "Correct" (Rating 2):

   - Exact Match is ideal for identifying "correct" completions because it strictly requires the generated code to match the original exactly. When Exact Match is 1, the manual rating is consistently 2 ("correct"). However, it's too strict for partially correct cases, where even minor differences lead to a score of zero.
2. CHRF as the Best Metric for "Partially Correct" (Rating 1):

   - CHRF measures character-level similarity, making it sensitive to small variations in code. We see higher CHRF scores with increasing manual ratings, which suggests it’s effective at capturing "partially correct" cases where the generated code is close but not identical to the original.
3. Edit Distance BLEU are very random and unusfull in this case

**All 3 metrics are far from perfect but the CHRF is the most accurate.**
