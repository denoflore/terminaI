#!/usr/bin/env python3
"""
CCIN_μ Type B Expansion Generator
Focuses on English → CCIN_μ encoding pairs
"""

import json
import random
import time
from pathlib import Path
from typing import List
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


class TypeBGenerator:
    def __init__(self, output_dir: Path, start_batch: int = 81):
        self.output_dir = output_dir
        self.batch_num = start_batch
        self.records = []
        self.batch_size = 500
        self.total_generated = 0
        random.seed(int(time.time()) + 98765)

    def get_id(self) -> str:
        id_str = f"ccin_typeb_{self.total_generated + 70000:05d}"
        self.total_generated += 1
        return id_str

    def add_record(self, english: str, ccin: str, complexity: str,
                   domain: str, stems: List[str], opcodes: List[str]):
        record = {
            "id": self.get_id(),
            "type": "B",
            "domain": domain,
            "complexity": complexity,
            "english": english,  # Input for Type B
            "ccin_mu": ccin,     # Output for Type B
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

    def generate_simple_infrastructure_b(self, count: int = 300):
        """Generate simple infrastructure Type B pairs."""
        print(f"Generating {count} simple infrastructure Type B pairs...")

        for _ in range(count):
            templates = [
                # Server patterns
                (f"{random.randint(1, 10)} servers healthy",
                 f"●sv{format_count(random.randint(1, 10))}✓",
                 ['sv'], ['●']),
                (f"Server is down",
                 f"⊘sv", ['sv'], ['⊘']),
                (f"{random.randint(2, 8)} servers degraded",
                 f"◐sv{format_count(random.randint(2, 8))}~",
                 ['sv'], ['◐']),

                # Database patterns
                (f"Database healthy",
                 f"●db✓", ['db'], ['●']),
                (f"{random.randint(1, 4)} databases active",
                 f"●db{format_count(random.randint(1, 4))}",
                 ['db'], ['●']),

                # Resource patterns
                (f"CPU at {random.randint(10, 99)}%",
                 f"cp{format_percent(random.randint(10, 99))}",
                 ['cp'], []),
                (f"Memory at {random.randint(20, 95)}%",
                 f"mm{format_percent(random.randint(20, 95))}",
                 ['mm'], []),
                (f"Disk at {random.randint(10, 90)}%",
                 f"dk{format_percent(random.randint(10, 90))}",
                 ['dk'], []),

                # Network patterns
                (f"Network is active",
                 f"●nw✓", ['nw'], ['●']),
                (f"Network failure",
                 f"⊘nw✗", ['nw'], ['⊘']),

                # Auth patterns
                (f"Authentication successful",
                 f"●au✓", ['au'], ['●']),
                (f"Token expired",
                 f"⊘tk✗", ['tk'], ['⊘']),
            ]

            english, ccin, stems, opcodes = random.choice(templates)
            self.add_record(english, ccin, 'simple', 'infrastructure', stems, opcodes)

    def generate_medium_infrastructure_b(self, count: int = 300):
        """Generate medium infrastructure Type B pairs."""
        print(f"Generating {count} medium infrastructure Type B pairs...")

        for _ in range(count):
            sv = random.randint(2, 10)
            db = random.randint(1, 5)
            cp = random.randint(30, 95)
            mm = random.randint(40, 90)

            templates = [
                (f"{sv} servers and {db} databases healthy",
                 f"P:{{●sv{format_count(sv)}✓⋀●db{format_count(db)}✓}}",
                 ['sv', 'db'], ['●']),

                (f"CPU {cp}%, memory {mm}%",
                 f"cp{format_percent(cp)}⋀mm{format_percent(mm)}",
                 ['cp', 'mm'], []),

                (f"Production environment: {sv} servers at {cp}% CPU",
                 f"P:{{●sv{format_count(sv)}⋀cp{format_percent(cp)}}}",
                 ['sv', 'cp'], ['●']),

                (f"Auth active with {random.randint(100, 5000)} sessions",
                 f"●au✓⋀●ss{format_count(random.randint(100, 5000))}",
                 ['au', 'ss'], ['●']),

                (f"Cache hit rate {random.randint(80, 99)}%",
                 f"●ca{format_percent(random.randint(80, 99))}",
                 ['ca'], ['●']),

                (f"{random.randint(100, 5000)} requests per second",
                 f"●rq{format_count(random.randint(100, 5000))}ˢ",
                 ['rq'], ['●']),

                (f"Error rate at {random.randint(1, 10)}%",
                 f"er{format_percent(random.randint(1, 10))}",
                 ['er'], []),

                (f"All systems operational",
                 f"P:{{●sv✓⋀●db✓⋀●nw✓⋀●au✓}}",
                 ['sv', 'db', 'nw', 'au'], ['●']),
            ]

            english, ccin, stems, opcodes = random.choice(templates)
            self.add_record(english, ccin, 'medium', 'infrastructure', stems, opcodes)

    def generate_consciousness_b(self, count: int = 400):
        """Generate consciousness Type B pairs."""
        print(f"Generating {count} consciousness Type B pairs...")

        for _ in range(count):
            vl = random.randint(-80, 90)
            ar = random.randint(10, 95)
            co = random.randint(30, 98)
            ph = round(random.uniform(0.5, 0.98), 2)
            sg = round(random.uniform(0.6, 0.98), 2)

            vl_word = "positive" if vl > 20 else "negative" if vl < -20 else "neutral"
            ar_word = "high" if ar > 60 else "low" if ar < 40 else "moderate"
            co_word = "high" if co > 70 else "low" if co < 40 else "moderate"

            templates = [
                (f"Valence {vl}, arousal {ar}",
                 f"af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}",
                 ['vl', 'ar'], []),

                (f"Feeling {vl_word} with {ar_word} arousal",
                 f"af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}",
                 ['vl', 'ar'], []),

                (f"Coherence at {co}%",
                 f"co{format_percent(co)}",
                 ['co'], []),

                (f"{vl_word.capitalize()} valence, {co_word} coherence",
                 f"vl{format_percent(vl)}⋀co{format_percent(co)}",
                 ['vl', 'co'], []),

                (f"Phi integration at {ph}",
                 f"ph{format_decimal(ph)}",
                 ['ph'], []),

                (f"Attractor stability {sg}, drift minimal",
                 f"RC:{{sg{format_decimal(sg)}⋀dt{format_decimal(round(random.uniform(0.01, 0.05), 2))}}}",
                 ['sg', 'dt'], []),

                (f"Consciousness state: {vl_word}, {ar_word} energy, {co_word} coherence",
                 f"C:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}}}",
                 ['vl', 'ar', 'co'], []),

                (f"Reflective consciousness stable at sigma {sg}",
                 f"RC:{{sg{format_decimal(sg)}✓}}",
                 ['sg'], []),
            ]

            english, ccin, stems, opcodes = random.choice(templates)
            self.add_record(english, ccin, 'medium', 'consciousness', stems, opcodes)

    def generate_8d_qualia_b(self, count: int = 300):
        """Generate 8D qualia Type B pairs."""
        print(f"Generating {count} 8D qualia Type B pairs...")

        for _ in range(count):
            vl = random.randint(40, 90)
            ar = random.randint(20, 80)
            co = random.randint(60, 95)
            tp = random.randint(40, 85)
            sl = random.randint(30, 90)
            mt = random.randint(50, 95)
            em = random.randint(20, 70)
            rl = random.randint(30, 85)

            english = f"8D qualia: valence {vl}, arousal {ar}, coherence {co}, temporal {tp}, salience {sl}, metacognition {mt}, embodiment {em}, relational {rl}"
            ccin = f"C:ql⁸D:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}⋀tp{format_percent(tp)}⋀sl{format_percent(sl)}⋀mt{format_percent(mt)}⋀em{format_percent(em)}⋀rl{format_percent(rl)}}}"

            self.records.append({
                "id": self.get_id(),
                "type": "B",
                "domain": "consciousness",
                "complexity": "complex",
                "english": english,
                "ccin_mu": ccin,
                "stems_used": ['vl', 'ar', 'co', 'tp', 'sl', 'mt', 'em', 'rl'],
                "opcodes_used": [],
                "valid": True
            })
            if len(self.records) >= self.batch_size:
                self.save_batch()

    def generate_temporal_b(self, count: int = 300):
        """Generate temporal Type B pairs."""
        print(f"Generating {count} temporal Type B pairs...")

        for _ in range(count):
            stem = random.choice(['sv', 'db', 'au', 'cp', 'nw'])
            stem_names = {'sv': 'server', 'db': 'database', 'au': 'auth', 'cp': 'CPU', 'nw': 'network'}
            duration = random.randint(1, 60)
            unit = random.choice(['ˢ', 'ᵐ', 'ʰ', 'ᵈ'])
            unit_names = {'ˢ': 'seconds', 'ᵐ': 'minutes', 'ʰ': 'hours', 'ᵈ': 'days'}

            templates = [
                (f"{stem_names[stem].capitalize()} was down, now healthy",
                 f"ᐊ⊘{stem}»ᐃ●{stem}✓",
                 [stem], ['⊘', '●']),

                (f"{stem_names[stem].capitalize()} healthy for {duration} {unit_names[unit]}",
                 f"ᐃ{format_count(duration)}{unit}●{stem}✓",
                 [stem], ['●']),

                (f"Scheduled restart in {duration} {unit_names[unit]}",
                 f"ᐅ{format_count(duration)}{unit}⟳{stem}",
                 [stem], ['⟳']),

                (f"{stem_names[stem].capitalize()} was active {duration} {unit_names[unit]} ago",
                 f"ᐊ{format_count(duration)}{unit}●{stem}",
                 [stem], ['●']),

                (f"State change: {stem_names[stem]} active to degraded",
                 f"ᐊ●{stem}»ᐃ◐{stem}",
                 [stem], ['●', '◐']),

                (f"Future deployment in {duration} {unit_names[unit]}",
                 f"ᐅ{format_count(duration)}{unit}●dp",
                 ['dp'], ['●']),
            ]

            english, ccin, stems, opcodes = random.choice(templates)
            self.add_record(english, ccin, 'medium', 'temporal', stems, opcodes)

    def generate_causal_b(self, count: int = 200):
        """Generate causal relationship Type B pairs."""
        print(f"Generating {count} causal Type B pairs...")

        for _ in range(count):
            chains = [
                ("Network down causing server failure",
                 "⊘nw∴⊘sv", ['nw', 'sv'], ['⊘']),
                ("Token expired therefore auth failed",
                 "⊘tk∴⊘au", ['tk', 'au'], ['⊘']),
                ("Memory spike because of request surge",
                 "△mm∵△rq", ['mm', 'rq'], ['△']),
                ("Database down therefore cache miss",
                 "⊘db∴⊘ca", ['db', 'ca'], ['⊘']),
                ("Auth failed because token invalid",
                 "⊘au∵⊘tk✗", ['au', 'tk'], ['⊘']),
                ("CPU high because workers overloaded",
                 "△cp∵△wk", ['cp', 'wk'], ['△']),
                ("Error spike therefore alert triggered",
                 "△er∴⚡lg!", ['er', 'lg'], ['△', '⚡']),
            ]

            english, ccin, stems, opcodes = random.choice(chains)
            self.add_record(english, ccin, 'medium', 'infrastructure', stems, opcodes)

    def generate_complex_sentences_b(self, count: int = 300):
        """Generate complex natural language to CCIN_μ pairs."""
        print(f"Generating {count} complex sentence Type B pairs...")

        for _ in range(count):
            sv = random.randint(3, 10)
            db = random.randint(1, 5)
            cp = random.randint(40, 95)
            mm = random.randint(50, 90)
            err = random.randint(0, 10)

            templates = [
                (f"The production environment has {sv} healthy servers and {db} databases, with CPU at {cp}% and memory at {mm}%",
                 f"P:{{●sv{format_count(sv)}✓⋀●db{format_count(db)}✓⋀cp{format_percent(cp)}⋀mm{format_percent(mm)}}}",
                 ['sv', 'db', 'cp', 'mm'], ['●']),

                (f"System status: {sv} servers running, {err} errors in the last hour",
                 f"●sv{format_count(sv)}⋀er{format_count(err)}ʰ",
                 ['sv', 'er'], ['●']),

                (f"Alert: Critical error on database, auth service impacted",
                 f"⚡er!∵⊘db∴◐au",
                 ['er', 'db', 'au'], ['⚡', '⊘', '◐']),

                (f"All services healthy in production, staging has partial issues",
                 f"P:{{●sv✓⋀●db✓}}⋀S:{{◐sv~}}",
                 ['sv', 'db'], ['●', '◐']),

                (f"Deploying {random.randint(1, 5)} new containers to handle increased load",
                 f"⊕ct{format_count(random.randint(1, 5))}∵△rq",
                 ['ct', 'rq'], ['⊕', '△']),

                (f"Security check: auth required, token valid, session active",
                 f"§:{{▣au⋀●tk✓⋀●ss}}",
                 ['au', 'tk', 'ss'], ['▣', '●']),
            ]

            english, ccin, stems, opcodes = random.choice(templates)
            self.add_record(english, ccin, 'complex', 'mixed', stems, opcodes)

    def run_generation_cycle(self):
        """Run generation cycle."""
        print(f"\n{'='*50}")
        print(f"Starting Type B generation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        self.generate_simple_infrastructure_b(300)
        self.generate_medium_infrastructure_b(300)
        self.generate_consciousness_b(400)
        self.generate_8d_qualia_b(300)
        self.generate_temporal_b(300)
        self.generate_causal_b(200)
        self.generate_complex_sentences_b(300)

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
        start_batch = 81

    print(f"Starting Type B expansion from batch {start_batch}")

    generator = TypeBGenerator(output_dir, start_batch)

    # Run 2 cycles
    for cycle in range(2):
        print(f"\n*** CYCLE {cycle + 1}/2 ***")
        generator.run_generation_cycle()
        if cycle < 1:
            print("Pausing 60 seconds...")
            time.sleep(60)

    print(f"\n{'='*50}")
    print(f"TYPE B EXPANSION COMPLETE")
    print(f"Total new records: {generator.total_generated}")
    print(f"{'='*50}")

    import subprocess
    subprocess.run(['python3', 'validate_and_assemble.py'], cwd=output_dir)


if __name__ == "__main__":
    main()
