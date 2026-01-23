#!/usr/bin/env python3
"""
CCIN_μ Infrastructure Domain Generator
Phase 3: Generate 1500 infrastructure/technical domain pairs
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Tuple

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

# Infrastructure stems
INFRA_STEMS = {
    'sv': {'name': 'server', 'plural': 'servers', 'countable': True},
    'db': {'name': 'database', 'plural': 'databases', 'countable': True},
    'ca': {'name': 'cache', 'plural': 'caches', 'countable': True},
    'nw': {'name': 'network', 'plural': 'network connections', 'countable': False},
    'fw': {'name': 'firewall', 'plural': 'firewalls', 'countable': True},
    'lb': {'name': 'load balancer', 'plural': 'load balancers', 'countable': True},
    'ct': {'name': 'container', 'plural': 'containers', 'countable': True},
    'vm': {'name': 'VM', 'plural': 'VMs', 'countable': True},
    'gp': {'name': 'GPU', 'plural': 'GPUs', 'countable': True},
    'cp': {'name': 'CPU', 'plural': 'CPUs', 'countable': False, 'resource': True},
    'mm': {'name': 'memory', 'plural': 'memory', 'countable': False, 'resource': True},
    'dk': {'name': 'disk', 'plural': 'disks', 'countable': False, 'resource': True},
    'cl': {'name': 'cluster', 'plural': 'clusters', 'countable': True},
    'nd': {'name': 'node', 'plural': 'nodes', 'countable': True},
    'pd': {'name': 'pod', 'plural': 'pods', 'countable': True},
    'sc': {'name': 'service', 'plural': 'services', 'countable': True},
}

# Application stems
APP_STEMS = {
    'au': {'name': 'auth', 'plural': 'auth services', 'action': 'authentication'},
    'az': {'name': 'authorization', 'plural': 'authz checks', 'action': 'authorization'},
    'tk': {'name': 'token', 'plural': 'tokens', 'countable': True},
    'ss': {'name': 'session', 'plural': 'sessions', 'countable': True},
    'us': {'name': 'user', 'plural': 'users', 'countable': True},
    'rq': {'name': 'request', 'plural': 'requests', 'countable': True, 'rate': True},
    'rs': {'name': 'response', 'plural': 'responses', 'countable': True, 'rate': True},
    'er': {'name': 'error', 'plural': 'errors', 'countable': True},
    'lg': {'name': 'log', 'plural': 'logs', 'countable': True},
    'ev': {'name': 'event', 'plural': 'events', 'countable': True},
    'mg': {'name': 'message', 'plural': 'messages', 'countable': True},
    'ap': {'name': 'API', 'plural': 'APIs', 'countable': True},
    'ws': {'name': 'websocket', 'plural': 'websockets', 'countable': True},
    'qu': {'name': 'queue', 'plural': 'queues', 'countable': True},
    'wk': {'name': 'worker', 'plural': 'workers', 'countable': True},
}

# Data stems
DATA_STEMS = {
    'da': {'name': 'data', 'plural': 'data'},
    'fl': {'name': 'file', 'plural': 'files', 'countable': True},
    'dr': {'name': 'directory', 'plural': 'directories', 'countable': True},
    'cf': {'name': 'config', 'plural': 'configs', 'countable': True},
    'en': {'name': 'env var', 'plural': 'env vars', 'countable': True},
    'st': {'name': 'state', 'plural': 'states'},
    'sc': {'name': 'schema', 'plural': 'schemas', 'countable': True},
    'rc': {'name': 'record', 'plural': 'records', 'countable': True},
}

# State opcodes
STATE_OPCODES = {
    '●': 'active/healthy',
    '◌': 'inactive/offline',
    '◐': 'partial/degraded',
}

# Action/signal opcodes
ACTION_OPCODES = {
    '⊘': 'down/failed',
    '⟲': 'cycling/recurring',
    '⟳': 'restarting/reversing',
    '△': 'increasing/rising',
    '▽': 'decreasing/falling',
    '⊕': 'adding/creating',
    '⊖': 'removing/deleting',
    '⚡': 'critical/urgent',
    '◇': 'optional',
    '▣': 'required',
    '▢': 'empty/null',
    '!': 'alert',
}

# Common error scenarios
ERROR_SCENARIOS = [
    ('token expired', '⊘tk:{exp}', ['tk']),
    ('SSL certificate invalid', '⊘tk:{ssl⊘}', ['tk']),
    ('connection refused', '⊘nw:{conn⊘ref}', ['nw']),
    ('timeout exceeded', '⊘rq:{timeout}', ['rq']),
    ('rate limit hit', '⊘rq:{rate⚡}', ['rq']),
    ('out of memory', '⊘mm:{oom}', ['mm']),
    ('disk full', '⊘dk:{full}', ['dk']),
    ('port unavailable', '⊘nw:{port⊘}', ['nw']),
    ('permission denied', '⊘az:{denied}', ['az']),
    ('resource exhausted', '⊘cp:{exhaust}', ['cp']),
]

# Health report templates
HEALTH_TEMPLATES = [
    "I:{{●sv{sv_count}✓⋀●db{db_count}✓}}",
    "I:{{●sv{sv_count}✓⋀●db{db_count}✓⋀●ca{ca_count}✓}}",
    "I:{{●sv{sv_count}✓⋀●nw✓⋀cp%{cp}⋀mm%{mm}}}",
    "I:CLUSTER:{{●nd{nd_count}⋀●pd{pd_count}⋀●ct{ct_count}}}",
    "I:{{cp%{cp}⋀mm%{mm}⋀dk%{dk}}}",
    "I:{{cp%{cp}⋀mm%{mm}⋀gp%{gp}}}",
]


class InfrastructureGenerator:
    def __init__(self, output_dir: Path, start_id: int = 2000, batch_num: int = 6):
        self.output_dir = output_dir
        self.current_id = start_id
        self.batch_num = batch_num
        self.records = []
        self.batch_size = 500
        random.seed(44)

    def get_id(self) -> str:
        id_str = f"ccin_infra_{self.current_id:05d}"
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
            "domain": "infrastructure",
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

    def generate_simple_infra(self):
        """Generate simple single-component infrastructure examples."""
        print("Generating simple infrastructure examples...")

        # Simple state with count
        for stem, info in INFRA_STEMS.items():
            if info.get('countable', False):
                for count in [1, 2, 3, 4, 5, 8, 10, 12, 16, 20]:
                    for op in ['●', '◌', '◐']:
                        op_desc = STATE_OPCODES[op]
                        ccin = f"{op}{stem}{format_count(count)}"
                        english = f"{count} {info['plural']} {op_desc}"
                        self.add_record(ccin, english, 'simple', [stem], [op])

                    # With health marker
                    ccin = f"●{stem}{format_count(count)}✓"
                    english = f"{count} {info['plural']} healthy"
                    self.add_record(ccin, english, 'simple', [stem], ['●'])

                    ccin = f"⊘{stem}{format_count(count)}✗"
                    english = f"{count} {info['plural']} failed"
                    self.add_record(ccin, english, 'simple', [stem], ['⊘'])

            # Resource percentage
            if info.get('resource', False):
                for pct in [15, 25, 35, 45, 55, 65, 75, 85, 95]:
                    ccin = f"{stem}{format_percent(pct)}"
                    english = f"{info['name']} at {pct}%"
                    self.add_record(ccin, english, 'simple', [stem], [])

                    # With delta
                    for op in ['△', '▽']:
                        direction = 'rising' if op == '△' else 'falling'
                        ccin = f"{op}{stem}{format_percent(pct)}"
                        english = f"{info['name']} {direction} to {pct}%"
                        self.add_record(ccin, english, 'simple', [stem], [op])

        # Application stems
        for stem, info in APP_STEMS.items():
            # Active/inactive states
            for op in ['●', '⊘']:
                state = 'active' if op == '●' else 'down'
                ccin = f"{op}{stem}"
                english = f"{info['name']} {state}"
                self.add_record(ccin, english, 'simple', [stem], [op])

            if info.get('countable', False):
                for count in [5, 10, 50, 100, 500, 1000]:
                    ccin = f"●{stem}{format_count(count)}"
                    english = f"{count} {info['plural']} active"
                    self.add_record(ccin, english, 'simple', [stem], ['●'])

            if info.get('rate', False):
                for rate in [10, 50, 100, 500, 1000]:
                    ccin = f"{stem}{format_count(rate)}ˢ"
                    english = f"{rate} {info['plural']} per second"
                    self.add_record(ccin, english, 'simple', [stem], [])

    def generate_health_reports(self):
        """Generate system health report examples."""
        print("Generating health report examples...")

        for _ in range(150):
            sv_count = random.randint(1, 20)
            db_count = random.randint(1, 6)
            ca_count = random.randint(1, 4)
            cp = random.randint(20, 95)
            mm = random.randint(30, 90)
            dk = random.randint(15, 85)
            gp = random.randint(10, 98)
            nd_count = random.randint(3, 12)
            pd_count = random.randint(5, 50)
            ct_count = random.randint(10, 100)

            template = random.choice(HEALTH_TEMPLATES)
            ccin = template.format(
                sv_count=format_count(sv_count),
                db_count=format_count(db_count),
                ca_count=format_count(ca_count),
                cp=format_count(cp),
                mm=format_count(mm),
                dk=format_count(dk),
                gp=format_count(gp),
                nd_count=format_count(nd_count),
                pd_count=format_count(pd_count),
                ct_count=format_count(ct_count),
            )

            # Build description based on template
            if 'CLUSTER' in ccin:
                english = f"Kubernetes cluster: {nd_count} nodes, {pd_count} pods, {ct_count} containers healthy"
                stems = ['nd', 'pd', 'ct']
            elif 'gp' in ccin:
                english = f"Resource utilization: CPU {cp}%, memory {mm}%, GPU {gp}%"
                stems = ['cp', 'mm', 'gp']
            elif 'dk' in ccin:
                english = f"Resource utilization: CPU {cp}%, memory {mm}%, disk {dk}%"
                stems = ['cp', 'mm', 'dk']
            elif 'nw' in ccin:
                english = f"Infrastructure: {sv_count} servers healthy, network OK, CPU {cp}%, memory {mm}%"
                stems = ['sv', 'nw', 'cp', 'mm']
            elif 'ca' in ccin:
                english = f"Infrastructure: {sv_count} servers, {db_count} databases, {ca_count} caches all healthy"
                stems = ['sv', 'db', 'ca']
            else:
                english = f"Infrastructure: {sv_count} servers healthy, {db_count} databases healthy"
                stems = ['sv', 'db']

            self.add_record(ccin, english, 'medium', stems, ['●'])

    def generate_error_states(self):
        """Generate error state and alert examples."""
        print("Generating error state examples...")

        for scenario_name, ccin_pattern, stems in ERROR_SCENARIOS:
            for _ in range(15):
                ccin = ccin_pattern
                english = f"Error: {scenario_name}"
                self.add_record(ccin, english, 'simple', stems, ['⊘'])

        # Cascading errors
        cascade_patterns = [
            ("⊘nw∴⊘db∴⚡er", "Network down, causing database failure, critical error", ['nw', 'db', 'er']),
            ("⊘tk∴⊘au∴⊘ss", "Token failed, causing auth failure, sessions terminated", ['tk', 'au', 'ss']),
            ("⊘ca∴△db⋀△cp", "Cache failed, causing database and CPU spike", ['ca', 'db', 'cp']),
            ("⊘lb∴⊘sv³∴⚡er", "Load balancer down, 3 servers unreachable, critical error", ['lb', 'sv', 'er']),
            ("⊘nw∴⊘ap∴⚡mg", "Network down, API unreachable, critical messages queued", ['nw', 'ap', 'mg']),
        ]

        for ccin, english, stems in cascade_patterns:
            for _ in range(20):
                self.add_record(ccin, english, 'medium', stems, ['⊘', '∴', '⚡'])

        # Alert patterns
        for _ in range(100):
            component = random.choice(['sv', 'db', 'nw', 'au', 'ap', 'ca'])
            count = random.randint(1, 5)
            info = {**INFRA_STEMS, **APP_STEMS}.get(component, {'name': component})

            ccin = f"!I:{{⊘{component}{format_count(count) if count > 1 else ''}∴⚡er}}"
            english = f"ALERT: {count if count > 1 else ''} {info.get('plural', info['name']) if count > 1 else info['name']} down, critical error"
            self.add_record(ccin, english, 'medium', [component, 'er'], ['!', '⊘', '⚡'])

    def generate_multi_component(self):
        """Generate multi-component infrastructure states."""
        print("Generating multi-component examples...")

        # Mixed health/degraded states
        for _ in range(100):
            healthy_svs = random.randint(3, 10)
            degraded_svs = random.randint(0, 2)
            healthy_dbs = random.randint(1, 4)
            failed_dbs = random.randint(0, 1)
            errors = random.randint(0, 5)

            parts = [f"●sv{format_count(healthy_svs)}✓"]
            desc_parts = [f"{healthy_svs} servers healthy"]

            if degraded_svs > 0:
                parts.append(f"◐sv{format_count(degraded_svs)}~")
                desc_parts.append(f"{degraded_svs} servers degraded")

            parts.append(f"●db{format_count(healthy_dbs)}✓")
            desc_parts.append(f"{healthy_dbs} databases healthy")

            if failed_dbs > 0:
                parts.append(f"⊘db{format_count(failed_dbs)}✗")
                desc_parts.append(f"{failed_dbs} database failed")

            if errors > 0:
                parts.append(f"⚡er{format_count(errors)}")
                desc_parts.append(f"{errors} critical errors")

            ccin = f"I:{{{('⋀'.join(parts))}}}"
            english = ", ".join(desc_parts)

            stems = ['sv', 'db']
            if errors > 0:
                stems.append('er')
            opcodes = ['●']
            if degraded_svs > 0:
                opcodes.append('◐')
            if failed_dbs > 0:
                opcodes.append('⊘')
            if errors > 0:
                opcodes.append('⚡')

            self.add_record(ccin, english, 'medium', stems, opcodes)

        # Resource utilization scenarios
        for _ in range(100):
            cp = random.randint(10, 99)
            mm = random.randint(15, 98)
            dk = random.randint(10, 95)

            if cp > 90 or mm > 90 or dk > 90:
                severity = '⚡'
                sev_text = 'CRITICAL: '
            elif cp > 75 or mm > 75 or dk > 75:
                severity = '!'
                sev_text = 'WARNING: '
            else:
                severity = ''
                sev_text = ''

            ccin = f"{severity}I:{{cp{format_percent(cp)}⋀mm{format_percent(mm)}⋀dk{format_percent(dk)}}}"
            english = f"{sev_text}Resources: CPU {cp}%, memory {mm}%, disk {dk}%"

            opcodes = []
            if severity:
                opcodes.append(severity)

            self.add_record(ccin, english, 'medium', ['cp', 'mm', 'dk'], opcodes)

        # Application layer states
        for _ in range(100):
            rq_rate = random.randint(10, 5000)
            rs_rate = random.randint(int(rq_rate * 0.8), rq_rate)
            err_rate = random.randint(0, int(rq_rate * 0.1))
            sessions = random.randint(50, 10000)

            ccin = f"A:{{rq{format_count(rq_rate)}ˢ⋀rs{format_count(rs_rate)}ˢ⋀er{format_count(err_rate)}ˢ⋀ss{format_count(sessions)}}}"

            success_rate = round((rs_rate / rq_rate) * 100, 1) if rq_rate > 0 else 100
            english = f"Application: {rq_rate} req/s, {rs_rate} resp/s ({success_rate}% success), {err_rate} err/s, {sessions} sessions"

            self.add_record(ccin, english, 'complex', ['rq', 'rs', 'er', 'ss'], [])

    def generate_kubernetes_patterns(self):
        """Generate Kubernetes/container orchestration patterns."""
        print("Generating Kubernetes patterns...")

        for _ in range(100):
            nodes = random.randint(3, 20)
            healthy_nodes = random.randint(int(nodes * 0.7), nodes)
            pods = random.randint(20, 200)
            running_pods = random.randint(int(pods * 0.9), pods)
            containers = random.randint(pods, pods * 3)

            ccin = f"I:K8S:{{\n  nd:{format_count(healthy_nodes)}/{format_count(nodes)}✓\n  pd:{format_count(running_pods)}/{format_count(pods)}✓\n  ct{format_count(containers)}✓\n}}"

            english = f"Kubernetes cluster: {healthy_nodes}/{nodes} nodes healthy, {running_pods}/{pods} pods running, {containers} containers"

            self.add_record(ccin, english, 'complex', ['nd', 'pd', 'ct'], ['●'])

        # Deployment scenarios
        for _ in range(50):
            replicas = random.randint(3, 10)
            ready = random.randint(0, replicas)
            restarting = random.randint(0, replicas - ready)

            if ready == replicas:
                status = '●'
                status_text = 'healthy'
            elif ready > 0:
                status = '◐'
                status_text = 'partial'
            else:
                status = '⊘'
                status_text = 'down'

            ccin = f"K8S:DEPLOY:{{{status}pd{format_count(ready)}/{format_count(replicas)}⋀⟲{format_count(restarting)}}}"
            english = f"Deployment {status_text}: {ready}/{replicas} pods ready, {restarting} restarting"

            self.add_record(ccin, english, 'medium', ['pd'], [status, '⟲'])

    def generate_network_patterns(self):
        """Generate network and connectivity patterns."""
        print("Generating network patterns...")

        for _ in range(80):
            # Connection states
            ws_count = random.randint(10, 1000)
            active = random.randint(int(ws_count * 0.7), ws_count)

            ccin = f"N:{{ws{format_count(active)}/{format_count(ws_count)}⋀●nw✓}}"
            english = f"Network: {active}/{ws_count} websocket connections active, network healthy"
            self.add_record(ccin, english, 'medium', ['ws', 'nw'], ['●'])

        # Latency patterns
        for _ in range(50):
            latency = random.randint(1, 500)
            if latency < 50:
                status = '●'
                desc = 'normal'
            elif latency < 200:
                status = '◐'
                desc = 'elevated'
            else:
                status = '⊘'
                desc = 'high'

            ccin = f"N:{{lt{format_count(latency)}ms⋀{status}}}"
            english = f"Network latency {desc}: {latency}ms"
            self.add_record(ccin, english, 'simple', ['nw'], [status])

        # Firewall rules
        for _ in range(30):
            rules_active = random.randint(10, 100)
            blocked = random.randint(0, 50)

            ccin = f"N:FW:{{●rl{format_count(rules_active)}⋀⊘{format_count(blocked)}}}"
            english = f"Firewall: {rules_active} rules active, {blocked} requests blocked"
            self.add_record(ccin, english, 'medium', ['fw'], ['●', '⊘'])

    def generate_type_b_pairs(self):
        """Generate Type B (English → CCIN_μ) infrastructure pairs."""
        print("Generating Type B infrastructure pairs...")

        # Static patterns (no substitution needed)
        static_patterns = [
            ("All systems operational", "I:{{●sv✓⋀●db✓⋀●nw✓}}", ['sv', 'db', 'nw']),
            ("Database is down", "⊘db", ['db']),
            ("Three servers unhealthy", "⊘sv³✗", ['sv']),
            ("Cache performance degraded", "◐ca~", ['ca']),
            ("Authentication service failing", "⊘au∵⊘tk", ['au', 'tk']),
            ("Load balancer offline", "⊘lb✗", ['lb']),
            ("Network connection lost", "⊘nw", ['nw']),
            ("GPU utilization maxed", "⚡gp%⁹⁹", ['gp']),
        ]

        for english, ccin, stems in static_patterns:
            for _ in range(15):
                opcodes = []
                for op in ['●', '◌', '◐', '⊘', '△', '▽', '⚡', '!']:
                    if op in ccin:
                        opcodes.append(op)
                self.add_record(ccin, english, 'medium', stems, opcodes, pair_type='B')

        # Dynamic patterns with value substitution
        for _ in range(50):
            cp = random.randint(75, 99)
            ccin = f"△cp{format_percent(cp)}"
            self.add_record(ccin, "Server load is high", 'medium', ['cp'], ['△'], pair_type='B')

            mm = random.randint(85, 99)
            ccin = f"⚡mm{format_percent(mm)}"
            self.add_record(ccin, "Memory usage critical", 'medium', ['mm'], ['⚡'], pair_type='B')

            dk = random.randint(80, 95)
            ccin = f"!dk{format_percent(dk)}"
            self.add_record(ccin, "Disk space running low", 'medium', ['dk'], ['!'], pair_type='B')

            rate = random.randint(100, 5000)
            ccin = f"△rq{format_count(rate)}ˢ"
            self.add_record(ccin, "API requests spiking", 'medium', ['rq'], ['△'], pair_type='B')

            count = random.randint(5, 50)
            ccin = f"●pd{format_count(count)}✓"
            self.add_record(ccin, "All pods healthy", 'medium', ['pd'], ['●'], pair_type='B')

            rate2 = random.randint(10, 500)
            ccin = f"△er{format_count(rate2)}ˢ"
            self.add_record(ccin, "Error rate increasing", 'medium', ['er'], ['△'], pair_type='B')

            ss_count = random.randint(50, 500)
            ccin = f"▽ss{format_count(ss_count)}"
            self.add_record(ccin, "Session count dropping", 'medium', ['ss'], ['▽'], pair_type='B')

    def generate_all(self):
        """Generate all infrastructure domain pairs."""
        self.generate_simple_infra()
        self.generate_health_reports()
        self.generate_error_states()
        self.generate_multi_component()
        self.generate_kubernetes_patterns()
        self.generate_network_patterns()
        self.generate_type_b_pairs()

        if self.records:
            self.save_batch()

        print(f"\nTotal infrastructure batches: {self.batch_num - 6}")
        print(f"Total infrastructure records: {self.current_id - 2000}")


def main():
    output_dir = Path(__file__).parent
    generator = InfrastructureGenerator(output_dir)
    generator.generate_all()

    # Update stats
    stats_path = output_dir / "generation_stats.json"
    with open(stats_path, 'r') as f:
        stats = json.load(f)

    stats["phase3_infrastructure"] = {
        "total_generated": generator.current_id - 2000,
        "batches": generator.batch_num - 6
    }

    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"\nUpdated stats: {stats_path}")


if __name__ == "__main__":
    main()
