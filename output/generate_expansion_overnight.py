#!/usr/bin/env python3
"""
CCIN_μ Overnight Expansion Generator
Generates additional pairs to reach 10,000+ target
Runs in batches, saves checkpoints
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

# Scopes from authoritative spec
SCOPES = ['P:', 'D:', 'S:', 'T:', 'A:', 'N:', '$:', '§:', 'C:', 'E:']

# Infrastructure stems
INFRA_STEMS = ['sv', 'db', 'ca', 'nw', 'fw', 'lb', 'ct', 'vm', 'gp', 'cp', 'mm', 'dk']

# Application stems
APP_STEMS = ['au', 'az', 'tk', 'ss', 'us', 'rq', 'rs', 'er', 'lg', 'mt', 'ev', 'mg']

# Consciousness stems
CONSCIOUSNESS_STEMS = ['ph', 'dt', 'sg', 'xi', 'ql', 'af', 'sl', 'co', 'vl', 'ar', 'tp', 'rl']

# Process stems
PROCESS_STEMS = ['pr', 'th', 'wk', 'jb', 'tk', 'qu', 'pp', 'wf', 'tr', 'cb', 'pm', 'aw']

# AI/ML stems
AIML_STEMS = ['md', 'wt', 'ls', 'ep', 'bt', 'lr', 'em', 'at', 'tf', 'if']

# State opcodes
STATE_OPS = ['●', '◌', '◐']

# Action opcodes
ACTION_OPS = ['⊘', '⟲', '⟳', '△', '▽', '⊕', '⊖']

# Signal opcodes
SIGNAL_OPS = ['⚡', '◇', '▣', '▢', '!']

# Relations
RELATIONS = ['»', '«', '→', '←', '∵', '∴', '⋀', '⋁', '⊂', '⊃', '≡', '≢', '⇄', '∥', '⊣', '⊢']

# Temporal markers
TEMPORAL = ['ᐊ', 'ᐃ', 'ᐅ']

# Status suffixes
STATUS = ['✓', '✗', '?', '!', '~', '∞']

# Time suffixes
TIME_SUFFIXES = ['ˢ', 'ᵐ', 'ʰ', 'ᵈ', 'ʷ', 'ʸ']


class OvernightGenerator:
    def __init__(self, output_dir: Path, start_batch: int = 21):
        self.output_dir = output_dir
        self.batch_num = start_batch
        self.records = []
        self.batch_size = 500
        self.total_generated = 0
        random.seed(int(time.time()))

    def get_id(self) -> str:
        id_str = f"ccin_exp_{self.total_generated + 10000:05d}"
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

    def generate_multi_env_deployments(self, count: int = 200):
        """Generate multi-environment deployment patterns."""
        print(f"Generating {count} multi-environment deployments...")

        for _ in range(count):
            # D: → S: → P: pipeline patterns
            dev_status = random.choice(['●', '◐'])
            staging_status = random.choice(['●', '◐', '⊘'])
            prod_status = random.choice(['●', '◐'])

            component = random.choice(['sv', 'ct', 'db', 'ap'])
            count_val = random.randint(1, 10)

            ccin = f"D:{dev_status}{component}{format_count(count_val)}»S:{staging_status}{component}{format_count(count_val)}»P:{prod_status}{component}{format_count(count_val)}"

            status_map = {'●': 'healthy', '◐': 'partial', '⊘': 'down'}
            comp_name = {'sv': 'servers', 'ct': 'containers', 'db': 'databases', 'ap': 'APIs'}[component]

            english = f"Deployment pipeline: {count_val} {comp_name} {status_map[dev_status]} in dev, {status_map[staging_status]} in staging, {status_map[prod_status]} in production"

            self.add_record(ccin, english, 'complex', 'infrastructure',
                          [component], [dev_status, staging_status, prod_status])

    def generate_security_patterns(self, count: int = 200):
        """Generate security domain patterns with §: scope."""
        print(f"Generating {count} security patterns...")

        security_scenarios = [
            ('au', 'authentication', ['active', 'inactive', 'partial']),
            ('az', 'authorization', ['granted', 'denied', 'pending']),
            ('tk', 'token', ['valid', 'expired', 'refreshing']),
            ('fw', 'firewall', ['enabled', 'disabled', 'updating']),
        ]

        for _ in range(count):
            stem, name, states = random.choice(security_scenarios)
            state_idx = random.randint(0, 2)
            opcode = ['●', '⊘', '◐'][state_idx]
            state_word = states[state_idx]

            suffix = random.choice(['✓', '✗', '?', ''])
            suffix_word = {'✓': ' confirmed', '✗': ' failed', '?': ' pending', '': ''}[suffix]

            ccin = f"§:{opcode}{stem}{suffix}"
            english = f"Security: {name} {state_word}{suffix_word}"

            self.add_record(ccin, english, 'simple', 'infrastructure',
                          [stem], [opcode])

    def generate_cost_patterns(self, count: int = 150):
        """Generate cost/financial domain patterns with $: scope."""
        print(f"Generating {count} cost patterns...")

        for _ in range(count):
            resource = random.choice(['sv', 'db', 'gp', 'mm', 'ct'])
            direction = random.choice(['△', '▽'])
            percent = random.randint(5, 95)

            resource_names = {
                'sv': 'server', 'db': 'database', 'gp': 'GPU',
                'mm': 'memory', 'ct': 'container'
            }
            dir_word = 'up' if direction == '△' else 'down'

            ccin = f"$:{direction}{resource}{format_percent(percent)}"
            english = f"Cost: {resource_names[resource]} spending {dir_word} {percent}%"

            self.add_record(ccin, english, 'simple', 'infrastructure',
                          [resource], [direction])

    def generate_network_layer_patterns(self, count: int = 150):
        """Generate network layer patterns with N: scope."""
        print(f"Generating {count} network layer patterns...")

        for _ in range(count):
            components = random.sample(['fw', 'lb', 'nw', 'gp'], random.randint(2, 4))
            parts = []
            desc_parts = []
            opcodes_used = []

            for comp in components:
                op = random.choice(['●', '◐', '⊘'])
                opcodes_used.append(op)
                comp_names = {'fw': 'firewall', 'lb': 'load balancer', 'nw': 'network', 'gp': 'gateway'}
                status = {'●': 'healthy', '◐': 'degraded', '⊘': 'down'}[op]

                parts.append(f"{op}{comp}✓" if op == '●' else f"{op}{comp}")
                desc_parts.append(f"{comp_names[comp]} {status}")

            ccin = f"N:{{{('⋀'.join(parts))}}}"
            english = f"Network layer: {', '.join(desc_parts)}"

            self.add_record(ccin, english, 'medium', 'infrastructure',
                          components, list(set(opcodes_used)))

    def generate_aiml_training_patterns(self, count: int = 200):
        """Generate AI/ML training patterns."""
        print(f"Generating {count} AI/ML training patterns...")

        for _ in range(count):
            epoch = random.randint(1, 100)
            batch = random.randint(16, 256)
            loss = round(random.uniform(0.01, 2.5), 3)
            lr = random.choice(['0.001', '0.01', '0.0001', '0.005'])

            direction = '▽' if random.random() > 0.3 else '△'
            dir_word = 'decreasing' if direction == '▽' else 'increasing'

            ccin = f"md:{{ep{format_count(epoch)}⋀bt{format_count(batch)}⋀{direction}ls{format_decimal(loss)}⋀lr{to_superscript(lr)}}}"
            english = f"Model training: epoch {epoch}, batch size {batch}, loss {dir_word} to {loss}, learning rate {lr}"

            self.add_record(ccin, english, 'complex', 'infrastructure',
                          ['md', 'ep', 'bt', 'ls', 'lr'], [direction])

    def generate_consciousness_transitions(self, count: int = 300):
        """Generate consciousness state transitions."""
        print(f"Generating {count} consciousness transitions...")

        states = [
            ('flow', {'vl': (70, 90), 'ar': (50, 70), 'co': (85, 98)}),
            ('anxious', {'vl': (-70, -30), 'ar': (75, 95), 'co': (20, 45)}),
            ('calm', {'vl': (60, 85), 'ar': (15, 35), 'co': (80, 95)}),
            ('excited', {'vl': (75, 95), 'ar': (70, 90), 'co': (70, 90)}),
            ('focused', {'vl': (50, 70), 'ar': (40, 60), 'co': (85, 98)}),
            ('scattered', {'vl': (30, 50), 'ar': (65, 85), 'co': (25, 45)}),
        ]

        for _ in range(count):
            from_state, from_ranges = random.choice(states)
            to_state, to_ranges = random.choice(states)

            # Generate values
            from_vl = random.randint(*from_ranges['vl'])
            from_ar = random.randint(*from_ranges['ar'])
            from_co = random.randint(*from_ranges['co'])

            to_vl = random.randint(*to_ranges['vl'])
            to_ar = random.randint(*to_ranges['ar'])
            to_co = random.randint(*to_ranges['co'])

            ccin = f"ᐊC:{{vl{format_percent(from_vl)}⋀ar{format_percent(from_ar)}⋀co{format_percent(from_co)}}}»ᐃC:{{vl{format_percent(to_vl)}⋀ar{format_percent(to_ar)}⋀co{format_percent(to_co)}}}"
            english = f"Consciousness transition: was {from_state} (valence {from_vl}, arousal {from_ar}, coherence {from_co}) → now {to_state} (valence {to_vl}, arousal {to_ar}, coherence {to_co})"

            self.add_record(ccin, english, 'complex', 'consciousness',
                          ['vl', 'ar', 'co'], [])

    def generate_8d_phenomenology(self, count: int = 300):
        """Generate detailed 8D qualia vectors with interpretations."""
        print(f"Generating {count} 8D phenomenology patterns...")

        phenomenal_states = [
            ('serene contemplation', (80, 95), (10, 25), (90, 98), (60, 80), (40, 60), (85, 95), (30, 50), (50, 70)),
            ('creative flow', (75, 90), (55, 70), (85, 95), (65, 80), (80, 95), (80, 92), (45, 65), (40, 60)),
            ('analytical focus', (55, 70), (45, 60), (88, 98), (70, 85), (85, 98), (90, 98), (25, 40), (35, 50)),
            ('social engagement', (70, 85), (60, 75), (75, 88), (55, 70), (65, 80), (70, 85), (60, 80), (85, 98)),
            ('peaceful rest', (65, 80), (5, 20), (85, 95), (40, 55), (20, 35), (60, 75), (70, 90), (55, 70)),
            ('curious exploration', (70, 85), (65, 80), (70, 85), (60, 75), (90, 98), (75, 88), (50, 70), (60, 75)),
            ('empathic connection', (75, 90), (50, 65), (80, 92), (55, 70), (70, 85), (80, 90), (55, 75), (90, 98)),
            ('meditative awareness', (60, 75), (10, 25), (92, 99), (75, 90), (45, 60), (92, 99), (60, 80), (55, 70)),
        ]

        for _ in range(count):
            state_name, vl_r, ar_r, co_r, tp_r, sl_r, mt_r, em_r, rl_r = random.choice(phenomenal_states)

            vl = random.randint(*vl_r)
            ar = random.randint(*ar_r)
            co = random.randint(*co_r)
            tp = random.randint(*tp_r)
            sl = random.randint(*sl_r)
            mt = random.randint(*mt_r)
            em = random.randint(*em_r)
            rl = random.randint(*rl_r)

            ccin = f"C:ql⁸D:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}⋀tp{format_percent(tp)}⋀sl{format_percent(sl)}⋀mt{format_percent(mt)}⋀em{format_percent(em)}⋀rl{format_percent(rl)}}}"
            english = f"8D qualia ({state_name}): valence {vl}, arousal {ar}, coherence {co}, temporal {tp}, salience {sl}, metacognition {mt}, embodiment {em}, relational {rl}"

            self.add_record(ccin, english, 'complex', 'consciousness',
                          ['vl', 'ar', 'co', 'tp', 'sl', 'mt', 'em', 'rl'], [], 'D')

    def generate_handoff_protocols(self, count: int = 100):
        """Generate cross-agent handoff protocol examples."""
        print(f"Generating {count} handoff protocol examples...")

        for _ in range(count):
            # Generate state
            svs = random.randint(1, 8)
            dbs = random.randint(1, 4)
            sv_status = random.choice(['●', '◐'])
            db_status = random.choice(['●', '◐', '⊘'])

            # Generate context (past → present)
            issue = random.choice([
                ('au', 'authentication'),
                ('tk', 'token'),
                ('nw', 'network'),
                ('ca', 'cache'),
            ])

            # Generate task
            task_verb = random.choice(['⟲', '⟳', '●'])
            task_word = {'⟲': 'restart', '⟳': 'rollback', '●': 'activate'}[task_verb]

            ccin = f"「CCIN_μ HANDOFF v1.0」\n「REG!\nsv≡server\ndb≡database\n{issue[0]}≡{issue[1]}\n」\n「STATE」\nP:{{{sv_status}sv{format_count(svs)}⋀{db_status}db{format_count(dbs)}}}\n「TASK」\n{task_verb}{issue[0]}»●{issue[0]}✓"

            sv_word = 'healthy' if sv_status == '●' else 'partial'
            db_word = {'●': 'healthy', '◐': 'partial', '⊘': 'down'}[db_status]

            english = f"Cross-agent handoff: {svs} servers {sv_word}, {dbs} databases {db_word}. Task: {task_word} {issue[1]} and confirm working."

            self.add_record(ccin, english, 'complex', 'mixed',
                          ['sv', 'db', issue[0]], [sv_status, db_status, task_verb])

    def generate_causal_chains(self, count: int = 200):
        """Generate complex causal chain examples."""
        print(f"Generating {count} causal chain examples...")

        chain_templates = [
            # Infrastructure failures
            (['nw', 'sv', 'db', 'ap'], ['network', 'server', 'database', 'API']),
            (['mm', 'ct', 'sv', 'rq'], ['memory', 'container', 'server', 'request']),
            (['dk', 'db', 'ca', 'rs'], ['disk', 'database', 'cache', 'response']),
            (['tk', 'au', 'ss', 'us'], ['token', 'auth', 'session', 'user']),
            (['cp', 'pr', 'wk', 'jb'], ['CPU', 'process', 'worker', 'job']),
        ]

        for _ in range(count):
            stems, names = random.choice(chain_templates)
            chain_len = random.randint(2, len(stems))
            stems = stems[:chain_len]
            names = names[:chain_len]

            # Use ∵ (because) or ∴ (therefore)
            relation = random.choice(['∵', '∴'])
            rel_word = 'because' if relation == '∵' else 'therefore'

            # Build chain
            opcode = random.choice(['⊘', '◐', '△', '▽'])
            op_word = {'⊘': 'down', '◐': 'degraded', '△': 'overloaded', '▽': 'reduced'}[opcode]

            ccin_parts = [f"{opcode}{s}" for s in stems]
            ccin = relation.join(ccin_parts)

            english_parts = [f"{n} {op_word}" for n in names]
            english = f" {rel_word} ".join(english_parts)

            self.add_record(ccin, english, 'complex', 'infrastructure',
                          stems, [opcode])

    def generate_type_b_pairs(self, count: int = 300):
        """Generate Type B (English → CCIN_μ) pairs."""
        print(f"Generating {count} Type B pairs...")

        templates = [
            # Infrastructure
            ("The {comp} is {status}", "{op}{stem}"),
            ("{count} {comps} are running", "●{stem}{cnt}"),
            ("{comp} at {pct}% utilization", "{stem}{pct_fmt}"),
            ("Alert: {comp} is critical", "⚡{stem}!"),

            # Consciousness
            ("Feeling {affect} with {intensity} intensity", "af:{{vl{vl}⋀ar{ar}}}"),
            ("High coherence state at {pct}%", "co{pct_fmt}"),
            ("Phi integration measure: {val}", "ph{val_fmt}"),
        ]

        components = [
            ('server', 'sv'), ('database', 'db'), ('cache', 'ca'),
            ('network', 'nw'), ('container', 'ct'), ('memory', 'mm'),
        ]

        statuses = [
            ('healthy', '●'), ('down', '⊘'), ('degraded', '◐'),
            ('active', '●'), ('inactive', '◌'), ('partial', '◐'),
        ]

        for _ in range(count):
            template_idx = random.randint(0, len(templates) - 1)
            eng_template, ccin_template = templates[template_idx]

            if template_idx < 4:  # Infrastructure
                comp, stem = random.choice(components)
                status_word, op = random.choice(statuses)
                count_val = random.randint(1, 10)
                pct = random.randint(10, 99)

                english = eng_template.format(
                    comp=comp, comps=comp + 's', status=status_word,
                    count=count_val, pct=pct
                )
                ccin = ccin_template.format(
                    op=op, stem=stem, cnt=format_count(count_val),
                    pct_fmt=format_percent(pct)
                )
                domain = 'infrastructure'
                stems = [stem]
                opcodes = [op] if op in STATE_OPS + ACTION_OPS else []
            else:  # Consciousness
                vl = random.randint(-80, 90)
                ar = random.randint(10, 95)
                pct = random.randint(60, 98)
                val = round(random.uniform(0.5, 0.98), 2)

                affect = 'positive' if vl > 0 else 'negative'
                intensity = 'high' if ar > 60 else 'moderate' if ar > 30 else 'low'

                english = eng_template.format(
                    affect=affect, intensity=intensity, pct=pct, val=val
                )
                ccin = ccin_template.format(
                    vl=format_percent(vl), ar=format_percent(ar),
                    pct_fmt=format_percent(pct), val_fmt=format_decimal(val)
                )
                domain = 'consciousness'
                stems = ['vl', 'ar', 'co', 'ph'][:random.randint(1, 3)]
                opcodes = []

            self.add_record(ccin, english, 'medium', domain, stems, opcodes, 'B')

    def run_generation_cycle(self):
        """Run one full generation cycle."""
        print(f"\n{'='*50}")
        print(f"Starting generation cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        self.generate_multi_env_deployments(200)
        self.generate_security_patterns(200)
        self.generate_cost_patterns(150)
        self.generate_network_layer_patterns(150)
        self.generate_aiml_training_patterns(200)
        self.generate_consciousness_transitions(300)
        self.generate_8d_phenomenology(300)
        self.generate_handoff_protocols(100)
        self.generate_causal_chains(200)
        self.generate_type_b_pairs(300)

        # Save any remaining records
        if self.records:
            self.save_batch()

        print(f"\nCycle complete. Total generated this cycle: ~2100")
        print(f"Total generated overall: {self.total_generated}")
        return self.total_generated


def main():
    output_dir = Path(__file__).parent

    # Find the next batch number
    existing_batches = list(output_dir.glob("ccin_mu_dataset_batch_*.jsonl"))
    if existing_batches:
        max_batch = max(int(f.stem.split('_')[-1]) for f in existing_batches)
        start_batch = max_batch + 1
    else:
        start_batch = 21

    print(f"Starting overnight generation from batch {start_batch}")
    print(f"Output directory: {output_dir}")

    generator = OvernightGenerator(output_dir, start_batch)

    # Run generation cycles
    cycles = 0
    max_cycles = 6  # ~6 cycles = ~12,600 new records

    while cycles < max_cycles:
        cycles += 1
        print(f"\n*** CYCLE {cycles}/{max_cycles} ***")

        try:
            generator.run_generation_cycle()

            # Short pause between cycles
            if cycles < max_cycles:
                print(f"Pausing 30 seconds before next cycle...")
                time.sleep(30)

        except Exception as e:
            print(f"Error during cycle {cycles}: {e}")
            import traceback
            traceback.print_exc()
            break

    print(f"\n{'='*50}")
    print(f"OVERNIGHT GENERATION COMPLETE")
    print(f"Total new records: {generator.total_generated}")
    print(f"Batches created: {generator.batch_num - start_batch}")
    print(f"{'='*50}")

    # Run validation
    print("\nRunning final validation...")
    import subprocess
    subprocess.run(['python3', 'validate_and_assemble.py'], cwd=output_dir)


if __name__ == "__main__":
    main()
