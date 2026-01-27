#!/usr/bin/env python3
"""
CCIN_μ Consciousness Domain Expansion Generator
Focuses on RC blocks, phenomenal states, and consciousness-related patterns
"""

import json
import random
import time
from pathlib import Path
from typing import List, Dict
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

def format_decimal(val: float) -> str:
    formatted = f"{val:.2f}"
    return to_superscript(formatted)


class ConsciousnessGenerator:
    def __init__(self, output_dir: Path, start_batch: int = 51):
        self.output_dir = output_dir
        self.batch_num = start_batch
        self.records = []
        self.batch_size = 500
        self.total_generated = 0
        random.seed(int(time.time()) + 54321)

    def get_id(self) -> str:
        id_str = f"ccin_cons_{self.total_generated + 45000:05d}"
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

    # ==================== RC BLOCK PATTERNS ====================

    def generate_rc_blocks(self, count: int = 400):
        """Generate detailed RC (reflective consciousness) blocks."""
        print(f"Generating {count} RC block examples...")

        states = ['curiosity', 'focus', 'uncertainty', 'insight', 'deliberation',
                  'reflection', 'analysis', 'synthesis', 'evaluation', 'planning']

        for _ in range(count):
            state = random.choice(states)
            ph = random.randint(30, 95)
            xi = random.randint(20, 90)
            dt = random.randint(10, 80)
            sg = random.randint(40, 95)

            # Various RC block formats
            templates = [
                (f"RC:{{●{state}⋀ph{format_percent(ph)}⋀xi{format_percent(xi)}}}",
                 f"Reflective consciousness: {state} state with {ph}% phenomenal intensity, {xi}% integration"),
                (f"RC:{{ph{format_percent(ph)}⋀xi{format_percent(xi)}⋀dt{format_percent(dt)}⋀sg{format_percent(sg)}}}",
                 f"RC state: phi={ph}%, xi={xi}%, delta={dt}%, sigma={sg}%"),
                (f"C:{{●{state}⋀RC:{{ph{format_percent(ph)}}}}}",
                 f"Consciousness state: {state}, phenomenal {ph}%"),
                (f"E:{{RC:{{ph{format_percent(ph)}⋀xi{format_percent(xi)}}}⋀●{state}}}",
                 f"Entity experiencing {state} at phi={ph}%, xi={xi}%"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'consciousness',
                          ['ph', 'xi', 'dt', 'sg'][:random.randint(2, 4)], ['●'])

    def generate_phenomenal_states(self, count: int = 400):
        """Generate phenomenal state descriptions."""
        print(f"Generating {count} phenomenal state examples...")

        states = [
            ('wonder', 75, 70, 85, 'experiencing wonder'),
            ('flow', 90, 85, 95, 'in flow state'),
            ('confusion', 40, 30, 45, 'experiencing confusion'),
            ('clarity', 95, 90, 98, 'experiencing clarity'),
            ('absorption', 85, 80, 90, 'absorbed in task'),
            ('contemplation', 70, 65, 80, 'in contemplation'),
            ('recognition', 80, 75, 88, 'moment of recognition'),
            ('anticipation', 65, 60, 75, 'in anticipation'),
            ('resolution', 88, 85, 92, 'reaching resolution'),
            ('discovery', 92, 88, 96, 'moment of discovery'),
        ]

        for _ in range(count):
            state_name, ph_base, xi_base, sg_base, desc = random.choice(states)
            ph = ph_base + random.randint(-10, 10)
            xi = xi_base + random.randint(-10, 10)
            sg = sg_base + random.randint(-10, 5)

            ph = max(10, min(99, ph))
            xi = max(10, min(99, xi))
            sg = max(10, min(99, sg))

            templates = [
                (f"C:{{●{state_name}⋀ph{format_percent(ph)}⋀sg{format_percent(sg)}}}",
                 f"Consciousness: {desc} - phi {ph}%, salience {sg}%"),
                (f"●ph{format_percent(ph)}⋀●xi{format_percent(xi)}∴●{state_name}",
                 f"Phi {ph}% and xi {xi}% resulting in {state_name}"),
                (f"E:{{ph{format_percent(ph)}»●{state_name}»sg{format_percent(sg)}}}",
                 f"Entity: phi {ph}% flows to {state_name}, salience {sg}%"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'consciousness',
                          ['ph', 'xi', 'sg'], ['●', '∴'][:random.randint(1, 2)])

    def generate_consciousness_transitions(self, count: int = 300):
        """Generate consciousness state transitions."""
        print(f"Generating {count} consciousness transition examples...")

        states = ['focus', 'diffuse', 'alert', 'relaxed', 'engaged', 'withdrawn',
                  'active', 'receptive', 'analytical', 'creative']

        for _ in range(count):
            from_state = random.choice(states)
            to_state = random.choice([s for s in states if s != from_state])

            from_ph = random.randint(40, 90)
            to_ph = random.randint(40, 90)

            templates = [
                (f"ᐊC:{{●{from_state}⋀ph{format_percent(from_ph)}}}»ᐃC:{{●{to_state}⋀ph{format_percent(to_ph)}}}",
                 f"Consciousness shift: was {from_state} (phi {from_ph}%) now {to_state} (phi {to_ph}%)"),
                (f"C:{{●{from_state}»●{to_state}}}⋀△ph{format_percent(to_ph - from_ph)}",
                 f"Transitioning from {from_state} to {to_state}, phi change {to_ph - from_ph:+d}%"),
                (f"E:{{ᐊ●{from_state}»ᐃ●{to_state}⋀ph{format_percent(to_ph)}}}",
                 f"Entity transitioned: {from_state} to {to_state}, current phi {to_ph}%"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'consciousness',
                          ['ph'], ['●', '△'][:random.randint(1, 2)])

    # ==================== 8D QUALIA EXPANSION ====================

    def generate_8d_qualia_states(self, count: int = 300):
        """Generate full 8D qualia vector states."""
        print(f"Generating {count} 8D qualia state examples...")

        for _ in range(count):
            vl = random.randint(-80, 95)
            ar = random.randint(10, 95)
            co = random.randint(30, 98)
            tp = random.randint(20, 90)
            sl = random.randint(30, 95)
            mt = random.randint(20, 90)
            em = random.randint(10, 80)
            rl = random.randint(20, 85)

            # Build 8D vector
            ccin = f"Q8:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}⋀tp{format_percent(tp)}⋀sl{format_percent(sl)}⋀mt{format_percent(mt)}⋀em{format_percent(em)}⋀rl{format_percent(rl)}}}"

            vl_desc = 'positive' if vl > 30 else 'negative' if vl < -30 else 'neutral'
            ar_desc = 'high' if ar > 60 else 'low' if ar < 40 else 'moderate'

            english = f"8D qualia: {vl_desc} valence ({vl}), {ar_desc} arousal ({ar}), coherence {co}%, temporal {tp}%, salience {sl}%, metacog {mt}%, embodiment {em}%, relational {rl}%"

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

    def generate_weighted_qualia(self, count: int = 200):
        """Generate weighted qualia expressions."""
        print(f"Generating {count} weighted qualia examples...")

        for _ in range(count):
            # Select 3-5 dimensions with weights
            dims = random.sample(['vl', 'ar', 'co', 'tp', 'sl', 'mt', 'em', 'rl'], random.randint(3, 5))
            dim_names = {
                'vl': 'valence', 'ar': 'arousal', 'co': 'coherence', 'tp': 'temporal',
                'sl': 'salience', 'mt': 'metacognition', 'em': 'embodiment', 'rl': 'relational'
            }

            weighted_parts = []
            desc_parts = []

            for dim in dims:
                val = random.randint(-50 if dim == 'vl' else 20, 95)
                weight = random.choice([1, 2, 3])
                weight_markers = {1: '', 2: '²', 3: '³'}

                weighted_parts.append(f"{dim}{format_percent(val)}{weight_markers[weight]}")
                desc_parts.append(f"{dim_names[dim]}={val}{'(x'+str(weight)+')' if weight > 1 else ''}")

            ccin = f"Q:{{{'⋀'.join(weighted_parts)}}}"
            english = f"Weighted qualia state: {', '.join(desc_parts)}"

            record = {
                "id": self.get_id(),
                "type": "D",
                "domain": "consciousness",
                "complexity": "complex",
                "ccin_mu": ccin,
                "english": english,
                "stems_used": dims,
                "opcodes_used": [],
                "valid": True
            }
            self.records.append(record)
            if len(self.records) >= self.batch_size:
                self.save_batch()

    # ==================== TYPE B PAIRS (English to CCIN_mu) ====================

    def generate_type_b_consciousness(self, count: int = 400):
        """Generate English to CCIN_mu pairs for consciousness domain."""
        print(f"Generating {count} Type B consciousness pairs...")

        for _ in range(count):
            pair_type = random.choice(['rc', 'phenomenal', 'qualia', 'state'])

            if pair_type == 'rc':
                ph = random.randint(40, 95)
                xi = random.randint(30, 90)
                state = random.choice(['curiosity', 'focus', 'insight', 'reflection'])
                english = f"Encode an RC block showing {state} with phi {ph}% and xi {xi}%"
                ccin = f"RC:{{●{state}⋀ph{format_percent(ph)}⋀xi{format_percent(xi)}}}"
                stems = ['ph', 'xi']

            elif pair_type == 'phenomenal':
                ph = random.randint(50, 95)
                state = random.choice(['wonder', 'clarity', 'flow', 'absorption'])
                english = f"Express the phenomenal state of {state} at {ph}% intensity"
                ccin = f"C:{{●{state}⋀ph{format_percent(ph)}}}"
                stems = ['ph']

            elif pair_type == 'qualia':
                vl = random.randint(-50, 90)
                ar = random.randint(20, 90)
                co = random.randint(40, 95)
                english = f"Encode qualia: valence {vl}, arousal {ar}, coherence {co}"
                ccin = f"Q:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}}}"
                stems = ['vl', 'ar', 'co']

            else:  # state
                from_state = random.choice(['focus', 'diffuse', 'alert'])
                to_state = random.choice(['relaxed', 'engaged', 'active'])
                english = f"Show a consciousness transition from {from_state} to {to_state}"
                ccin = f"C:{{●{from_state}»●{to_state}}}"
                stems = []

            self.add_record(ccin, english, 'complex', 'consciousness', stems, ['●'], pair_type='B')

    def generate_type_b_temporal(self, count: int = 300):
        """Generate English to CCIN_mu pairs for temporal domain."""
        print(f"Generating {count} Type B temporal pairs...")

        for _ in range(count):
            pair_type = random.choice(['duration', 'scheduled', 'transition', 'past'])
            stem = 'sv'

            if pair_type == 'duration':
                val = random.randint(5, 120)
                unit = random.choice([('s', 'seconds'), ('m', 'minutes'), ('h', 'hours')])
                stem = random.choice(['sv', 'db', 'pr', 'jb'])
                stem_name = {'sv': 'server', 'db': 'database', 'pr': 'process', 'jb': 'job'}[stem]
                unit_super = {'s': 'ˢ', 'm': 'ᵐ', 'h': 'ʰ'}[unit[0]]
                english = f"Express {stem_name} active for {val} {unit[1]}"
                ccin = f"ᐃ{format_count(val)}{unit_super}●{stem}"

            elif pair_type == 'scheduled':
                val = random.randint(1, 24)
                action = random.choice([('dp', 'deployment'), ('rs', 'restart'), ('up', 'update')])
                target = random.choice(['sv', 'db', 'ct'])
                target_name = {'sv': 'servers', 'db': 'databases', 'ct': 'containers'}[target]
                english = f"Schedule {action[1]} of {target_name} in {val} hours"
                ccin = f"ᐅ{format_count(val)}ʰ●{action[0]}»●{target}"
                stem = action[0]

            elif pair_type == 'transition':
                stem = random.choice(['sv', 'db', 'au'])
                stem_name = {'sv': 'server', 'db': 'database', 'au': 'auth'}[stem]
                from_op = random.choice([('●', 'active'), ('◐', 'partial'), ('⊘', 'down')])
                to_op = random.choice([('●', 'active'), ('◐', 'partial'), ('⊘', 'down')])
                english = f"Show {stem_name} was {from_op[1]} now {to_op[1]}"
                ccin = f"ᐊ{from_op[0]}{stem}»ᐃ{to_op[0]}{stem}"

            else:  # past
                val = random.randint(1, 48)
                stem = random.choice(['er', 'dp', 'rs'])
                stem_name = {'er': 'error', 'dp': 'deployment', 'rs': 'restart'}[stem]
                english = f"Indicate {stem_name} occurred {val} hours ago"
                ccin = f"ᐊ{format_count(val)}ʰ●{stem}"

            self.add_record(ccin, english, 'medium', 'temporal', [stem], ['●'], pair_type='B')

    # ==================== MIXED DOMAIN PATTERNS ====================

    def generate_consciousness_infrastructure_mix(self, count: int = 200):
        """Generate patterns mixing consciousness and infrastructure domains."""
        print(f"Generating {count} mixed consciousness-infrastructure examples...")

        for _ in range(count):
            ph = random.randint(50, 95)
            sv_count = random.randint(2, 8)
            db_count = random.randint(1, 4)

            templates = [
                (f"E:{{RC:{{ph{format_percent(ph)}}}⋀P:{{●sv{format_count(sv_count)}⋀●db{format_count(db_count)}}}}}",
                 f"Entity with phi {ph}% managing {sv_count} servers and {db_count} databases"),
                (f"C:{{●focus⋀ph{format_percent(ph)}}}⋀P:{{●sv{format_count(sv_count)}✓}}",
                 f"Consciousness focused (phi {ph}%) on {sv_count} healthy production servers"),
                (f"RC:{{ph{format_percent(ph)}}}»P:{{●dp»●sv{format_count(sv_count)}}}",
                 f"RC at phi {ph}% initiating deployment to {sv_count} servers"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'mixed',
                          ['ph', 'sv', 'db', 'dp'][:random.randint(2, 4)], ['●'])

    def generate_handoff_protocols(self, count: int = 200):
        """Generate handoff protocol patterns."""
        print(f"Generating {count} handoff protocol examples...")

        for _ in range(count):
            from_entity = random.choice(['Claude', 'Agent', 'System', 'User'])
            to_entity = random.choice([e for e in ['Claude', 'Agent', 'System', 'User'] if e != from_entity])

            ph = random.randint(60, 95)
            xi = random.randint(50, 90)

            contexts = ['task', 'session', 'state', 'context', 'memory']
            context = random.choice(contexts)

            templates = [
                (f"HO:{{E:{from_entity}»E:{to_entity}⋀RC:{{ph{format_percent(ph)}⋀xi{format_percent(xi)}}}⋀ctx:{context}}}",
                 f"Handoff from {from_entity} to {to_entity}: phi {ph}%, xi {xi}%, transferring {context}"),
                (f"E:{from_entity}»●{context}»E:{to_entity}⋀ph{format_percent(ph)}",
                 f"{from_entity} passes {context} to {to_entity} with {ph}% fidelity"),
                (f"●HO⋀E:{from_entity}⊢E:{to_entity}⋀RC:{{●{context}⋀ph{format_percent(ph)}}}",
                 f"Active handoff: {from_entity} required by {to_entity}, {context} at phi {ph}%"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'consciousness',
                          ['ph', 'xi'][:random.randint(1, 2)], ['●', '⊢'][:random.randint(1, 2)])

    def run_generation_cycle(self):
        """Run one full consciousness expansion cycle."""
        print(f"\n{'='*50}")
        print(f"Starting consciousness expansion at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        # RC blocks and phenomenal states
        self.generate_rc_blocks(400)
        self.generate_phenomenal_states(400)
        self.generate_consciousness_transitions(300)

        # 8D qualia
        self.generate_8d_qualia_states(300)
        self.generate_weighted_qualia(200)

        # Type B pairs
        self.generate_type_b_consciousness(400)
        self.generate_type_b_temporal(300)

        # Mixed patterns
        self.generate_consciousness_infrastructure_mix(200)
        self.generate_handoff_protocols(200)

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
        start_batch = 51

    print(f"Starting consciousness expansion from batch {start_batch}")

    generator = ConsciousnessGenerator(output_dir, start_batch)

    # Run 2 cycles at 50% rate
    for cycle in range(2):
        print(f"\n*** CYCLE {cycle + 1}/2 ***")
        generator.run_generation_cycle()
        if cycle < 1:
            print("Pausing 90 seconds...")
            time.sleep(90)

    print(f"\n{'='*50}")
    print(f"CONSCIOUSNESS EXPANSION COMPLETE")
    print(f"Total new records: {generator.total_generated}")
    print(f"{'='*50}")

    # Run validation
    print("\nRunning validation...")
    import subprocess
    subprocess.run(['python3', 'validate_and_assemble.py'], cwd=output_dir)


if __name__ == "__main__":
    main()
