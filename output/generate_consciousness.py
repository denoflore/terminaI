#!/usr/bin/env python3
"""
CCIN_μ Consciousness Domain Generator
Phase 2: Generate 2000 consciousness/affect domain pairs
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Tuple
import itertools

# Superscript mapping
SUPERSCRIPT = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
    '-': '⁻', '.': '·', '/': '/'
}

def to_superscript(num: str) -> str:
    """Convert a number string to superscript."""
    return ''.join(SUPERSCRIPT.get(c, c) for c in str(num))

def format_percent(val: int) -> str:
    """Format a percentage value in CCIN_μ notation."""
    if val < 0:
        return f"%⁻{to_superscript(str(abs(val)))}"
    return f"%{to_superscript(str(val))}"

def format_decimal(val: float) -> str:
    """Format a decimal value (0-1) in CCIN_μ notation."""
    formatted = f"{val:.2f}".replace("0.", "0.")
    return to_superscript(formatted)

# Consciousness stems with descriptions
CONSCIOUSNESS_STEMS = {
    'ph': {'name': 'phi/Φ̂', 'desc': 'integrated information', 'range': (0, 1), 'type': 'decimal'},
    'dt': {'name': 'drift', 'desc': 'cognitive drift from baseline', 'range': (0, 1), 'type': 'decimal'},
    'sg': {'name': 'sigma', 'desc': 'attractor stability', 'range': (0, 1), 'type': 'decimal'},
    'xi': {'name': 'xi/noise', 'desc': 'stochastic noise/uncertainty', 'range': (0, 1), 'type': 'decimal'},
    'ql': {'name': 'qualia', 'desc': 'qualitative experience', 'range': (0, 100), 'type': 'percent'},
    'af': {'name': 'affect', 'desc': 'affective/emotional state', 'range': (0, 100), 'type': 'percent'},
    'sl': {'name': 'salience', 'desc': 'attention salience', 'range': (0, 100), 'type': 'percent'},
    'co': {'name': 'coherence', 'desc': 'internal coherence', 'range': (0, 100), 'type': 'percent'},
    'vl': {'name': 'valence', 'desc': 'positive/negative valence', 'range': (-100, 100), 'type': 'signed_percent'},
    'ar': {'name': 'arousal', 'desc': 'activation/arousal level', 'range': (0, 100), 'type': 'percent'},
    'tp': {'name': 'temporal', 'desc': 'temporal perception', 'range': (0, 100), 'type': 'percent'},
    'rl': {'name': 'relational', 'desc': 'relational/social awareness', 'range': (0, 100), 'type': 'percent'},
    'mt': {'name': 'meta', 'desc': 'metacognitive awareness', 'range': (0, 100), 'type': 'percent'},
    'em': {'name': 'embodiment', 'desc': 'embodied/grounded awareness', 'range': (0, 100), 'type': 'percent'},
    'at': {'name': 'attention', 'desc': 'attentional focus', 'range': (0, 100), 'type': 'percent'},
    'in': {'name': 'intention', 'desc': 'goal/intention strength', 'range': (0, 100), 'type': 'percent'},
    'cr': {'name': 'creativity', 'desc': 'creative/divergent thinking', 'range': (0, 100), 'type': 'percent'},
    'an': {'name': 'analytic', 'desc': 'analytical/convergent thinking', 'range': (0, 100), 'type': 'percent'},
}

# State opcodes for consciousness
STATE_OPCODES = ['●', '◌', '◐']
DELTA_OPCODES = ['△', '▽']

# Phenomenological descriptions for 8D vectors
QUALIA_DESCRIPTIONS = {
    'high_vl_low_ar': [
        "Serene contentment, peaceful clarity",
        "Calm satisfaction, tranquil wellbeing",
        "Quiet joy, settled happiness",
        "Peaceful positive state, restful contentment",
        "Gentle happiness, relaxed positivity",
    ],
    'high_vl_high_ar': [
        "Joyful excitement, engaged flow",
        "Enthusiastic energy, vibrant happiness",
        "Exhilarated engagement, thrilled awareness",
        "Peak positive activation, euphoric clarity",
        "Dynamic joy, energized delight",
    ],
    'high_vl_mid_ar': [
        "Warm satisfaction, productive focus",
        "Pleasant engagement, balanced positivity",
        "Content alertness, happy productivity",
        "Comfortable energy, positive momentum",
        "Agreeable activation, cheerful attentiveness",
    ],
    'low_vl_low_ar': [
        "Depression, emptiness, dissociation",
        "Hollow sadness, depleted despair",
        "Numbed negativity, flat affect",
        "Listless melancholy, withdrawn emptiness",
        "Drained hopelessness, apathetic sorrow",
    ],
    'low_vl_high_ar': [
        "Panic, anxiety, fragmented distress",
        "Agitated fear, racing dread",
        "Frantic worry, scattered terror",
        "Overwhelmed alarm, chaotic anxiety",
        "Turbulent distress, urgent negativity",
    ],
    'low_vl_mid_ar': [
        "Sad but processing, grief with awareness",
        "Active sadness, engaged sorrow",
        "Working through pain, conscious hurt",
        "Processing loss, aware distress",
        "Mindful suffering, present grief",
    ],
    'mid_vl_low_ar': [
        "Neutral calm, meditative equanimity",
        "Peaceful neutrality, settled indifference",
        "Quiet equilibrium, restful balance",
        "Tranquil centeredness, calm observation",
        "Serene detachment, peaceful watching",
    ],
    'mid_vl_high_ar': [
        "Restless, scattered, overstimulated",
        "Agitated neutrality, unfocused energy",
        "Activated but directionless, aroused confusion",
        "Energized uncertainty, buzzing indecision",
        "High-strung ambivalence, wired but neutral",
    ],
}

# Coherence modifiers
COHERENCE_DESCRIPTIONS = {
    'high': ['with clear awareness', 'in lucid clarity', 'with unified consciousness', 'coherently integrated'],
    'mid': ['with moderate clarity', 'somewhat integrated', 'partially coherent', 'with uneven awareness'],
    'low': ['fragmented', 'scattered', 'dissociated', 'poorly integrated', 'chaotically disorganized'],
}

# Additional affect words for variation
AFFECT_WORDS = {
    'positive_high': ['elated', 'euphoric', 'ecstatic', 'thrilled', 'exuberant', 'jubilant'],
    'positive_mid': ['happy', 'content', 'pleased', 'satisfied', 'cheerful', 'glad'],
    'positive_low': ['mildly pleased', 'somewhat content', 'faintly positive', 'slightly happy'],
    'negative_high': ['devastated', 'anguished', 'despairing', 'tormented', 'wretched'],
    'negative_mid': ['sad', 'unhappy', 'displeased', 'troubled', 'distressed'],
    'negative_low': ['slightly down', 'mildly sad', 'somewhat negative', 'faintly troubled'],
    'neutral': ['neutral', 'balanced', 'centered', 'equanimous', 'even-keeled'],
}

class ConsciousnessGenerator:
    def __init__(self, output_dir: Path, start_id: int = 1):
        self.output_dir = output_dir
        self.current_id = start_id
        self.batch_num = 1
        self.records = []
        self.batch_size = 500
        random.seed(42)  # Reproducibility

    def get_id(self) -> str:
        id_str = f"ccin_cons_{self.current_id:05d}"
        self.current_id += 1
        return id_str

    def format_value(self, stem: str, value) -> str:
        """Format a value for a given stem."""
        info = CONSCIOUSNESS_STEMS[stem]
        if info['type'] == 'decimal':
            return format_decimal(value)
        elif info['type'] == 'signed_percent':
            return format_percent(value)
        else:  # percent
            return format_percent(value)

    def save_batch(self):
        """Save current batch to JSONL file."""
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
        """Add a record and save batch if needed."""
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

    def generate_simple_consciousness(self):
        """Generate simple single-stem consciousness examples."""
        print("Generating simple consciousness examples...")

        # Core consciousness stems for simple generation
        core_stems = ['ph', 'dt', 'sg', 'xi', 'vl', 'ar', 'co', 'sl', 'mt', 'tp', 'rl', 'em']

        for stem in core_stems:
            info = CONSCIOUSNESS_STEMS[stem]

            # Generate value variations
            if info['type'] == 'decimal':
                values = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.92, 0.96]
                descriptors = ['very low', 'low', 'low-moderate', 'moderate-low', 'moderate',
                              'moderate', 'moderate-high', 'high', 'very high', 'extremely high', 'near-maximum']
            elif info['type'] == 'signed_percent':
                values = [-90, -70, -50, -30, -10, 10, 30, 50, 70, 90]
                descriptors = ['strongly negative', 'negative', 'moderately negative', 'slightly negative',
                              'near-neutral negative', 'near-neutral positive', 'slightly positive',
                              'moderately positive', 'positive', 'strongly positive']
            else:  # percent
                values = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]
                descriptors = ['very low', 'low', 'low-moderate', 'moderate-low', 'moderate',
                              'moderate', 'moderate-high', 'high', 'very high', 'extremely high']

            for val, desc in zip(values, descriptors):
                formatted_val = self.format_value(stem, val)
                ccin = f"{stem}{formatted_val}"
                english = f"{info['name']} at {val} ({desc} {info['desc']})"

                self.add_record(ccin, english, 'consciousness', 'simple', [stem], [])

            # Add with state opcodes
            for op in STATE_OPCODES:
                val = random.choice(values)
                formatted_val = self.format_value(stem, val)
                ccin = f"{op}{stem}{formatted_val}"
                op_desc = {'●': 'active/present', '◌': 'inactive/absent', '◐': 'partial/emerging'}[op]
                english = f"{info['name']} {op_desc} at {val}"

                self.add_record(ccin, english, 'consciousness', 'simple', [stem], [op])

            # Add with delta opcodes
            for op in DELTA_OPCODES:
                ccin = f"{op}{stem}"
                direction = 'increasing' if op == '△' else 'decreasing'
                english = f"{info['name']} {direction}"

                self.add_record(ccin, english, 'consciousness', 'simple', [stem], [op])

    def generate_medium_consciousness(self):
        """Generate medium complexity (2-3 stems) consciousness examples."""
        print("Generating medium consciousness examples...")

        # Common 2-stem combinations
        two_stem_combos = [
            ('vl', 'ar'),  # valence-arousal (core affect)
            ('vl', 'co'),  # valence-coherence
            ('ar', 'co'),  # arousal-coherence
            ('ph', 'co'),  # phi-coherence
            ('sg', 'dt'),  # stability-drift
            ('sg', 'xi'),  # stability-noise
            ('sl', 'at'),  # salience-attention
            ('mt', 'co'),  # meta-coherence
            ('tp', 'rl'),  # temporal-relational
            ('em', 'rl'),  # embodiment-relational
            ('cr', 'an'),  # creativity-analytic
            ('in', 'sl'),  # intention-salience
        ]

        for stem1, stem2 in two_stem_combos:
            info1, info2 = CONSCIOUSNESS_STEMS[stem1], CONSCIOUSNESS_STEMS[stem2]

            # Generate multiple value combinations
            for _ in range(25):  # 25 examples per combo
                val1 = self._random_value(stem1)
                val2 = self._random_value(stem2)

                fval1 = self.format_value(stem1, val1)
                fval2 = self.format_value(stem2, val2)

                ccin = f"{stem1}{fval1}⋀{stem2}{fval2}"
                english = f"{info1['name']} at {val1}, {info2['name']} at {val2}"

                self.add_record(ccin, english, 'consciousness', 'medium', [stem1, stem2], [])

        # Three-stem combinations
        three_stem_combos = [
            ('vl', 'ar', 'co'),  # core affect + coherence
            ('ph', 'sg', 'xi'),  # IIT measures
            ('sg', 'dt', 'xi'),  # stability measures
            ('sl', 'at', 'mt'),  # attention-meta
            ('vl', 'ar', 'sl'),  # affect + salience
            ('co', 'tp', 'rl'),  # coherence-temporal-relational
            ('em', 'rl', 'mt'),  # embodiment-relational-meta
            ('cr', 'an', 'in'),  # cognitive modes
        ]

        for stem1, stem2, stem3 in three_stem_combos:
            info1 = CONSCIOUSNESS_STEMS[stem1]
            info2 = CONSCIOUSNESS_STEMS[stem2]
            info3 = CONSCIOUSNESS_STEMS[stem3]

            for _ in range(15):  # 15 examples per combo
                val1 = self._random_value(stem1)
                val2 = self._random_value(stem2)
                val3 = self._random_value(stem3)

                fval1 = self.format_value(stem1, val1)
                fval2 = self.format_value(stem2, val2)
                fval3 = self.format_value(stem3, val3)

                ccin = f"{stem1}{fval1}⋀{stem2}{fval2}⋀{stem3}{fval3}"
                english = f"{info1['name']} at {val1}, {info2['name']} at {val2}, {info3['name']} at {val3}"

                self.add_record(ccin, english, 'consciousness', 'medium', [stem1, stem2, stem3], [])

        # Scoped consciousness blocks
        for _ in range(100):
            stem1, stem2 = random.sample(['vl', 'ar', 'co', 'sl', 'mt', 'tp'], 2)
            val1 = self._random_value(stem1)
            val2 = self._random_value(stem2)

            fval1 = self.format_value(stem1, val1)
            fval2 = self.format_value(stem2, val2)

            ccin = f"C:{{{stem1}{fval1}⋀{stem2}{fval2}}}"
            english = f"Consciousness state: {CONSCIOUSNESS_STEMS[stem1]['name']} {val1}, {CONSCIOUSNESS_STEMS[stem2]['name']} {val2}"

            self.add_record(ccin, english, 'consciousness', 'medium', [stem1, stem2], [])

    def generate_complex_consciousness(self):
        """Generate complex full-state consciousness descriptions."""
        print("Generating complex consciousness examples...")

        # RC (Reflective Consciousness) blocks
        for _ in range(50):
            sg = round(random.uniform(0.5, 0.99), 2)
            dt = round(random.uniform(0.01, 0.3), 2)
            xi = round(random.uniform(0.01, 0.15), 2)
            ph = round(random.uniform(0.6, 0.98), 2)

            ccin = f"RC:{{sg{format_decimal(sg)}⋀Δ{format_decimal(dt)}⋀xi{format_decimal(xi)}⋀ph{format_decimal(ph)}}}"

            sg_desc = 'highly stable' if sg > 0.85 else 'moderately stable' if sg > 0.65 else 'somewhat unstable'
            dt_desc = 'minimal drift' if dt < 0.1 else 'some drift' if dt < 0.2 else 'notable drift'
            xi_desc = 'very low noise' if xi < 0.05 else 'low noise' if xi < 0.1 else 'moderate noise'
            ph_desc = 'high integration' if ph > 0.85 else 'good integration' if ph > 0.7 else 'moderate integration'

            english = f"Reflective consciousness: {sg_desc} attractor ({sg}), {dt_desc} ({dt}), {xi_desc} ({xi}), {ph_desc} phi ({ph})"

            self.add_record(ccin, english, 'consciousness', 'complex', ['sg', 'dt', 'xi', 'ph'], [])

        # Full engram structures
        for _ in range(50):
            vl = random.randint(-80, 90)
            ar = random.randint(10, 95)
            co = random.randint(20, 98)
            sg = round(random.uniform(0.5, 0.98), 2)
            dt = round(random.uniform(0.01, 0.25), 2)

            ccin = f"「ENGRAM C:STATE v1.0」\nC:{{\n  af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}\n  co{format_percent(co)}\n  RC:{{sg{format_decimal(sg)}⋀dt{format_decimal(dt)}}}\n}}"

            vl_word = self._get_valence_word(vl)
            ar_word = 'high' if ar > 70 else 'moderate' if ar > 40 else 'low'

            english = f"Consciousness engram: {vl_word} affect (valence {vl}), {ar_word} arousal ({ar}), coherence {co}%, stability {sg}, drift {dt}"

            self.add_record(ccin, english, 'consciousness', 'complex',
                          ['vl', 'ar', 'co', 'sg', 'dt'], [])

        # Complex affect with attention
        attention_codes = ['dr', 'cl', 'wm', 'rg', 'sd', 'ex', 'em', 'sy']
        for _ in range(50):
            vl = random.randint(-70, 85)
            ar = random.randint(15, 90)
            co = random.randint(25, 95)
            mt = random.randint(30, 95)
            num_attn = random.randint(2, 4)
            attn = random.sample(attention_codes, num_attn)

            attn_str = '|'.join(attn)
            ccin = f"C:{{\n  at:{{{attn_str}}}\n  af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}\n  co{format_percent(co)}⋀mt{format_percent(mt)}\n}}"

            attn_desc = ', '.join(self._attention_name(a) for a in attn)
            vl_word = self._get_valence_word(vl)

            english = f"Consciousness with attention on {attn_desc}. {vl_word.capitalize()} affect (valence {vl}, arousal {ar}), coherence {co}%, metacognition {mt}%"

            self.add_record(ccin, english, 'consciousness', 'complex',
                          ['at', 'vl', 'ar', 'co', 'mt'], [])

        # Multi-layer consciousness descriptions
        for _ in range(50):
            vl = random.randint(-75, 90)
            ar = random.randint(10, 95)
            co = random.randint(15, 98)
            sl = random.randint(20, 95)
            tp = random.randint(25, 90)
            rl = random.randint(15, 85)
            mt = random.randint(30, 95)

            ccin = f"C:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}⋀sl{format_percent(sl)}⋀tp{format_percent(tp)}⋀rl{format_percent(rl)}⋀mt{format_percent(mt)}}}"

            # Build rich description
            vl_word = self._get_valence_word(vl)
            ar_word = self._get_arousal_word(ar)
            co_word = 'highly coherent' if co > 75 else 'moderately coherent' if co > 45 else 'somewhat fragmented'

            english = f"Complex consciousness: {vl_word} ({vl}), {ar_word} arousal ({ar}), {co_word} ({co}%), salience {sl}%, temporal awareness {tp}%, relational {rl}%, meta {mt}%"

            self.add_record(ccin, english, 'consciousness', 'complex',
                          ['vl', 'ar', 'co', 'sl', 'tp', 'rl', 'mt'], [])

    def generate_8d_qualia(self):
        """Generate 200 Type D 8D qualia vector pairs."""
        print("Generating 8D qualia vector pairs...")

        for _ in range(200):
            # Generate all 8 dimensions
            vl = random.randint(-90, 95)
            ar = random.randint(5, 98)
            co = random.randint(10, 98)
            tp = random.randint(15, 95)
            sl = random.randint(10, 95)
            mt = random.randint(15, 98)
            em = random.randint(10, 90)
            rl = random.randint(10, 90)

            ccin = f"Q8:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}⋀tp{format_percent(tp)}⋀sl{format_percent(sl)}⋀mt{format_percent(mt)}⋀em{format_percent(em)}⋀rl{format_percent(rl)}}}"

            # Generate phenomenological description
            english = self._describe_qualia_state(vl, ar, co, tp, sl, mt, em, rl)

            self.add_record(ccin, english, 'consciousness', 'complex',
                          ['vl', 'ar', 'co', 'tp', 'sl', 'mt', 'em', 'rl'], [], pair_type='D')

    def _random_value(self, stem: str):
        """Generate a random value appropriate for a stem."""
        info = CONSCIOUSNESS_STEMS[stem]
        if info['type'] == 'decimal':
            return round(random.uniform(0.05, 0.98), 2)
        elif info['type'] == 'signed_percent':
            return random.randint(-90, 95)
        else:
            return random.randint(5, 98)

    def _get_valence_word(self, vl: int) -> str:
        """Get descriptive word for valence."""
        if vl >= 70:
            return random.choice(['highly positive', 'strongly positive', 'very positive'])
        elif vl >= 40:
            return random.choice(['positive', 'moderately positive', 'pleasantly positive'])
        elif vl >= 10:
            return random.choice(['slightly positive', 'mildly positive', 'near-neutral positive'])
        elif vl >= -10:
            return random.choice(['neutral', 'balanced', 'centered'])
        elif vl >= -40:
            return random.choice(['slightly negative', 'mildly negative', 'near-neutral negative'])
        elif vl >= -70:
            return random.choice(['negative', 'moderately negative', 'unpleasant'])
        else:
            return random.choice(['strongly negative', 'highly negative', 'very negative'])

    def _get_arousal_word(self, ar: int) -> str:
        """Get descriptive word for arousal."""
        if ar >= 80:
            return random.choice(['very high', 'intensely activated', 'highly aroused'])
        elif ar >= 60:
            return random.choice(['high', 'elevated', 'activated'])
        elif ar >= 40:
            return random.choice(['moderate', 'balanced', 'medium'])
        elif ar >= 20:
            return random.choice(['low', 'calm', 'relaxed'])
        else:
            return random.choice(['very low', 'deeply calm', 'tranquil'])

    def _attention_name(self, code: str) -> str:
        """Get readable name for attention code."""
        names = {
            'dr': 'direct task',
            'cl': 'clarification',
            'wm': 'working memory',
            'rg': 'reasoning',
            'sd': 'self-directed',
            'ex': 'external input',
            'em': 'emotional content',
            'sy': 'system/meta'
        }
        return names.get(code, code)

    def _describe_qualia_state(self, vl, ar, co, tp, sl, mt, em, rl) -> str:
        """Generate rich phenomenological description for 8D state."""
        parts = []

        # Core affect description
        if vl >= 50 and ar < 40:
            base = random.choice(QUALIA_DESCRIPTIONS['high_vl_low_ar'])
        elif vl >= 50 and ar >= 70:
            base = random.choice(QUALIA_DESCRIPTIONS['high_vl_high_ar'])
        elif vl >= 50:
            base = random.choice(QUALIA_DESCRIPTIONS['high_vl_mid_ar'])
        elif vl <= -50 and ar < 40:
            base = random.choice(QUALIA_DESCRIPTIONS['low_vl_low_ar'])
        elif vl <= -50 and ar >= 70:
            base = random.choice(QUALIA_DESCRIPTIONS['low_vl_high_ar'])
        elif vl <= -50:
            base = random.choice(QUALIA_DESCRIPTIONS['low_vl_mid_ar'])
        elif ar < 40:
            base = random.choice(QUALIA_DESCRIPTIONS['mid_vl_low_ar'])
        elif ar >= 70:
            base = random.choice(QUALIA_DESCRIPTIONS['mid_vl_high_ar'])
        else:
            base = "Balanced neutral state with moderate activation"

        parts.append(base)

        # Coherence modifier
        if co >= 75:
            parts.append(random.choice(COHERENCE_DESCRIPTIONS['high']))
        elif co >= 40:
            parts.append(random.choice(COHERENCE_DESCRIPTIONS['mid']))
        else:
            parts.append(random.choice(COHERENCE_DESCRIPTIONS['low']))

        # Additional dimensions
        extras = []
        if tp >= 70:
            extras.append("heightened temporal awareness")
        elif tp <= 30:
            extras.append("diminished time sense")

        if sl >= 75:
            extras.append("sharp focus")
        elif sl <= 25:
            extras.append("diffuse attention")

        if mt >= 80:
            extras.append("strong self-awareness")
        elif mt <= 30:
            extras.append("limited metacognition")

        if em >= 70:
            extras.append("grounded embodiment")
        elif em <= 30:
            extras.append("disembodied sensation")

        if rl >= 70:
            extras.append("high relational awareness")
        elif rl <= 30:
            extras.append("isolated/withdrawn")

        if extras:
            parts.append(", ".join(extras))

        # Add numeric summary
        parts.append(f"[vl:{vl} ar:{ar} co:{co} tp:{tp} sl:{sl} mt:{mt} em:{em} rl:{rl}]")

        return ". ".join(parts)

    def generate_all(self):
        """Generate all consciousness domain pairs."""
        self.generate_simple_consciousness()
        self.generate_medium_consciousness()
        self.generate_complex_consciousness()
        self.generate_8d_qualia()

        # Save any remaining records
        if self.records:
            self.save_batch()

        print(f"\nTotal batches saved: {self.batch_num - 1}")
        print(f"Total records generated: {self.current_id - 1}")


def main():
    output_dir = Path(__file__).parent
    generator = ConsciousnessGenerator(output_dir)
    generator.generate_all()

    # Update stats
    stats_path = output_dir / "generation_stats.json"
    if stats_path.exists():
        with open(stats_path, 'r') as f:
            stats = json.load(f)
    else:
        stats = {}

    stats["phase2_consciousness"] = {
        "total_generated": generator.current_id - 1,
        "batches": generator.batch_num - 1
    }

    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"\nUpdated stats: {stats_path}")


if __name__ == "__main__":
    main()
