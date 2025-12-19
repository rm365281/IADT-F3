# Fine-Tuning Llama-3.2-3B-Instruct with Unsloth

This guide explains how to fine-tune the [unsloth/Llama-3.2-3B-Instruct](https://huggingface.co/unsloth/llama-3.2-3b-instruct) model using your own medical Q&A data. The process uses Unsloth for efficient LoRA fine-tuning and produces a LoRA adapter that can be merged into a GGUF file for deployment.

## 1. Generate the Training Dataset

First, you need to create the datasets for training. This involves converting your XML Q&A files to JSONL and generating symptom-to-disease pairs.

### Step 1.1: Convert XML to JSONL

Run the following script to convert all XML files in `fine_tuned_model/data/` to a JSONL dataset:

```bash
python fine_tuned_model/xml_to_jsonl.py
```

This will create `fine_tuned_model/dataset/dataset_alpaca.jsonl`.

### Step 1.2: Generate Symptom-to-Disease Dataset

Run the following script to generate a dataset mapping symptoms to diseases:

```bash
python fine_tuned_model/disease_extraction.py
```

This will create `fine_tuned_model/dataset/dataset_symptoms_to_disease.jsonl`.

## 2. Fine-Tune the Model

Use the generated datasets to fine-tune the base model. Run:

```bash
python fine_tuned_model/fine_tunning_llama3_2_3b.py
```

- This script uses the Unsloth library to fine-tune `unsloth/llama-3.2-3b-instruct-unsloth-bnb-4bit` with your datasets.
- The process will output a LoRA adapter in the `tech3_lora_model` directory and attempt to push it to Hugging Face.

**Important:**
- Before running, edit `fine_tunning_llama3_2_3b.py` and replace `hugging-face-pat` with your real Hugging Face Personal Access Token (with write permissions).
- Replace `repo` with your actual Hugging Face repository name.

## 3. Merge LoRA Adapter and Export GGUF

After fine-tuning and uploading the LoRA adapter, merge it with the base model to create a GGUF file for deployment.

This step uses the Hugging Face CLI. Example command:

```bash
# Install the CLI if needed
pip install huggingface_hub

# Log in to Hugging Face
huggingface-cli login

# Download the base model and LoRA adapter, then merge and export to GGUF
# (Refer to Unsloth or Hugging Face documentation for the exact merge/export commands)
```

## Summary

1. Generate datasets: `xml_to_jsonl.py` and `disease_extraction.py`
2. Fine-tune with `fine_tunning_llama3_2_3b.py` (edit PAT and repo first)
3. Merge LoRA and export GGUF using Hugging Face CLI

For more details, see the scripts in `fine_tuned_model/`.
