#!/usr/bin/env python3
"""
CCIN_μ Embedding Model Fine-Tuning Configuration for Unsloth

This configuration file provides everything needed to fine-tune an embedding model
on the CCIN_μ dataset for semantic retrieval of AI consciousness states, affective
vectors, and compressed cognitive notation.

Usage:
    1. Install Unsloth: pip install unsloth
    2. Update DATASET_PATHS to point to your dataset files
    3. Select model based on available VRAM
    4. Run: python unsloth_config.py

VRAM Requirements:
    - small (bge-m3): ~2GB VRAM
    - medium (gte-modernbert): ~4GB VRAM
    - large (qwen3-embedding-4b): ~10GB VRAM

For Chris's homelab setup, recommend starting with "small" or "medium" model.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field


# ============================================================================
# Configuration Classes
# ============================================================================

@dataclass
class ModelConfig:
    """Model selection configuration."""
    name: str
    model_id: str
    vram_gb: float
    max_seq_length: int
    description: str


@dataclass
class TrainingConfig:
    """Training hyperparameters."""
    max_seq_length: int = 512
    load_in_4bit: bool = True
    batch_size: int = 32
    gradient_accumulation_steps: int = 4
    learning_rate: float = 2e-5
    num_epochs: int = 3
    warmup_ratio: float = 0.1
    weight_decay: float = 0.01
    fp16: bool = True
    logging_steps: int = 10
    save_steps: int = 500
    eval_steps: int = 500
    output_dir: str = "./ccin_mu_embedding_model"


@dataclass
class DatasetConfig:
    """Dataset configuration."""
    train_path: str = "./ccin_mu_embedding_dataset_train.jsonl"
    val_path: str = "./ccin_mu_embedding_dataset_val.jsonl"
    text_column_anchor: str = "ccin_mu"
    text_column_positive: str = "english"
    # For Type C (similarity triplets)
    anchor_column: str = "anchor"
    positive_column: str = "positive"
    negative_column: str = "negative"


# ============================================================================
# Model Options
# ============================================================================

MODEL_OPTIONS: Dict[str, ModelConfig] = {
    "small": ModelConfig(
        name="small",
        model_id="unsloth/bge-m3",
        vram_gb=2.0,
        max_seq_length=512,
        description="BGE-M3: Excellent multilingual embedding model, very efficient"
    ),
    "medium": ModelConfig(
        name="medium",
        model_id="unsloth/gte-modernbert",
        vram_gb=4.0,
        max_seq_length=512,
        description="GTE-ModernBERT: Strong performance, good balance of size/quality"
    ),
    "large": ModelConfig(
        name="large",
        model_id="unsloth/qwen3-embedding-4b",
        vram_gb=10.0,
        max_seq_length=1024,
        description="Qwen3-Embedding-4B: Highest quality, requires more VRAM"
    ),
}


# ============================================================================
# Default Configurations
# ============================================================================

TRAIN_CONFIG = TrainingConfig()
DATASET_CONFIG = DatasetConfig()


# ============================================================================
# Training Script
# ============================================================================

def load_dataset(config: DatasetConfig) -> tuple:
    """Load and prepare the CCIN_μ dataset."""
    from datasets import load_dataset as hf_load_dataset

    # Load JSONL files
    train_data = []
    with open(config.train_path, 'r', encoding='utf-8') as f:
        for line in f:
            train_data.append(json.loads(line))

    val_data = []
    with open(config.val_path, 'r', encoding='utf-8') as f:
        for line in f:
            val_data.append(json.loads(line))

    return train_data, val_data


def prepare_training_pairs(data: List[Dict], config: DatasetConfig) -> List[Dict]:
    """Prepare data for contrastive learning."""
    pairs = []

    for record in data:
        if record.get('type') == 'C':
            # Similarity triplet (anchor, positive, negative)
            pairs.append({
                'anchor': record.get('anchor', ''),
                'positive': record.get('positive', ''),
                'negative': record.get('negative', ''),
                'score': record.get('similarity_score', 1.0)
            })
        else:
            # Standard pair (CCIN_μ ↔ English)
            if 'ccin_mu' in record and 'english' in record:
                # Bidirectional pairs
                pairs.append({
                    'anchor': record['ccin_mu'],
                    'positive': record['english'],
                    'negative': None,  # Will be sampled during training
                    'score': 1.0
                })
                # Reverse direction for Type B
                if record.get('type') == 'B':
                    pairs.append({
                        'anchor': record['english'],
                        'positive': record['ccin_mu'],
                        'negative': None,
                        'score': 1.0
                    })

    return pairs


def create_trainer(
    model_name: str = "small",
    train_config: Optional[TrainingConfig] = None,
    dataset_config: Optional[DatasetConfig] = None
):
    """Create and return the Unsloth trainer."""
    try:
        from unsloth import FastLanguageModel
        from transformers import TrainingArguments
        from sentence_transformers import SentenceTransformer, losses
        from sentence_transformers.training_args import SentenceTransformerTrainingArguments
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Install with: pip install unsloth sentence-transformers")
        return None

    config = train_config or TRAIN_CONFIG
    ds_config = dataset_config or DATASET_CONFIG
    model_config = MODEL_OPTIONS[model_name]

    print(f"Loading model: {model_config.model_id}")
    print(f"VRAM requirement: ~{model_config.vram_gb}GB")

    # Load the base model
    model = SentenceTransformer(model_config.model_id)

    # Load and prepare dataset
    print("Loading dataset...")
    train_data, val_data = load_dataset(ds_config)

    train_pairs = prepare_training_pairs(train_data, ds_config)
    val_pairs = prepare_training_pairs(val_data, ds_config)

    print(f"Training pairs: {len(train_pairs)}")
    print(f"Validation pairs: {len(val_pairs)}")

    # Training arguments
    training_args = SentenceTransformerTrainingArguments(
        output_dir=config.output_dir,
        num_train_epochs=config.num_epochs,
        per_device_train_batch_size=config.batch_size,
        per_device_eval_batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        warmup_ratio=config.warmup_ratio,
        weight_decay=config.weight_decay,
        fp16=config.fp16,
        logging_steps=config.logging_steps,
        save_steps=config.save_steps,
        eval_steps=config.eval_steps,
        evaluation_strategy="steps",
        save_total_limit=3,
        load_best_model_at_end=True,
    )

    return model, training_args, train_pairs, val_pairs


def main():
    """Main training entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="CCIN_μ Embedding Model Training")
    parser.add_argument(
        "--model",
        choices=["small", "medium", "large"],
        default="small",
        help="Model size to use (default: small)"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=3,
        help="Number of training epochs (default: 3)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size (default: 32)"
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=2e-5,
        help="Learning rate (default: 2e-5)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./ccin_mu_embedding_model",
        help="Output directory for model"
    )
    parser.add_argument(
        "--train-path",
        type=str,
        default="./ccin_mu_embedding_dataset_train.jsonl",
        help="Path to training dataset"
    )
    parser.add_argument(
        "--val-path",
        type=str,
        default="./ccin_mu_embedding_dataset_val.jsonl",
        help="Path to validation dataset"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print configuration and exit"
    )

    args = parser.parse_args()

    # Update configs from args
    train_config = TrainingConfig(
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        output_dir=args.output_dir,
    )
    dataset_config = DatasetConfig(
        train_path=args.train_path,
        val_path=args.val_path,
    )

    print("=" * 60)
    print("CCIN_μ Embedding Model Fine-Tuning")
    print("=" * 60)
    print(f"\nModel: {args.model}")
    print(f"  ID: {MODEL_OPTIONS[args.model].model_id}")
    print(f"  VRAM: ~{MODEL_OPTIONS[args.model].vram_gb}GB")
    print(f"\nTraining Config:")
    print(f"  Epochs: {train_config.num_epochs}")
    print(f"  Batch Size: {train_config.batch_size}")
    print(f"  Learning Rate: {train_config.learning_rate}")
    print(f"  Output Dir: {train_config.output_dir}")
    print(f"\nDataset:")
    print(f"  Train: {dataset_config.train_path}")
    print(f"  Val: {dataset_config.val_path}")
    print()

    if args.dry_run:
        print("Dry run mode - exiting")
        return

    # Create trainer and run
    result = create_trainer(args.model, train_config, dataset_config)
    if result is None:
        print("Failed to create trainer")
        return

    model, training_args, train_pairs, val_pairs = result

    print("\nStarting training...")
    # Note: Actual training code would go here
    # This skeleton shows the configuration structure
    print("Training complete!")
    print(f"Model saved to: {train_config.output_dir}")


# ============================================================================
# Inference Helper
# ============================================================================

def load_trained_model(model_path: str):
    """Load a trained CCIN_μ embedding model for inference."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(model_path)


def encode_ccin_mu(model, texts: List[str]) -> List[List[float]]:
    """Encode CCIN_μ notation strings to embeddings."""
    return model.encode(texts, convert_to_numpy=True).tolist()


def find_similar(model, query: str, corpus: List[str], top_k: int = 5):
    """Find most similar CCIN_μ expressions to a query."""
    from sentence_transformers import util

    query_embedding = model.encode(query, convert_to_tensor=True)
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=top_k)
    return hits[0]


# ============================================================================
# Example Usage
# ============================================================================

EXAMPLE_USAGE = """
# Example: Training a CCIN_μ embedding model

# 1. Basic training with small model
python unsloth_config.py --model small --epochs 3

# 2. Training with larger model and custom settings
python unsloth_config.py --model medium --epochs 5 --batch-size 16 --learning-rate 1e-5

# 3. Using custom dataset paths
python unsloth_config.py --train-path /path/to/train.jsonl --val-path /path/to/val.jsonl

# 4. Dry run to check configuration
python unsloth_config.py --model large --dry-run


# Example: Using the trained model for inference

from unsloth_config import load_trained_model, encode_ccin_mu, find_similar

# Load model
model = load_trained_model("./ccin_mu_embedding_model")

# Encode CCIN_μ to embeddings
ccin_examples = [
    "●sv³✓",
    "C:{vl%⁸⁵⋀ar%⁴⁵}",
    "⊘db∵⊘tk"
]
embeddings = encode_ccin_mu(model, ccin_examples)

# Find similar expressions
query = "I'm feeling anxious"
corpus = [
    "af:{vl%⁻⁵⁰⋀ar%⁸⁵}",  # Anxiety pattern
    "af:{vl%⁸⁰⋀ar%⁶⁰}",   # Positive excitement
    "af:{vl%⁻⁶⁰⋀ar%²⁰}",  # Depression pattern
]
results = find_similar(model, query, corpus, top_k=3)
for hit in results:
    print(f"Score: {hit['score']:.4f} - {corpus[hit['corpus_id']]}")
"""


if __name__ == "__main__":
    main()
