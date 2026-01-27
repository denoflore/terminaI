#!/usr/bin/env python3
"""
CCIN_μ Similarity & 8D Qualia Expansion
Generates more Type C triplets and Type D 8D qualia vectors
"""

import json
import random
import time
import math
from pathlib import Path
from typing import List, Dict
from datetime import datetime

SUPERSCRIPT = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
    '-': '⁻', '.': '·'
}

def to_superscript(num: str) -> str:
    return ''.join(SUPERSCRIPT.get(c, c) for c in str(num))

def format_count(val: int) -> str:
    return to_superscript(str(val))

def format_percent(val: int) -> str:
    if val < 0:
        return f"%⁻{to_superscript(str(abs(val)))}"
    return f"%{to_superscript(str(val))}"

def format_decimal(val: float) -> str:
    return to_superscript(f"{val:.2f}")


class SimilarityGenerator:
    def __init__(self, output_dir: Path, start_batch: int = 91):
        self.output_dir = output_dir
        self.batch_num = start_batch
        self.records = []
        self.batch_size = 500
        self.total_generated = 0
        random.seed(int(time.time()) + 11111)

    def get_id(self) -> str:
        id_str = f"ccin_sim_{self.total_generated + 80000:05d}"
        self.total_generated += 1
        return id_str

    def save_batch(self):
        if not self.records:
            return
        filename = f"ccin_mu_dataset_batch_{self.batch_num:03d}.jsonl"
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            for record in self.records:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Saved batch {self.batch_num} with {len(self.records)} records")
        self.batch_num += 1
        self.records = []

    def add_triplet(self, anchor: str, positive: str, negative: str,
                    anchor_english: str, domain: str, stems: List[str], opcodes: List[str],
                    similarity: float = 0.9):
        record = {
            "id": self.get_id(),
            "type": "C",
            "domain": domain,
            "complexity": "medium",
            "anchor": anchor,
            "positive": positive,
            "negative": negative,
            "anchor_english": anchor_english,
            "similarity_score": similarity,
            "stems_used": stems,
            "opcodes_used": opcodes,
            "valid": True
        }
        self.records.append(record)
        if len(self.records) >= self.batch_size:
            self.save_batch()

    def add_8d_record(self, ccin: str, english: str, stems: List[str]):
        record = {
            "id": self.get_id(),
            "type": "D",
            "domain": "consciousness",
            "complexity": "complex",
            "ccin_mu": ccin,
            "english": english,
            "stems_used": stems,
            "opcodes_used": [],
            "valid": True
        }
        self.records.append(record)
        if len(self.records) >= self.batch_size:
            self.save_batch()

    # ==================== TYPE C SIMILARITY TRIPLETS ====================

    def generate_affect_similarity(self, count: int = 300):
        """Generate affect similarity triplets."""
        print(f"Generating {count} affect similarity triplets...")

        for _ in range(count):
            # Anchor affect state
            vl = random.randint(-60, 80)
            ar = random.randint(20, 90)

            anchor = f"af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}"

            # Positive: similar affect
            pos_vl = vl + random.randint(-10, 10)
            pos_ar = ar + random.randint(-10, 10)
            positive = f"af:{{vl{format_percent(pos_vl)}⋀ar{format_percent(pos_ar)}}}"

            # Negative: opposite or very different
            neg_vl = -vl if random.random() > 0.5 else vl + random.randint(30, 60) * random.choice([-1, 1])
            neg_ar = 100 - ar if random.random() > 0.5 else ar + random.randint(30, 50) * random.choice([-1, 1])
            neg_vl = max(-100, min(100, neg_vl))
            neg_ar = max(0, min(100, neg_ar))
            negative = f"af:{{vl{format_percent(neg_vl)}⋀ar{format_percent(neg_ar)}}}"

            vl_word = "positive" if vl > 0 else "negative"
            ar_word = "high" if ar > 60 else "moderate" if ar > 40 else "low"

            self.add_triplet(anchor, positive, negative,
                           f"{vl_word} valence, {ar_word} arousal",
                           'affect', ['vl', 'ar'], [], 0.92)

    def generate_rc_similarity(self, count: int = 200):
        """Generate RC block similarity triplets."""
        print(f"Generating {count} RC similarity triplets...")

        for _ in range(count):
            sg = round(random.uniform(0.6, 0.98), 2)
            dt = round(random.uniform(0.01, 0.1), 2)
            xi = round(random.uniform(0.01, 0.05), 2)

            anchor = f"RC:{{sg{format_decimal(sg)}⋀dt{format_decimal(dt)}⋀xi{format_decimal(xi)}}}"

            # Similar RC
            pos_sg = round(sg + random.uniform(-0.05, 0.05), 2)
            pos_dt = round(dt + random.uniform(-0.02, 0.02), 2)
            pos_xi = round(xi + random.uniform(-0.01, 0.01), 2)
            pos_sg = max(0.5, min(1.0, pos_sg))
            pos_dt = max(0.01, min(0.2, pos_dt))
            pos_xi = max(0.01, min(0.1, pos_xi))
            positive = f"RC:{{sg{format_decimal(pos_sg)}⋀dt{format_decimal(pos_dt)}⋀xi{format_decimal(pos_xi)}}}"

            # Different RC
            neg_sg = round(1.0 - sg + random.uniform(-0.1, 0.1), 2)
            neg_dt = round(0.15 - dt + random.uniform(-0.05, 0.05), 2)
            neg_sg = max(0.3, min(1.0, neg_sg))
            neg_dt = max(0.01, min(0.2, neg_dt))
            negative = f"RC:{{sg{format_decimal(neg_sg)}⋀dt{format_decimal(neg_dt)}⋀xi{format_decimal(round(random.uniform(0.05, 0.1), 2))}}}"

            stability = "stable" if sg > 0.8 and dt < 0.05 else "moderate" if sg > 0.6 else "unstable"

            self.add_triplet(anchor, positive, negative,
                           f"RC {stability}: σ={sg}, drift={dt}",
                           'consciousness', ['sg', 'dt', 'xi'], [], 0.88)

    def generate_infrastructure_health_similarity(self, count: int = 300):
        """Generate infrastructure health similarity triplets."""
        print(f"Generating {count} infrastructure health similarity triplets...")

        for _ in range(count):
            sv = random.randint(2, 10)
            db = random.randint(1, 5)
            sv_status = random.choice(['●', '◐'])
            db_status = random.choice(['●', '◐'])

            anchor = f"P:{{{sv_status}sv{format_count(sv)}⋀{db_status}db{format_count(db)}}}"

            # Similar
            pos_sv = sv + random.randint(-1, 1)
            pos_db = db + random.randint(-1, 1)
            pos_sv = max(1, pos_sv)
            pos_db = max(1, pos_db)
            positive = f"P:{{{sv_status}sv{format_count(pos_sv)}⋀{db_status}db{format_count(pos_db)}}}"

            # Different
            neg_status = '⊘' if sv_status == '●' else '●'
            neg_sv = sv + random.randint(3, 8) * random.choice([-1, 1])
            neg_sv = max(1, neg_sv)
            negative = f"P:{{{neg_status}sv{format_count(neg_sv)}⋀⊘db{format_count(1)}}}"

            status_word = "healthy" if sv_status == '●' else "degraded"

            self.add_triplet(anchor, positive, negative,
                           f"{sv} servers {status_word}, {db} databases",
                           'infrastructure', ['sv', 'db'], [sv_status, db_status], 0.85)

    def generate_resource_similarity(self, count: int = 300):
        """Generate resource utilization similarity triplets."""
        print(f"Generating {count} resource similarity triplets...")

        for _ in range(count):
            cp = random.randint(30, 95)
            mm = random.randint(40, 90)

            anchor = f"cp{format_percent(cp)}⋀mm{format_percent(mm)}"

            # Similar
            pos_cp = cp + random.randint(-5, 5)
            pos_mm = mm + random.randint(-5, 5)
            pos_cp = max(10, min(99, pos_cp))
            pos_mm = max(10, min(99, pos_mm))
            positive = f"cp{format_percent(pos_cp)}⋀mm{format_percent(pos_mm)}"

            # Different
            neg_cp = 100 - cp + random.randint(-10, 10)
            neg_mm = 100 - mm + random.randint(-10, 10)
            neg_cp = max(10, min(99, neg_cp))
            neg_mm = max(10, min(99, neg_mm))
            negative = f"cp{format_percent(neg_cp)}⋀mm{format_percent(neg_mm)}"

            self.add_triplet(anchor, positive, negative,
                           f"CPU {cp}%, memory {mm}%",
                           'infrastructure', ['cp', 'mm'], [], 0.9)

    def generate_causal_similarity(self, count: int = 200):
        """Generate causal chain similarity triplets."""
        print(f"Generating {count} causal similarity triplets...")

        chains = [
            (['nw', 'sv', 'db'], ['network', 'server', 'database']),
            (['tk', 'au', 'ss'], ['token', 'auth', 'session']),
            (['mm', 'ct', 'pr'], ['memory', 'container', 'process']),
            (['rq', 'cp', 'er'], ['request', 'CPU', 'error']),
        ]

        for _ in range(count):
            stems, names = random.choice(chains)
            op = random.choice(['⊘', '△', '▽'])

            anchor = f"{op}{stems[0]}∴{op}{stems[1]}∴{op}{stems[2]}"

            # Similar chain (same pattern)
            positive = f"{op}{stems[0]}∴{op}{stems[1]}"

            # Different chain
            other_stems, _ = random.choice([c for c in chains if c[0] != stems])
            other_op = random.choice([o for o in ['⊘', '△', '▽', '●'] if o != op])
            negative = f"{other_op}{other_stems[0]}∴{other_op}{other_stems[1]}"

            op_word = {'⊘': 'failure', '△': 'increase', '▽': 'decrease'}[op]

            self.add_triplet(anchor, positive, negative,
                           f"{names[0]} {op_word} cascade",
                           'infrastructure', stems, [op], 0.82)

    # ==================== TYPE D 8D QUALIA ====================

    def generate_phenomenal_states(self, count: int = 400):
        """Generate detailed 8D phenomenal state vectors."""
        print(f"Generating {count} phenomenal state 8D vectors...")

        states = [
            ('deep focus', (60, 80), (40, 60), (85, 98), (70, 85), (85, 98), (88, 98), (25, 45), (30, 50)),
            ('creative flow', (75, 90), (55, 70), (80, 95), (60, 75), (75, 90), (80, 95), (45, 65), (40, 60)),
            ('peaceful rest', (70, 85), (10, 25), (85, 98), (50, 65), (25, 40), (70, 85), (65, 85), (60, 75)),
            ('social joy', (80, 95), (65, 80), (75, 90), (55, 70), (70, 85), (70, 85), (55, 75), (85, 98)),
            ('analytical thought', (55, 70), (45, 60), (90, 98), (75, 90), (90, 98), (92, 99), (20, 35), (35, 50)),
            ('meditative calm', (65, 80), (10, 25), (92, 99), (80, 95), (40, 55), (95, 99), (55, 75), (50, 65)),
            ('excited discovery', (80, 95), (75, 90), (70, 85), (55, 70), (90, 98), (75, 88), (50, 70), (55, 70)),
            ('empathic connection', (75, 90), (50, 65), (80, 92), (55, 70), (65, 80), (80, 90), (60, 80), (92, 99)),
            ('contemplative wonder', (70, 85), (35, 50), (85, 95), (70, 85), (75, 90), (85, 95), (45, 65), (55, 70)),
            ('playful engagement', (80, 95), (70, 85), (70, 85), (50, 65), (80, 92), (65, 80), (70, 88), (70, 85)),
        ]

        for _ in range(count):
            state_name, vl_r, ar_r, co_r, tp_r, sl_r, mt_r, em_r, rl_r = random.choice(states)

            vl = random.randint(*vl_r)
            ar = random.randint(*ar_r)
            co = random.randint(*co_r)
            tp = random.randint(*tp_r)
            sl = random.randint(*sl_r)
            mt = random.randint(*mt_r)
            em = random.randint(*em_r)
            rl = random.randint(*rl_r)

            ccin = f"C:ql⁸D:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}⋀tp{format_percent(tp)}⋀sl{format_percent(sl)}⋀mt{format_percent(mt)}⋀em{format_percent(em)}⋀rl{format_percent(rl)}}}"
            english = f"8D phenomenal state ({state_name}): valence {vl}, arousal {ar}, coherence {co}, temporal {tp}, salience {sl}, metacognition {mt}, embodiment {em}, relational {rl}"

            self.add_8d_record(ccin, english, ['vl', 'ar', 'co', 'tp', 'sl', 'mt', 'em', 'rl'])

    def generate_weighted_qualia(self, count: int = 300):
        """Generate weighted 8D qualia with emphasis patterns."""
        print(f"Generating {count} weighted 8D qualia vectors...")

        # Different emphasis profiles
        profiles = [
            ('cognitive', {'mt': 1.5, 'sl': 1.3, 'co': 1.2}),
            ('emotional', {'vl': 1.4, 'ar': 1.3, 'rl': 1.2}),
            ('embodied', {'em': 1.5, 'ar': 1.2, 'tp': 1.1}),
            ('social', {'rl': 1.5, 'em': 1.2, 'vl': 1.1}),
            ('reflective', {'mt': 1.4, 'co': 1.3, 'tp': 1.2}),
        ]

        for _ in range(count):
            profile_name, weights = random.choice(profiles)

            base = {
                'vl': random.randint(50, 80),
                'ar': random.randint(30, 70),
                'co': random.randint(60, 90),
                'tp': random.randint(50, 80),
                'sl': random.randint(50, 85),
                'mt': random.randint(60, 90),
                'em': random.randint(40, 70),
                'rl': random.randint(50, 80),
            }

            # Apply weights
            for dim, weight in weights.items():
                base[dim] = min(99, int(base[dim] * weight))

            dims = ['vl', 'ar', 'co', 'tp', 'sl', 'mt', 'em', 'rl']
            ccin = f"C:ql⁸D:{{{'⋀'.join([f'{d}{format_percent(base[d])}' for d in dims])}}}"
            english = f"8D qualia ({profile_name} emphasis): " + ", ".join([f"{d}={base[d]}" for d in dims])

            self.add_8d_record(ccin, english, dims)

    def generate_transitional_qualia(self, count: int = 200):
        """Generate qualia state transitions."""
        print(f"Generating {count} transitional 8D qualia...")

        for _ in range(count):
            # From state
            from_vl = random.randint(30, 70)
            from_ar = random.randint(40, 80)
            from_co = random.randint(50, 85)

            # To state (different)
            to_vl = from_vl + random.randint(-30, 30)
            to_ar = from_ar + random.randint(-30, 30)
            to_co = from_co + random.randint(-20, 20)
            to_vl = max(-80, min(95, to_vl))
            to_ar = max(10, min(95, to_ar))
            to_co = max(30, min(98, to_co))

            ccin = f"ᐊC:{{vl{format_percent(from_vl)}⋀ar{format_percent(from_ar)}⋀co{format_percent(from_co)}}}»ᐃC:{{vl{format_percent(to_vl)}⋀ar{format_percent(to_ar)}⋀co{format_percent(to_co)}}}"
            english = f"Qualia transition: from (v={from_vl}, a={from_ar}, c={from_co}) to (v={to_vl}, a={to_ar}, c={to_co})"

            self.add_8d_record(ccin, english, ['vl', 'ar', 'co'])

    def run_generation_cycle(self):
        """Run generation cycle."""
        print(f"\n{'='*50}")
        print(f"Starting similarity/8D generation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        # Type C triplets
        self.generate_affect_similarity(300)
        self.generate_rc_similarity(200)
        self.generate_infrastructure_health_similarity(300)
        self.generate_resource_similarity(300)
        self.generate_causal_similarity(200)

        # Type D 8D qualia
        self.generate_phenomenal_states(400)
        self.generate_weighted_qualia(300)
        self.generate_transitional_qualia(200)

        if self.records:
            self.save_batch()

        print(f"\nCycle complete. Total generated: {self.total_generated}")
        return self.total_generated


def main():
    output_dir = Path(__file__).parent

    existing = list(output_dir.glob("ccin_mu_dataset_batch_*.jsonl"))
    if existing:
        max_batch = max(int(f.stem.split('_')[-1]) for f in existing)
        start_batch = max_batch + 1
    else:
        start_batch = 91

    print(f"Starting similarity/8D expansion from batch {start_batch}")

    generator = SimilarityGenerator(output_dir, start_batch)

    for cycle in range(2):
        print(f"\n*** CYCLE {cycle + 1}/2 ***")
        generator.run_generation_cycle()
        if cycle < 1:
            print("Pausing 60 seconds...")
            time.sleep(60)

    print(f"\n{'='*50}")
    print(f"SIMILARITY/8D EXPANSION COMPLETE")
    print(f"Total new records: {generator.total_generated}")
    print(f"{'='*50}")

    import subprocess
    subprocess.run(['python3', 'validate_and_assemble.py'], cwd=output_dir)


if __name__ == "__main__":
    main()
