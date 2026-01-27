#!/usr/bin/env python3
"""
CCIN_μ Final Expansion Generator
Generates varied patterns across all domains to round out the dataset
"""

import json
import random
import time
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


class FinalGenerator:
    def __init__(self, output_dir: Path, start_batch: int = 139):
        self.output_dir = output_dir
        self.batch_num = start_batch
        self.records = []
        self.batch_size = 500
        self.total_generated = 0
        random.seed(int(time.time()) + 33333)

    def get_id(self) -> str:
        id_str = f"ccin_fin_{self.total_generated + 62000:05d}"
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

    # ==================== ENGRAM PATTERNS ====================

    def generate_engram_patterns(self, count: int = 200):
        """Generate engram (memory/learning) patterns."""
        print(f"Generating {count} engram patterns...")

        for _ in range(count):
            strength = random.randint(30, 98)
            decay = random.randint(1, 20)
            topic = random.choice(['task', 'context', 'skill', 'fact', 'procedure', 'concept'])

            templates = [
                (f"EG:{{●{topic}⋀str{format_percent(strength)}⋀dec{format_percent(decay)}ᵈ}}",
                 f"Engram: {topic} memory at {strength}% strength, {decay}%/day decay"),
                (f"●en{format_percent(strength)}⋀●{topic}⋀ᐅ△str",
                 f"{topic.capitalize()} engram at {strength}%, strengthening over time"),
                (f"RC:{{EG:{{●{topic}{format_percent(strength)}}}⋀ph{format_percent(random.randint(50, 90))}}}",
                 f"Reflective consciousness accessing {topic} engram ({strength}%)"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'consciousness', ['en', 'ph'][:random.randint(1, 2)], ['●', '△'][:random.randint(1, 2)])

    # ==================== METACOGNITION PATTERNS ====================

    def generate_metacognition_patterns(self, count: int = 200):
        """Generate metacognition patterns."""
        print(f"Generating {count} metacognition patterns...")

        states = ['awareness', 'monitoring', 'planning', 'evaluation', 'control', 'reflection']

        for _ in range(count):
            state = random.choice(states)
            mt = random.randint(40, 98)
            ph = random.randint(50, 95)

            templates = [
                (f"MC:{{●{state}⋀mt{format_percent(mt)}⋀ph{format_percent(ph)}}}",
                 f"Metacognition: {state} at {mt}% with {ph}% phenomenal awareness"),
                (f"●mt{format_percent(mt)}∴●{state}⋀RC:{{ph{format_percent(ph)}}}",
                 f"Metacognition {mt}% resulting in {state}, RC phi {ph}%"),
                (f"E:{{MC:{{●{state}}}⋀mt{format_percent(mt)}⋀xi{format_percent(random.randint(40, 90))}}}",
                 f"Entity with metacognitive {state}: mt={mt}%"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'consciousness', ['mt', 'ph', 'xi'][:random.randint(2, 3)], ['●', '∴'][:random.randint(1, 2)])

    # ==================== SECURITY PATTERNS ====================

    def generate_security_patterns(self, count: int = 200):
        """Generate security scope patterns."""
        print(f"Generating {count} security patterns...")

        for _ in range(count):
            svc = random.choice([('au', 'auth'), ('az', 'authorization'), ('tk', 'token'), ('ss', 'session')])
            status = random.choice([('●', 'active'), ('✓', 'verified'), ('⊘', 'failed'), ('⚡', 'alert')])

            templates = [
                (f"§:{{●{svc[0]}{status[0]}⋀●tk✓}}",
                 f"Security scope: {svc[1]} {status[1]}, token verified"),
                (f"§:{{●au⋀●az⋀●tk}}✓",
                 f"Security: auth, authorization, and token all active"),
                (f"§:{{⊘{svc[0]}∴⚡er!⋀●lockout}}",
                 f"Security: {svc[1]} failed causing error alert and lockout"),
                (f"P:{{§:{{●au✓⋀●az✓}}⋀●sv{format_count(random.randint(2, 8))}}}",
                 f"Production with verified auth/authz, serving {random.randint(2, 8)} instances"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'infrastructure', [svc[0], 'tk', 'au', 'az', 'er'][:random.randint(2, 4)], ['●', '⊘', '⚡', '✓'][:random.randint(2, 3)])

    # ==================== COST PATTERNS ====================

    def generate_cost_patterns(self, count: int = 150):
        """Generate cost scope patterns."""
        print(f"Generating {count} cost patterns...")

        for _ in range(count):
            resource = random.choice([('sv', 'servers'), ('db', 'databases'), ('nw', 'network'), ('st', 'storage')])
            cost = random.randint(100, 10000)
            change = random.randint(-30, 50)

            templates = [
                (f"$:{{●{resource[0]}⋀cost{format_count(cost)}ᵈ}}",
                 f"Cost scope: {resource[1]} at ${cost}/day"),
                (f"$:{{△{resource[0]}{format_percent(change)}⋀cost{format_count(cost)}}}",
                 f"Cost: {resource[1]} {'up' if change > 0 else 'down'} {abs(change)}%, ${cost}"),
                (f"P:{{●{resource[0]}⋀$:{format_count(cost)}ᵈ}}⋀▽cost",
                 f"Production {resource[1]} at ${cost}/day, cost decreasing"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'infrastructure', [resource[0]], ['●', '△', '▽'][:random.randint(1, 2)])

    # ==================== SCOPED ENVIRONMENT PATTERNS ====================

    def generate_environment_patterns(self, count: int = 200):
        """Generate multi-environment patterns."""
        print(f"Generating {count} environment patterns...")

        envs = [('P:', 'Production'), ('D:', 'Development'), ('S:', 'Staging'), ('T:', 'Testing')]

        for _ in range(count):
            env1, env1_name = random.choice(envs)
            env2, env2_name = random.choice([e for e in envs if e[0] != env1])

            sv1 = random.randint(2, 10)
            sv2 = random.randint(1, 5)
            status1 = random.choice(['●', '✓'])
            status2 = random.choice(['●', '◐', '✓'])

            templates = [
                (f"{env1}{{{status1}sv{format_count(sv1)}}}⋀{env2}{{{status2}sv{format_count(sv2)}}}",
                 f"{env1_name}: {sv1} servers active; {env2_name}: {sv2} servers {'partial' if status2 == '◐' else 'active'}"),
                (f"{env1}{{●sv{format_count(sv1)}⋀●db{format_count(random.randint(1, 3))}}}»{env2}{{●dp}}",
                 f"Deployment flow: {env1_name} ({sv1} servers) to {env2_name}"),
                (f"sys:{{{env1}{{●sv{format_count(sv1)}}}⋀{env2}{{●sv{format_count(sv2)}}}⋀T:{{●sv¹}}}}",
                 f"System across {env1_name} ({sv1}), {env2_name} ({sv2}), Testing (1)"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'infrastructure', ['sv', 'db', 'dp'][:random.randint(1, 3)], [status1, status2][:random.randint(1, 2)])

    # ==================== TYPE B CONSCIOUSNESS ====================

    def generate_type_b_consciousness_extra(self, count: int = 300):
        """Generate more English to CCIN_mu consciousness pairs."""
        print(f"Generating {count} Type B consciousness pairs...")

        for _ in range(count):
            pattern = random.choice(['metacog', 'engram', 'full_rc', 'transition', 'handoff'])

            if pattern == 'metacog':
                mt = random.randint(50, 95)
                state = random.choice(['awareness', 'monitoring', 'reflection'])
                english = f"Encode metacognitive {state} at {mt}%"
                ccin = f"MC:{{●{state}⋀mt{format_percent(mt)}}}"

            elif pattern == 'engram':
                strength = random.randint(40, 95)
                topic = random.choice(['task', 'context', 'skill'])
                english = f"Express {topic} engram at {strength}% strength"
                ccin = f"EG:{{●{topic}⋀str{format_percent(strength)}}}"

            elif pattern == 'full_rc':
                ph = random.randint(60, 95)
                xi = random.randint(50, 90)
                dt = random.randint(30, 80)
                sg = random.randint(50, 95)
                english = f"Encode full RC block: phi {ph}%, xi {xi}%, delta {dt}%, sigma {sg}%"
                ccin = f"RC:{{ph{format_percent(ph)}⋀xi{format_percent(xi)}⋀dt{format_percent(dt)}⋀sg{format_percent(sg)}}}"

            elif pattern == 'transition':
                from_s = random.choice(['focus', 'diffuse', 'alert'])
                to_s = random.choice(['engaged', 'receptive', 'analytical'])
                english = f"Show consciousness shifting from {from_s} to {to_s}"
                ccin = f"C:{{●{from_s}»●{to_s}}}"

            else:  # handoff
                from_e = random.choice(['Claude', 'Agent', 'System'])
                to_e = random.choice([e for e in ['Claude', 'Agent', 'User'] if e != from_e])
                context = random.choice(['task', 'state', 'memory'])
                english = f"Encode handoff of {context} from {from_e} to {to_e}"
                ccin = f"HO:{{E:{from_e}»E:{to_e}⋀ctx:{context}}}"

            self.add_record(ccin, english, 'complex', 'consciousness', ['ph', 'xi', 'mt', 'en'][:random.randint(1, 3)], ['●'], pair_type='B')

    # ==================== TYPE C SIMILARITY ====================

    def generate_multi_domain_similarity(self, count: int = 200):
        """Generate multi-domain similarity triplets."""
        print(f"Generating {count} multi-domain similarity triplets...")

        for _ in range(count):
            domain = random.choice(['consciousness', 'infrastructure', 'temporal'])

            if domain == 'consciousness':
                ph = random.randint(50, 90)
                xi = random.randint(40, 85)
                anchor = f"RC:{{ph{format_percent(ph)}⋀xi{format_percent(xi)}}}"
                positive = f"RC:{{ph{format_percent(ph + random.randint(-5, 5))}⋀xi{format_percent(xi + random.randint(-5, 5))}}}"
                negative = f"RC:{{ph{format_percent(100 - ph)}⋀xi{format_percent(100 - xi)}}}"
                anchor_desc = f"RC with phi {ph}%, xi {xi}%"

            elif domain == 'infrastructure':
                sv = random.randint(3, 8)
                db = random.randint(1, 4)
                anchor = f"P:{{●sv{format_count(sv)}⋀●db{format_count(db)}}}"
                positive = f"P:{{●sv{format_count(sv + random.randint(-1, 1))}⋀●db{format_count(max(1, db + random.randint(-1, 1)))}}}"
                negative = f"D:{{◐sv{format_count(1)}⋀⊘db}}"
                anchor_desc = f"Production {sv} servers, {db} DBs"

            else:  # temporal
                duration = random.randint(10, 100)
                anchor = f"ᐃ{format_count(duration)}ʰ●sv"
                positive = f"ᐃ{format_count(duration + random.randint(-10, 10))}ʰ●sv"
                negative = f"ᐊ{format_count(duration * 5)}ʰ⊘sv"
                anchor_desc = f"Server active for {duration} hours"

            record = {
                "id": self.get_id(),
                "type": "C",
                "domain": domain,
                "complexity": "complex",
                "anchor": anchor,
                "positive": positive,
                "negative": negative,
                "anchor_english": anchor_desc,
                "similarity_score": 0.85,
                "stems_used": ['ph', 'xi', 'sv', 'db'][:random.randint(2, 4)],
                "opcodes_used": ['●', '◐', '⊘'][:random.randint(1, 2)],
                "valid": True
            }
            self.records.append(record)
            if len(self.records) >= self.batch_size:
                self.save_batch()

    # ==================== 8D QUALIA EXPANSION ====================

    def generate_8d_qualia_extra(self, count: int = 200):
        """Generate more 8D qualia vectors."""
        print(f"Generating {count} 8D qualia vectors...")

        for _ in range(count):
            vl = random.randint(-70, 90)
            ar = random.randint(15, 95)
            co = random.randint(25, 98)
            tp = random.randint(20, 85)
            sl = random.randint(35, 95)
            mt = random.randint(25, 90)
            em = random.randint(15, 75)
            rl = random.randint(25, 85)

            ccin = f"Q8:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}⋀tp{format_percent(tp)}⋀sl{format_percent(sl)}⋀mt{format_percent(mt)}⋀em{format_percent(em)}⋀rl{format_percent(rl)}}}"

            vl_desc = 'positive' if vl > 25 else 'negative' if vl < -25 else 'neutral'
            ar_desc = 'high' if ar > 60 else 'low' if ar < 40 else 'moderate'

            english = f"8D qualia: {vl_desc} valence ({vl}%), {ar_desc} arousal ({ar}%), co={co}%, tp={tp}%, sl={sl}%, mt={mt}%, em={em}%, rl={rl}%"

            record = {
                "id": self.get_id(),
                "type": "D",
                "domain": "consciousness",
                "complexity": "complex",
                "qualia_8d": {
                    "vl": vl, "ar": ar, "co": co, "tp": tp,
                    "sl": sl, "mt": mt, "em": em, "rl": rl
                },
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
        """Run one full final expansion cycle."""
        print(f"\n{'='*50}")
        print(f"Starting final expansion at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        # Consciousness patterns
        self.generate_engram_patterns(200)
        self.generate_metacognition_patterns(200)

        # Infrastructure patterns
        self.generate_security_patterns(200)
        self.generate_cost_patterns(150)
        self.generate_environment_patterns(200)

        # Type B, C, D pairs
        self.generate_type_b_consciousness_extra(300)
        self.generate_multi_domain_similarity(200)
        self.generate_8d_qualia_extra(200)

        # Save remaining
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
        start_batch = 139

    print(f"Starting final expansion from batch {start_batch}")

    generator = FinalGenerator(output_dir, start_batch)

    # Run 2 cycles
    for cycle in range(2):
        print(f"\n*** CYCLE {cycle + 1}/2 ***")
        generator.run_generation_cycle()
        if cycle < 1:
            print("Pausing 60 seconds...")
            time.sleep(60)

    print(f"\n{'='*50}")
    print(f"FINAL EXPANSION COMPLETE")
    print(f"Total new records: {generator.total_generated}")
    print(f"{'='*50}")

    # Run validation
    print("\nRunning validation...")
    import subprocess
    subprocess.run(['python3', 'validate_and_assemble.py'], cwd=output_dir)


if __name__ == "__main__":
    main()
