#!/usr/bin/env python3
"""
CCIN_μ Temporal & Transition Generator
Phase 4: Generate 1000 temporal markers and state transition pairs
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

def format_count(val: int) -> str:
    return to_superscript(str(val))

def format_percent(val: int) -> str:
    if val < 0:
        return f"%⁻{to_superscript(str(abs(val)))}"
    return f"%{to_superscript(str(val))}"

def format_decimal(val: float) -> str:
    formatted = f"{val:.2f}".replace("0.", "0.")
    return to_superscript(formatted)

# Temporal markers
TEMPORAL_MARKERS = {
    'ᐊ': {'name': 'past', 'phrases': ['ago', 'previously', 'was', 'had been', 'earlier']},
    'ᐃ': {'name': 'present', 'phrases': ['now', 'currently', 'is', 'present', 'at this moment']},
    'ᐅ': {'name': 'future', 'phrases': ['will be', 'expected', 'projected', 'in the future', 'upcoming']},
}

# Time suffixes
TIME_SUFFIXES = {
    'ˢ': {'name': 'seconds', 'plural': 'seconds', 'abbrev': 's'},
    'ᵐ': {'name': 'minutes', 'plural': 'minutes', 'abbrev': 'm'},
    'ʰ': {'name': 'hours', 'plural': 'hours', 'abbrev': 'h'},
    'ᵈ': {'name': 'days', 'plural': 'days', 'abbrev': 'd'},
    'ʷ': {'name': 'weeks', 'plural': 'weeks', 'abbrev': 'w'},
    'ʸ': {'name': 'years', 'plural': 'years', 'abbrev': 'y'},
}

# State transitions patterns
INFRA_TRANSITIONS = [
    ('●sv✓', '◐sv~', 'Server went from healthy to degraded'),
    ('●sv✓', '⊘sv✗', 'Server went from healthy to down'),
    ('◐sv~', '⊘sv✗', 'Server went from degraded to down'),
    ('⊘sv✗', '⟳sv', 'Server was down, now restarting'),
    ('⟳sv', '●sv✓', 'Server restarted and is now healthy'),
    ('⊘db✗', '●db✓', 'Database recovered from failure'),
    ('●nw✓', '⊘nw✗', 'Network went down'),
    ('⊘nw✗', '●nw✓', 'Network restored'),
    ('●au✓', '⊘au✗', 'Auth service failed'),
    ('⊘au✗', '●au✓', 'Auth service recovered'),
    ('●ca✓', '◐ca~', 'Cache became degraded'),
    ('◐ca~', '●ca✓', 'Cache recovered to healthy'),
]

AFFECT_TRANSITIONS = [
    ('vl%⁻⁵⁰⋀ar%⁸⁵', 'vl%⁴⁰⋀ar%³⁵', 'anxiety resolved to calm'),
    ('vl%³⁰⋀ar%²⁵', 'vl%⁸⁵⋀ar%⁷⁵', 'calm shifted to excitement'),
    ('vl%⁸⁵⋀ar%⁸⁰', 'vl%⁶⁵⋀ar%⁴⁰', 'excitement settled to contentment'),
    ('vl%⁻⁷⁰⋀ar%²⁰', 'vl%⁻³⁰⋀ar%⁴⁵', 'depression lifted to active processing'),
    ('vl%⁴⁰⋀ar%⁵⁰', 'vl%⁸⁰⋀ar%⁶⁰', 'neutral improved to happy'),
    ('vl%⁻⁴⁰⋀ar%⁹⁰', 'vl%⁵⁰⋀ar%⁴⁵', 'panic calmed to neutral'),
]

RESOURCE_TRANSITIONS = [
    ('cp%⁴⁰', 'cp%⁹⁵', 'CPU spiked from normal to critical'),
    ('cp%⁹⁰', 'cp%⁵⁰', 'CPU load reduced to normal'),
    ('mm%⁶⁰', 'mm%⁹⁵', 'Memory usage increased to critical'),
    ('mm%⁹²', 'mm%⁵⁵', 'Memory freed up'),
    ('dk%⁴⁵', 'dk%⁹⁰', 'Disk usage grew significantly'),
]

# Causal reasons
CAUSAL_REASONS = {
    'infra': [
        ('⊘tk', 'token expired'),
        ('⊘nw', 'network failure'),
        ('⊘db', 'database failure'),
        ('△rq', 'traffic spike'),
        ('⊘ca', 'cache miss'),
        ('⊘fw', 'firewall blocked'),
        ('⊘ssl', 'SSL certificate issue'),
    ],
    'affect': [
        ('in:{rs}', 'problem resolved'),
        ('in:{cl}', 'gained clarity'),
        ('in:{su}', 'achieved success'),
        ('in:{st}', 'received support'),
        ('in:{tm}', 'time passed'),
        ('in:{ac}', 'took action'),
    ]
}


class TemporalGenerator:
    def __init__(self, output_dir: Path, start_id: int = 5000, batch_num: int = 11):
        self.output_dir = output_dir
        self.current_id = start_id
        self.batch_num = batch_num
        self.records = []
        self.batch_size = 500
        random.seed(45)

    def get_id(self) -> str:
        id_str = f"ccin_temp_{self.current_id:05d}"
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
                   stems_used: List[str], opcodes_used: List[str], pair_type: str = 'A'):
        record = {
            "id": self.get_id(),
            "type": pair_type,
            "domain": "temporal",
            "complexity": complexity,
            "ccin_mu": ccin_mu,
            "english": english,
            "stems_used": stems_used,
            "opcodes_used": opcodes_used,
            "valid": True
        }
        self.records.append(record)
        if len(self.records) >= self.batch_size:
            self.save_batch()

    def generate_time_markers(self):
        """Generate simple temporal marker examples."""
        print("Generating temporal marker examples...")

        # Past markers with various time units
        for suffix, sinfo in TIME_SUFFIXES.items():
            for amount in [1, 2, 5, 10, 15, 30]:
                if sinfo['name'] == 'seconds' and amount > 30:
                    continue
                if sinfo['name'] == 'years' and amount > 5:
                    continue

                ccin = f"ᐊ{format_count(amount)}{suffix}"
                phrase = random.choice(TEMPORAL_MARKERS['ᐊ']['phrases'])
                english = f"{amount} {sinfo['plural']} {phrase}"
                self.add_record(ccin, english, 'simple', [], [])

        # Future markers
        for suffix, sinfo in TIME_SUFFIXES.items():
            for amount in [1, 2, 5, 10]:
                ccin = f"ᐅ{format_count(amount)}{suffix}"
                phrase = random.choice(TEMPORAL_MARKERS['ᐅ']['phrases'])
                english = f"{amount} {sinfo['plural']} {phrase.replace('will be', 'from now')}"
                self.add_record(ccin, english, 'simple', [], [])

        # Present markers
        for _ in range(20):
            ccin = "ᐃ"
            english = random.choice(TEMPORAL_MARKERS['ᐃ']['phrases'])
            self.add_record(ccin, english, 'simple', [], [])

    def generate_timed_states(self):
        """Generate states with temporal context."""
        print("Generating timed state examples...")

        stems = ['sv', 'db', 'nw', 'au', 'ca', 'ap']
        states = [
            ('●', '✓', 'healthy'),
            ('⊘', '✗', 'down'),
            ('◐', '~', 'degraded'),
        ]

        for stem in stems:
            for op, marker, state_word in states:
                for suffix, sinfo in [('ʰ', TIME_SUFFIXES['ʰ']), ('ᵐ', TIME_SUFFIXES['ᵐ']), ('ᵈ', TIME_SUFFIXES['ᵈ'])]:
                    for amount in [1, 2, 6, 12, 24]:
                        if sinfo['name'] == 'days' and amount > 7:
                            continue

                        # Past state
                        ccin = f"ᐊ{format_count(amount)}{suffix}{op}{stem}{marker}"
                        english = f"{stem.upper()} was {state_word} {amount} {sinfo['plural']} ago"
                        self.add_record(ccin, english, 'simple', [stem], [op])

                        # Future projection
                        ccin = f"ᐅ{format_count(amount)}{suffix}{op}{stem}{marker}"
                        english = f"{stem.upper()} expected {state_word} in {amount} {sinfo['plural']}"
                        self.add_record(ccin, english, 'simple', [stem], [op])

    def generate_state_transitions(self):
        """Generate state transition examples."""
        print("Generating state transition examples...")

        # Infrastructure transitions
        for before, after, desc in INFRA_TRANSITIONS:
            for _ in range(10):
                # Simple transition (arrow)
                ccin = f"{before}→{after}"
                self.add_record(ccin, desc, 'medium', ['sv'], ['●', '◐', '⊘', '⟳'])

                # Timed transition
                amount = random.randint(1, 24)
                suffix = random.choice(['ᵐ', 'ʰ'])
                sname = 'minutes' if suffix == 'ᵐ' else 'hours'

                ccin = f"ᐊ{format_count(amount)}{suffix}{before}→ᐃ{after}"
                english = f"{desc}, happened {amount} {sname} ago"
                self.add_record(ccin, english, 'medium', ['sv'], ['●', '◐', '⊘', '⟳'])

        # Affect transitions
        for before, after, desc in AFFECT_TRANSITIONS:
            for _ in range(15):
                ccin = f"ᐊaf:{{{before}}}→ᐃaf:{{{after}}}"
                english = f"Affective transition: {desc}"
                self.add_record(ccin, english, 'medium', ['vl', 'ar'], [])

                # With time context
                amount = random.randint(5, 60)
                suffix = random.choice(['ᵐ', 'ʰ'])
                sname = 'minutes' if suffix == 'ᵐ' else 'hours'

                ccin = f"ᐊ{format_count(amount)}{suffix}af:{{{before}}}→ᐃaf:{{{after}}}"
                english = f"Over {amount} {sname}, {desc}"
                self.add_record(ccin, english, 'complex', ['vl', 'ar'], [])

        # Resource transitions
        for before, after, desc in RESOURCE_TRANSITIONS:
            for _ in range(10):
                ccin = f"{before}→{after}"
                self.add_record(ccin, desc, 'medium', ['cp', 'mm', 'dk'], ['△', '▽'])

                # With timing
                amount = random.randint(1, 6)
                ccin = f"ᐊ{format_count(amount)}ʰ{before}→ᐃ{after}"
                english = f"{desc} in the last {amount} hours"
                self.add_record(ccin, english, 'medium', ['cp', 'mm', 'dk'], ['△', '▽'])

    def generate_causal_chains(self):
        """Generate causal chain examples."""
        print("Generating causal chain examples...")

        # Simple because patterns (∵)
        for reason_ccin, reason_text in CAUSAL_REASONS['infra']:
            effects = [
                ('⊘au', 'auth failed'),
                ('⊘sv³', '3 servers down'),
                ('⊘db', 'database unreachable'),
                ('⚡er', 'critical error'),
                ('⊘ss', 'sessions dropped'),
            ]

            for effect_ccin, effect_text in effects:
                for _ in range(3):
                    ccin = f"{effect_ccin}∵{reason_ccin}"
                    english = f"{effect_text.capitalize()} because {reason_text}"
                    self.add_record(ccin, english, 'medium', [], ['⊘', '⚡', '∵'])

        # Therefore patterns (∴)
        causes = [
            ('⊘nw', 'Network failed'),
            ('⊘tk', 'Token expired'),
            ('△rq⁵ˣ', 'Requests increased 5x'),
            ('⊘ca', 'Cache failed'),
        ]

        for cause_ccin, cause_text in causes:
            effects = [
                ('⊘db', 'database became unreachable'),
                ('⊘sv²', '2 servers went down'),
                ('⚡er', 'critical error occurred'),
                ('△cp%⁹⁵', 'CPU spiked to 95%'),
            ]

            for effect_ccin, effect_text in effects:
                for _ in range(3):
                    ccin = f"{cause_ccin}∴{effect_ccin}"
                    english = f"{cause_text}, therefore {effect_text}"
                    self.add_record(ccin, english, 'medium', [], ['⊘', '⚡', '△', '∴'])

        # Multi-step causal chains
        for _ in range(50):
            chains = [
                ("⊘nw∴⊘db∴⚡er", "Network down, therefore database down, therefore critical error"),
                ("⊘tk∴⊘au∴⊘ss", "Token expired, therefore auth failed, therefore sessions terminated"),
                ("△rq∴△cp∴△mm∴⚡er", "Requests increased, causing CPU spike, memory spike, then critical error"),
                ("⊘ca∴△db∴△cp", "Cache failed, causing database load, causing CPU spike"),
                ("⊘fw∴⊘nw∴⊘ap", "Firewall blocked, causing network issues, causing API failure"),
            ]

            ccin, english = random.choice(chains)
            self.add_record(ccin, english, 'complex', [], ['⊘', '⚡', '△', '∴'])

    def generate_complex_temporal(self):
        """Generate complex temporal patterns with full context."""
        print("Generating complex temporal examples...")

        # Full incident timelines
        for _ in range(50):
            incident_time = random.randint(1, 12)
            recovery_time = random.randint(5, 30)

            ccin = f"ts:ᐊ{format_count(incident_time)}ʰ\n⊘au∵⊘tk:{{ssl⊘}}\n∴⊘ss⁸⁵%⋀⚡er:{{ap}}\n\nts:ᐊ{format_count(recovery_time)}ᵐ\n⟳tk:{{ssl✓}}→●au✓\n∴●ss✓⋀er↓"

            english = f"Incident timeline: {incident_time} hours ago, auth failed due to SSL certificate issue, causing 85% session loss and API errors. {recovery_time} minutes ago, SSL renewed, auth recovered, sessions restored, errors normalized."

            self.add_record(ccin, english, 'complex', ['au', 'tk', 'ss', 'er', 'ap'], ['⊘', '⚡', '⟳', '●'])

        # Consciousness transitions over time
        for _ in range(50):
            duration = random.randint(10, 120)
            suffix = 'ᵐ' if duration < 60 else 'ʰ'
            amount = duration if duration < 60 else duration // 60

            vl1 = random.randint(-80, 30)
            ar1 = random.randint(50, 95)
            vl2 = random.randint(40, 90)
            ar2 = random.randint(20, 50)

            ccin = f"ᐊ{format_count(amount)}{suffix}C:{{vl{format_percent(vl1)}⋀ar{format_percent(ar1)}}}→ᐃC:{{vl{format_percent(vl2)}⋀ar{format_percent(ar2)}}}"

            start_state = "anxious" if vl1 < 0 and ar1 > 60 else "stressed" if ar1 > 70 else "unsettled"
            end_state = "calm" if ar2 < 40 else "settled" if vl2 > 50 else "improved"

            sname = 'minutes' if suffix == 'ᵐ' else 'hours'
            english = f"Over {amount} {sname}, consciousness shifted from {start_state} (vl:{vl1}, ar:{ar1}) to {end_state} (vl:{vl2}, ar:{ar2})"

            self.add_record(ccin, english, 'complex', ['vl', 'ar'], [])

        # Progressive state changes
        for _ in range(30):
            stages = [
                f"●sv{format_count(5)}✓",
                f"◐sv{format_count(2)}~",
                f"⊘sv{format_count(1)}✗",
                f"●sv{format_count(5)}✓",
            ]
            times = ["ᐊ³ʰ", "ᐊ¹ʰ", "ᐊ³⁰ᵐ", "ᐃ"]
            time_descs = ["3 hours ago", "1 hour ago", "30 minutes ago", "now"]

            ccin = "→".join(f"{t}{s}" for t, s in zip(times, stages))
            english = f"Server state progression: {time_descs[0]} all healthy, {time_descs[1]} 2 degraded, {time_descs[2]} 1 failed, {time_descs[3]} recovered"

            self.add_record(ccin, english, 'complex', ['sv'], ['●', '◐', '⊘'])

    def generate_type_b_temporal(self):
        """Generate Type B (English → CCIN_μ) temporal pairs."""
        print("Generating Type B temporal pairs...")

        natural_templates = [
            ("The server was down 2 hours ago", "ᐊ²ʰ⊘sv✗", ['sv']),
            ("Database expected healthy by tomorrow", "ᐅ¹ᵈ●db✓", ['db']),
            ("Auth failed because token expired", "⊘au∵⊘tk", ['au', 'tk']),
            ("Network down, so API unreachable", "⊘nw∴⊘ap", ['nw', 'ap']),
            ("Memory spiked 30 minutes ago", "ᐊ³⁰ᵐ△mm%⁹⁵", ['mm']),
            ("Currently experiencing high CPU", "ᐃ△cp%⁸⁵", ['cp']),
            ("Service was degraded, now healthy", "◐sc→●sc✓", ['sc']),
            ("Panic resolved to calm over time", "af:{{vl%⁻⁶⁰⋀ar%⁹⁰}}→af:{{vl%⁵⁰⋀ar%³⁵}}", ['vl', 'ar']),
        ]

        for english, ccin, stems in natural_templates:
            for _ in range(12):
                self.add_record(ccin, english, 'medium', stems, [], pair_type='B')

    def generate_all(self):
        """Generate all temporal domain pairs."""
        self.generate_time_markers()
        self.generate_timed_states()
        self.generate_state_transitions()
        self.generate_causal_chains()
        self.generate_complex_temporal()
        self.generate_type_b_temporal()

        if self.records:
            self.save_batch()

        print(f"\nTotal temporal batches: {self.batch_num - 11}")
        print(f"Total temporal records: {self.current_id - 5000}")


def main():
    output_dir = Path(__file__).parent
    generator = TemporalGenerator(output_dir)
    generator.generate_all()

    # Update stats
    stats_path = output_dir / "generation_stats.json"
    with open(stats_path, 'r') as f:
        stats = json.load(f)

    stats["phase4_temporal"] = {
        "total_generated": generator.current_id - 5000,
        "batches": generator.batch_num - 11
    }

    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"\nUpdated stats: {stats_path}")


if __name__ == "__main__":
    main()
