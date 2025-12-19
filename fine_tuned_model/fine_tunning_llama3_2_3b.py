import torch

from unsloth import to_sharegpt, FastLanguageModel
from unsloth.chat_templates import get_chat_template, train_on_responses_only
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer
from transformers import DataCollatorForSeq2Seq

max_seq_length = 2048
dtype = None 
load_in_4bit = True 

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/llama-3.2-3b-instruct-unsloth-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit
)

model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
    use_rslora = False,
    loftq_config = None,
)


tokenizer = get_chat_template(
    tokenizer,
    chat_template = "llama-3.1",
)


dataset = load_dataset("json", data_files="dataset/*jsonl", split = "train")

dataset

def to_sharegpt(example):
  instruction = example['instruction']
  input = example['input']
  response = example['output']

  messages = []
  if input:
    messages.append({"role": "user", "content": input})
  messages.append({"role": "user", "content": instruction})
  messages.append({"role": "assistant", "content": response})
  return {"conversations": messages}

dataset = dataset.map(to_sharegpt)

dataset

def formatting_prompts_func(examples):
    convos = examples["conversations"]
    texts = [tokenizer.apply_chat_template(convo, tokenize = False, add_generation_prompt = False) for convo in convos]
    return { "text" : texts, }

dataset = dataset.map(formatting_prompts_func, batched = True,)

dataset

dataset[5]["conversations"]

dataset[5]["text"]

"""
Train the model
"""

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    data_collator = DataCollatorForSeq2Seq(tokenizer = tokenizer),
    packing = False,
    args = SFTConfig(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        max_steps = 60,
        learning_rate = 2e-4,
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.001,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        report_to = "none",
    ),
)

trainer = train_on_responses_only(
    trainer,
    instruction_part = "<|start_header_id|>user<|end_header_id|>\n\n",
    response_part = "<|start_header_id|>assistant<|end_header_id|>\n\n",
)

tokenizer.decode(trainer.train_dataset[5]["input_ids"])

space = tokenizer(" ", add_special_tokens = False).input_ids[0]
tokenizer.decode([space if x == -100 else x for x in trainer.train_dataset[5]["labels"]])

gpu_stats = torch.cuda.get_device_properties(0)
start_gpu_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
max_memory = round(gpu_stats.total_memory / 1024 / 1024 / 1024, 3)
print(f"GPU = {gpu_stats.name}. Max memory = {max_memory} GB.")
print(f"{start_gpu_memory} GB of memory reserved.")

trainer_stats = trainer.train()

used_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
used_memory_for_lora = round(used_memory - start_gpu_memory, 3)
used_percentage = round(used_memory / max_memory * 100, 3)
lora_percentage = round(used_memory_for_lora / max_memory * 100, 3)
print(f"{trainer_stats.metrics['train_runtime']} seconds used for training.")
print(
    f"{round(trainer_stats.metrics['train_runtime']/60, 2)} minutes used for training."
)
print(f"Peak reserved memory = {used_memory} GB.")
print(f"Peak reserved memory for training = {used_memory_for_lora} GB.")
print(f"Peak reserved memory % of max memory = {used_percentage} %.")
print(f"Peak reserved memory for training % of max memory = {lora_percentage} %.")

tokenizer = get_chat_template(
    tokenizer,
    chat_template = "llama-3.1",
)
FastLanguageModel.for_inference(model)

messages = [
    {"role": "user", "content": "Who is at risk for Wilms Tumor and Other Childhood Kidney Tumors?"},
]
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize = True,
    add_generation_prompt = True,
    return_tensors = "pt",
).to("cuda")

outputs = model.generate(input_ids = inputs, max_new_tokens = 64, use_cache = True,
                         temperature = 1.5, min_p = 0.1)
tokenizer.batch_decode(outputs)

"""
Saving, loading finetuned models
"""

model.save_pretrained("tech3_lora_model")  # Local saving
tokenizer.save_pretrained("tech3_lora_model")  # Local saving
model.push_to_hub("repo/tech3_lora_model", token = "hugging-face-pat") # Online saving
tokenizer.push_to_hub("repo/tech3_lora_model", token = "hugging-face-pat") # Online saving