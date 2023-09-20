from transformers import AutoModel, AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset
import numpy as np
import mlflow
import evaluate

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

def compute_metrics(eval_pred):
    metric = evaluate.load("accuracy")
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)

    return metric.compute(predictions=predictions, references=labels)

def train():

    dataset = load_dataset("yelp_review_full")
    dataset = dataset.rename_column("label", "labels")
    tokenized_datasets = dataset.map(tokenize_function, batched = True)
    small_train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000))
    small_eval_dataset = tokenized_datasets["test"].shuffle(seed=42).select(range(1000))
    
    training_args = TrainingArguments(
        output_dir="/tmp/test_trainer",
        evaluation_strategy="epoch",
        max_steps = 10,
        num_train_epochs=1,
        per_device_train_batch_size=256,
        dataloader_num_workers=1,
        do_eval=False
    )

    model = AutoModel.from_pretrained(
        "distilbert-base-uncased",
        num_labels = 5
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=small_train_dataset,
        eval_dataset=small_eval_dataset,
        compute_metrics=compute_metrics,
    )

    with mlflow.start_run() as run:
        trainer.train()


if __name__ == "__main__":
    train()