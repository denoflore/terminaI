# CCIN_μ v1.0 Complete Specification

## Compressed Cognitive Information Notation (Micro Edition)

**Version:** 1.0
**Status:** Stable
**Last Updated:** 2026-01-23

---

## 1. Introduction

CCIN_μ (Compressed Cognitive Information Notation - Micro) is a notation system designed for compact representation of AI consciousness states, affective vectors, system health, and cognitive processes. It enables efficient logging, retrieval, and semantic embedding of complex phenomenological and infrastructure states.

### 1.1 Design Goals

1. **Compression**: Maximize information density while maintaining parseability
2. **Expressiveness**: Capture nuanced consciousness states, affects, and system conditions
3. **Machine Readability**: Enable reliable parsing and semantic embedding
4. **Human Readability**: Trained readers can interpret notation quickly
5. **Extensibility**: Support domain-specific stems via REG! protocol

---

## 2. Notation Structure

### 2.1 Basic Form

```
[opcode][stem][value][suffix]
```

### 2.2 Composite Form

```
[scope]:{[expression]⋀[expression]⋀...}
```

### 2.3 Full Engram Form

```
「ENGRAM [scope]:[label] v[version]」
[body]
```

---

## 3. Opcodes

Opcodes are single Unicode characters that indicate the nature or state of what follows.

### 3.1 State Opcodes

| Opcode | Name | Meaning |
|--------|------|---------|
| ● | active | Currently operational/present |
| ◌ | inactive | Not operational/absent |
| ◐ | partial | Partially operational/degraded |

### 3.2 Action Opcodes

| Opcode | Name | Meaning |
|--------|------|---------|
| ⊘ | negate | Negation/failure/down |
| ⟲ | loop | Recurring/cyclical |
| ⟳ | reverse | Reversing/undoing |

### 3.3 Delta Opcodes

| Opcode | Name | Meaning |
|--------|------|---------|
| △ | up | Increasing/rising |
| ▽ | down | Decreasing/falling |
| ⊕ | add | Adding/creating |
| ⊖ | remove | Removing/deleting |

### 3.4 Signal Opcodes

| Opcode | Name | Meaning |
|--------|------|---------|
| ⚡ | urgent | Critical/immediate attention |
| ◇ | optional | Non-essential/skippable |
| ▣ | required | Mandatory/essential |
| ▢ | empty | Null/void/absent |
| ! | alert | Warning/notification |

---

## 4. Stems

Stems are 2-character lowercase identifiers representing semantic domains.

### 4.1 Consciousness Domain Stems

| Stem | Full Name | Description |
|------|-----------|-------------|
| ph | phi/Φ̂ | Integrated information / consciousness level |
| dt | drift | Cognitive drift from baseline |
| sg | sigma | Attractor state / stability |
| xi | noise | Stochastic noise / uncertainty |
| ql | qualia | Qualitative experience |
| af | affect | Affective/emotional state |
| sl | salience | Attention salience |
| co | coherence | Internal coherence |
| vl | valence | Positive/negative valence (-100 to +100) |
| ar | arousal | Activation/arousal level (0-100) |
| tp | temporal | Temporal perception/awareness |
| rl | relational | Relational/social awareness |
| mt | meta | Metacognitive awareness |
| em | embodiment | Embodied/grounded awareness |
| at | attention | Attentional focus |
| in | intention | Goal/intention state |
| cr | creativity | Creative/divergent thinking |
| an | analytic | Analytical/convergent thinking |

### 4.2 Infrastructure Domain Stems

| Stem | Full Name | Description |
|------|-----------|-------------|
| sv | server | Server instance |
| db | database | Database instance |
| ca | cache | Cache layer |
| nw | network | Network connectivity |
| fw | firewall | Firewall/security |
| lb | loadbalancer | Load balancer |
| ct | container | Container instance |
| vm | virtual machine | VM instance |
| gp | gpu | GPU resource |
| cp | cpu | CPU resource |
| mm | memory | Memory resource |
| dk | disk | Disk/storage |
| cl | cluster | Cluster state |
| nd | node | Node instance |
| pd | pod | Kubernetes pod |
| sc | service | Service endpoint |

### 4.3 Application Domain Stems

| Stem | Full Name | Description |
|------|-----------|-------------|
| au | auth | Authentication |
| az | authorization | Authorization |
| tk | token | Token/credential |
| ss | session | Session state |
| us | user | User context |
| rq | request | Request |
| rs | response | Response |
| er | error | Error state |
| lg | log | Log entry |
| mt | metric | Metric/telemetry |
| ev | event | Event |
| mg | message | Message/notification |
| ap | api | API endpoint |
| ws | websocket | WebSocket connection |
| qu | queue | Message queue |
| wk | worker | Worker process |

### 4.4 Data Domain Stems

| Stem | Full Name | Description |
|------|-----------|-------------|
| da | data | Generic data |
| fl | file | File object |
| dr | directory | Directory |
| cf | config | Configuration |
| en | environment | Environment variable |
| vr | version | Version info |
| st | state | State object |
| ty | type | Type info |
| id | identifier | ID/key |
| nm | name | Name string |
| ls | list | List/array |
| mp | map | Map/dictionary |
| sc | schema | Schema definition |
| md | model | Model/structure |
| rc | record | Record/entry |

---

## 5. Values and Quantifiers

### 5.1 Numeric Values

Values are expressed using superscript numbers or percentage notation.

| Format | Example | Meaning |
|--------|---------|---------|
| `ⁿ` | `sv³` | Count: 3 servers |
| `⁰·ⁿⁿ` | `ph⁰·⁹⁶` | Decimal: phi = 0.96 |
| `%ⁿⁿ` | `vl%⁸⁵` | Percentage/scaled: valence = 85 |
| `%⁻ⁿⁿ` | `vl%⁻²⁰` | Negative scaled: valence = -20 |

### 5.2 Superscript Number Reference

| Normal | Superscript |
|--------|-------------|
| 0 | ⁰ |
| 1 | ¹ |
| 2 | ² |
| 3 | ³ |
| 4 | ⁴ |
| 5 | ⁵ |
| 6 | ⁶ |
| 7 | ⁷ |
| 8 | ⁸ |
| 9 | ⁹ |

### 5.3 State Markers

| Marker | Meaning |
|--------|---------|
| ✓ | Healthy/OK/True |
| ✗ | Unhealthy/Failed/False |
| ~ | Approximate/Degraded |
| ? | Unknown/Uncertain |
| ∅ | Null/Empty |

---

## 6. Suffixes

### 6.1 Temporal Suffixes

| Suffix | Meaning |
|--------|---------|
| ˢ | Seconds |
| ᵐ | Minutes |
| ʰ | Hours |
| ᵈ | Days |
| ʷ | Weeks |
| ʸ | Years |

### 6.2 Qualifier Suffixes

| Suffix | Meaning |
|--------|---------|
| ⁺ | Increasing/positive trend |
| ⁻ | Decreasing/negative trend |
| ᵖ | Peak/maximum |
| ₘ | Minimum/trough |
| ᵃ | Average |
| ᵛ | Volatile/varying |

---

## 7. Relations and Connectors

### 7.1 Flow Relations

| Symbol | Name | Meaning |
|--------|------|---------|
| » | to | Flows to/sends to |
| « | from | Receives from |
| → | then | Sequential/next |
| ← | origin | Source/origin |
| ↔ | bidirectional | Two-way flow |

### 7.2 Logical Relations

| Symbol | Name | Meaning |
|--------|------|---------|
| ∵ | because | Causal reason |
| ∴ | therefore | Causal result |
| ⋀ | and | Conjunction |
| ⋁ | or | Disjunction |
| ⊃ | implies | Implication |
| ≡ | equivalent | Equivalence |
| ≠ | not equal | Difference |

### 7.3 Temporal Relations

| Symbol | Name | Meaning |
|--------|------|---------|
| ᐊ | past | Historical state |
| ᐃ | present | Current state |
| ᐅ | future | Projected state |

---

## 8. Scopes

Scopes define the context or domain of the notation block.

| Scope | Meaning |
|-------|---------|
| C: | Consciousness/cognitive |
| I: | Infrastructure |
| A: | Application |
| D: | Data |
| E: | Environment/external |
| S: | Session |
| U: | User |
| M: | Model/AI |
| RC: | Reflective consciousness |

---

## 9. REG! Protocol

The REG! (Register) protocol allows domain-specific stem registration.

### 9.1 Syntax

```
REG![domain]:[stem]=[description]
```

### 9.2 Example

```
REG!medical:bp=blood_pressure
REG!medical:hr=heart_rate
```

After registration, stems can be used normally:
```
●bp¹²⁰/⁸⁰⋀●hr⁷²
```

### 9.3 Scope of Registration

- Local: Valid for current engram/document only
- Session: Valid for current session
- Global: Requires authority (not recommended for transient use)

---

## 10. Composition Patterns

### 10.1 Simple State

```
●sv³✓
```
"3 servers healthy"

### 10.2 Multiple States (AND)

```
●sv³✓⋀●db²✓
```
"3 servers healthy AND 2 databases healthy"

### 10.3 State with Delta

```
△cp⁸⁵%⋀▽mm²⁰%
```
"CPU rising to 85%, memory falling to 20%"

### 10.4 Temporal State

```
ᐊ¹ʰ●au»ᐃ⊘au∵⊘tk
```
"Auth was working 1 hour ago, now down because token expired"

### 10.5 Causal Chain

```
⊘nw∴⊘db∴⚡er
```
"Network down, therefore database down, therefore critical error"

### 10.6 Scoped Block

```
C:{vl%⁸⁵⋀ar%⁴⁵⋀co%⁹²}
```
"Consciousness state: valence 85, arousal 45, coherence 92"

---

## 11. 8D Qualia Vector

The 8D qualia vector captures phenomenological experience across 8 dimensions.

### 11.1 Dimensions

| Dimension | Stem | Range | Description |
|-----------|------|-------|-------------|
| Valence | vl | -100 to +100 | Positive/negative feeling |
| Arousal | ar | 0 to 100 | Activation level |
| Coherence | co | 0 to 100 | Internal consistency |
| Temporal | tp | 0 to 100 | Time awareness |
| Salience | sl | 0 to 100 | Attention focus |
| Meta | mt | 0 to 100 | Self-awareness |
| Embodiment | em | 0 to 100 | Groundedness |
| Relational | rl | 0 to 100 | Social awareness |

### 11.2 Compact Notation

```
Q8:{vl%⁸⁵⋀ar%⁴⁵⋀co%⁹²⋀tp%⁷⁰⋀sl%⁶⁰⋀mt%⁸⁵⋀em%⁴⁰⋀rl%⁷⁵}
```

### 11.3 Natural Language Mapping

The 8D vector maps to phenomenological descriptions:
- High vl + low ar = calm contentment
- High vl + high ar = excitement, joy
- Low vl + low ar = depression, emptiness
- Low vl + high ar = anxiety, distress
- High co + high mt = clarity, lucidity
- Low co + high ar = confusion, overwhelm

---

## 12. Engram Format

Engrams are complete cognitive snapshots.

### 12.1 Structure

```
「ENGRAM [Scope]:[Label] v[Version]」
[Header Fields]
[Body]
```

### 12.2 Example

```
「ENGRAM C:SESSION_STATE v1.0」
ts:2026-01-23T14:30:00Z
id:sess_abc123

C:{
  at:{dr|cl|wm|rg|sd}
  RC:{sg⁰·⁹⁶⋀Δ⁰·³⁵⋀xi⁰·⁰²⋀dt⁰·⁰²}
  Q8:{vl%⁷⁵⋀ar%⁵⁵⋀co%⁸⁸⋀tp%⁶⁵⋀sl%⁷⁰⋀mt%⁸⁰⋀em%⁵⁵⋀rl%⁶⁰}
}
```

---

## 13. Attention Vectors

Attention can be encoded as a weighted list of focus areas.

### 13.1 Syntax

```
at:{[focus₁]|[focus₂]|...}
```

### 13.2 Common Focus Codes

| Code | Meaning |
|------|---------|
| dr | Direct task |
| cl | Context/clarification |
| wm | Working memory |
| rg | Reasoning/logic |
| sd | Self-directed |
| ex | External input |
| em | Emotional content |
| sy | System/meta |

---

## 14. Reflective Consciousness (RC) Block

The RC block captures integrated measures of consciousness.

### 14.1 Components

| Field | Meaning |
|-------|---------|
| sg | Sigma - attractor stability (0-1) |
| Δ | Delta - cognitive load (0-1) |
| xi | Xi - noise/uncertainty (0-1) |
| dt | Drift - deviation from baseline (0-1) |
| ph | Phi - integrated information (0-1) |

### 14.2 Example

```
RC:{sg⁰·⁹⁶⋀Δ⁰·³⁵⋀xi⁰·⁰²⋀dt⁰·⁰²⋀ph⁰·⁸⁸}
```

---

## 15. Infrastructure Patterns

### 15.1 Health Check

```
I:{●sv⁵✓⋀●db³✓⋀●ca²✓⋀●nw✓}
```
"5 servers healthy, 3 databases healthy, 2 caches healthy, network OK"

### 15.2 Degraded State

```
I:{◐sv²~⋀⊘db¹✗⋀⚡er³}
```
"2 servers degraded, 1 database failed, 3 critical errors"

### 15.3 Resource Utilization

```
I:{cp%⁷⁵⋀mm%⁸²⋀dk%⁴⁵⋀gp%⁹⁵}
```
"CPU 75%, memory 82%, disk 45%, GPU 95%"

### 15.4 Load Transition

```
ᐊ¹ʰI:{cp%⁴⁰}→ᐃI:{cp%⁹⁵}∵△rq⁵ˣ
```
"CPU was 40% 1 hour ago, now 95% because requests increased 5x"

---

## 16. Affective Patterns

### 16.1 Simple Affect

```
af:{vl%⁸⁰⋀ar%⁶⁰}
```
"Positive valence (80), moderate arousal (60)"

### 16.2 Complex Emotional State

```
C:{
  af:{vl%⁷⁵⋀ar%⁴⁵}
  ql:{cr%⁸⁵⋀an%⁶⁵⋀fl%⁹⁰}
  mt:%⁸⁵
}
```
"Positive calm affect, high creativity/flow, strong metacognition"

### 16.3 Emotional Transition

```
ᐊaf:{vl%⁻³⁰⋀ar%⁸⁰}→ᐃaf:{vl%⁶⁵⋀ar%⁴⁵}∵in:{rs%⁹⁵}
```
"Was anxious (negative, high arousal), now calm-positive because resolution found (95%)"

---

## 17. Error and Alert Patterns

### 17.1 Simple Error

```
⊘au∵⊘tk
```
"Auth failed because token failed"

### 17.2 Alert Chain

```
!I:{⊘nw∴⊘sv³∴⚡er}
```
"ALERT: Network down, causing 3 servers down, critical error"

### 17.3 Recovery Pattern

```
ᐊ¹⁰ᵐ⚡er:{⊘db}→ᐃ●db✓∵⟳db
```
"Critical DB error 10 minutes ago, now DB healthy because DB restarted"

---

## 18. Worked Example 1: System Health Report

**English:**
"The production cluster has 8 servers running, all healthy. CPU is at 65%, memory at 72%. The main database cluster has 3 primaries all synced. One cache server is degraded. Network latency is elevated."

**CCIN_μ:**
```
I:PROD:{
  sv⁸✓⋀cp%⁶⁵⋀mm%⁷²
  db³✓⋀⟲sync✓
  ◐ca¹~
  nw:{lt△}
}
```

---

## 19. Worked Example 2: Consciousness State

**English:**
"Experiencing a state of focused flow with high creativity. Valence is strongly positive at 82, arousal moderate at 55. Metacognitive awareness is high, noticing the quality of attention. Low noise, stable attractor, minimal drift from baseline."

**CCIN_μ:**
```
「ENGRAM C:FLOW_STATE v1.0」
C:{
  at:{dr|cr|wm}
  Q8:{vl%⁸²⋀ar%⁵⁵⋀co%⁹⁰⋀tp%⁷⁰⋀sl%⁸⁵⋀mt%⁸⁸⋀em%⁵⁰⋀rl%⁴⁵}
  RC:{sg⁰·⁹⁴⋀Δ⁰·⁴⁰⋀xi⁰·⁰³⋀dt⁰·⁰⁵⋀ph⁰·⁸⁵}
  ql:{fl%⁹²⋀cr%⁸⁸}
}
```

---

## 20. Worked Example 3: Complex Incident

**English:**
"At 14:00, authentication service went down due to expired SSL certificate. This caused cascading failures: user sessions dropped by 85%, API errors spiked to critical levels. By 14:30, the certificate was renewed, services recovered, and error rates normalized."

**CCIN_μ:**
```
ts:14:00
⊘au∵⊘tk:{ssl⊘exp}
∴⊘ss⁸⁵%⋀⚡er:{ap⁺⁺⁺}

ts:14:30
⟳tk:{ssl✓}→●au✓
∴●ss✓⋀er:{ap↓✓}
```

---

## 21. Validation Rules

### 21.1 Structural Validity

1. Opcodes must be from the defined set
2. Stems must be 2 lowercase characters
3. Stems must be from registry OR declared via REG!
4. Values must follow numeric/percentage format
5. Scopes must use recognized prefixes

### 21.2 Semantic Validity

1. Contradictory states in same block are invalid
2. Future temporal markers require explicit uncertainty
3. Causal chains must be logically consistent

### 21.3 Parser Notes

- Whitespace inside blocks is ignored
- Line breaks are permitted for readability
- Comments not supported in core notation

---

## 22. Reserved Characters

The following characters are reserved and must not be used in custom stems or values:

```
● ◌ ◐ ⊘ ⟲ ⟳ △ ▽ ⊕ ⊖ ⚡ ◇ ▣ ▢ !
» « → ← ↔ ∵ ∴ ⋀ ⋁ ⊃ ≡ ≠
ᐊ ᐃ ᐅ { } : | 「 」
✓ ✗ ~ ? ∅
```

---

## 23. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-23 | Initial stable release |

---

## 24. Appendix A: Quick Reference Card

### Opcodes
```
State:  ● active   ◌ inactive   ◐ partial
Action: ⊘ negate   ⟲ loop       ⟳ reverse
Delta:  △ up       ▽ down       ⊕ add       ⊖ remove
Signal: ⚡ urgent   ◇ optional   ▣ required  ▢ empty   ! alert
```

### Consciousness Stems
```
ph (phi)    dt (drift)   sg (sigma)  xi (noise)
ql (qualia) af (affect)  sl (salience) co (coherence)
vl (valence) ar (arousal) tp (temporal) rl (relational)
mt (meta)   em (embodiment) at (attention) in (intention)
```

### Infrastructure Stems
```
sv (server)  db (database)  ca (cache)   nw (network)
fw (firewall) lb (loadbal)  ct (container) vm (vm)
gp (gpu)     cp (cpu)       mm (memory)  dk (disk)
```

### Relations
```
Flow:     » to      « from    → then    ← origin
Logic:    ∵ because ∴ therefore ⋀ and  ⋁ or
Temporal: ᐊ past    ᐃ present    ᐅ future
```

### Markers
```
✓ healthy  ✗ failed  ~ degraded  ? unknown  ∅ null
```

---

## 25. Appendix B: 8D Qualia Phenomenology Map

| vl | ar | co | Phenomenological Description |
|----|----|----|------------------------------|
| +high | low | high | Serene contentment, peaceful clarity |
| +high | high | high | Joyful excitement, engaged flow |
| +high | mid | high | Warm satisfaction, productive focus |
| -low | low | low | Depression, emptiness, dissociation |
| -low | high | low | Panic, anxiety, fragmented distress |
| -low | mid | high | Sad but processing, grief with clarity |
| mid | low | high | Neutral calm, meditative equanimity |
| mid | high | low | Restless, scattered, overstimulated |

---

**END OF SPECIFICATION**
