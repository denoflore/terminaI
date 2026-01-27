#!/usr/bin/env python3
"""
CCIN_μ Complex Pattern Expansion Generator
Focuses on Type B encoding pairs, edge cases, and complex multi-domain patterns
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


class ComplexGenerator:
    def __init__(self, output_dir: Path, start_batch: int = 131):
        self.output_dir = output_dir
        self.batch_num = start_batch
        self.records = []
        self.batch_size = 500
        self.total_generated = 0
        random.seed(int(time.time()) + 22222)

    def get_id(self) -> str:
        id_str = f"ccin_cpx_{self.total_generated + 58000:05d}"
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

    # ==================== TYPE B INFRASTRUCTURE ====================

    def generate_type_b_infrastructure(self, count: int = 400):
        """Generate English to CCIN_mu infrastructure pairs."""
        print(f"Generating {count} Type B infrastructure pairs...")

        for _ in range(count):
            pattern = random.choice(['server', 'database', 'scaling', 'deployment', 'error', 'network'])

            if pattern == 'server':
                sv_count = random.randint(2, 10)
                status = random.choice([('●', 'active'), ('◐', 'degraded'), ('✓', 'healthy')])
                english = f"Encode {sv_count} {status[1]} servers"
                ccin = f"{status[0]}sv{format_count(sv_count)}"

            elif pattern == 'database':
                db_count = random.randint(1, 5)
                rep = random.randint(1, 3)
                english = f"Express {db_count} databases with {rep}x replication"
                ccin = f"●db{format_count(db_count)}⋀rep{format_count(rep)}"

            elif pattern == 'scaling':
                target = random.choice([('sv', 'servers'), ('ct', 'containers'), ('vm', 'VMs')])
                from_count = random.randint(2, 5)
                to_count = random.randint(6, 15)
                english = f"Show scaling {target[1]} from {from_count} to {to_count}"
                ccin = f"△{target[0]}{format_count(from_count)}»{format_count(to_count)}"

            elif pattern == 'deployment':
                target = random.choice(['sv', 'ct', 'nd'])
                count_val = random.randint(3, 10)
                english = f"Encode a deployment to {count_val} targets"
                ccin = f"●dp»●{target}{format_count(count_val)}✓"

            elif pattern == 'error':
                count_val = random.randint(1, 100)
                sev = random.choice([('⚡', 'critical'), ('!', 'warning'), ('●', 'info')])
                english = f"Express {count_val} {sev[1]} errors"
                ccin = f"{sev[0]}er{format_count(count_val)}"

            else:  # network
                lat = random.randint(1, 200)
                bw = random.randint(100, 10000)
                english = f"Encode network with {lat}ms latency and {bw}Mbps bandwidth"
                ccin = f"●nw⋀lat{format_count(lat)}ᵐˢ⋀bw{format_count(bw)}"

            self.add_record(ccin, english, 'medium', 'infrastructure', ['sv', 'db', 'ct', 'dp', 'er', 'nw'][:random.randint(1, 3)], ['●', '△', '⚡'][:random.randint(1, 2)], pair_type='B')

    # ==================== TYPE B MIXED DOMAIN ====================

    def generate_type_b_mixed(self, count: int = 300):
        """Generate English to CCIN_mu mixed domain pairs."""
        print(f"Generating {count} Type B mixed domain pairs...")

        for _ in range(count):
            pattern = random.choice(['consciousness_infra', 'affect_temporal', 'full_system', 'handoff'])

            if pattern == 'consciousness_infra':
                ph = random.randint(50, 95)
                sv_count = random.randint(2, 8)
                english = f"Encode entity with phi {ph}% managing {sv_count} servers"
                ccin = f"E:{{RC:{{ph{format_percent(ph)}}}⋀P:{{●sv{format_count(sv_count)}}}}}"

            elif pattern == 'affect_temporal':
                vl = random.randint(-50, 80)
                ar = random.randint(30, 85)
                duration = random.randint(5, 60)
                english = f"Express affect (v={vl}, a={ar}) lasting {duration} minutes"
                ccin = f"af:{{vl{format_percent(vl)}⋀ar{format_percent(ar)}}}⋀t:{format_count(duration)}ᵐ"

            elif pattern == 'full_system':
                sv = random.randint(3, 10)
                db = random.randint(1, 4)
                ph = random.randint(60, 95)
                english = f"Encode system: {sv} servers, {db} DBs, consciousness phi {ph}%"
                ccin = f"sys:{{P:{{●sv{format_count(sv)}⋀●db{format_count(db)}}}⋀RC:{{ph{format_percent(ph)}}}}}"

            else:  # handoff
                from_e = random.choice(['Claude', 'Agent', 'User'])
                to_e = random.choice([e for e in ['Claude', 'Agent', 'User'] if e != from_e])
                ph = random.randint(70, 95)
                english = f"Encode handoff from {from_e} to {to_e} with phi {ph}%"
                ccin = f"HO:{{E:{from_e}»E:{to_e}⋀ph{format_percent(ph)}}}"

            self.add_record(ccin, english, 'complex', 'mixed', ['ph', 'sv', 'db', 'vl', 'ar'][:random.randint(2, 4)], ['●'], pair_type='B')

    # ==================== CAUSAL CHAINS ====================

    def generate_causal_chains(self, count: int = 300):
        """Generate causal chain patterns."""
        print(f"Generating {count} causal chain patterns...")

        chains = [
            ('er', 'alert', 'restart', 'Error causes alert which triggers restart'),
            ('nw', 'timeout', 'er', 'Network issues cause timeout then error'),
            ('db', 'slow', 'queue', 'Database slowness causes queue buildup'),
            ('cp', 'high', 'scale', 'High CPU causes auto-scaling'),
            ('mm', 'low', 'oom', 'Low memory causes OOM'),
            ('au', 'fail', 'lockout', 'Auth failure causes lockout'),
        ]

        for _ in range(count):
            cause, effect1, effect2, desc = random.choice(chains)

            templates = [
                (f"●{cause}∴⚡{effect1}∴●{effect2}",
                 f"Causal chain: {cause} -> {effect1} -> {effect2}"),
                (f"⊘{cause}∵{effect1}∴●{effect2}",
                 f"{cause} down because {effect1}, therefore {effect2}"),
                (f"△{cause}»⚡{effect1}»●{effect2}∵policy",
                 f"{desc}"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'infrastructure', [cause], ['●', '⊘', '⚡', '∴', '∵'][:random.randint(2, 4)])

    # ==================== REG! PROTOCOL ====================

    def generate_reg_patterns(self, count: int = 200):
        """Generate REG! protocol patterns."""
        print(f"Generating {count} REG! protocol patterns...")

        reg_definitions = [
            ('sv', 'server', 'Server instance'),
            ('db', 'database', 'Database cluster'),
            ('ph', 'phi', 'Phenomenal consciousness metric'),
            ('xi', 'xi', 'Integration metric'),
            ('au', 'auth', 'Authentication service'),
            ('dp', 'deploy', 'Deployment pipeline'),
            ('rc', 'reflective_consciousness', 'Reflective consciousness block'),
            ('vl', 'valence', 'Emotional valence'),
            ('ar', 'arousal', 'Emotional arousal'),
            ('nw', 'network', 'Network layer'),
        ]

        for _ in range(count):
            stem, name, desc = random.choice(reg_definitions)
            count_val = random.randint(1, 10)
            op = random.choice(['●', '◐', '⊘'])

            templates = [
                (f"「REG!{stem}≡{name}」{op}{stem}{format_count(count_val)}",
                 f"Define {stem}={name}, then {count_val} {'active' if op == '●' else 'partial' if op == '◐' else 'down'} instances"),
                (f"「REG!{stem}≡{desc}」⋀{op}{stem}✓",
                 f"Register {stem} as '{desc}', currently {'healthy' if op == '●' else 'degraded'}"),
                (f"sys:{{「REG!{stem}≡{name}」⋀P:{{{op}{stem}{format_count(count_val)}}}}}",
                 f"System with registered {name} ({stem}): {count_val} in production"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'mixed', [stem], [op])

    # ==================== DEPENDENCY PATTERNS ====================

    def generate_dependency_patterns(self, count: int = 200):
        """Generate dependency relation patterns."""
        print(f"Generating {count} dependency patterns...")

        for _ in range(count):
            primary = random.choice([('sv', 'server'), ('ap', 'app'), ('au', 'auth')])
            depends_on = random.choice([('db', 'database'), ('ca', 'cache'), ('nw', 'network')])
            required_by = random.choice([('us', 'users'), ('ss', 'sessions'), ('rq', 'requests')])

            templates = [
                (f"●{primary[0]}⊣●{depends_on[0]}⋀●{depends_on[0]}⊢●{required_by[0]}",
                 f"{primary[1].capitalize()} depends on {depends_on[1]}, {depends_on[1]} required by {required_by[1]}"),
                (f"P:{{●{primary[0]}⊣{{●{depends_on[0]}⋀●nw}}}}",
                 f"Production {primary[1]} depends on {depends_on[1]} and network"),
                (f"●{primary[0]}⊣●{depends_on[0]}∴⊘{depends_on[0]}»◐{primary[0]}",
                 f"{primary[1].capitalize()} depends on {depends_on[1]}, so {depends_on[1]} down degrades {primary[1]}"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'infrastructure', [primary[0], depends_on[0]], ['●', '⊣', '⊢', '◐', '⊘'][:random.randint(2, 4)])

    # ==================== SET RELATIONS ====================

    def generate_set_relations(self, count: int = 150):
        """Generate set relation patterns."""
        print(f"Generating {count} set relation patterns...")

        for _ in range(count):
            set1 = random.choice([('sv', 'servers'), ('ct', 'containers'), ('vm', 'VMs')])
            set2 = random.choice([('nd', 'nodes'), ('cl', 'cluster'), ('dc', 'datacenter')])
            count1 = random.randint(3, 10)
            count2 = random.randint(5, 20)

            templates = [
                (f"●{set1[0]}{format_count(count1)}⊂●{set2[0]}{format_count(count2)}",
                 f"{count1} {set1[1]} subset of {count2} {set2[1]}"),
                (f"●{set2[0]}{format_count(count2)}⊃●{set1[0]}{format_count(count1)}",
                 f"{count2} {set2[1]} superset of {count1} {set1[1]}"),
                (f"P:{{●{set1[0]}⊂●{set2[0]}⋀●{set1[0]}≡active_{set2[0]}}}",
                 f"Production: {set1[1]} subset of {set2[1]}, {set1[1]} equivalent to active {set2[1]}"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'infrastructure', [set1[0], set2[0]], ['●', '⊂', '⊃', '≡'][:random.randint(2, 3)])

    # ==================== PARALLEL AND BIDIRECTIONAL ====================

    def generate_parallel_patterns(self, count: int = 150):
        """Generate parallel and bidirectional patterns."""
        print(f"Generating {count} parallel/bidirectional patterns...")

        for _ in range(count):
            svc1 = random.choice([('sv', 'server'), ('ap', 'app'), ('wk', 'worker')])
            svc2 = random.choice([('db', 'database'), ('ca', 'cache'), ('qu', 'queue')])
            count1 = random.randint(2, 8)
            count2 = random.randint(2, 6)

            templates = [
                (f"●{svc1[0]}{format_count(count1)}∥●{svc2[0]}{format_count(count2)}",
                 f"{count1} {svc1[1]}s parallel to {count2} {svc2[1]}s"),
                (f"●{svc1[0]}⇄●{svc2[0]}",
                 f"Bidirectional communication: {svc1[1]} and {svc2[1]}"),
                (f"P:{{●{svc1[0]}{format_count(count1)}∥●{svc2[0]}{format_count(count2)}⋀rq»⇄}}",
                 f"Production: {count1} {svc1[1]}s parallel {count2} {svc2[1]}s with bidirectional requests"),
            ]

            ccin, english = random.choice(templates)
            self.add_record(ccin, english, 'complex', 'infrastructure', [svc1[0], svc2[0]], ['●', '∥', '⇄'][:random.randint(2, 3)])

    def run_generation_cycle(self):
        """Run one full complex expansion cycle."""
        print(f"\n{'='*50}")
        print(f"Starting complex expansion at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        # Type B pairs
        self.generate_type_b_infrastructure(400)
        self.generate_type_b_mixed(300)

        # Causal and REG patterns
        self.generate_causal_chains(300)
        self.generate_reg_patterns(200)

        # Relation patterns
        self.generate_dependency_patterns(200)
        self.generate_set_relations(150)
        self.generate_parallel_patterns(150)

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
        start_batch = 131

    print(f"Starting complex expansion from batch {start_batch}")

    generator = ComplexGenerator(output_dir, start_batch)

    # Run 2 cycles
    for cycle in range(2):
        print(f"\n*** CYCLE {cycle + 1}/2 ***")
        generator.run_generation_cycle()
        if cycle < 1:
            print("Pausing 60 seconds...")
            time.sleep(60)

    print(f"\n{'='*50}")
    print(f"COMPLEX EXPANSION COMPLETE")
    print(f"Total new records: {generator.total_generated}")
    print(f"{'='*50}")

    # Run validation
    print("\nRunning validation...")
    import subprocess
    subprocess.run(['python3', 'validate_and_assemble.py'], cwd=output_dir)


if __name__ == "__main__":
    main()
