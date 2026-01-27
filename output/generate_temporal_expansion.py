#!/usr/bin/env python3
"""
CCIN_μ Temporal Domain Expansion Generator
Focuses on temporal patterns, durations, schedules, and state transitions over time
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


class TemporalGenerator:
    def __init__(self, output_dir: Path, start_batch: int = 113):
        self.output_dir = output_dir
        self.batch_num = start_batch
        self.records = []
        self.batch_size = 500
        self.total_generated = 0
        random.seed(int(time.time()) + 98765)

    def get_id(self) -> str:
        id_str = f"ccin_temp_{self.total_generated + 50000:05d}"
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

    # ==================== DURATION PATTERNS ====================

    def generate_uptime_patterns(self, count: int = 300):
        """Generate uptime duration patterns."""
        print(f"Generating {count} uptime patterns...")

        stems = ['sv', 'db', 'ca', 'nw', 'au', 'ct', 'vm']
        stem_names = {'sv': 'server', 'db': 'database', 'ca': 'cache', 'nw': 'network',
                      'au': 'auth', 'ct': 'container', 'vm': 'VM'}

        for _ in range(count):
            stem = random.choice(stems)
            duration = random.randint(1, 365)
            unit = random.choice([('ᵈ', 'days'), ('ʰ', 'hours'), ('ᵐ', 'minutes')])

            templates = [
                (f"ᐃ{format_count(duration)}{unit[0]}●{stem}✓",
                 f"{stem_names[stem]} healthy for {duration} {unit[1]}"),
                (f"●{stem}⋀up{format_count(duration)}{unit[0]}",
                 f"Active {stem_names[stem]} with {duration} {unit[1]} uptime"),
                (f"P:{{●{stem}✓⋀up{format_count(duration)}{unit[0]}⋀er{format_count(0)}}}",
                 f"Production {stem_names[stem]}: healthy, {duration} {unit[1]} uptime, zero errors"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'temporal', [stem], ['●'])

    def generate_downtime_patterns(self, count: int = 200):
        """Generate downtime and outage patterns."""
        print(f"Generating {count} downtime patterns...")

        stems = ['sv', 'db', 'nw', 'au']
        stem_names = {'sv': 'server', 'db': 'database', 'nw': 'network', 'au': 'auth'}

        for _ in range(count):
            stem = random.choice(stems)
            duration = random.randint(1, 120)
            unit = random.choice([('ˢ', 'seconds'), ('ᵐ', 'minutes'), ('ʰ', 'hours')])

            templates = [
                (f"ᐊ{format_count(duration)}{unit[0]}⊘{stem}»ᐃ●{stem}✓",
                 f"{stem_names[stem]} was down for {duration} {unit[1]}, now recovered"),
                (f"⊘{stem}⋀down{format_count(duration)}{unit[0]}",
                 f"{stem_names[stem]} down for {duration} {unit[1]}"),
                (f"ᐊ⊘{stem}{format_count(duration)}{unit[0]}∴⚡er!",
                 f"{stem_names[stem]} was down {duration} {unit[1]}, caused error alert"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'temporal', [stem, 'er'][:random.randint(1, 2)], ['⊘', '●', '⚡'][:random.randint(1, 2)])

    # ==================== SCHEDULING PATTERNS ====================

    def generate_scheduled_tasks(self, count: int = 300):
        """Generate scheduled task patterns."""
        print(f"Generating {count} scheduled task patterns...")

        tasks = [
            ('dp', 'deployment'), ('rs', 'restart'), ('up', 'update'),
            ('bk', 'backup'), ('sp', 'stop'), ('sc', 'scale')
        ]
        targets = [
            ('sv', 'servers'), ('db', 'databases'), ('ct', 'containers'),
            ('vm', 'VMs'), ('nd', 'nodes')
        ]

        for _ in range(count):
            task, task_name = random.choice(tasks)
            target, target_name = random.choice(targets)
            time_val = random.randint(1, 72)
            unit = random.choice([('ᵐ', 'minutes'), ('ʰ', 'hours')])
            count_val = random.randint(1, 10)

            templates = [
                (f"ᐅ{format_count(time_val)}{unit[0]}●{task}»●{target}{format_count(count_val)}",
                 f"Scheduled: {task_name} of {count_val} {target_name} in {time_val} {unit[1]}"),
                (f"sched:{{ᐅ{format_count(time_val)}{unit[0]}⋀●{task}⋀{target}{format_count(count_val)}}}",
                 f"Schedule block: {task_name} {count_val} {target_name} in {time_val} {unit[1]}"),
                (f"T:{{ᐅ{format_count(time_val)}{unit[0]}}}⋀P:{{●{task}»●{target}{format_count(count_val)}}}",
                 f"Timed operation: {task_name} to {count_val} production {target_name} in {time_val} {unit[1]}"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'temporal', [task, target], ['●'])

    def generate_recurring_patterns(self, count: int = 200):
        """Generate recurring/periodic patterns."""
        print(f"Generating {count} recurring patterns...")

        for _ in range(count):
            action = random.choice(['bk', 'sc', 'mt', 'lg', 'rs'])
            action_names = {'bk': 'backup', 'sc': 'scan', 'mt': 'metrics', 'lg': 'log rotation', 'rs': 'restart'}
            interval = random.randint(1, 24)
            unit = random.choice([('ʰ', 'hours'), ('ᵈ', 'days')])

            templates = [
                (f"⟲{format_count(interval)}{unit[0]}●{action}",
                 f"Recurring {action_names[action]} every {interval} {unit[1]}"),
                (f"●{action}⋀⟲{format_count(interval)}{unit[0]}⋀P:",
                 f"Production {action_names[action]} recurring every {interval} {unit[1]}"),
                (f"sched:{{⟲{format_count(interval)}{unit[0]}⋀●{action}✓}}",
                 f"Scheduled recurring: {action_names[action]} every {interval} {unit[1]}, healthy"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'temporal', [action], ['●', '⟲'])

    # ==================== STATE TRANSITIONS ====================

    def generate_status_transitions(self, count: int = 300):
        """Generate status transition patterns."""
        print(f"Generating {count} status transition patterns...")

        stems = ['sv', 'db', 'ca', 'au', 'ct', 'vm', 'jb', 'pr']
        stem_names = {'sv': 'server', 'db': 'database', 'ca': 'cache', 'au': 'auth',
                      'ct': 'container', 'vm': 'VM', 'jb': 'job', 'pr': 'process'}

        status_pairs = [
            ('●', '◐', 'active', 'degraded'),
            ('●', '⊘', 'active', 'down'),
            ('◐', '●', 'degraded', 'active'),
            ('◐', '⊘', 'degraded', 'down'),
            ('⊘', '●', 'down', 'active'),
            ('⊘', '◐', 'down', 'degraded'),
            ('◌', '●', 'inactive', 'active'),
            ('●', '◌', 'active', 'inactive'),
        ]

        for _ in range(count):
            stem = random.choice(stems)
            from_op, to_op, from_name, to_name = random.choice(status_pairs)

            templates = [
                (f"ᐊ{from_op}{stem}»ᐃ{to_op}{stem}",
                 f"{stem_names[stem]} transitioned from {from_name} to {to_name}"),
                (f"{from_op}{stem}»{to_op}{stem}⋀t:",
                 f"{stem_names[stem]} {from_name} to {to_name}, timed"),
                (f"ᐊ{from_op}{stem}»ᐃ{to_op}{stem}∵er",
                 f"{stem_names[stem]} changed {from_name} to {to_name} because of error"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'medium', 'temporal', [stem], [from_op, to_op])

    def generate_multi_step_transitions(self, count: int = 200):
        """Generate multi-step state transitions."""
        print(f"Generating {count} multi-step transition patterns...")

        for _ in range(count):
            stem = random.choice(['sv', 'db', 'dp', 'jb'])
            stem_names = {'sv': 'server', 'db': 'database', 'dp': 'deployment', 'jb': 'job'}

            states = random.sample(['◌', '◐', '●', '✓'], 3)
            state_names = {'◌': 'init', '◐': 'partial', '●': 'active', '✓': 'complete'}

            ccin = f"ᐊ{states[0]}{stem}»{states[1]}{stem}»ᐃ{states[2]}{stem}"
            english = f"{stem_names[stem]}: {state_names[states[0]]} -> {state_names[states[1]]} -> {state_names[states[2]]}"

            self.add_record(ccin, english, 'complex', 'temporal', [stem], states)

    # ==================== DEPLOYMENT PIPELINES ====================

    def generate_deployment_timelines(self, count: int = 200):
        """Generate deployment timeline patterns."""
        print(f"Generating {count} deployment timeline patterns...")

        for _ in range(count):
            build_time = random.randint(1, 30)
            test_time = random.randint(1, 60)
            deploy_time = random.randint(1, 15)

            templates = [
                (f"dp:{{ᐊ{format_count(build_time)}ᵐ●bd»{format_count(test_time)}ᵐ●ts»ᐃ{format_count(deploy_time)}ᵐ●rl}}",
                 f"Deployment pipeline: build {build_time}m, test {test_time}m, release {deploy_time}m"),
                (f"ᐊ●bd{format_count(build_time)}ᵐ»●ts{format_count(test_time)}ᵐ»●rl{format_count(deploy_time)}ᵐ»ᐃ●dp✓",
                 f"Build ({build_time}m) -> test ({test_time}m) -> release ({deploy_time}m) -> deployed"),
                (f"P:{{dp:{{●bd»●ts»●rl}}⋀t:{format_count(build_time + test_time + deploy_time)}ᵐ}}",
                 f"Production deployment: build, test, release pipeline in {build_time + test_time + deploy_time}m total"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'temporal', ['dp', 'bd', 'ts', 'rl'][:random.randint(2, 4)], ['●'])

    # ==================== TYPE B TEMPORAL ====================

    def generate_type_b_temporal(self, count: int = 300):
        """Generate English to CCIN_mu temporal pairs."""
        print(f"Generating {count} Type B temporal pairs...")

        for _ in range(count):
            pattern = random.choice(['uptime', 'schedule', 'transition', 'recurring', 'pipeline'])

            if pattern == 'uptime':
                stem = random.choice(['sv', 'db', 'au'])
                stem_name = {'sv': 'server', 'db': 'database', 'au': 'auth'}[stem]
                duration = random.randint(1, 100)
                unit = random.choice([('ʰ', 'hours'), ('ᵈ', 'days')])
                english = f"Express {stem_name} has been active for {duration} {unit[1]}"
                ccin = f"●{stem}⋀up{format_count(duration)}{unit[0]}"

            elif pattern == 'schedule':
                action = random.choice([('dp', 'deployment'), ('rs', 'restart')])
                time_val = random.randint(1, 24)
                english = f"Schedule a {action[1]} in {time_val} hours"
                ccin = f"ᐅ{format_count(time_val)}ʰ●{action[0]}"

            elif pattern == 'transition':
                stem = random.choice(['sv', 'db'])
                stem_name = {'sv': 'server', 'db': 'database'}[stem]
                english = f"Show {stem_name} went from degraded to active"
                ccin = f"ᐊ◐{stem}»ᐃ●{stem}"

            elif pattern == 'recurring':
                action = random.choice([('bk', 'backup'), ('sc', 'scan')])
                interval = random.randint(1, 24)
                english = f"Set up recurring {action[1]} every {interval} hours"
                ccin = f"⟲{format_count(interval)}ʰ●{action[0]}"

            else:  # pipeline
                build = random.randint(5, 20)
                test = random.randint(10, 30)
                english = f"Express a deployment pipeline: build {build} minutes, then test {test} minutes"
                ccin = f"●bd{format_count(build)}ᵐ»●ts{format_count(test)}ᵐ»●dp"

            self.add_record(ccin, english, 'medium', 'temporal', ['sv', 'db', 'dp', 'bk'][:random.randint(1, 2)], ['●'], pair_type='B')

    # ==================== TYPE C TEMPORAL SIMILARITY ====================

    def generate_temporal_similarity_triplets(self, count: int = 200):
        """Generate temporal similarity triplets."""
        print(f"Generating {count} temporal similarity triplets...")

        for _ in range(count):
            stem = random.choice(['sv', 'db', 'jb'])
            duration = random.randint(5, 100)
            unit = random.choice(['ʰ', 'ᵈ'])

            anchor = f"●{stem}⋀up{format_count(duration)}{unit}"
            
            # Positive: similar duration
            pos_duration = duration + random.randint(-5, 5)
            pos_duration = max(1, pos_duration)
            positive = f"●{stem}⋀up{format_count(pos_duration)}{unit}"
            
            # Negative: very different duration or different status
            neg_duration = duration * random.choice([0.1, 5])
            neg_duration = int(max(1, neg_duration))
            negative = f"⊘{stem}⋀down{format_count(neg_duration)}{unit}"

            record = {
                "id": self.get_id(),
                "type": "C",
                "domain": "temporal",
                "complexity": "medium",
                "anchor": anchor,
                "positive": positive,
                "negative": negative,
                "anchor_english": f"Active {stem} for {duration} units",
                "similarity_score": 0.90,
                "stems_used": [stem],
                "opcodes_used": ['●', '⊘'],
                "valid": True
            }
            self.records.append(record)
            if len(self.records) >= self.batch_size:
                self.save_batch()

    def run_generation_cycle(self):
        """Run one full temporal expansion cycle."""
        print(f"\n{'='*50}")
        print(f"Starting temporal expansion at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        # Duration patterns
        self.generate_uptime_patterns(300)
        self.generate_downtime_patterns(200)

        # Scheduling
        self.generate_scheduled_tasks(300)
        self.generate_recurring_patterns(200)

        # Transitions
        self.generate_status_transitions(300)
        self.generate_multi_step_transitions(200)

        # Pipelines
        self.generate_deployment_timelines(200)

        # Type B and C
        self.generate_type_b_temporal(300)
        self.generate_temporal_similarity_triplets(200)

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
        start_batch = 113

    print(f"Starting temporal expansion from batch {start_batch}")

    generator = TemporalGenerator(output_dir, start_batch)

    # Run 2 cycles
    for cycle in range(2):
        print(f"\n*** CYCLE {cycle + 1}/2 ***")
        generator.run_generation_cycle()
        if cycle < 1:
            print("Pausing 60 seconds...")
            time.sleep(60)

    print(f"\n{'='*50}")
    print(f"TEMPORAL EXPANSION COMPLETE")
    print(f"Total new records: {generator.total_generated}")
    print(f"{'='*50}")

    # Run validation
    print("\nRunning validation...")
    import subprocess
    subprocess.run(['python3', 'validate_and_assemble.py'], cwd=output_dir)


if __name__ == "__main__":
    main()
