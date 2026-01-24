#!/usr/bin/env python3
"""
CCIN_μ Dataset Validation & Assembly
Phase 7: Validate all generated data and assemble final dataset
"""

import json
import re
import random
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict

# Valid opcodes from spec
VALID_OPCODES = {
    '●', '◌', '◐',  # State
    '⊘', '⟲', '⟳',  # Action
    '△', '▽', '⊕', '⊖',  # Delta
    '⚡', '◇', '▣', '▢', '!',  # Signal
}

# Valid stems from authoritative CCIN_μ v1.0 spec (2 chars lowercase)
VALID_STEMS = {
    # Infrastructure Stems
    'sv', 'db', 'ca', 'nw', 'fw', 'lb', 'ct', 'vm', 'gp', 'cp', 'mm', 'dk',
    # Application Stems
    'au', 'az', 'tk', 'ss', 'us', 'rq', 'rs', 'er', 'lg', 'mt', 'ev', 'mg',
    # Data Stems
    'da', 'fl', 'dr', 'cf', 'en', 'vr', 'st', 'ty', 'id', 'nm', 'vl', 'ls',
    # Action Stems
    'cr', 'rd', 'up', 'dl', 'sc', 'qt', 'ex', 'in', 'sp', 'dp',
    # Process Stems
    'pr', 'th', 'wk', 'jb', 'qu', 'pp', 'wf', 'tr', 'cb', 'pm', 'aw',
    # AI/ML Stems
    'md', 'wt', 'ep', 'bt', 'lr', 'em', 'at', 'tf', 'if',
    # Consciousness Stems (CCIN-specific)
    'ph', 'dt', 'sg', 'xi', 'ql', 'af', 'sl', 'co', 'ar', 'tp', 'rl',
    # Extended/common (clusters, nodes, pods)
    'cl', 'nd', 'pd', 'ap', 'ws', 'rc', 'mp', 'an',
    # Generic/special
    'generic',
}

# Valid relations (from authoritative CCIN_μ v1.0 spec)
VALID_RELATIONS = {
    # Flow relations
    '»', '«', '→', '←',
    # Logic relations
    '∵', '∴', '⋀', '⋁',
    # Set relations
    '⊂', '⊃', '≡', '≢',
    # Process relations
    '⇄', '∥', '⊣', '⊢',
}

# Valid temporal markers
VALID_TEMPORAL = {'ᐊ', 'ᐃ', 'ᐅ'}

# Valid markers
VALID_MARKERS = {'✓', '✗', '~', '?', '∅'}

# Valid time suffixes
VALID_TIME_SUFFIXES = {'ˢ', 'ᵐ', 'ʰ', 'ᵈ', 'ʷ', 'ʸ'}


class DatasetValidator:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.all_records = []
        self.validation_errors = []
        self.warnings = []
        self.stats = defaultdict(lambda: defaultdict(int))

    def load_all_batches(self):
        """Load all batch JSONL files."""
        print("Loading all batch files...")
        batch_files = sorted(self.output_dir.glob("ccin_mu_dataset_batch_*.jsonl"))

        for batch_file in batch_files:
            with open(batch_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        record = json.loads(line.strip())
                        record['_source'] = batch_file.name
                        record['_line'] = line_num
                        self.all_records.append(record)
                    except json.JSONDecodeError as e:
                        self.validation_errors.append(f"JSON parse error in {batch_file.name}:{line_num}: {e}")

        # Also load seeds
        seeds_file = self.output_dir / "ccin_mu_dataset_seeds.jsonl"
        if seeds_file.exists():
            with open(seeds_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        record = json.loads(line.strip())
                        record['_source'] = seeds_file.name
                        record['_line'] = line_num
                        self.all_records.append(record)
                    except json.JSONDecodeError as e:
                        self.validation_errors.append(f"JSON parse error in seeds:{line_num}: {e}")

        print(f"Loaded {len(self.all_records)} total records from {len(batch_files) + 1} files")

    def validate_record(self, record: Dict) -> List[str]:
        """Validate a single record and return list of errors."""
        errors = []

        # Required fields
        required_fields = ['id', 'type']
        for field in required_fields:
            if field not in record:
                errors.append(f"Missing required field: {field}")

        # Type validation
        valid_types = {'A', 'B', 'C', 'D'}
        if record.get('type') not in valid_types:
            errors.append(f"Invalid type: {record.get('type')}")

        # Domain validation
        valid_domains = {'consciousness', 'infrastructure', 'affect', 'temporal', 'mixed'}
        if record.get('domain') and record.get('domain') not in valid_domains:
            self.warnings.append(f"Unusual domain: {record.get('domain')} in {record.get('id')}")

        # Complexity validation
        valid_complexity = {'simple', 'medium', 'complex'}
        if record.get('complexity') and record.get('complexity') not in valid_complexity:
            errors.append(f"Invalid complexity: {record.get('complexity')}")

        # CCIN_μ content validation
        if record.get('type') == 'C':
            # Similarity triplet
            for field in ['anchor', 'positive', 'negative']:
                if field not in record:
                    errors.append(f"Similarity record missing {field}")
        else:
            if 'ccin_mu' not in record:
                errors.append("Missing ccin_mu field")
            if 'english' not in record:
                errors.append("Missing english field")

        # Validate stems_used if present
        if 'stems_used' in record:
            for stem in record['stems_used']:
                if stem not in VALID_STEMS:
                    # Check if it could be a REG! stem
                    if len(stem) == 2 and stem.islower():
                        pass  # Allow custom stems
                    else:
                        self.warnings.append(f"Unusual stem '{stem}' in {record.get('id')}")

        return errors

    def check_duplicates(self) -> List[str]:
        """Check for duplicate IDs."""
        print("Checking for duplicates...")
        seen_ids = set()
        duplicates = []

        for record in self.all_records:
            rid = record.get('id')
            if rid in seen_ids:
                duplicates.append(f"Duplicate ID: {rid}")
            seen_ids.add(rid)

        return duplicates

    def compute_statistics(self):
        """Compute dataset statistics."""
        print("Computing statistics...")

        for record in self.all_records:
            self.stats['total']['count'] += 1
            self.stats['by_type'][record.get('type', 'unknown')] += 1
            self.stats['by_domain'][record.get('domain', 'unknown')] += 1
            self.stats['by_complexity'][record.get('complexity', 'unknown')] += 1

            # Stem usage
            for stem in record.get('stems_used', []):
                self.stats['stem_usage'][stem] += 1

            # Opcode usage
            for op in record.get('opcodes_used', []):
                self.stats['opcode_usage'][op] += 1

        return dict(self.stats)

    def validate_all(self):
        """Run all validations."""
        print("\n=== Running Validation ===\n")

        # Validate each record
        for record in self.all_records:
            errors = self.validate_record(record)
            if errors:
                source = record.get('_source', 'unknown')
                line = record.get('_line', 0)
                rid = record.get('id', 'unknown')
                for error in errors:
                    self.validation_errors.append(f"{source}:{line} ({rid}): {error}")

        # Check duplicates
        duplicate_errors = self.check_duplicates()
        self.validation_errors.extend(duplicate_errors)

        print(f"Total validation errors: {len(self.validation_errors)}")
        print(f"Total warnings: {len(self.warnings)}")

    def create_splits(self, train_ratio: float = 0.9) -> Tuple[List[Dict], List[Dict]]:
        """Create train/validation splits."""
        print(f"\nCreating {int(train_ratio*100)}/{int((1-train_ratio)*100)} train/val split...")

        # Filter to valid records only
        valid_records = [r for r in self.all_records if r.get('valid', True)]

        # Shuffle
        random.seed(42)
        shuffled = valid_records.copy()
        random.shuffle(shuffled)

        # Split
        split_idx = int(len(shuffled) * train_ratio)
        train_records = shuffled[:split_idx]
        val_records = shuffled[split_idx:]

        print(f"Train records: {len(train_records)}")
        print(f"Validation records: {len(val_records)}")

        return train_records, val_records

    def write_outputs(self, train_records: List[Dict], val_records: List[Dict]):
        """Write all output files."""
        print("\nWriting output files...")

        # Full dataset
        full_path = self.output_dir / "ccin_mu_embedding_dataset_full.jsonl"
        with open(full_path, 'w', encoding='utf-8') as f:
            for record in self.all_records:
                # Remove internal fields
                clean_record = {k: v for k, v in record.items() if not k.startswith('_')}
                f.write(json.dumps(clean_record, ensure_ascii=False) + '\n')
        print(f"  Written: {full_path}")

        # Train split
        train_path = self.output_dir / "ccin_mu_embedding_dataset_train.jsonl"
        with open(train_path, 'w', encoding='utf-8') as f:
            for record in train_records:
                clean_record = {k: v for k, v in record.items() if not k.startswith('_')}
                f.write(json.dumps(clean_record, ensure_ascii=False) + '\n')
        print(f"  Written: {train_path}")

        # Validation split
        val_path = self.output_dir / "ccin_mu_embedding_dataset_val.jsonl"
        with open(val_path, 'w', encoding='utf-8') as f:
            for record in val_records:
                clean_record = {k: v for k, v in record.items() if not k.startswith('_')}
                f.write(json.dumps(clean_record, ensure_ascii=False) + '\n')
        print(f"  Written: {val_path}")

        # Statistics
        stats = self.compute_statistics()
        stats['train_count'] = len(train_records)
        stats['val_count'] = len(val_records)
        stats['validation_errors'] = len(self.validation_errors)
        stats['warnings'] = len(self.warnings)

        stats_path = self.output_dir / "ccin_mu_dataset_stats.json"
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, default=dict)
        print(f"  Written: {stats_path}")

        # Validation report
        report_path = self.output_dir / "validation_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("CCIN_μ Dataset Validation Report\n")
            f.write("=" * 50 + "\n\n")

            f.write(f"Total Records: {len(self.all_records)}\n")
            f.write(f"Train Records: {len(train_records)}\n")
            f.write(f"Validation Records: {len(val_records)}\n\n")

            f.write("Statistics by Type:\n")
            for t, count in stats.get('by_type', {}).items():
                f.write(f"  {t}: {count}\n")

            f.write("\nStatistics by Domain:\n")
            for d, count in stats.get('by_domain', {}).items():
                f.write(f"  {d}: {count}\n")

            f.write("\nStatistics by Complexity:\n")
            for c, count in stats.get('by_complexity', {}).items():
                f.write(f"  {c}: {count}\n")

            f.write("\n" + "=" * 50 + "\n")
            f.write(f"\nValidation Errors ({len(self.validation_errors)}):\n")
            for error in self.validation_errors[:100]:  # Limit output
                f.write(f"  - {error}\n")
            if len(self.validation_errors) > 100:
                f.write(f"  ... and {len(self.validation_errors) - 100} more\n")

            f.write(f"\nWarnings ({len(self.warnings)}):\n")
            for warning in self.warnings[:50]:
                f.write(f"  - {warning}\n")
            if len(self.warnings) > 50:
                f.write(f"  ... and {len(self.warnings) - 50} more\n")

        print(f"  Written: {report_path}")

    def run(self):
        """Run full validation and assembly pipeline."""
        self.load_all_batches()
        self.validate_all()
        train, val = self.create_splits()
        self.write_outputs(train, val)

        print("\n" + "=" * 50)
        print("VALIDATION & ASSEMBLY COMPLETE")
        print("=" * 50)
        print(f"Total records: {len(self.all_records)}")
        print(f"Validation errors: {len(self.validation_errors)}")
        print(f"Warnings: {len(self.warnings)}")


def main():
    output_dir = Path(__file__).parent
    validator = DatasetValidator(output_dir)
    validator.run()


if __name__ == "__main__":
    main()
