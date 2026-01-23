#!/usr/bin/env python3
"""
CCIN_μ Edge Cases & Complex Compositions Generator
Phase 6: Generate 1500 challenging examples for model robustness
"""

import json
import random
from pathlib import Path
from typing import List

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


class EdgeCaseGenerator:
    def __init__(self, output_dir: Path, start_id: int = 9000, batch_num: int = 18):
        self.output_dir = output_dir
        self.current_id = start_id
        self.batch_num = batch_num
        self.records = []
        self.batch_size = 500
        random.seed(47)

    def get_id(self) -> str:
        id_str = f"ccin_edge_{self.current_id:05d}"
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

    def add_record(self, ccin_mu: str, english: str, complexity: str,
                   stems_used: List[str], opcodes_used: List[str],
                   category: str, pair_type: str = 'A'):
        record = {
            "id": self.get_id(),
            "type": pair_type,
            "domain": "mixed",
            "complexity": complexity,
            "ccin_mu": ccin_mu,
            "english": english,
            "stems_used": stems_used,
            "opcodes_used": opcodes_used,
            "category": category,
            "valid": True
        }
        self.records.append(record)
        if len(self.records) >= self.batch_size:
            self.save_batch()

    def generate_reg_protocol(self):
        """Generate REG! protocol examples."""
        print("Generating REG! protocol examples...")

        # Medical domain
        medical_stems = [
            ('bp', 'blood_pressure', '120/80'),
            ('hr', 'heart_rate', '72'),
            ('sp', 'oxygen_saturation', '98%'),
            ('bt', 'body_temperature', '37.2°C'),
            ('rr', 'respiratory_rate', '16'),
            ('gl', 'glucose_level', '95mg/dL'),
        ]

        for stem, full_name, typical in medical_stems:
            for _ in range(10):
                # Registration + usage
                val = random.randint(60, 140) if stem == 'hr' else random.randint(90, 100) if stem == 'sp' else random.randint(70, 130)
                ccin = f"REG!medical:{stem}={full_name}\n●{stem}{format_count(val)}✓"
                english = f"Register medical stem '{stem}' as {full_name}. {full_name.replace('_', ' ').title()} is healthy at {val}"
                self.add_record(ccin, english, 'complex', [stem], ['●'], 'reg_protocol')

        # Financial domain
        finance_stems = [
            ('px', 'price', 'market price'),
            ('vl', 'volume', 'trading volume'),
            ('mk', 'market_cap', 'market capitalization'),
            ('rt', 'return', 'return rate'),
        ]

        for stem, full_name, desc in finance_stems:
            for _ in range(8):
                val = random.randint(10, 200)
                direction = random.choice(['△', '▽'])
                dir_word = 'rising' if direction == '△' else 'falling'
                ccin = f"REG!finance:{stem}={full_name}\n{direction}{stem}{format_percent(val)}"
                english = f"Register finance stem '{stem}' as {full_name}. {desc.capitalize()} {dir_word} to {val}%"
                self.add_record(ccin, english, 'complex', [stem], [direction], 'reg_protocol')

        # IoT/Sensor domain
        iot_stems = [
            ('tm', 'temperature', 'degrees'),
            ('hm', 'humidity', 'percent'),
            ('pr', 'pressure', 'hPa'),
            ('lt', 'light', 'lux'),
            ('mo', 'motion', 'detected'),
        ]

        for stem, full_name, unit in iot_stems:
            for _ in range(8):
                val = random.randint(20, 80)
                ccin = f"REG!iot:{stem}={full_name}\n●{stem}{format_count(val)}"
                english = f"Register IoT stem '{stem}' as {full_name}. Current {full_name} reading: {val} {unit}"
                self.add_record(ccin, english, 'complex', [stem], ['●'], 'reg_protocol')

    def generate_nested_compositions(self):
        """Generate deeply nested composition examples."""
        print("Generating nested composition examples...")

        # Nested scopes
        for _ in range(100):
            vl = random.randint(-80, 90)
            ar = random.randint(10, 95)
            co = random.randint(20, 98)
            sg = round(random.uniform(0.5, 0.98), 2)
            dt = round(random.uniform(0.01, 0.25), 2)

            ccin = f"「ENGRAM C:SESSION v1.0」\nts:2026-01-23\nC:{{\n  af:{{\n    vl{format_percent(vl)}⋀ar{format_percent(ar)}\n  }}\n  co{format_percent(co)}\n  RC:{{\n    sg{format_decimal(sg)}⋀dt{format_decimal(dt)}\n  }}\n}}"

            english = f"Session engram: affect block with valence {vl}, arousal {ar}. Coherence {co}%. RC block with stability {sg}, drift {dt}."

            self.add_record(ccin, english, 'complex',
                          ['vl', 'ar', 'co', 'sg', 'dt'], [], 'nested_composition')

        # Triple-nested infrastructure
        for _ in range(50):
            svs = random.randint(3, 10)
            dbs = random.randint(1, 4)
            cp = random.randint(30, 95)
            mm = random.randint(40, 90)

            ccin = f"I:PROD:{{\n  CLUSTER:{{\n    nd{format_count(random.randint(3, 8))}\n    pd{format_count(random.randint(10, 50))}\n  }}\n  SERVICES:{{\n    sv{format_count(svs)}✓⋀db{format_count(dbs)}✓\n  }}\n  RESOURCES:{{\n    cp{format_percent(cp)}⋀mm{format_percent(mm)}\n  }}\n}}"

            english = f"Production infrastructure with nested cluster, services, and resource blocks"

            self.add_record(ccin, english, 'complex',
                          ['nd', 'pd', 'sv', 'db', 'cp', 'mm'], ['●'], 'nested_composition')

        # Multi-layer consciousness
        for _ in range(50):
            attention_codes = random.sample(['dr', 'cl', 'wm', 'rg', 'sd', 'ex'], random.randint(2, 4))
            vl = random.randint(-70, 85)
            ar = random.randint(15, 90)
            co = random.randint(25, 95)
            mt = random.randint(30, 95)
            sg = round(random.uniform(0.6, 0.98), 2)
            ph = round(random.uniform(0.5, 0.95), 2)

            at_str = '|'.join(attention_codes)
            ccin = f"C:{{\n  at:{{{at_str}}}\n  af:{{\n    vl{format_percent(vl)}⋀ar{format_percent(ar)}\n  }}\n  ql:{{\n    co{format_percent(co)}⋀mt{format_percent(mt)}\n  }}\n  RC:{{\n    sg{format_decimal(sg)}⋀ph{format_decimal(ph)}\n  }}\n}}"

            english = f"Multi-layer consciousness: attention on {', '.join(attention_codes)}, affect (vl:{vl}, ar:{ar}), qualia (co:{co}%, mt:{mt}%), RC (sg:{sg}, ph:{ph})"

            self.add_record(ccin, english, 'complex',
                          ['at', 'vl', 'ar', 'co', 'mt', 'sg', 'ph'], [], 'nested_composition')

    def generate_multi_scope(self):
        """Generate multi-scope declaration examples."""
        print("Generating multi-scope examples...")

        for _ in range(100):
            # Combined consciousness and infrastructure
            vl = random.randint(30, 85)
            ar = random.randint(20, 70)
            svs = random.randint(3, 8)
            cp = random.randint(40, 85)

            ccin = f"C:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}\nI:{{●sv{format_count(svs)}✓⋀cp{format_percent(cp)}}}"

            english = f"Consciousness scope: valence {vl}, arousal {ar}. Infrastructure scope: {svs} servers healthy, CPU {cp}%"

            self.add_record(ccin, english, 'complex',
                          ['vl', 'ar', 'sv', 'cp'], ['●'], 'multi_scope')

        for _ in range(50):
            # Session + Environment + Application
            ss_count = random.randint(10, 500)
            rq_rate = random.randint(50, 2000)
            err_rate = random.randint(0, 50)

            ccin = f"S:{{●ss{format_count(ss_count)}}}\nE:{{●nw✓⋀●fw✓}}\nA:{{rq{format_count(rq_rate)}ˢ⋀er{format_count(err_rate)}ˢ}}"

            english = f"Session: {ss_count} active. Environment: network and firewall healthy. Application: {rq_rate} req/s, {err_rate} err/s"

            self.add_record(ccin, english, 'complex',
                          ['ss', 'nw', 'fw', 'rq', 'er'], ['●'], 'multi_scope')

    def generate_maximum_compression(self):
        """Generate maximum compression examples."""
        print("Generating maximum compression examples...")

        compressions = [
            ("●⁵✓", "5 active and healthy", ['generic']),
            ("⊘³✗", "3 failed", ['generic']),
            ("△⁹⁵", "rising to 95", ['generic']),
            ("▽¹⁰", "falling to 10", ['generic']),
            ("⚡!", "critical alert", ['generic']),
            ("●»●", "active to active", ['generic']),
            ("⊘∵⊘", "failed because failed", ['generic']),
            ("⟲³", "cycling 3 times", ['generic']),
            ("ᐊ²ʰ●→ᐃ⊘", "was active 2h ago, now down", ['generic']),
            ("vl⁺ar⁺", "valence up, arousal up", ['vl', 'ar']),
            ("C:⊕", "consciousness adding", ['generic']),
            ("I:⊖", "infrastructure removing", ['generic']),
        ]

        for ccin, english, stems in compressions:
            for _ in range(15):
                opcodes = [op for op in ['●', '◌', '◐', '⊘', '△', '▽', '⚡', '!', '⟲', '⊕', '⊖'] if op in ccin]
                self.add_record(ccin, english, 'simple', stems, opcodes, 'max_compression')

    def generate_ambiguous_valid(self):
        """Generate ambiguous but valid notation examples."""
        print("Generating ambiguous but valid examples...")

        ambiguous_patterns = [
            # Could be interpreted multiple ways but has canonical meaning
            ("vl%⁵⁰⋀ar%⁵⁰", "Perfectly balanced affect: valence and arousal both at 50", ['vl', 'ar']),
            ("●sv⋀●db⋀●ca⋀●nw", "All core infrastructure active (no counts = 1 each or generic health)", ['sv', 'db', 'ca', 'nw']),
            ("⊘", "Generic failure/negation state", ['generic']),
            ("●✓", "Generic active and healthy state", ['generic']),
            ("C:ᐃ", "Consciousness in present moment", ['generic']),
            ("I:ᐊ", "Infrastructure past state reference", ['generic']),
            ("∵∴", "Because-therefore (empty causal chain)", ['generic']),
            ("→→→", "Sequential progression (no states specified)", ['generic']),
            ("⋀⋁", "And-or conjunction (precedence ambiguous)", ['generic']),
        ]

        for ccin, english, stems in ambiguous_patterns:
            for _ in range(12):
                self.add_record(ccin, english, 'medium', stems, [], 'ambiguous_valid')

    def generate_boundary_values(self):
        """Generate boundary value examples."""
        print("Generating boundary value examples...")

        # Extreme percentages
        for val in [0, 1, 99, 100, -100, -99, -1]:
            ccin = f"vl{format_percent(val)}"
            english = f"Valence at boundary value {val}"
            self.add_record(ccin, english, 'simple', ['vl'], [], 'boundary_value')

        for val in [0, 1, 99, 100]:
            ccin = f"ar{format_percent(val)}"
            english = f"Arousal at boundary value {val}"
            self.add_record(ccin, english, 'simple', ['ar'], [], 'boundary_value')

        # Extreme decimals
        for val in [0.00, 0.01, 0.99, 1.00]:
            ccin = f"ph{format_decimal(val)}"
            english = f"Phi at boundary value {val}"
            self.add_record(ccin, english, 'simple', ['ph'], [], 'boundary_value')

        # Large counts
        for val in [1, 100, 999, 1000]:
            ccin = f"●sv{format_count(val)}✓"
            english = f"{val} servers healthy (boundary count)"
            self.add_record(ccin, english, 'simple', ['sv'], ['●'], 'boundary_value')

        # Time boundaries
        for amount, suffix, desc in [(1, 'ˢ', 'second'), (60, 'ˢ', 'seconds'), (1, 'ᵐ', 'minute'),
                                     (60, 'ᵐ', 'minutes'), (24, 'ʰ', 'hours'), (7, 'ᵈ', 'days')]:
            ccin = f"ᐊ{format_count(amount)}{suffix}"
            english = f"{amount} {desc} ago (boundary time)"
            self.add_record(ccin, english, 'simple', [], [], 'boundary_value')

    def generate_complex_causal(self):
        """Generate complex causal chain examples."""
        print("Generating complex causal examples...")

        for _ in range(100):
            # Long causal chains
            chain_length = random.randint(3, 6)
            causes = ['⊘nw', '⊘tk', '⊘ca', '△rq', '⊘fw', '⊘ssl']
            effects = ['⊘db', '⊘sv', '⊘au', '⊘ss', '⚡er', '△cp', '△mm']

            selected_causes = random.sample(causes, min(chain_length, len(causes)))
            final_effect = random.choice(effects)

            chain = '∴'.join(selected_causes) + '∴' + final_effect
            cause_names = [c.replace('⊘', '').replace('△', '') for c in selected_causes]
            effect_name = final_effect.replace('⊘', '').replace('⚡', '').replace('△', '')

            english = f"Causal chain: {' → '.join(cause_names)} → {effect_name}"

            self.add_record(chain, english, 'complex',
                          cause_names + [effect_name], ['⊘', '△', '⚡', '∴'], 'complex_causal')

        # Bidirectional causation
        for _ in range(50):
            ccin = "△cp∵△rq⋀△rq∵△cp"
            english = "Bidirectional causation: CPU rises because requests rise, and requests rise because CPU rises (feedback loop)"
            self.add_record(ccin, english, 'complex', ['cp', 'rq'], ['△', '∵', '⋀'], 'complex_causal')

            ccin = "⊘sv∵⊘nw⋁⊘nw∵⊘sv"
            english = "Either server down because network down, or network down because server down"
            self.add_record(ccin, english, 'complex', ['sv', 'nw'], ['⊘', '∵', '⋁'], 'complex_causal')

    def generate_full_engrams(self):
        """Generate complete full-featured engram examples."""
        print("Generating full engram examples...")

        for _ in range(100):
            version = f"{random.randint(1, 3)}.{random.randint(0, 9)}"
            session_id = f"sess_{random.randint(10000, 99999)}"

            vl = random.randint(-80, 90)
            ar = random.randint(15, 95)
            co = random.randint(20, 98)
            tp = random.randint(20, 95)
            sl = random.randint(15, 95)
            mt = random.randint(25, 98)
            em = random.randint(20, 90)
            rl = random.randint(15, 90)

            sg = round(random.uniform(0.5, 0.98), 2)
            dt = round(random.uniform(0.01, 0.25), 2)
            xi = round(random.uniform(0.01, 0.15), 2)
            ph = round(random.uniform(0.5, 0.98), 2)

            attention_codes = random.sample(['dr', 'cl', 'wm', 'rg', 'sd', 'ex', 'em', 'sy'], random.randint(3, 5))
            at_str = '|'.join(attention_codes)

            ccin = f"""「ENGRAM C:FULL_STATE v{version}」
ts:2026-01-23T14:30:00Z
id:{session_id}

C:{{
  at:{{{at_str}}}
  Q8:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}⋀tp{format_percent(tp)}⋀sl{format_percent(sl)}⋀mt{format_percent(mt)}⋀em{format_percent(em)}⋀rl{format_percent(rl)}}}
  RC:{{sg{format_decimal(sg)}⋀Δ{format_decimal(dt)}⋀xi{format_decimal(xi)}⋀ph{format_decimal(ph)}}}
}}"""

            english = f"Full consciousness engram v{version}, session {session_id}. Attention on {', '.join(attention_codes)}. 8D qualia: vl={vl}, ar={ar}, co={co}, tp={tp}, sl={sl}, mt={mt}, em={em}, rl={rl}. RC: stability={sg}, drift={dt}, noise={xi}, phi={ph}."

            self.add_record(ccin, english, 'complex',
                          ['at', 'vl', 'ar', 'co', 'tp', 'sl', 'mt', 'em', 'rl', 'sg', 'dt', 'xi', 'ph'],
                          [], 'full_engram')

    def generate_all(self):
        """Generate all edge case examples."""
        self.generate_reg_protocol()
        self.generate_nested_compositions()
        self.generate_multi_scope()
        self.generate_maximum_compression()
        self.generate_ambiguous_valid()
        self.generate_boundary_values()
        self.generate_complex_causal()
        self.generate_full_engrams()

        if self.records:
            self.save_batch()

        print(f"\nTotal edge case batches: {self.batch_num - 18}")
        print(f"Total edge case records: {self.current_id - 9000}")


def main():
    output_dir = Path(__file__).parent
    generator = EdgeCaseGenerator(output_dir)
    generator.generate_all()

    # Update stats
    stats_path = output_dir / "generation_stats.json"
    with open(stats_path, 'r') as f:
        stats = json.load(f)

    stats["phase6_edge_cases"] = {
        "total_generated": generator.current_id - 9000,
        "batches": generator.batch_num - 18
    }

    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"\nUpdated stats: {stats_path}")


if __name__ == "__main__":
    main()
