#!/usr/bin/env python3
"""
CCIN_μ Targeted Expansion Generator
Focuses on under-represented domains, types, stems, and opcodes
"""

import json
import random
import time
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import math

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


class TargetedGenerator:
    def __init__(self, output_dir: Path, start_batch: int = 51):
        self.output_dir = output_dir
        self.batch_num = start_batch
        self.records = []
        self.batch_size = 500
        self.total_generated = 0
        random.seed(int(time.time()) + 12345)

    def get_id(self) -> str:
        id_str = f"ccin_tgt_{self.total_generated + 30000:05d}"
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

    # ==================== AFFECT DOMAIN EXPANSION ====================

    def generate_affect_states(self, count: int = 400):
        """Generate detailed affect state examples."""
        print(f"Generating {count} affect state examples...")

        affect_descriptors = [
            # (name, vl_range, ar_range, description)
            ('joy', (70, 95), (60, 85), 'joyful and energized'),
            ('contentment', (65, 85), (20, 40), 'content and relaxed'),
            ('excitement', (75, 95), (75, 95), 'excited and stimulated'),
            ('serenity', (70, 90), (10, 30), 'serene and peaceful'),
            ('interest', (55, 75), (50, 70), 'interested and engaged'),
            ('amusement', (70, 90), (55, 75), 'amused and entertained'),
            ('pride', (75, 90), (50, 70), 'proud and accomplished'),
            ('love', (85, 98), (45, 65), 'loving and connected'),
            ('awe', (70, 90), (60, 80), 'awed and inspired'),
            ('gratitude', (80, 95), (35, 55), 'grateful and appreciative'),
            ('hope', (65, 85), (45, 65), 'hopeful and optimistic'),
            ('sadness', (-70, -40), (20, 45), 'sad and melancholic'),
            ('anxiety', (-60, -30), (70, 90), 'anxious and worried'),
            ('fear', (-75, -50), (80, 95), 'fearful and alarmed'),
            ('anger', (-65, -35), (75, 95), 'angry and frustrated'),
            ('disgust', (-70, -45), (50, 70), 'disgusted and repulsed'),
            ('boredom', (-30, -5), (10, 30), 'bored and unstimulated'),
            ('confusion', (-40, -10), (55, 75), 'confused and uncertain'),
            ('surprise', (0, 50), (70, 90), 'surprised and startled'),
            ('nostalgia', (30, 60), (30, 50), 'nostalgic and wistful'),
        ]

        for _ in range(count):
            name, vl_range, ar_range, desc = random.choice(affect_descriptors)
            vl = random.randint(*vl_range)
            ar = random.randint(*ar_range)

            ccin = f"af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}"
            english = f"Affective state: {desc} - valence {vl}, arousal {ar}"

            self.add_record(ccin, english, 'simple', 'affect', ['vl', 'ar'], [])

    def generate_affect_transitions(self, count: int = 300):
        """Generate affect state transitions."""
        print(f"Generating {count} affect transition examples...")

        states = [
            ('calm', (50, 70), (15, 35)),
            ('anxious', (-50, -20), (70, 90)),
            ('happy', (70, 90), (50, 70)),
            ('sad', (-60, -30), (20, 40)),
            ('excited', (75, 95), (75, 95)),
            ('peaceful', (60, 80), (10, 25)),
            ('frustrated', (-50, -25), (65, 85)),
            ('content', (65, 85), (25, 45)),
        ]

        for _ in range(count):
            from_state, from_vl_r, from_ar_r = random.choice(states)
            to_state, to_vl_r, to_ar_r = random.choice(states)

            from_vl = random.randint(*from_vl_r)
            from_ar = random.randint(*from_ar_r)
            to_vl = random.randint(*to_vl_r)
            to_ar = random.randint(*to_ar_r)

            # Use temporal markers
            ccin = f"ᐊaf:{{vl{format_percent(from_vl)}⋀ar{format_percent(from_ar)}}}»ᐃaf:{{vl{format_percent(to_vl)}⋀ar{format_percent(to_ar)}}}"
            english = f"Affect transition: was {from_state} (v={from_vl}, a={from_ar}) → now {to_state} (v={to_vl}, a={to_ar})"

            self.add_record(ccin, english, 'medium', 'affect', ['vl', 'ar'], [])

    def generate_affect_with_coherence(self, count: int = 300):
        """Generate affect states with coherence dimension."""
        print(f"Generating {count} affect+coherence examples...")

        for _ in range(count):
            vl = random.randint(-80, 90)
            ar = random.randint(10, 95)
            co = random.randint(20, 98)

            vl_word = 'positive' if vl > 20 else 'negative' if vl < -20 else 'neutral'
            ar_word = 'high' if ar > 60 else 'low' if ar < 40 else 'moderate'
            co_word = 'high' if co > 70 else 'low' if co < 40 else 'moderate'

            ccin = f"af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}}}"
            english = f"Affect state: {vl_word} valence ({vl}), {ar_word} arousal ({ar}), {co_word} coherence ({co})"

            self.add_record(ccin, english, 'medium', 'affect', ['vl', 'ar', 'co'], [])

    # ==================== TYPE C SIMILARITY EXPANSION ====================

    def compute_similarity(self, vals1: Dict, vals2: Dict) -> float:
        """Compute similarity between two value dicts."""
        common = set(vals1.keys()) & set(vals2.keys())
        if not common:
            return 0.0
        dot = sum(vals1[k] * vals2[k] for k in common)
        n1 = math.sqrt(sum(v**2 for k, v in vals1.items() if k in common))
        n2 = math.sqrt(sum(v**2 for k, v in vals2.items() if k in common))
        if n1 == 0 or n2 == 0:
            return 0.0
        return round(dot / (n1 * n2), 2)

    def generate_temporal_similarity_triplets(self, count: int = 200):
        """Generate temporal pattern similarity triplets."""
        print(f"Generating {count} temporal similarity triplets...")

        for _ in range(count):
            # Anchor: past→present state
            stem = random.choice(['sv', 'db', 'au', 'cp', 'mm'])
            past_op = random.choice(['●', '◐', '⊘'])
            present_op = random.choice(['●', '◐', '⊘'])

            anchor = f"ᐊ{past_op}{stem}»ᐃ{present_op}{stem}"

            # Positive: similar transition pattern
            pos_past = past_op
            pos_present = present_op
            pos = f"ᐊ{pos_past}{stem}»ᐃ{pos_present}{stem}✓"

            # Negative: different transition pattern
            neg_past = random.choice([op for op in ['●', '◐', '⊘'] if op != past_op])
            neg_present = random.choice([op for op in ['●', '◐', '⊘'] if op != present_op])
            neg = f"ᐊ{neg_past}{stem}»ᐃ{neg_present}{stem}"

            stem_name = {'sv': 'server', 'db': 'database', 'au': 'auth', 'cp': 'CPU', 'mm': 'memory'}[stem]
            op_names = {'●': 'active', '◐': 'partial', '⊘': 'down'}

            anchor_desc = f"{stem_name} {op_names[past_op]}→{op_names[present_op]}"

            record = {
                "id": self.get_id(),
                "type": "C",
                "domain": "temporal",
                "complexity": "medium",
                "anchor": anchor,
                "positive": pos,
                "negative": neg,
                "anchor_english": anchor_desc,
                "similarity_score": 0.95,
                "stems_used": [stem],
                "opcodes_used": list(set([past_op, present_op])),
                "valid": True
            }
            self.records.append(record)
            if len(self.records) >= self.batch_size:
                self.save_batch()

    def generate_infrastructure_similarity_triplets(self, count: int = 200):
        """Generate infrastructure state similarity triplets."""
        print(f"Generating {count} infrastructure similarity triplets...")

        for _ in range(count):
            # Create anchor infrastructure state
            sv_count = random.randint(2, 8)
            db_count = random.randint(1, 4)
            sv_status = random.choice(['●', '◐'])
            db_status = random.choice(['●', '◐', '⊘'])

            anchor = f"P:{{{sv_status}sv{format_count(sv_count)}⋀{db_status}db{format_count(db_count)}}}"

            # Positive: similar counts and status
            pos_sv = sv_count + random.randint(-1, 1)
            pos_db = db_count + random.randint(-1, 1)
            pos_sv = max(1, pos_sv)
            pos_db = max(1, pos_db)
            positive = f"P:{{{sv_status}sv{format_count(pos_sv)}⋀{db_status}db{format_count(pos_db)}}}"

            # Negative: very different
            neg_sv = sv_count + random.randint(3, 6) * random.choice([-1, 1])
            neg_sv = max(1, neg_sv)
            neg_status = '⊘' if sv_status == '●' else '●'
            negative = f"P:{{{neg_status}sv{format_count(neg_sv)}⋀⊘db{format_count(1)}}}"

            record = {
                "id": self.get_id(),
                "type": "C",
                "domain": "infrastructure",
                "complexity": "medium",
                "anchor": anchor,
                "positive": positive,
                "negative": negative,
                "anchor_english": f"{sv_count} servers, {db_count} databases",
                "similarity_score": 0.88,
                "stems_used": ['sv', 'db'],
                "opcodes_used": list(set([sv_status, db_status])),
                "valid": True
            }
            self.records.append(record)
            if len(self.records) >= self.batch_size:
                self.save_batch()

    # ==================== UNDER-USED STEMS EXPANSION ====================

    def generate_user_patterns(self, count: int = 200):
        """Generate patterns with user (us) stem."""
        print(f"Generating {count} user pattern examples...")

        for _ in range(count):
            user_count = random.randint(10, 10000)
            op = random.choice(['●', '◐', '△', '▽', '⊕', '⊖'])

            templates = [
                (f"{op}us{format_count(user_count)}", f"{'Active' if op == '●' else 'Partial' if op == '◐' else 'Increasing' if op == '△' else 'Decreasing' if op == '▽' else 'Adding' if op == '⊕' else 'Removing'} {user_count} users"),
                (f"●us{format_count(user_count)}⋀●ss{format_count(int(user_count * 0.8))}", f"{user_count} active users with {int(user_count * 0.8)} sessions"),
                (f"△us{format_percent(random.randint(5, 50))}ᵈ", f"User growth {random.randint(5, 50)}% daily"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'simple', 'infrastructure', ['us', 'ss'][:random.randint(1, 2)], [op])

    def generate_logging_patterns(self, count: int = 150):
        """Generate patterns with log (lg) stem."""
        print(f"Generating {count} logging pattern examples...")

        for _ in range(count):
            op = random.choice(['●', '◌', '◐', '⚡', '△', '▽'])
            count_val = random.randint(10, 10000)

            templates = [
                (f"{op}lg{format_count(count_val)}ˢ", f"{'Active' if op == '●' else 'No' if op == '◌' else 'Partial' if op == '◐' else 'Critical' if op == '⚡' else 'Increasing' if op == '△' else 'Decreasing'} logging at {count_val}/sec"),
                (f"●lg✓⋀er{format_count(random.randint(0, 10))}", f"Logging active, {random.randint(0, 10)} errors captured"),
                (f"⚡lg!∵△ev{format_count(count_val)}", f"Critical logging alert due to {count_val} events spike"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'simple', 'infrastructure', ['lg', 'er', 'ev'][:random.randint(1, 3)], [op])

    def generate_event_message_patterns(self, count: int = 150):
        """Generate patterns with event (ev) and message (mg) stems."""
        print(f"Generating {count} event/message pattern examples...")

        for _ in range(count):
            ev_count = random.randint(100, 50000)
            mg_count = random.randint(50, 10000)

            templates = [
                (f"●ev{format_count(ev_count)}ˢ⋀●mg{format_count(mg_count)}ˢ", f"{ev_count} events/sec, {mg_count} messages/sec"),
                (f"△ev{format_percent(random.randint(10, 100))}⋀◐qu{format_count(random.randint(100, 5000))}", f"Events up {random.randint(10, 100)}%, queue at {random.randint(100, 5000)}"),
                (f"⚡ev!∵△mg{format_count(mg_count)}", f"Event alert due to message spike of {mg_count}"),
                (f"●ev{format_count(ev_count)}»●qu{format_count(int(ev_count * 0.1))}»●wk{format_count(random.randint(4, 16))}", f"{ev_count} events flow to queue of {int(ev_count * 0.1)}, processed by {random.randint(4, 16)} workers"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'infrastructure', ['ev', 'mg', 'qu', 'wk'][:random.randint(2, 4)], ['●', '△', '⚡'][:random.randint(1, 2)])

    def generate_vm_cluster_patterns(self, count: int = 150):
        """Generate patterns with vm and cluster (cl) stems."""
        print(f"Generating {count} VM/cluster pattern examples...")

        for _ in range(count):
            vm_count = random.randint(2, 50)
            cl_count = random.randint(1, 5)

            templates = [
                (f"●vm{format_count(vm_count)}✓⋀●cl{format_count(cl_count)}✓", f"{vm_count} VMs healthy across {cl_count} clusters"),
                (f"◐vm{format_count(vm_count)}~⋀cp{format_percent(random.randint(60, 95))}", f"{vm_count} VMs degraded, CPU at {random.randint(60, 95)}%"),
                (f"P:{{●cl{format_count(cl_count)}⋀●vm{format_count(vm_count)}⋀●nd{format_count(vm_count * 2)}}}", f"Production: {cl_count} clusters, {vm_count} VMs, {vm_count * 2} nodes"),
                (f"△vm{format_count(random.randint(1, 5))}∵△rq{format_percent(random.randint(20, 80))}", f"Scaling up {random.randint(1, 5)} VMs due to {random.randint(20, 80)}% request increase"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'infrastructure', ['vm', 'cl', 'nd', 'cp', 'rq'][:random.randint(2, 4)], ['●', '◐', '△'][:random.randint(1, 2)])

    # ==================== UNDER-USED OPCODES EXPANSION ====================

    def generate_inactive_patterns(self, count: int = 200):
        """Generate patterns with inactive (◌) opcode."""
        print(f"Generating {count} inactive (◌) opcode examples...")

        stems = ['sv', 'db', 'ca', 'nw', 'au', 'ct', 'vm', 'wk']
        stem_names = {'sv': 'server', 'db': 'database', 'ca': 'cache', 'nw': 'network',
                     'au': 'auth', 'ct': 'container', 'vm': 'VM', 'wk': 'worker'}

        for _ in range(count):
            stem = random.choice(stems)
            count_val = random.randint(1, 5)

            templates = [
                (f"◌{stem}{format_count(count_val)}", f"{count_val} {stem_names[stem]}{'s' if count_val > 1 else ''} inactive"),
                (f"◌{stem}⋀●{random.choice([s for s in stems if s != stem])}✓", f"{stem_names[stem]} inactive, {stem_names[random.choice([s for s in stems if s != stem])]} active"),
                (f"ᐊ●{stem}»ᐃ◌{stem}", f"{stem_names[stem]} was active, now inactive"),
                (f"◌{stem}∵⊘nw", f"{stem_names[stem]} inactive because network down"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'simple', 'infrastructure', [stem], ['◌'])

    def generate_optional_patterns(self, count: int = 150):
        """Generate patterns with optional (◇) opcode."""
        print(f"Generating {count} optional (◇) opcode examples...")

        for _ in range(count):
            stem = random.choice(['lg', 'ca', 'mt', 'ev', 'cf'])
            stem_names = {'lg': 'logging', 'ca': 'cache', 'mt': 'metrics', 'ev': 'events', 'cf': 'config'}

            templates = [
                (f"◇{stem}", f"{stem_names[stem]} optional"),
                (f"▣au⋀◇{stem}", f"Auth required, {stem_names[stem]} optional"),
                (f"P:{{●sv³✓⋀◇{stem}}}", f"Production: 3 servers healthy, {stem_names[stem]} optional"),
                (f"◇{stem}⋁▣{stem}", f"{stem_names[stem]} either optional or required"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'simple', 'infrastructure', [stem, 'au', 'sv'][:random.randint(1, 3)], ['◇', '▣'][:random.randint(1, 2)])

    def generate_required_empty_patterns(self, count: int = 150):
        """Generate patterns with required (▣) and empty (▢) opcodes."""
        print(f"Generating {count} required/empty opcode examples...")

        for _ in range(count):
            stem = random.choice(['au', 'tk', 'cf', 'ss', 'az'])
            stem_names = {'au': 'authentication', 'tk': 'token', 'cf': 'config', 'ss': 'session', 'az': 'authorization'}

            # Required patterns
            req_templates = [
                (f"▣{stem}", f"{stem_names[stem]} required"),
                (f"▣{stem}⊣●sv", f"{stem_names[stem]} required before server access"),
                (f"▣au⋀▣az⋀▣tk", f"Auth, authorization, and token all required"),
            ]

            # Empty patterns
            empty_templates = [
                (f"▢{stem}", f"{stem_names[stem]} empty/null"),
                (f"▢{stem}»⚡er", f"Empty {stem_names[stem]} causing error"),
                (f"▢tk∴⊘au", f"Empty token therefore auth failed"),
            ]

            if random.random() > 0.5:
                ccin, english = random.choice(req_templates)
                self.add_record(ccin, english, 'simple', 'infrastructure', [stem, 'au', 'az', 'tk', 'sv'][:random.randint(1, 4)], ['▣'])
            else:
                ccin, english = random.choice(empty_templates)
                self.add_record(ccin, english, 'simple', 'infrastructure', [stem, 'er', 'au', 'tk'][:random.randint(1, 3)], ['▢', '⚡', '⊘'][:random.randint(1, 2)])

    # ==================== TEMPORAL DOMAIN EXPANSION ====================

    def generate_duration_patterns(self, count: int = 200):
        """Generate duration-based temporal patterns."""
        print(f"Generating {count} duration pattern examples...")

        for _ in range(count):
            stem = random.choice(['sv', 'db', 'pr', 'jb', 'dp'])
            stem_names = {'sv': 'server', 'db': 'database', 'pr': 'process', 'jb': 'job', 'dp': 'deployment'}

            duration = random.randint(1, 60)
            unit = random.choice(['ˢ', 'ᵐ', 'ʰ', 'ᵈ'])
            unit_names = {'ˢ': 'seconds', 'ᵐ': 'minutes', 'ʰ': 'hours', 'ᵈ': 'days'}

            op = random.choice(['●', '◐', '⊘'])
            op_names = {'●': 'active', '◐': 'partial', '⊘': 'down'}

            templates = [
                (f"ᐃ{format_count(duration)}{unit}{op}{stem}", f"{stem_names[stem]} {op_names[op]} for {duration} {unit_names[unit]}"),
                (f"ᐊ{format_count(duration)}{unit}{op}{stem}»ᐃ●{stem}✓", f"{stem_names[stem]} was {op_names[op]} {duration} {unit_names[unit]} ago, now healthy"),
                (f"ᐅ{format_count(duration)}{unit}●{stem}", f"{stem_names[stem]} will be active in {duration} {unit_names[unit]}"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'temporal', [stem], [op])

    def generate_scheduled_patterns(self, count: int = 200):
        """Generate scheduled/future temporal patterns."""
        print(f"Generating {count} scheduled pattern examples...")

        for _ in range(count):
            action = random.choice(['dp', 'rs', 'up', 'sp'])
            action_names = {'dp': 'deployment', 'rs': 'restart', 'up': 'update', 'sp': 'stop'}

            time_val = random.randint(1, 48)
            unit = random.choice(['ᵐ', 'ʰ'])
            unit_name = 'minutes' if unit == 'ᵐ' else 'hours'

            target = random.choice(['sv', 'db', 'ct', 'vm'])
            target_names = {'sv': 'servers', 'db': 'databases', 'ct': 'containers', 'vm': 'VMs'}
            count_val = random.randint(1, 10)

            ccin = f"ᐅ{format_count(time_val)}{unit}●{action}»●{target}{format_count(count_val)}"
            english = f"Scheduled: {action_names[action]} of {count_val} {target_names[target]} in {time_val} {unit_name}"

            self.add_record(ccin, english, 'medium', 'temporal', [action, target], ['●'])

    def run_generation_cycle(self):
        """Run one full targeted generation cycle."""
        print(f"\n{'='*50}")
        print(f"Starting targeted generation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        # Affect domain expansion
        self.generate_affect_states(400)
        self.generate_affect_transitions(300)
        self.generate_affect_with_coherence(300)

        # Type C similarity expansion
        self.generate_temporal_similarity_triplets(200)
        self.generate_infrastructure_similarity_triplets(200)

        # Under-used stems expansion
        self.generate_user_patterns(200)
        self.generate_logging_patterns(150)
        self.generate_event_message_patterns(150)
        self.generate_vm_cluster_patterns(150)

        # Under-used opcodes expansion
        self.generate_inactive_patterns(200)
        self.generate_optional_patterns(150)
        self.generate_required_empty_patterns(150)

        # Temporal domain expansion
        self.generate_duration_patterns(200)
        self.generate_scheduled_patterns(200)

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

    print(f"Starting targeted expansion from batch {start_batch}")

    generator = TargetedGenerator(output_dir, start_batch)

    # Run 3 cycles for comprehensive coverage
    for cycle in range(3):
        print(f"\n*** CYCLE {cycle + 1}/3 ***")
        generator.run_generation_cycle()
        if cycle < 2:
            print("Pausing 60 seconds...")
            time.sleep(60)

    print(f"\n{'='*50}")
    print(f"TARGETED EXPANSION COMPLETE")
    print(f"Total new records: {generator.total_generated}")
    print(f"{'='*50}")

    # Run validation
    print("\nRunning validation...")
    import subprocess
    subprocess.run(['python3', 'validate_and_assemble.py'], cwd=output_dir)


if __name__ == "__main__":
    main()
