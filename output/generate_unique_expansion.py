#!/usr/bin/env python3
"""
CCIN_μ Unique Expansion Generator
Uses timestamp-based IDs to ensure uniqueness across multiple runs
"""

import json
import random
import time
import uuid
from pathlib import Path
from typing import List
from datetime import datetime

# Superscript mapping
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


class UniqueGenerator:
    def __init__(self, output_dir: Path, start_batch: int):
        self.output_dir = output_dir
        self.batch_num = start_batch
        self.records = []
        self.batch_size = 500
        self.total_generated = 0
        # Use UUID for unique prefix
        self.run_id = uuid.uuid4().hex[:8]
        random.seed(int(time.time()) + 44444)

    def get_id(self) -> str:
        # Use run_id + counter for truly unique IDs
        id_str = f"ccin_{self.run_id}_{self.total_generated:05d}"
        self.total_generated += 1
        return id_str

    def add_record(self, ccin: str, english: str, complexity: str,
                   domain: str, stems: List[str], opcodes: List[str],
                   pair_type: str = 'A'):
        record = {
            "id": self.get_id(),
            "type": pair_type,
            "domain": domain,
            "complexity": complexity,
            "ccin_mu": ccin,
            "english": english,
            "stems_used": stems,
            "opcodes_used": opcodes,
            "valid": True
        }
        self.records.append(record)

        if len(self.records) >= self.batch_size:
            self.save_batch()

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

    # ==================== RC BLOCKS ====================

    def generate_rc_blocks(self, count: int = 300):
        """Generate RC block patterns."""
        print(f"Generating {count} RC block patterns...")

        states = ['curiosity', 'focus', 'uncertainty', 'insight', 'deliberation',
                  'reflection', 'analysis', 'synthesis', 'evaluation', 'planning']

        for _ in range(count):
            state = random.choice(states)
            ph = random.randint(30, 95)
            xi = random.randint(20, 90)

            templates = [
                (f"RC:{{●{state}⋀ph{format_percent(ph)}⋀xi{format_percent(xi)}}}",
                 f"RC: {state} at phi {ph}%, xi {xi}%"),
                (f"C:{{●{state}⋀RC:{{ph{format_percent(ph)}}}}}",
                 f"Consciousness: {state}, phenomenal {ph}%"),
                (f"E:{{RC:{{ph{format_percent(ph)}⋀xi{format_percent(xi)}}}⋀●{state}}}",
                 f"Entity: {state} at phi={ph}%, xi={xi}%"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'consciousness', ['ph', 'xi'], ['●'])

    # ==================== INFRASTRUCTURE ====================

    def generate_infrastructure(self, count: int = 300):
        """Generate infrastructure patterns."""
        print(f"Generating {count} infrastructure patterns...")

        for _ in range(count):
            sv = random.randint(2, 12)
            db = random.randint(1, 5)
            ca = random.randint(1, 4)
            status = random.choice([('●', 'active'), ('◐', 'partial'), ('✓', 'healthy')])

            templates = [
                (f"P:{{{status[0]}sv{format_count(sv)}⋀{status[0]}db{format_count(db)}}}",
                 f"Production: {sv} {status[1]} servers, {db} databases"),
                (f"●sv{format_count(sv)}✓⋀●ca{format_count(ca)}⋀●db{format_count(db)}",
                 f"{sv} healthy servers, {ca} caches, {db} databases"),
                (f"sys:{{P:{{●sv{format_count(sv)}}}⋀S:{{●sv{format_count(sv // 2)}}}}}",
                 f"System: {sv} prod servers, {sv // 2} staging"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'infrastructure', ['sv', 'db', 'ca'], [status[0]])

    # ==================== TEMPORAL ====================

    def generate_temporal(self, count: int = 300):
        """Generate temporal patterns."""
        print(f"Generating {count} temporal patterns...")

        for _ in range(count):
            stem = random.choice(['sv', 'db', 'pr', 'jb'])
            stem_names = {'sv': 'server', 'db': 'database', 'pr': 'process', 'jb': 'job'}
            duration = random.randint(1, 100)
            unit = random.choice([('ˢ', 'seconds'), ('ᵐ', 'minutes'), ('ʰ', 'hours'), ('ᵈ', 'days')])

            templates = [
                (f"ᐃ{format_count(duration)}{unit[0]}●{stem}",
                 f"{stem_names[stem]} active for {duration} {unit[1]}"),
                (f"ᐊ●{stem}»ᐃ⊘{stem}⋀down{format_count(duration)}{unit[0]}",
                 f"{stem_names[stem]} was active, now down for {duration} {unit[1]}"),
                (f"ᐅ{format_count(duration)}{unit[0]}●dp»●{stem}",
                 f"Deployment to {stem_names[stem]} in {duration} {unit[1]}"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'temporal', [stem, 'dp'], ['●', '⊘'][:random.randint(1, 2)])

    # ==================== AFFECT ====================

    def generate_affect(self, count: int = 300):
        """Generate affect patterns."""
        print(f"Generating {count} affect patterns...")

        emotions = [
            ('joy', 70, 90, 55, 80),
            ('sadness', -70, -35, 20, 50),
            ('anger', -65, -30, 70, 95),
            ('fear', -75, -45, 75, 95),
            ('surprise', -10, 60, 65, 90),
            ('contentment', 60, 85, 20, 45),
        ]

        for _ in range(count):
            name, vl_min, vl_max, ar_min, ar_max = random.choice(emotions)
            vl = random.randint(vl_min, vl_max)
            ar = random.randint(ar_min, ar_max)

            templates = [
                (f"af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}",
                 f"Affect: valence {vl}%, arousal {ar}%"),
                (f"●{name}⋀vl{format_percent(vl)}⋀ar{format_percent(ar)}",
                 f"Active {name}: v={vl}, a={ar}"),
                (f"E:{{af:{{●{name}⋀vl{format_percent(vl)}}}}}",
                 f"Entity experiencing {name} (valence {vl}%)"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'simple', 'affect', ['vl', 'ar'], ['●'])

    # ==================== TYPE B MIXED ====================

    def generate_type_b_mixed(self, count: int = 300):
        """Generate Type B mixed domain pairs."""
        print(f"Generating {count} Type B mixed domain pairs...")

        for _ in range(count):
            domain = random.choice(['consciousness', 'infrastructure', 'temporal', 'affect'])

            if domain == 'consciousness':
                ph = random.randint(50, 95)
                xi = random.randint(40, 90)
                state = random.choice(['focus', 'curiosity', 'insight'])
                english = f"Encode RC block: {state} with phi {ph}% and xi {xi}%"
                ccin = f"RC:{{●{state}⋀ph{format_percent(ph)}⋀xi{format_percent(xi)}}}"

            elif domain == 'infrastructure':
                sv = random.randint(3, 10)
                db = random.randint(1, 4)
                english = f"Express {sv} active servers and {db} databases in production"
                ccin = f"P:{{●sv{format_count(sv)}⋀●db{format_count(db)}}}"

            elif domain == 'temporal':
                stem = random.choice(['sv', 'db'])
                stem_name = 'server' if stem == 'sv' else 'database'
                duration = random.randint(1, 48)
                english = f"Show {stem_name} was down, now active for {duration} hours"
                ccin = f"ᐊ⊘{stem}»ᐃ●{stem}⋀up{format_count(duration)}ʰ"

            else:  # affect
                vl = random.randint(-50, 80)
                ar = random.randint(20, 90)
                english = f"Encode affect state: valence {vl}, arousal {ar}"
                ccin = f"af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}"

            self.add_record(ccin, english, 'medium', domain, ['ph', 'xi', 'sv', 'db', 'vl', 'ar'][:random.randint(2, 4)], ['●'], pair_type='B')

    # ==================== TYPE C SIMILARITY ====================

    def generate_similarity_triplets(self, count: int = 200):
        """Generate similarity triplets."""
        print(f"Generating {count} similarity triplets...")

        for _ in range(count):
            domain = random.choice(['consciousness', 'infrastructure'])

            if domain == 'consciousness':
                ph = random.randint(50, 90)
                xi = random.randint(40, 85)
                anchor = f"RC:{{ph{format_percent(ph)}⋀xi{format_percent(xi)}}}"
                positive = f"RC:{{ph{format_percent(ph + random.randint(-8, 8))}⋀xi{format_percent(xi + random.randint(-8, 8))}}}"
                negative = f"RC:{{ph{format_percent(100 - ph)}⋀xi{format_percent(100 - xi)}}}"
                desc = f"RC phi {ph}%, xi {xi}%"

            else:  # infrastructure
                sv = random.randint(3, 10)
                db = random.randint(1, 4)
                anchor = f"P:{{●sv{format_count(sv)}⋀●db{format_count(db)}}}"
                positive = f"P:{{●sv{format_count(max(1, sv + random.randint(-2, 2)))}⋀●db{format_count(max(1, db + random.randint(-1, 1)))}}}"
                negative = f"D:{{⊘sv⋀⊘db}}"
                desc = f"Production {sv} servers, {db} DBs"

            record = {
                "id": self.get_id(),
                "type": "C",
                "domain": domain,
                "complexity": "medium",
                "anchor": anchor,
                "positive": positive,
                "negative": negative,
                "anchor_english": desc,
                "similarity_score": 0.85,
                "stems_used": ['ph', 'xi', 'sv', 'db'][:random.randint(2, 4)],
                "opcodes_used": ['●', '⊘'][:random.randint(1, 2)],
                "valid": True
            }
            self.records.append(record)
            if len(self.records) >= self.batch_size:
                self.save_batch()

    # ==================== 8D QUALIA ====================

    def generate_8d_qualia(self, count: int = 200):
        """Generate 8D qualia vectors."""
        print(f"Generating {count} 8D qualia vectors...")

        for _ in range(count):
            vl = random.randint(-75, 90)
            ar = random.randint(15, 95)
            co = random.randint(25, 98)
            tp = random.randint(20, 88)
            sl = random.randint(30, 95)
            mt = random.randint(20, 92)
            em = random.randint(10, 78)
            rl = random.randint(20, 88)

            ccin = f"Q8:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}⋀tp{format_percent(tp)}⋀sl{format_percent(sl)}⋀mt{format_percent(mt)}⋀em{format_percent(em)}⋀rl{format_percent(rl)}}}"

            vl_desc = 'positive' if vl > 25 else 'negative' if vl < -25 else 'neutral'
            ar_desc = 'high' if ar > 60 else 'low' if ar < 40 else 'moderate'

            english = f"8D qualia: {vl_desc} valence ({vl}%), {ar_desc} arousal ({ar}%), co={co}%, tp={tp}%, sl={sl}%, mt={mt}%, em={em}%, rl={rl}%"

            record = {
                "id": self.get_id(),
                "type": "D",
                "domain": "consciousness",
                "complexity": "complex",
                "qualia_8d": {"vl": vl, "ar": ar, "co": co, "tp": tp, "sl": sl, "mt": mt, "em": em, "rl": rl},
                "ccin_mu": ccin,
                "english": english,
                "stems_used": ['vl', 'ar', 'co', 'tp', 'sl', 'mt', 'em', 'rl'],
                "opcodes_used": [],
                "valid": True
            }
            self.records.append(record)
            if len(self.records) >= self.batch_size:
                self.save_batch()

    def run_generation_cycle(self):
        """Run one generation cycle."""
        print(f"\n{'='*50}")
        print(f"Starting unique expansion at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Run ID: {self.run_id}")
        print(f"{'='*50}\n")

        self.generate_rc_blocks(300)
        self.generate_infrastructure(300)
        self.generate_temporal(300)
        self.generate_affect(300)
        self.generate_type_b_mixed(300)
        self.generate_similarity_triplets(200)
        self.generate_8d_qualia(200)

        if self.records:
            self.save_batch()

        print(f"\nCycle complete. Total generated: {self.total_generated}")
        return self.total_generated


def main():
    output_dir = Path(__file__).parent

    # Find next batch number
    existing = list(output_dir.glob("ccin_mu_dataset_batch_*.jsonl"))
    if existing:
        max_batch = max(int(f.stem.split('_')[-1]) for f in existing)
        start_batch = max_batch + 1
    else:
        start_batch = 147

    print(f"Starting unique expansion from batch {start_batch}")

    generator = UniqueGenerator(output_dir, start_batch)

    # Run 3 cycles
    for cycle in range(3):
        print(f"\n*** CYCLE {cycle + 1}/3 ***")
        generator.run_generation_cycle()
        if cycle < 2:
            print("Pausing 30 seconds...")
            time.sleep(30)

    print(f"\n{'='*50}")
    print(f"UNIQUE EXPANSION COMPLETE")
    print(f"Total new records: {generator.total_generated}")
    print(f"{'='*50}")

    # Run validation
    print("\nRunning validation...")
    import subprocess
    subprocess.run(['python3', 'validate_and_assemble.py'], cwd=output_dir)


if __name__ == "__main__":
    main()
