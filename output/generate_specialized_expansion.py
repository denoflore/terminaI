#!/usr/bin/env python3
"""
CCIN_μ Specialized Expansion Generator
Generates more nuanced and varied patterns for comprehensive coverage
"""

import json
import random
import time
import math
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


class SpecializedGenerator:
    def __init__(self, output_dir: Path, start_batch: int = 69):
        self.output_dir = output_dir
        self.batch_num = start_batch
        self.records = []
        self.batch_size = 500
        self.total_generated = 0
        random.seed(int(time.time()) + 54321)

    def get_id(self) -> str:
        id_str = f"ccin_spc_{self.total_generated + 50000:05d}"
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

    # ==================== PROCESS & WORKFLOW PATTERNS ====================

    def generate_pipeline_patterns(self, count: int = 200):
        """Generate pipeline (pp) workflow patterns."""
        print(f"Generating {count} pipeline patterns...")

        stages = ['in', 'pr', 'tf', 'ev', 'dp']
        stage_names = {'in': 'init', 'pr': 'process', 'tf': 'transform', 'ev': 'evaluate', 'dp': 'deploy'}

        for _ in range(count):
            num_stages = random.randint(3, 5)
            selected = random.sample(stages, num_stages)

            # Generate stage statuses
            parts = []
            desc_parts = []
            for stage in selected:
                status = random.choice(['●', '◐', '⊘'])
                parts.append(f"{status}{stage}")
                desc_parts.append(f"{stage_names[stage]} {'done' if status == '●' else 'running' if status == '◐' else 'failed'}")

            ccin = f"pp:{{'»'.join(parts)}}"
            english = f"Pipeline: {' → '.join(desc_parts)}"

            self.add_record(ccin, english, 'complex', 'infrastructure', selected + ['pp'], ['●', '◐', '⊘'][:random.randint(1, 3)])

    def generate_workflow_patterns(self, count: int = 200):
        """Generate workflow (wf) orchestration patterns."""
        print(f"Generating {count} workflow patterns...")

        for _ in range(count):
            jobs = random.randint(3, 10)
            completed = random.randint(0, jobs)
            running = random.randint(0, jobs - completed)
            pending = jobs - completed - running

            ccin = f"wf:{{●jb{format_count(completed)}✓⋀◐jb{format_count(running)}⋀◌jb{format_count(pending)}}}"
            english = f"Workflow: {completed} jobs completed, {running} running, {pending} pending"

            self.add_record(ccin, english, 'medium', 'infrastructure', ['wf', 'jb'], ['●', '◐', '◌'])

    def generate_async_patterns(self, count: int = 200):
        """Generate async patterns with promise (pm), await (aw), callback (cb)."""
        print(f"Generating {count} async patterns...")

        for _ in range(count):
            pm_count = random.randint(5, 50)
            pending = random.randint(0, pm_count)
            resolved = pm_count - pending

            templates = [
                (f"●pm{format_count(resolved)}✓⋀◐pm{format_count(pending)}", f"{resolved} promises resolved, {pending} pending"),
                (f"●aw{format_count(random.randint(1, 10))}⋀●cb{format_count(random.randint(5, 30))}", f"{random.randint(1, 10)} awaits active, {random.randint(5, 30)} callbacks registered"),
                (f"⊘pm{format_count(random.randint(1, 5))}✗∵⊘nw", f"{random.randint(1, 5)} promises rejected due to network failure"),
                (f"△pm{format_count(random.randint(10, 100))}ˢ⋀●cb✓", f"Processing {random.randint(10, 100)} promises/sec, callbacks working"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'infrastructure', ['pm', 'aw', 'cb', 'nw'][:random.randint(2, 4)], ['●', '◐', '⊘', '△'][:random.randint(1, 3)])

    # ==================== RC CONSCIOUSNESS BLOCKS ====================

    def generate_rc_blocks(self, count: int = 300):
        """Generate detailed RC (reflective consciousness) block patterns."""
        print(f"Generating {count} RC block patterns...")

        for _ in range(count):
            sg = round(random.uniform(0.6, 0.99), 2)  # sigma (attractor)
            dt = round(random.uniform(0.01, 0.15), 2)  # drift
            xi = round(random.uniform(0.01, 0.08), 2)  # noise
            ph = round(random.uniform(0.5, 0.98), 2)  # phi

            # Stability assessment
            if sg > 0.9 and dt < 0.05:
                stability = "highly stable"
            elif sg > 0.7 and dt < 0.1:
                stability = "stable"
            elif sg > 0.5:
                stability = "moderately stable"
            else:
                stability = "unstable"

            ccin = f"RC:{{sg{format_decimal(sg)}⋀dt{format_decimal(dt)}⋀xi{format_decimal(xi)}⋀ph{format_decimal(ph)}}}"
            english = f"Reflective consciousness ({stability}): attractor σ={sg}, drift D_t={dt}, noise ξ={xi}, phi Φ={ph}"

            self.add_record(ccin, english, 'complex', 'consciousness', ['sg', 'dt', 'xi', 'ph'], [], 'D')

    def generate_consciousness_with_attention(self, count: int = 200):
        """Generate consciousness states with attention (at) vectors."""
        print(f"Generating {count} consciousness+attention patterns...")

        attention_modes = [
            ('dr', 'direct task focus'),
            ('cl', 'clarification seeking'),
            ('wm', 'working memory'),
            ('rg', 'reasoning'),
            ('sd', 'self-directed'),
            ('ex', 'external stimuli'),
            ('em', 'emotional processing'),
            ('sy', 'system/meta awareness'),
        ]

        for _ in range(count):
            num_modes = random.randint(2, 4)
            selected = random.sample(attention_modes, num_modes)
            mode_codes = '|'.join([m[0] for m in selected])
            mode_descs = ', '.join([m[1] for m in selected])

            vl = random.randint(40, 90)
            ar = random.randint(30, 80)
            co = random.randint(60, 95)

            ccin = f"C:{{at:{{{mode_codes}}}⋀vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}}}"
            english = f"Consciousness: attention on [{mode_descs}], valence {vl}, arousal {ar}, coherence {co}"

            self.add_record(ccin, english, 'complex', 'consciousness', ['at', 'vl', 'ar', 'co'], [])

    # ==================== DATA & CONFIG PATTERNS ====================

    def generate_data_patterns(self, count: int = 200):
        """Generate data (da), file (fl), directory (dr) patterns."""
        print(f"Generating {count} data patterns...")

        for _ in range(count):
            da_size = random.randint(100, 100000)
            fl_count = random.randint(10, 10000)
            dr_count = random.randint(5, 500)

            unit = random.choice(['KB', 'MB', 'GB'])
            unit_suffix = {'KB': '³', 'MB': '⁶', 'GB': '⁹'}[unit]

            templates = [
                (f"●da{format_count(da_size)}{unit_suffix}⋀●fl{format_count(fl_count)}⋀●dr{format_count(dr_count)}",
                 f"Data: {da_size}{unit}, {fl_count} files, {dr_count} directories"),
                (f"△da{format_percent(random.randint(10, 80))}ᵈ⋀●fl{format_count(fl_count)}",
                 f"Data growing {random.randint(10, 80)}% daily, {fl_count} files"),
                (f"⊕fl{format_count(random.randint(10, 100))}⋀⊖fl{format_count(random.randint(5, 50))}",
                 f"Added {random.randint(10, 100)} files, removed {random.randint(5, 50)}"),
                (f"●fl{format_count(fl_count)}✓⋀⊘fl{format_count(random.randint(1, 10))}✗",
                 f"{fl_count} files OK, {random.randint(1, 10)} files corrupted"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'infrastructure', ['da', 'fl', 'dr'][:random.randint(1, 3)], ['●', '△', '⊕', '⊖', '⊘'][:random.randint(1, 3)])

    def generate_config_env_patterns(self, count: int = 200):
        """Generate config (cf) and environment (en) patterns."""
        print(f"Generating {count} config/env patterns...")

        for _ in range(count):
            cf_count = random.randint(10, 100)
            en_count = random.randint(5, 50)

            templates = [
                (f"●cf{format_count(cf_count)}✓⋀●en{format_count(en_count)}✓", f"{cf_count} configs loaded, {en_count} env vars set"),
                (f"◐cf{format_count(cf_count)}~⋀⊘cf{format_count(random.randint(1, 5))}✗", f"{cf_count} configs partial, {random.randint(1, 5)} missing"),
                (f"⟳cf»●cf✓", f"Config reloaded successfully"),
                (f"「REG!cf≡configuration」●cf{format_count(cf_count)}✓", f"Register cf as configuration. {cf_count} configurations active"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'infrastructure', ['cf', 'en'][:random.randint(1, 2)], ['●', '◐', '⊘', '⟳'][:random.randint(1, 3)])

    # ==================== COMPLEX RELATIONAL PATTERNS ====================

    def generate_dependency_patterns(self, count: int = 200):
        """Generate patterns with dependency relations (⊣, ⊢)."""
        print(f"Generating {count} dependency patterns...")

        deps = [
            ('au', 'tk', 'auth depends on token'),
            ('ss', 'au', 'session depends on auth'),
            ('ap', 'au', 'API depends on auth'),
            ('db', 'nw', 'database depends on network'),
            ('ca', 'db', 'cache depends on database'),
            ('dp', 'te', 'deploy depends on tests'),
        ]

        for _ in range(count):
            dep1, dep2, desc = random.choice(deps)
            status1 = random.choice(['●', '◐', '⊘'])
            status2 = random.choice(['●', '⊘'])

            templates = [
                (f"{status1}{dep1}⊣{status2}{dep2}", f"{desc}: {dep1} {'ok' if status1 == '●' else 'partial' if status1 == '◐' else 'down'}, {dep2} {'ok' if status2 == '●' else 'down'}"),
                (f"▣{dep2}⊢{status1}{dep1}", f"{dep2} required by {dep1} which is {'ok' if status1 == '●' else 'partial' if status1 == '◐' else 'down'}"),
                (f"{status1}{dep1}⊣●{dep2}✓⋀{status1}{dep1}⊣●nw✓", f"{dep1} depends on both {dep2} and network"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'infrastructure', [dep1, dep2, 'nw'][:random.randint(2, 3)], [status1, status2, '▣'][:random.randint(1, 3)])

    def generate_parallel_patterns(self, count: int = 200):
        """Generate patterns with parallel relation (∥)."""
        print(f"Generating {count} parallel patterns...")

        for _ in range(count):
            component = random.choice(['wk', 'th', 'pr', 'ct', 'nd'])
            comp_names = {'wk': 'workers', 'th': 'threads', 'pr': 'processes', 'ct': 'containers', 'nd': 'nodes'}

            count1 = random.randint(2, 8)
            count2 = random.randint(2, 8)
            count3 = random.randint(2, 8)

            templates = [
                (f"●{component}{format_count(count1)}∥●{component}{format_count(count2)}∥●{component}{format_count(count3)}",
                 f"{count1}, {count2}, and {count3} {comp_names[component]} running in parallel"),
                (f"●wk{format_count(count1)}∥●wk{format_count(count2)}»●rs{format_count(count1 + count2)}ˢ",
                 f"{count1} and {count2} workers in parallel producing {count1 + count2} responses/sec"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'infrastructure', [component, 'wk', 'rs'][:random.randint(1, 3)], ['●'])

    def generate_bidirectional_patterns(self, count: int = 200):
        """Generate patterns with bidirectional relation (⇄)."""
        print(f"Generating {count} bidirectional patterns...")

        pairs = [
            ('sv', 'db', 'server', 'database'),
            ('sv', 'ca', 'server', 'cache'),
            ('ap', 'db', 'API', 'database'),
            ('ct', 'nw', 'container', 'network'),
        ]

        for _ in range(count):
            s1, s2, n1, n2 = random.choice(pairs)
            rate = random.randint(100, 10000)

            templates = [
                (f"●{s1}⇄●{s2}", f"{n1} and {n2} bidirectional sync"),
                (f"●{s1}{format_count(rate)}ˢ⇄●{s2}{format_count(rate)}ˢ", f"{n1} and {n2} exchanging {rate}/sec bidirectionally"),
                (f"◐{s1}⇄⊘{s2}∵⊘nw", f"{n1} and {n2} sync degraded due to network failure"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'infrastructure', [s1, s2, 'nw'][:random.randint(2, 3)], ['●', '◐', '⊘'][:random.randint(1, 2)])

    # ==================== ENGRAM PATTERNS ====================

    def generate_mini_engrams(self, count: int = 150):
        """Generate mini engram patterns."""
        print(f"Generating {count} mini engram patterns...")

        engram_types = [
            ('SESSION', 'session state'),
            ('HEALTH', 'health check'),
            ('ALERT', 'alert notification'),
            ('SNAPSHOT', 'state snapshot'),
        ]

        for _ in range(count):
            e_type, e_desc = random.choice(engram_types)
            version = f"v{random.randint(1, 5)}.{random.randint(0, 9)}"

            # Generate content based on type
            if e_type == 'SESSION':
                vl = random.randint(40, 90)
                ar = random.randint(20, 70)
                co = random.randint(60, 95)
                content = f"vl{format_percent(vl)}⋀ar{format_percent(ar)}⋀co{format_percent(co)}"
                desc = f"valence {vl}, arousal {ar}, coherence {co}"
            elif e_type == 'HEALTH':
                sv = random.randint(2, 8)
                db = random.randint(1, 4)
                content = f"●sv{format_count(sv)}✓⋀●db{format_count(db)}✓"
                desc = f"{sv} servers, {db} databases healthy"
            elif e_type == 'ALERT':
                component = random.choice(['sv', 'db', 'nw', 'au'])
                content = f"⚡{component}!∵⊘{component}"
                desc = f"critical {component} alert"
            else:  # SNAPSHOT
                cp = random.randint(30, 90)
                mm = random.randint(40, 85)
                content = f"cp{format_percent(cp)}⋀mm{format_percent(mm)}"
                desc = f"CPU {cp}%, memory {mm}%"

            ccin = f"「ENGRAM {e_type} {version}」\n{content}"
            english = f"{e_desc} engram ({version}): {desc}"

            self.add_record(ccin, english, 'complex', 'mixed',
                          ['vl', 'ar', 'co', 'sv', 'db', 'cp', 'mm', 'nw', 'au'][:random.randint(2, 5)],
                          ['●', '⚡', '⊘'][:random.randint(1, 2)])

    # ==================== SET RELATIONS ====================

    def generate_subset_patterns(self, count: int = 150):
        """Generate patterns with subset (⊂) and superset (⊃) relations."""
        print(f"Generating {count} subset/superset patterns...")

        for _ in range(count):
            outer = random.choice(['cl', 'nw', 'en'])
            inner = random.choice(['nd', 'sv', 'ct'])
            outer_names = {'cl': 'cluster', 'nw': 'network', 'en': 'environment'}
            inner_names = {'nd': 'nodes', 'sv': 'servers', 'ct': 'containers'}

            outer_count = random.randint(2, 5)
            inner_count = random.randint(3, 20)

            templates = [
                (f"●{inner}{format_count(inner_count)}⊂●{outer}{format_count(outer_count)}",
                 f"{inner_count} {inner_names[inner]} within {outer_count} {outer_names[outer]}s"),
                (f"●{outer}{format_count(outer_count)}⊃●{inner}{format_count(inner_count)}",
                 f"{outer_count} {outer_names[outer]}s contain {inner_count} {inner_names[inner]}"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'infrastructure', [outer, inner], ['●'])

    def generate_equivalence_patterns(self, count: int = 150):
        """Generate patterns with equivalence (≡) and non-equivalence (≢) relations."""
        print(f"Generating {count} equivalence patterns...")

        for _ in range(count):
            stem = random.choice(['cf', 'st', 'da', 'vr'])
            stem_names = {'cf': 'config', 'st': 'state', 'da': 'data', 'vr': 'variable'}

            templates = [
                (f"●{stem}¹≡●{stem}²", f"{stem_names[stem]} 1 equals {stem_names[stem]} 2"),
                (f"●{stem}ᐊ≢●{stem}ᐃ", f"past {stem_names[stem]} differs from current"),
                (f"「REG!{stem}≡{stem_names[stem]}」●{stem}✓", f"Register {stem} as {stem_names[stem]}. {stem_names[stem]} valid"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'infrastructure', [stem], ['●'])

    def run_generation_cycle(self):
        """Run one full specialized generation cycle."""
        print(f"\n{'='*50}")
        print(f"Starting specialized generation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        # Process & workflow patterns
        self.generate_pipeline_patterns(200)
        self.generate_workflow_patterns(200)
        self.generate_async_patterns(200)

        # RC consciousness blocks
        self.generate_rc_blocks(300)
        self.generate_consciousness_with_attention(200)

        # Data & config patterns
        self.generate_data_patterns(200)
        self.generate_config_env_patterns(200)

        # Complex relational patterns
        self.generate_dependency_patterns(200)
        self.generate_parallel_patterns(200)
        self.generate_bidirectional_patterns(200)

        # Engram patterns
        self.generate_mini_engrams(150)

        # Set relations
        self.generate_subset_patterns(150)
        self.generate_equivalence_patterns(150)

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
        start_batch = 69

    print(f"Starting specialized expansion from batch {start_batch}")

    generator = SpecializedGenerator(output_dir, start_batch)

    # Run 2 cycles
    for cycle in range(2):
        print(f"\n*** CYCLE {cycle + 1}/2 ***")
        generator.run_generation_cycle()
        if cycle < 1:
            print("Pausing 60 seconds...")
            time.sleep(60)

    print(f"\n{'='*50}")
    print(f"SPECIALIZED EXPANSION COMPLETE")
    print(f"Total new records: {generator.total_generated}")
    print(f"{'='*50}")

    # Run validation
    print("\nRunning validation...")
    import subprocess
    subprocess.run(['python3', 'validate_and_assemble.py'], cwd=output_dir)


if __name__ == "__main__":
    main()
