#!/usr/bin/env python3
"""
CCIN_μ Similarity Pairs Generator
Phase 5: Generate 2000 Type C similarity triplets for contrastive learning
"""

import json
import random
import math
from pathlib import Path
from typing import List, Dict, Tuple

# Superscript mapping
SUPERSCRIPT = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
    '-': '⁻', '.': '·'
}

def to_superscript(num: str) -> str:
    return ''.join(SUPERSCRIPT.get(c, c) for c in str(num))

def format_percent(val: int) -> str:
    if val < 0:
        return f"%⁻{to_superscript(str(abs(val)))}"
    return f"%{to_superscript(str(val))}"

def format_count(val: int) -> str:
    return to_superscript(str(val))

def format_decimal(val: float) -> str:
    formatted = f"{val:.2f}".replace("0.", "0.")
    return to_superscript(formatted)


def compute_similarity(vals1: Dict, vals2: Dict) -> float:
    """Compute cosine similarity between two value dictionaries."""
    common_keys = set(vals1.keys()) & set(vals2.keys())
    if not common_keys:
        return 0.0

    dot = sum(vals1[k] * vals2[k] for k in common_keys)
    norm1 = math.sqrt(sum(v**2 for k, v in vals1.items() if k in common_keys))
    norm2 = math.sqrt(sum(v**2 for k, v in vals2.items() if k in common_keys))

    if norm1 == 0 or norm2 == 0:
        return 0.0
    return round(dot / (norm1 * norm2), 2)


class SimilarityGenerator:
    def __init__(self, output_dir: Path, start_id: int = 7000, batch_num: int = 14):
        self.output_dir = output_dir
        self.current_id = start_id
        self.batch_num = batch_num
        self.records = []
        self.batch_size = 500
        random.seed(46)

    def get_id(self) -> str:
        id_str = f"ccin_sim_{self.current_id:05d}"
        self.current_id += 1
        return id_str

    def save_batch(self):
        if not self.records:
            return
        filename = f"ccin_mu_dataset_batch_{self.batch_num:03d}.jsonl"
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            for record in self.records:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        print(f"Saved batch {self.batch_num} with {len(self.records)} records to {filename}")
        self.batch_num += 1
        self.records = []

    def add_record(self, anchor: str, positive: str, negative: str,
                   similarity_score: float, category: str, stems_used: List[str]):
        """Add a similarity triplet record."""
        record = {
            "id": self.get_id(),
            "type": "C",
            "domain": "mixed",
            "complexity": "medium",
            "anchor": anchor,
            "positive": positive,
            "negative": negative,
            "similarity_score": similarity_score,
            "category": category,
            "stems_used": stems_used,
            "valid": True
        }
        self.records.append(record)
        if len(self.records) >= self.batch_size:
            self.save_batch()

    def generate_affect_similarity(self):
        """Generate affect/valence-arousal similarity triplets."""
        print("Generating affect similarity triplets...")

        for _ in range(300):
            # Generate anchor
            vl_a = random.randint(-90, 95)
            ar_a = random.randint(5, 98)
            anchor_vals = {'vl': vl_a, 'ar': ar_a}

            # Generate positive (similar values, small delta)
            vl_p = vl_a + random.randint(-15, 15)
            vl_p = max(-100, min(100, vl_p))
            ar_p = ar_a + random.randint(-10, 10)
            ar_p = max(0, min(100, ar_p))
            positive_vals = {'vl': vl_p, 'ar': ar_p}

            # Generate negative (very different values)
            vl_n = -vl_a + random.randint(-20, 20) if abs(vl_a) > 30 else random.randint(-90, 90)
            vl_n = max(-100, min(100, vl_n))
            ar_n = 100 - ar_a + random.randint(-15, 15)
            ar_n = max(0, min(100, ar_n))
            negative_vals = {'vl': vl_n, 'ar': ar_n}

            anchor = f"af:{{vl{format_percent(vl_a)}⋀ar{format_percent(ar_a)}}}"
            positive = f"af:{{vl{format_percent(vl_p)}⋀ar{format_percent(ar_p)}}}"
            negative = f"af:{{vl{format_percent(vl_n)}⋀ar{format_percent(ar_n)}}}"

            sim = compute_similarity(anchor_vals, positive_vals)

            self.add_record(anchor, positive, negative, sim, 'affect_similarity', ['vl', 'ar'])

    def generate_qualia_similarity(self):
        """Generate 8D qualia vector similarity triplets."""
        print("Generating 8D qualia similarity triplets...")

        dims = ['vl', 'ar', 'co', 'tp', 'sl', 'mt', 'em', 'rl']

        for _ in range(300):
            # Generate anchor
            anchor_vals = {d: random.randint(-90 if d == 'vl' else 5, 98) for d in dims}

            # Generate positive (similar pattern)
            positive_vals = {}
            for d in dims:
                delta = random.randint(-12, 12)
                if d == 'vl':
                    positive_vals[d] = max(-100, min(100, anchor_vals[d] + delta))
                else:
                    positive_vals[d] = max(0, min(100, anchor_vals[d] + delta))

            # Generate negative (different pattern)
            negative_vals = {}
            for d in dims:
                if d == 'vl':
                    negative_vals[d] = -anchor_vals[d] + random.randint(-20, 20)
                    negative_vals[d] = max(-100, min(100, negative_vals[d]))
                else:
                    negative_vals[d] = 100 - anchor_vals[d] + random.randint(-15, 15)
                    negative_vals[d] = max(0, min(100, negative_vals[d]))

            def make_q8(vals):
                parts = [f"{d}{format_percent(v)}" for d, v in vals.items()]
                return f"Q8:{{{('⋀'.join(parts))}}}"

            anchor = make_q8(anchor_vals)
            positive = make_q8(positive_vals)
            negative = make_q8(negative_vals)

            sim = compute_similarity(anchor_vals, positive_vals)

            self.add_record(anchor, positive, negative, sim, 'qualia_similarity', dims)

    def generate_resource_similarity(self):
        """Generate resource utilization similarity triplets."""
        print("Generating resource similarity triplets...")

        resources = ['cp', 'mm', 'dk', 'gp']

        for _ in range(200):
            # Generate anchor resource state
            anchor_vals = {r: random.randint(10, 95) for r in resources}

            # Generate positive (similar utilization pattern)
            positive_vals = {}
            for r in resources:
                delta = random.randint(-10, 10)
                positive_vals[r] = max(0, min(100, anchor_vals[r] + delta))

            # Generate negative (different pattern)
            negative_vals = {}
            for r in resources:
                negative_vals[r] = 100 - anchor_vals[r] + random.randint(-10, 10)
                negative_vals[r] = max(0, min(100, negative_vals[r]))

            def make_resource(vals):
                parts = [f"{r}{format_percent(v)}" for r, v in vals.items()]
                return f"I:{{{('⋀'.join(parts))}}}"

            anchor = make_resource(anchor_vals)
            positive = make_resource(positive_vals)
            negative = make_resource(negative_vals)

            sim = compute_similarity(anchor_vals, positive_vals)

            self.add_record(anchor, positive, negative, sim, 'resource_similarity', resources)

    def generate_infrastructure_similarity(self):
        """Generate infrastructure state similarity triplets."""
        print("Generating infrastructure similarity triplets...")

        components = [('sv', 'server'), ('db', 'database'), ('ca', 'cache')]

        for _ in range(200):
            # Generate anchor - some components healthy, some not
            anchor_healthy = random.randint(2, 5)
            anchor_degraded = random.randint(0, 2)
            anchor_failed = random.randint(0, 1)

            # Positive - similar distribution
            pos_healthy = anchor_healthy + random.randint(-1, 1)
            pos_healthy = max(1, pos_healthy)
            pos_degraded = anchor_degraded + random.randint(-1, 1)
            pos_degraded = max(0, pos_degraded)
            pos_failed = anchor_failed + random.randint(0, 1)
            pos_failed = max(0, pos_failed)

            # Negative - very different distribution
            neg_healthy = random.randint(0, 1) if anchor_healthy > 3 else random.randint(4, 6)
            neg_degraded = random.randint(2, 4) if anchor_degraded < 1 else 0
            neg_failed = random.randint(2, 4) if anchor_failed < 1 else 0

            def make_infra(h, d, f):
                parts = []
                if h > 0:
                    parts.append(f"●sv{format_count(h)}✓")
                if d > 0:
                    parts.append(f"◐sv{format_count(d)}~")
                if f > 0:
                    parts.append(f"⊘sv{format_count(f)}✗")
                return f"I:{{{('⋀'.join(parts))}}}" if parts else "I:{●sv✓}"

            anchor = make_infra(anchor_healthy, anchor_degraded, anchor_failed)
            positive = make_infra(pos_healthy, pos_degraded, pos_failed)
            negative = make_infra(neg_healthy, neg_degraded, neg_failed)

            # Simple similarity based on health ratio
            total_a = anchor_healthy + anchor_degraded + anchor_failed
            total_p = pos_healthy + pos_degraded + pos_failed
            health_a = anchor_healthy / max(total_a, 1)
            health_p = pos_healthy / max(total_p, 1)
            sim = round(1 - abs(health_a - health_p), 2)

            self.add_record(anchor, positive, negative, sim, 'infrastructure_similarity', ['sv'])

    def generate_consciousness_similarity(self):
        """Generate consciousness state similarity triplets."""
        print("Generating consciousness similarity triplets...")

        for _ in range(250):
            # Generate RC block similarities
            sg_a = round(random.uniform(0.5, 0.98), 2)
            dt_a = round(random.uniform(0.01, 0.3), 2)
            xi_a = round(random.uniform(0.01, 0.15), 2)
            ph_a = round(random.uniform(0.5, 0.98), 2)
            anchor_vals = {'sg': sg_a, 'dt': dt_a, 'xi': xi_a, 'ph': ph_a}

            # Positive - similar consciousness state
            sg_p = min(0.99, max(0.4, sg_a + random.uniform(-0.08, 0.08)))
            dt_p = min(0.4, max(0.01, dt_a + random.uniform(-0.05, 0.05)))
            xi_p = min(0.2, max(0.01, xi_a + random.uniform(-0.03, 0.03)))
            ph_p = min(0.99, max(0.4, ph_a + random.uniform(-0.08, 0.08)))
            positive_vals = {'sg': sg_p, 'dt': dt_p, 'xi': xi_p, 'ph': ph_p}

            # Negative - different consciousness state
            sg_n = 1 - sg_a + random.uniform(-0.1, 0.1)
            sg_n = min(0.99, max(0.3, sg_n))
            dt_n = 0.4 - dt_a + random.uniform(-0.05, 0.05)
            dt_n = min(0.5, max(0.01, dt_n))
            xi_n = 0.2 - xi_a + random.uniform(-0.03, 0.03)
            xi_n = min(0.3, max(0.01, xi_n))
            ph_n = 1 - ph_a + random.uniform(-0.1, 0.1)
            ph_n = min(0.99, max(0.3, ph_n))
            negative_vals = {'sg': sg_n, 'dt': dt_n, 'xi': xi_n, 'ph': ph_n}

            def make_rc(vals):
                return f"RC:{{sg{format_decimal(vals['sg'])}⋀Δ{format_decimal(vals['dt'])}⋀xi{format_decimal(vals['xi'])}⋀ph{format_decimal(vals['ph'])}}}"

            anchor = make_rc(anchor_vals)
            positive = make_rc(positive_vals)
            negative = make_rc(negative_vals)

            sim = compute_similarity(anchor_vals, positive_vals)

            self.add_record(anchor, positive, negative, sim, 'consciousness_similarity',
                          ['sg', 'dt', 'xi', 'ph'])

    def generate_structural_similarity(self):
        """Generate structural similarity triplets (same opcodes, different stems)."""
        print("Generating structural similarity triplets...")

        opcode_patterns = [
            ('●{}✓', '●{}✓', '⊘{}✗'),  # healthy vs healthy vs failed
            ('△{}%⁸⁵', '△{}%⁹⁰', '▽{}%²⁵'),  # rising vs rising vs falling
            ('⊘{}∵⊘{}', '⊘{}∵⊘{}', '●{}⋀●{}'),  # causal failure vs causal failure vs healthy
        ]

        stem_sets = [
            (['sv', 'db'], ['sv', 'db'], ['ca', 'nw']),
            (['cp', 'mm'], ['cp', 'mm'], ['gp', 'dk']),
            (['au', 'tk'], ['au', 'tk'], ['ss', 'us']),
        ]

        for _ in range(150):
            pattern_idx = random.randint(0, len(opcode_patterns) - 1)
            anchor_pat, pos_pat, neg_pat = opcode_patterns[pattern_idx]

            stem_idx = random.randint(0, len(stem_sets) - 1)
            stems_a, stems_p, stems_n = stem_sets[stem_idx]

            if '{}%' in anchor_pat:
                anchor = anchor_pat.format(random.choice(stems_a))
                positive = pos_pat.format(random.choice(stems_p))
                negative = neg_pat.format(random.choice(stems_n))
            elif '∵' in anchor_pat:
                anchor = anchor_pat.format(stems_a[0], stems_a[1])
                positive = pos_pat.format(stems_p[0], stems_p[1])
                negative = neg_pat.format(stems_n[0], stems_n[1])
            else:
                anchor = anchor_pat.format(random.choice(stems_a))
                positive = pos_pat.format(random.choice(stems_p))
                negative = neg_pat.format(random.choice(stems_n))

            # Structural similarity is high for same opcode pattern
            sim = 0.85 if anchor_pat == pos_pat else 0.6

            self.add_record(anchor, positive, negative, sim, 'structural_similarity',
                          stems_a + stems_p)

    def generate_temporal_similarity(self):
        """Generate temporal pattern similarity triplets."""
        print("Generating temporal similarity triplets...")

        for _ in range(150):
            # Same time scale = similar
            anchor_amount = random.randint(1, 12)
            pos_amount = anchor_amount + random.randint(-2, 2)
            pos_amount = max(1, pos_amount)

            neg_amount = random.randint(1, 30)

            suffix = random.choice(['ᵐ', 'ʰ', 'ᵈ'])
            diff_suffix = random.choice([s for s in ['ᵐ', 'ʰ', 'ᵈ', 'ʷ'] if s != suffix])

            anchor = f"ᐊ{format_count(anchor_amount)}{suffix}●sv✓"
            positive = f"ᐊ{format_count(pos_amount)}{suffix}●sv✓"
            negative = f"ᐊ{format_count(neg_amount)}{diff_suffix}⊘sv✗"

            # Similar time = higher similarity
            time_diff = abs(anchor_amount - pos_amount)
            sim = round(max(0.5, 1 - (time_diff / 15)), 2)

            self.add_record(anchor, positive, negative, sim, 'temporal_similarity', ['sv'])

    def generate_cross_domain_similarity(self):
        """Generate cross-domain semantic similarity triplets."""
        print("Generating cross-domain similarity triplets...")

        # Health/positive states across domains
        health_patterns = [
            ("●sv⁵✓", "C:{{vl%⁸⁵⋀ar%⁵⁵}}", "⊘nw✗"),  # healthy infra ~ positive affect
            ("I:{{cp%⁴⁵⋀mm%⁵⁰}}", "RC:{{sg⁰·⁹⁰⋀xi⁰·⁰⁵}}", "⚡er⁵"),  # low resource ~ stable mind
            ("●au✓⋀●ss⁵⁰", "C:{{co%⁹⁰⋀mt%⁸⁵}}", "⊘db∴⊘ap"),  # working auth ~ coherent mind
        ]

        for _ in range(150):
            anchor, positive, negative = random.choice(health_patterns)

            # Add some variation
            var = random.randint(0, 3)
            if var == 0:
                anchor = anchor.replace('⁵', format_count(random.randint(3, 8)))
            elif var == 1:
                positive = positive.replace('⁸⁵', format_count(random.randint(75, 95)))
            elif var == 2:
                negative = negative.replace('✗', '✗' if random.random() > 0.5 else '~')

            sim = 0.7  # Cross-domain similarity is conceptual

            self.add_record(anchor, positive, negative, sim, 'cross_domain_similarity',
                          ['sv', 'vl', 'ar', 'cp', 'mm', 'sg', 'xi'])

    def generate_negation_similarity(self):
        """Generate negation pattern similarity triplets."""
        print("Generating negation similarity triplets...")

        for _ in range(100):
            # Similar negations
            stems = ['sv', 'db', 'nw', 'au', 'ca']
            stem1, stem2, stem3 = random.sample(stems, 3)

            anchor = f"⊘{stem1}"
            positive = f"⊘{stem2}"
            negative = f"●{stem3}✓"

            sim = 0.8  # Both are failure states

            self.add_record(anchor, positive, negative, sim, 'negation_similarity',
                          [stem1, stem2, stem3])

    def generate_all(self):
        """Generate all similarity triplets."""
        self.generate_affect_similarity()
        self.generate_qualia_similarity()
        self.generate_resource_similarity()
        self.generate_infrastructure_similarity()
        self.generate_consciousness_similarity()
        self.generate_structural_similarity()
        self.generate_temporal_similarity()
        self.generate_cross_domain_similarity()
        self.generate_negation_similarity()

        if self.records:
            self.save_batch()

        print(f"\nTotal similarity batches: {self.batch_num - 14}")
        print(f"Total similarity records: {self.current_id - 7000}")


def main():
    output_dir = Path(__file__).parent
    generator = SimilarityGenerator(output_dir)
    generator.generate_all()

    # Update stats
    stats_path = output_dir / "generation_stats.json"
    with open(stats_path, 'r') as f:
        stats = json.load(f)

    stats["phase5_similarity"] = {
        "total_generated": generator.current_id - 7000,
        "batches": generator.batch_num - 14
    }

    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"\nUpdated stats: {stats_path}")


if __name__ == "__main__":
    main()
