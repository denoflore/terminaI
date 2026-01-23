#!/usr/bin/env python3
"""
CCIN_μ Consciousness Domain Expansion Generator
Phase 2 Expansion: Generate additional pairs to reach 2000 total
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

def format_decimal(val: float) -> str:
    formatted = f"{val:.2f}".replace("0.", "0.")
    return to_superscript(formatted)

# Additional phenomenological templates
FLOW_STATES = [
    "Deep creative flow with effortless concentration",
    "Absorbed engagement with task at hand",
    "Timeless immersion in the work",
    "Peak performance state with optimal challenge-skill balance",
    "Complete task absorption with diminished self-consciousness",
    "Fluid creative expression flowing naturally",
    "Harmonious merging of action and awareness",
    "Intrinsically rewarding engagement",
]

CONTEMPLATIVE_STATES = [
    "Quiet contemplation with clear observation",
    "Meditative awareness without grasping",
    "Spacious presence with minimal thought",
    "Receptive witnessing consciousness",
    "Gentle attention resting in present moment",
    "Open awareness without agenda",
    "Calm observation of arising experience",
    "Peaceful abiding in natural awareness",
]

ANALYTICAL_STATES = [
    "Focused analytical processing",
    "Careful logical reasoning engaged",
    "Systematic problem decomposition active",
    "Critical evaluation mode engaged",
    "Sequential reasoning proceeding step by step",
    "Pattern recognition scanning for structure",
    "Hypothesis testing in progress",
    "Deliberate systematic analysis",
]

SOCIAL_STATES = [
    "Warm relational attunement present",
    "Empathic connection with others",
    "Social awareness heightened",
    "Interpersonal sensitivity active",
    "Collaborative mind engaged",
    "Caring presence extending outward",
    "Responsive to social cues",
    "Attuned to relational dynamics",
]

TRANSITION_PATTERNS = [
    ("anxiety", "calm", "through deliberate breathing"),
    ("confusion", "clarity", "as understanding emerged"),
    ("fatigue", "alertness", "after brief rest"),
    ("distraction", "focus", "through intention setting"),
    ("agitation", "peace", "via mindful pausing"),
    ("overwhelm", "manageability", "by prioritizing"),
    ("negativity", "acceptance", "through reframing"),
    ("disconnection", "presence", "by grounding"),
]


class ExpansionGenerator:
    def __init__(self, output_dir: Path, start_id: int = 1105, batch_num: int = 4):
        self.output_dir = output_dir
        self.current_id = start_id
        self.batch_num = batch_num
        self.records = []
        self.batch_size = 500
        random.seed(43)  # Different seed for variety

    def get_id(self) -> str:
        id_str = f"ccin_cons_{self.current_id:05d}"
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

    def add_record(self, ccin_mu: str, english: str, domain: str, complexity: str,
                   stems_used: List[str], opcodes_used: List[str], pair_type: str = 'A'):
        record = {
            "id": self.get_id(),
            "type": pair_type,
            "domain": domain,
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

    def generate_flow_states(self):
        """Generate flow state descriptions."""
        print("Generating flow state examples...")

        for _ in range(80):
            vl = random.randint(65, 95)
            ar = random.randint(50, 80)
            co = random.randint(75, 98)
            sl = random.randint(70, 95)
            mt = random.randint(60, 90)
            cr = random.randint(65, 95)

            ccin = f"C:FLOW:{{\n  af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}\n  co{format_percent(co)}⋀sl{format_percent(sl)}\n  mt{format_percent(mt)}⋀cr{format_percent(cr)}\n}}"

            flow_desc = random.choice(FLOW_STATES)
            english = f"{flow_desc}. Valence {vl}, arousal {ar}, coherence {co}%, salience {sl}%, metacognition {mt}%, creativity {cr}%."

            self.add_record(ccin, english, 'consciousness', 'complex',
                          ['vl', 'ar', 'co', 'sl', 'mt', 'cr'], [])

    def generate_contemplative_states(self):
        """Generate contemplative/meditative states."""
        print("Generating contemplative state examples...")

        for _ in range(80):
            vl = random.randint(40, 75)
            ar = random.randint(10, 35)
            co = random.randint(70, 98)
            tp = random.randint(60, 95)
            mt = random.randint(70, 98)
            em = random.randint(50, 85)

            ccin = f"C:CONTEMPLATE:{{\n  af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}\n  co{format_percent(co)}⋀tp{format_percent(tp)}\n  mt{format_percent(mt)}⋀em{format_percent(em)}\n}}"

            state_desc = random.choice(CONTEMPLATIVE_STATES)
            english = f"{state_desc}. Valence {vl}, low arousal {ar}, coherence {co}%, temporal awareness {tp}%, metacognition {mt}%, embodiment {em}%."

            self.add_record(ccin, english, 'consciousness', 'complex',
                          ['vl', 'ar', 'co', 'tp', 'mt', 'em'], [])

    def generate_analytical_states(self):
        """Generate analytical/reasoning states."""
        print("Generating analytical state examples...")

        for _ in range(80):
            vl = random.randint(30, 70)
            ar = random.randint(40, 75)
            co = random.randint(65, 95)
            sl = random.randint(75, 98)
            an = random.randint(70, 98)
            at_codes = random.sample(['dr', 'rg', 'wm'], random.randint(2, 3))

            at_str = '|'.join(at_codes)
            ccin = f"C:ANALYTIC:{{\n  at:{{{at_str}}}\n  af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}\n  co{format_percent(co)}⋀sl{format_percent(sl)}⋀an{format_percent(an)}\n}}"

            state_desc = random.choice(ANALYTICAL_STATES)
            at_desc = ', '.join({'dr': 'direct task', 'rg': 'reasoning', 'wm': 'working memory'}[c] for c in at_codes)
            english = f"{state_desc}. Attention on {at_desc}. Valence {vl}, arousal {ar}, coherence {co}%, salience {sl}%, analytic {an}%."

            self.add_record(ccin, english, 'consciousness', 'complex',
                          ['vl', 'ar', 'co', 'sl', 'an', 'at'], [])

    def generate_social_states(self):
        """Generate socially-oriented states."""
        print("Generating social state examples...")

        for _ in range(80):
            vl = random.randint(45, 90)
            ar = random.randint(35, 75)
            co = random.randint(55, 90)
            rl = random.randint(65, 98)
            em = random.randint(50, 85)
            mt = random.randint(45, 85)

            ccin = f"C:SOCIAL:{{\n  af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}\n  co{format_percent(co)}⋀rl{format_percent(rl)}\n  em{format_percent(em)}⋀mt{format_percent(mt)}\n}}"

            state_desc = random.choice(SOCIAL_STATES)
            english = f"{state_desc}. Valence {vl}, arousal {ar}, coherence {co}%, relational awareness {rl}%, embodiment {em}%, metacognition {mt}%."

            self.add_record(ccin, english, 'consciousness', 'complex',
                          ['vl', 'ar', 'co', 'rl', 'em', 'mt'], [])

    def generate_state_transitions(self):
        """Generate consciousness state transitions."""
        print("Generating state transition examples...")

        for from_state, to_state, mechanism in TRANSITION_PATTERNS:
            for _ in range(12):
                # Before state
                if from_state in ['anxiety', 'agitation', 'overwhelm']:
                    vl1, ar1 = random.randint(-70, -30), random.randint(65, 95)
                elif from_state in ['confusion', 'distraction']:
                    vl1, ar1 = random.randint(-20, 20), random.randint(50, 80)
                elif from_state in ['fatigue', 'disconnection']:
                    vl1, ar1 = random.randint(-40, 10), random.randint(10, 35)
                else:
                    vl1, ar1 = random.randint(-50, 0), random.randint(30, 70)

                # After state
                if to_state in ['calm', 'peace', 'presence']:
                    vl2, ar2 = random.randint(40, 80), random.randint(15, 45)
                elif to_state in ['clarity', 'focus', 'manageability']:
                    vl2, ar2 = random.randint(50, 85), random.randint(40, 70)
                elif to_state in ['alertness', 'acceptance']:
                    vl2, ar2 = random.randint(35, 75), random.randint(45, 75)
                else:
                    vl2, ar2 = random.randint(30, 70), random.randint(30, 60)

                ccin = f"ᐊaf:{{vl{format_percent(vl1)}⋀ar{format_percent(ar1)}}}→ᐃaf:{{vl{format_percent(vl2)}⋀ar{format_percent(ar2)}}}"

                english = f"Transitioned from {from_state} (valence {vl1}, arousal {ar1}) to {to_state} (valence {vl2}, arousal {ar2}) {mechanism}."

                self.add_record(ccin, english, 'consciousness', 'medium',
                              ['vl', 'ar'], [], pair_type='A')

    def generate_additional_qualia(self):
        """Generate more Type D qualia pairs with varied descriptions."""
        print("Generating additional 8D qualia pairs...")

        phenomenology_templates = [
            "Experiencing {affect} with {coherence_desc}. {temporal_desc}. {social_desc}.",
            "{affect}. {coherence_desc}, {awareness_desc}. {embodiment_desc}.",
            "State of {affect}. Awareness {coherence_desc}. {meta_desc}, {relational_desc}.",
            "{affect} consciousness. {coherence_desc} with {temporal_desc}. {social_embodiment}.",
        ]

        for _ in range(150):
            vl = random.randint(-95, 98)
            ar = random.randint(3, 99)
            co = random.randint(8, 99)
            tp = random.randint(10, 98)
            sl = random.randint(8, 99)
            mt = random.randint(12, 99)
            em = random.randint(8, 95)
            rl = random.randint(8, 95)

            ccin = f"Q8:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}⋀tp{format_percent(tp)}⋀sl{format_percent(sl)}⋀mt{format_percent(mt)}⋀em{format_percent(em)}⋀rl{format_percent(rl)}}}"

            # Build description components
            if vl >= 60:
                affect = random.choice(["positive wellbeing", "pleasant engagement", "joyful awareness", "contented presence"])
            elif vl >= 20:
                affect = random.choice(["mild positivity", "slight pleasantness", "gentle comfort", "quiet satisfaction"])
            elif vl >= -20:
                affect = random.choice(["neutral balance", "equanimous state", "centered presence", "even-keeled awareness"])
            elif vl >= -60:
                affect = random.choice(["mild discomfort", "slight unpleasantness", "gentle unease", "quiet distress"])
            else:
                affect = random.choice(["significant distress", "notable suffering", "strong negativity", "marked discomfort"])

            coherence_desc = f"{'high' if co > 70 else 'moderate' if co > 40 else 'low'} coherence ({co}%)"
            temporal_desc = f"Temporal awareness {'heightened' if tp > 70 else 'moderate' if tp > 40 else 'diminished'} ({tp}%)"
            social_desc = f"Relational awareness {'strong' if rl > 70 else 'moderate' if rl > 40 else 'minimal'} ({rl}%)"
            embodiment_desc = f"{'Grounded' if em > 60 else 'Moderate' if em > 35 else 'Disembodied'} presence ({em}%)"
            meta_desc = f"Metacognition {'strong' if mt > 70 else 'moderate' if mt > 40 else 'weak'} ({mt}%)"
            awareness_desc = f"salience {'sharp' if sl > 70 else 'moderate' if sl > 40 else 'diffuse'} ({sl}%)"
            relational_desc = f"social sense {'vivid' if rl > 70 else 'present' if rl > 40 else 'faint'}"
            social_embodiment = f"{'Embodied and connected' if (em > 60 and rl > 60) else 'Partially grounded' if (em > 40 or rl > 40) else 'Disconnected'}"

            template = random.choice(phenomenology_templates)
            english = template.format(
                affect=affect,
                coherence_desc=coherence_desc,
                temporal_desc=temporal_desc,
                social_desc=social_desc,
                embodiment_desc=embodiment_desc,
                meta_desc=meta_desc,
                awareness_desc=awareness_desc,
                relational_desc=relational_desc,
                social_embodiment=social_embodiment
            )

            # Add numeric summary
            english += f" [vl:{vl} ar:{ar} co:{co} tp:{tp} sl:{sl} mt:{mt} em:{em} rl:{rl}]"

            self.add_record(ccin, english, 'consciousness', 'complex',
                          ['vl', 'ar', 'co', 'tp', 'sl', 'mt', 'em', 'rl'], [], pair_type='D')

    def generate_type_b_pairs(self):
        """Generate Type B (English → CCIN_μ) pairs."""
        print("Generating Type B (English to CCIN_μ) pairs...")

        # Natural language consciousness descriptions that map to CCIN_μ
        descriptions = [
            ("I'm feeling really good and energetic right now", "af:{{vl%{vl}⋀ar%{ar}}}", {'vl': (70, 95), 'ar': (65, 90)}),
            ("Calm and peaceful, just resting in awareness", "af:{{vl%{vl}⋀ar%{ar}}}⋀mt%{mt}", {'vl': (50, 80), 'ar': (10, 30), 'mt': (60, 90)}),
            ("Anxious and stressed, heart racing", "af:{{vl%{vl}⋀ar%{ar}}}", {'vl': (-80, -50), 'ar': (70, 95)}),
            ("Deeply focused on the task, everything else faded away", "C:FLOW:{{sl%{sl}⋀co%{co}⋀at:{{dr|wm}}}}", {'sl': (80, 98), 'co': (75, 95)}),
            ("Feeling connected to others, warm and open", "C:{{vl%{vl}⋀rl%{rl}⋀em%{em}}}", {'vl': (60, 90), 'rl': (70, 95), 'em': (55, 85)}),
            ("Mind is scattered, hard to concentrate", "C:{{co%{co}⋀sl%{sl}⋀dt{dt}}}", {'co': (15, 35), 'sl': (10, 30), 'dt': (0.3, 0.6)}),
            ("Clear and lucid, everything makes sense", "C:{{co%{co}⋀mt%{mt}⋀sg{sg}}}", {'co': (80, 98), 'mt': (75, 95), 'sg': (0.85, 0.98)}),
            ("Sad but processing, working through feelings", "af:{{vl%{vl}⋀ar%{ar}}}⋀mt%{mt}", {'vl': (-60, -30), 'ar': (35, 55), 'mt': (60, 85)}),
            ("Neutral and observing, just watching thoughts pass", "C:{{vl%{vl}⋀ar%{ar}⋀mt%{mt}}}", {'vl': (-10, 20), 'ar': (15, 35), 'mt': (70, 95)}),
            ("Excited and creative, ideas flowing freely", "C:CREATIVE:{{vl%{vl}⋀ar%{ar}⋀cr%{cr}}}", {'vl': (65, 92), 'ar': (60, 85), 'cr': (75, 98)}),
        ]

        for english_template, ccin_template, ranges in descriptions:
            for _ in range(12):
                values = {}
                for key, (low, high) in ranges.items():
                    if isinstance(low, float):  # decimal
                        values[key] = format_decimal(round(random.uniform(low, high), 2))
                    else:
                        values[key] = format_percent(random.randint(low, high))

                ccin = ccin_template.format(**values)
                english = english_template

                # Determine stems used
                stems = []
                for stem in ['vl', 'ar', 'co', 'sl', 'mt', 'em', 'rl', 'cr', 'dt', 'sg']:
                    if stem in ccin_template:
                        stems.append(stem)

                self.add_record(ccin, english, 'consciousness', 'medium',
                              stems, [], pair_type='B')

    def generate_affective_variations(self):
        """Generate additional affect-focused variations."""
        print("Generating affective variations...")

        emotions = [
            ('joy', (70, 95), (55, 85)),
            ('contentment', (60, 85), (15, 40)),
            ('excitement', (65, 90), (70, 95)),
            ('serenity', (55, 80), (10, 30)),
            ('anticipation', (45, 75), (50, 75)),
            ('sadness', (-75, -40), (20, 45)),
            ('fear', (-80, -50), (70, 95)),
            ('anger', (-70, -40), (75, 95)),
            ('disgust', (-65, -35), (40, 65)),
            ('surprise', (0, 40), (60, 90)),
            ('boredom', (-30, 10), (10, 25)),
            ('frustration', (-60, -30), (55, 80)),
            ('relief', (50, 80), (20, 45)),
            ('gratitude', (65, 90), (35, 60)),
            ('curiosity', (40, 70), (50, 75)),
        ]

        for emotion, vl_range, ar_range in emotions:
            for _ in range(8):
                vl = random.randint(*vl_range)
                ar = random.randint(*ar_range)
                co = random.randint(30, 90)

                ccin = f"af:{{{emotion[:2]}}}⋀af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}⋀co{format_percent(co)}"
                english = f"Experiencing {emotion}: valence {vl}, arousal {ar}, coherence {co}%"

                self.add_record(ccin, english, 'affect', 'medium',
                              ['vl', 'ar', 'co'], [])

    def generate_all(self):
        """Generate all expansion pairs."""
        self.generate_flow_states()
        self.generate_contemplative_states()
        self.generate_analytical_states()
        self.generate_social_states()
        self.generate_state_transitions()
        self.generate_additional_qualia()
        self.generate_type_b_pairs()
        self.generate_affective_variations()

        if self.records:
            self.save_batch()

        print(f"\nTotal expansion batches: {self.batch_num - 4}")
        print(f"Total expansion records: {self.current_id - 1105}")


def main():
    output_dir = Path(__file__).parent
    generator = ExpansionGenerator(output_dir)
    generator.generate_all()

    # Update stats
    stats_path = output_dir / "generation_stats.json"
    with open(stats_path, 'r') as f:
        stats = json.load(f)

    stats["phase2_consciousness"]["expansion_generated"] = generator.current_id - 1105
    stats["phase2_consciousness"]["total_generated"] = generator.current_id - 1

    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"\nUpdated stats: {stats_path}")


if __name__ == "__main__":
    main()
