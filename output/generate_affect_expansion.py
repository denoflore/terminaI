#!/usr/bin/env python3
"""
CCIN_μ Affect Domain Expansion Generator
Focuses on emotional states, valence/arousal, and affective transitions
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


class AffectGenerator:
    def __init__(self, output_dir: Path, start_batch: int = 123):
        self.output_dir = output_dir
        self.batch_num = start_batch
        self.records = []
        self.batch_size = 500
        self.total_generated = 0
        random.seed(int(time.time()) + 11111)

    def get_id(self) -> str:
        id_str = f"ccin_aff_{self.total_generated + 55000:05d}"
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

    # ==================== BASIC AFFECT PATTERNS ====================

    def generate_valence_arousal_states(self, count: int = 400):
        """Generate basic valence-arousal state patterns."""
        print(f"Generating {count} valence-arousal state patterns...")

        emotions = [
            ('joy', 75, 90, 60, 85),
            ('contentment', 60, 85, 20, 45),
            ('excitement', 70, 95, 75, 95),
            ('serenity', 65, 88, 10, 35),
            ('interest', 50, 75, 45, 70),
            ('amusement', 65, 90, 55, 80),
            ('pride', 70, 92, 45, 70),
            ('love', 80, 98, 40, 70),
            ('awe', 65, 90, 55, 80),
            ('gratitude', 75, 95, 30, 55),
            ('hope', 60, 85, 40, 65),
            ('sadness', -75, -35, 20, 50),
            ('anxiety', -65, -25, 70, 95),
            ('fear', -80, -45, 75, 98),
            ('anger', -70, -30, 70, 95),
            ('disgust', -75, -40, 45, 75),
            ('boredom', -35, -5, 10, 35),
            ('confusion', -45, -10, 50, 75),
            ('surprise', -20, 60, 65, 90),
            ('nostalgia', 20, 55, 25, 50),
        ]

        for _ in range(count):
            name, vl_min, vl_max, ar_min, ar_max = random.choice(emotions)
            vl = random.randint(vl_min, vl_max)
            ar = random.randint(ar_min, ar_max)

            templates = [
                (f"af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}",
                 f"Affect: {name} - valence {vl}%, arousal {ar}%"),
                (f"●{name}⋀vl{format_percent(vl)}⋀ar{format_percent(ar)}",
                 f"Active {name}: valence={vl}, arousal={ar}"),
                (f"E:{{af:{{●{name}⋀vl{format_percent(vl)}⋀ar{format_percent(ar)}}}}}",
                 f"Entity experiencing {name} (v={vl}, a={ar})"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'simple', 'affect', ['vl', 'ar'], ['●'])

    def generate_affect_intensities(self, count: int = 300):
        """Generate affect intensity patterns."""
        print(f"Generating {count} affect intensity patterns...")

        emotions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust', 'interest', 'contentment']

        for _ in range(count):
            emotion = random.choice(emotions)
            intensity = random.randint(10, 100)
            
            intensity_word = 'mild' if intensity < 40 else 'moderate' if intensity < 70 else 'intense'

            templates = [
                (f"●{emotion}{format_percent(intensity)}",
                 f"{intensity_word.capitalize()} {emotion} at {intensity}% intensity"),
                (f"af:{{●{emotion}⋀int{format_percent(intensity)}}}",
                 f"Affect: {emotion} with {intensity}% intensity ({intensity_word})"),
                (f"E:{{●{emotion}{format_percent(intensity)}⋀sl{format_percent(random.randint(40, 95))}}}",
                 f"Entity: {intensity_word} {emotion} at {intensity}%, salient"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'simple', 'affect', ['vl', 'ar', 'sl'][:random.randint(1, 3)], ['●'])

    # ==================== AFFECT TRANSITIONS ====================

    def generate_affect_transitions(self, count: int = 300):
        """Generate affect state transitions."""
        print(f"Generating {count} affect transition patterns...")

        states = [
            ('calm', 55, 25), ('anxious', -45, 80), ('happy', 80, 65),
            ('sad', -55, 30), ('excited', 85, 90), ('peaceful', 70, 20),
            ('frustrated', -50, 75), ('content', 70, 35), ('angry', -60, 85),
            ('hopeful', 65, 50), ('fearful', -70, 90), ('relaxed', 60, 20),
        ]

        for _ in range(count):
            from_state = random.choice(states)
            to_state = random.choice([s for s in states if s[0] != from_state[0]])

            from_name, from_vl, from_ar = from_state
            to_name, to_vl, to_ar = to_state

            # Add some variation
            from_vl += random.randint(-10, 10)
            from_ar += random.randint(-10, 10)
            to_vl += random.randint(-10, 10)
            to_ar += random.randint(-10, 10)

            templates = [
                (f"ᐊaf:{{vl{format_percent(from_vl)}⋀ar{format_percent(from_ar)}}}»ᐃaf:{{vl{format_percent(to_vl)}⋀ar{format_percent(to_ar)}}}",
                 f"Affect shift: was {from_name} (v={from_vl},a={from_ar}) -> now {to_name} (v={to_vl},a={to_ar})"),
                (f"●{from_name}»●{to_name}⋀△vl{format_percent(to_vl - from_vl)}",
                 f"Transition {from_name} to {to_name}, valence change {to_vl - from_vl:+d}"),
                (f"E:{{ᐊ●{from_name}»ᐃ●{to_name}⋀ar{format_percent(to_ar)}}}",
                 f"Entity: was {from_name}, now {to_name} (arousal {to_ar}%)"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'affect', ['vl', 'ar'], ['●', '△'][:random.randint(1, 2)])

    def generate_affect_cascades(self, count: int = 200):
        """Generate affect cascade patterns (one emotion triggering another)."""
        print(f"Generating {count} affect cascade patterns...")

        cascades = [
            ('surprise', 'fear', 'because unexpected danger'),
            ('surprise', 'joy', 'because unexpected good news'),
            ('fear', 'anger', 'because threat response'),
            ('sadness', 'anger', 'because frustration'),
            ('anxiety', 'relief', 'because resolution'),
            ('confusion', 'interest', 'because curiosity'),
            ('boredom', 'interest', 'because new stimulus'),
            ('disgust', 'anger', 'because moral violation'),
            ('hope', 'joy', 'because fulfillment'),
            ('anticipation', 'excitement', 'because approaching event'),
        ]

        for _ in range(count):
            trigger, result, reason = random.choice(cascades)
            trigger_intensity = random.randint(50, 90)
            result_intensity = random.randint(40, 85)

            templates = [
                (f"●{trigger}{format_percent(trigger_intensity)}∴●{result}{format_percent(result_intensity)}",
                 f"{trigger.capitalize()} at {trigger_intensity}% therefore {result} at {result_intensity}%"),
                (f"●{trigger}»●{result}∵{reason.split()[-1]}",
                 f"{trigger.capitalize()} leads to {result} {reason}"),
                (f"af:{{●{trigger}∴●{result}⋀vl{format_percent(random.randint(-50, 80))}}}",
                 f"Affect cascade: {trigger} causes {result}"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'affect', ['vl', 'ar'], ['●', '∴', '∵'][:random.randint(1, 2)])

    # ==================== MIXED AFFECT STATES ====================

    def generate_mixed_affect(self, count: int = 200):
        """Generate mixed/ambivalent affect states."""
        print(f"Generating {count} mixed affect patterns...")

        mixed_states = [
            ('bittersweet', 'joy', 'sadness', 40, -30, 50),
            ('anxious_excitement', 'excitement', 'anxiety', 70, -40, 85),
            ('nostalgic_joy', 'joy', 'sadness', 60, -25, 45),
            ('relieved_sadness', 'relief', 'sadness', 50, -35, 40),
            ('hopeful_fear', 'hope', 'fear', 55, -50, 65),
            ('curious_apprehension', 'interest', 'anxiety', 60, -35, 70),
        ]

        for _ in range(count):
            name, pos_emo, neg_emo, pos_weight, neg_weight, arousal = random.choice(mixed_states)
            
            # Add variation
            pos_weight += random.randint(-10, 10)
            neg_weight += random.randint(-10, 10)
            arousal += random.randint(-15, 15)

            templates = [
                (f"af:{{●{pos_emo}⋀●{neg_emo}⋀vl{format_percent((pos_weight + neg_weight) // 2)}⋀ar{format_percent(arousal)}}}",
                 f"Mixed affect: {name} - both {pos_emo} and {neg_emo}, valence {(pos_weight + neg_weight) // 2}%, arousal {arousal}%"),
                (f"E:{{●{pos_emo}{format_percent(pos_weight)}⋁●{neg_emo}{format_percent(abs(neg_weight))}}}",
                 f"Entity experiencing either {pos_emo} ({pos_weight}%) or {neg_emo} ({abs(neg_weight)}%)"),
                (f"af:{{●{pos_emo}⋀●{neg_emo}}}≡{name}",
                 f"{pos_emo.capitalize()} combined with {neg_emo} equals {name}"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'affect', ['vl', 'ar'], ['●', '⋁', '≡'][:random.randint(1, 2)])

    # ==================== TYPE B AFFECT PAIRS ====================

    def generate_type_b_affect(self, count: int = 400):
        """Generate English to CCIN_mu affect pairs."""
        print(f"Generating {count} Type B affect pairs...")

        for _ in range(count):
            pattern = random.choice(['simple', 'transition', 'intensity', 'mixed'])

            if pattern == 'simple':
                emotion = random.choice(['joy', 'sadness', 'fear', 'anger', 'surprise', 'contentment'])
                vl = random.randint(-80, 90)
                ar = random.randint(15, 95)
                english = f"Encode the affect state of {emotion} with valence {vl} and arousal {ar}"
                ccin = f"af:{{●{emotion}⋀vl{format_percent(vl)}⋀ar{format_percent(ar)}}}"

            elif pattern == 'transition':
                from_emo = random.choice(['calm', 'anxious', 'happy'])
                to_emo = random.choice(['excited', 'peaceful', 'frustrated'])
                english = f"Express an emotional transition from {from_emo} to {to_emo}"
                ccin = f"ᐊ●{from_emo}»ᐃ●{to_emo}"

            elif pattern == 'intensity':
                emotion = random.choice(['joy', 'anger', 'fear', 'sadness'])
                intensity = random.randint(30, 95)
                english = f"Encode {intensity}% intensity {emotion}"
                ccin = f"●{emotion}{format_percent(intensity)}"

            else:  # mixed
                emo1 = random.choice(['hope', 'joy', 'interest'])
                emo2 = random.choice(['fear', 'sadness', 'anxiety'])
                english = f"Express a mixed emotional state combining {emo1} and {emo2}"
                ccin = f"af:{{●{emo1}⋀●{emo2}}}"

            self.add_record(ccin, english, 'medium', 'affect', ['vl', 'ar'], ['●'], pair_type='B')

    # ==================== TYPE C AFFECT SIMILARITY ====================

    def generate_affect_similarity_triplets(self, count: int = 200):
        """Generate affect similarity triplets."""
        print(f"Generating {count} affect similarity triplets...")

        for _ in range(count):
            base_vl = random.randint(-60, 80)
            base_ar = random.randint(20, 90)

            anchor = f"af:{{vl{format_percent(base_vl)}⋀ar{format_percent(base_ar)}}}"

            # Positive: similar values
            pos_vl = base_vl + random.randint(-10, 10)
            pos_ar = base_ar + random.randint(-10, 10)
            positive = f"af:{{vl{format_percent(pos_vl)}⋀ar{format_percent(pos_ar)}}}"

            # Negative: opposite values
            neg_vl = -base_vl + random.randint(-20, 20)
            neg_ar = 100 - base_ar + random.randint(-20, 20)
            negative = f"af:{{vl{format_percent(neg_vl)}⋀ar{format_percent(neg_ar)}}}"

            vl_word = 'positive' if base_vl > 20 else 'negative' if base_vl < -20 else 'neutral'
            ar_word = 'high' if base_ar > 60 else 'low' if base_ar < 40 else 'moderate'

            record = {
                "id": self.get_id(),
                "type": "C",
                "domain": "affect",
                "complexity": "medium",
                "anchor": anchor,
                "positive": positive,
                "negative": negative,
                "anchor_english": f"{vl_word} valence, {ar_word} arousal",
                "similarity_score": 0.88,
                "stems_used": ['vl', 'ar'],
                "opcodes_used": [],
                "valid": True
            }
            self.records.append(record)
            if len(self.records) >= self.batch_size:
                self.save_batch()

    def run_generation_cycle(self):
        """Run one full affect expansion cycle."""
        print(f"\n{'='*50}")
        print(f"Starting affect expansion at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        # Basic patterns
        self.generate_valence_arousal_states(400)
        self.generate_affect_intensities(300)

        # Transitions
        self.generate_affect_transitions(300)
        self.generate_affect_cascades(200)

        # Mixed states
        self.generate_mixed_affect(200)

        # Type B and C
        self.generate_type_b_affect(400)
        self.generate_affect_similarity_triplets(200)

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
        start_batch = 123

    print(f"Starting affect expansion from batch {start_batch}")

    generator = AffectGenerator(output_dir, start_batch)

    # Run 2 cycles
    for cycle in range(2):
        print(f"\n*** CYCLE {cycle + 1}/2 ***")
        generator.run_generation_cycle()
        if cycle < 1:
            print("Pausing 60 seconds...")
            time.sleep(60)

    print(f"\n{'='*50}")
    print(f"AFFECT EXPANSION COMPLETE")
    print(f"Total new records: {generator.total_generated}")
    print(f"{'='*50}")

    # Run validation
    print("\nRunning validation...")
    import subprocess
    subprocess.run(['python3', 'validate_and_assemble.py'], cwd=output_dir)


if __name__ == "__main__":
    main()
