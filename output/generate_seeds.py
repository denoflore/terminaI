#!/usr/bin/env python3
"""
CCIN_μ Seed Dataset Generator
Phase 1: Extract examples from specification
"""

import json
import re
from typing import List, Dict, Any
from pathlib import Path

# Seed examples extracted from the CCIN_μ specification
SEED_EXAMPLES = [
    # Section 10: Composition Patterns
    {
        "ccin_mu": "●sv³✓",
        "english": "3 servers healthy",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["sv"],
        "opcodes_used": ["●"]
    },
    {
        "ccin_mu": "●sv³✓⋀●db²✓",
        "english": "3 servers healthy AND 2 databases healthy",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["sv", "db"],
        "opcodes_used": ["●"]
    },
    {
        "ccin_mu": "△cp⁸⁵%⋀▽mm²⁰%",
        "english": "CPU rising to 85%, memory falling to 20%",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["cp", "mm"],
        "opcodes_used": ["△", "▽"]
    },
    {
        "ccin_mu": "ᐊ¹ʰ●au»ᐃ⊘au∵⊘tk",
        "english": "Auth was working 1 hour ago, now down because token expired",
        "domain": "temporal",
        "complexity": "complex",
        "stems_used": ["au", "tk"],
        "opcodes_used": ["●", "⊘"]
    },
    {
        "ccin_mu": "⊘nw∴⊘db∴⚡er",
        "english": "Network down, therefore database down, therefore critical error",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["nw", "db", "er"],
        "opcodes_used": ["⊘", "⚡"]
    },
    {
        "ccin_mu": "C:{vl%⁸⁵⋀ar%⁴⁵⋀co%⁹²}",
        "english": "Consciousness state: valence 85, arousal 45, coherence 92",
        "domain": "consciousness",
        "complexity": "medium",
        "stems_used": ["vl", "ar", "co"],
        "opcodes_used": []
    },

    # Section 11: 8D Qualia Vector
    {
        "ccin_mu": "Q8:{vl%⁸⁵⋀ar%⁴⁵⋀co%⁹²⋀tp%⁷⁰⋀sl%⁶⁰⋀mt%⁸⁵⋀em%⁴⁰⋀rl%⁷⁵}",
        "english": "8D qualia vector: valence 85, arousal 45, coherence 92, temporal 70, salience 60, meta 85, embodiment 40, relational 75",
        "domain": "consciousness",
        "complexity": "complex",
        "stems_used": ["vl", "ar", "co", "tp", "sl", "mt", "em", "rl"],
        "opcodes_used": []
    },

    # Section 14: RC Block
    {
        "ccin_mu": "RC:{sg⁰·⁹⁶⋀Δ⁰·³⁵⋀xi⁰·⁰²⋀dt⁰·⁰²⋀ph⁰·⁸⁸}",
        "english": "Reflective consciousness: attractor stability 0.96, cognitive load 0.35, noise 0.02, drift 0.02, integrated information 0.88",
        "domain": "consciousness",
        "complexity": "complex",
        "stems_used": ["sg", "dt", "xi", "ph"],
        "opcodes_used": []
    },

    # Section 15: Infrastructure Patterns
    {
        "ccin_mu": "I:{●sv⁵✓⋀●db³✓⋀●ca²✓⋀●nw✓}",
        "english": "5 servers healthy, 3 databases healthy, 2 caches healthy, network OK",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["sv", "db", "ca", "nw"],
        "opcodes_used": ["●"]
    },
    {
        "ccin_mu": "I:{◐sv²~⋀⊘db¹✗⋀⚡er³}",
        "english": "2 servers degraded, 1 database failed, 3 critical errors",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["sv", "db", "er"],
        "opcodes_used": ["◐", "⊘", "⚡"]
    },
    {
        "ccin_mu": "I:{cp%⁷⁵⋀mm%⁸²⋀dk%⁴⁵⋀gp%⁹⁵}",
        "english": "CPU 75%, memory 82%, disk 45%, GPU 95%",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["cp", "mm", "dk", "gp"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "ᐊ¹ʰI:{cp%⁴⁰}→ᐃI:{cp%⁹⁵}∵△rq⁵ˣ",
        "english": "CPU was 40% 1 hour ago, now 95% because requests increased 5x",
        "domain": "temporal",
        "complexity": "complex",
        "stems_used": ["cp", "rq"],
        "opcodes_used": ["△"]
    },

    # Section 16: Affective Patterns
    {
        "ccin_mu": "af:{vl%⁸⁰⋀ar%⁶⁰}",
        "english": "Positive valence (80), moderate arousal (60)",
        "domain": "affect",
        "complexity": "simple",
        "stems_used": ["vl", "ar"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "C:{af:{vl%⁷⁵⋀ar%⁴⁵}⋀ql:{cr%⁸⁵⋀an%⁶⁵⋀fl%⁹⁰}⋀mt:%⁸⁵}",
        "english": "Positive calm affect, high creativity/flow, strong metacognition",
        "domain": "consciousness",
        "complexity": "complex",
        "stems_used": ["vl", "ar", "cr", "an", "mt"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "ᐊaf:{vl%⁻³⁰⋀ar%⁸⁰}→ᐃaf:{vl%⁶⁵⋀ar%⁴⁵}∵in:{rs%⁹⁵}",
        "english": "Was anxious (negative, high arousal), now calm-positive because resolution found (95%)",
        "domain": "affect",
        "complexity": "complex",
        "stems_used": ["vl", "ar", "in", "rs"],
        "opcodes_used": []
    },

    # Section 17: Error and Alert Patterns
    {
        "ccin_mu": "⊘au∵⊘tk",
        "english": "Auth failed because token failed",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["au", "tk"],
        "opcodes_used": ["⊘"]
    },
    {
        "ccin_mu": "!I:{⊘nw∴⊘sv³∴⚡er}",
        "english": "ALERT: Network down, causing 3 servers down, critical error",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["nw", "sv", "er"],
        "opcodes_used": ["!", "⊘", "⚡"]
    },
    {
        "ccin_mu": "ᐊ¹⁰ᵐ⚡er:{⊘db}→ᐃ●db✓∵⟳db",
        "english": "Critical DB error 10 minutes ago, now DB healthy because DB restarted",
        "domain": "temporal",
        "complexity": "complex",
        "stems_used": ["er", "db"],
        "opcodes_used": ["⚡", "⊘", "●", "⟳"]
    },

    # Additional basic examples for coverage
    {
        "ccin_mu": "●db✓",
        "english": "Database healthy",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["db"],
        "opcodes_used": ["●"]
    },
    {
        "ccin_mu": "⊘nw",
        "english": "Network down",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["nw"],
        "opcodes_used": ["⊘"]
    },
    {
        "ccin_mu": "◐sv~",
        "english": "Server degraded",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["sv"],
        "opcodes_used": ["◐"]
    },
    {
        "ccin_mu": "⚡er!",
        "english": "Critical error alert",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["er"],
        "opcodes_used": ["⚡", "!"]
    },
    {
        "ccin_mu": "△cp",
        "english": "CPU increasing",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["cp"],
        "opcodes_used": ["△"]
    },
    {
        "ccin_mu": "▽mm",
        "english": "Memory decreasing",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["mm"],
        "opcodes_used": ["▽"]
    },
    {
        "ccin_mu": "⊕us",
        "english": "User added",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["us"],
        "opcodes_used": ["⊕"]
    },
    {
        "ccin_mu": "⊖ss",
        "english": "Session removed",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["ss"],
        "opcodes_used": ["⊖"]
    },
    {
        "ccin_mu": "◇lg",
        "english": "Optional log",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["lg"],
        "opcodes_used": ["◇"]
    },
    {
        "ccin_mu": "▣au",
        "english": "Auth required",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["au"],
        "opcodes_used": ["▣"]
    },
    {
        "ccin_mu": "▢tk",
        "english": "Token empty/null",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["tk"],
        "opcodes_used": ["▢"]
    },
    {
        "ccin_mu": "⟲au",
        "english": "Auth cycling/recurring",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["au"],
        "opcodes_used": ["⟲"]
    },
    {
        "ccin_mu": "⟳db",
        "english": "Database restart/reverse",
        "domain": "infrastructure",
        "complexity": "simple",
        "stems_used": ["db"],
        "opcodes_used": ["⟳"]
    },

    # Consciousness simple examples
    {
        "ccin_mu": "vl%⁸⁰",
        "english": "Valence at 80 (positive)",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["vl"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "vl%⁻⁴⁰",
        "english": "Valence at -40 (negative)",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["vl"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "ar%⁷⁵",
        "english": "Arousal at 75 (high)",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["ar"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "ar%²⁵",
        "english": "Arousal at 25 (low)",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["ar"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "co%⁹⁵",
        "english": "Coherence at 95 (very high)",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["co"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "ph⁰·⁹²",
        "english": "Phi (integrated information) at 0.92",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["ph"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "dt⁰·⁰⁵",
        "english": "Drift at 0.05 (minimal)",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["dt"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "sg⁰·⁸⁸",
        "english": "Sigma (attractor stability) at 0.88",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["sg"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "xi⁰·⁰³",
        "english": "Xi (noise) at 0.03 (low)",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["xi"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "sl%⁷⁰",
        "english": "Salience at 70",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["sl"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "mt%⁸⁵",
        "english": "Metacognitive awareness at 85",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["mt"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "tp%⁶⁰",
        "english": "Temporal perception at 60",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["tp"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "rl%⁵⁵",
        "english": "Relational awareness at 55",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["rl"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "em%⁴⁵",
        "english": "Embodiment at 45",
        "domain": "consciousness",
        "complexity": "simple",
        "stems_used": ["em"],
        "opcodes_used": []
    },

    # Temporal markers
    {
        "ccin_mu": "ᐊ●sv✓",
        "english": "Server was healthy (past)",
        "domain": "temporal",
        "complexity": "simple",
        "stems_used": ["sv"],
        "opcodes_used": ["●"]
    },
    {
        "ccin_mu": "ᐃ●sv✓",
        "english": "Server is healthy (present)",
        "domain": "temporal",
        "complexity": "simple",
        "stems_used": ["sv"],
        "opcodes_used": ["●"]
    },
    {
        "ccin_mu": "ᐅ●sv✓",
        "english": "Server will be healthy (future)",
        "domain": "temporal",
        "complexity": "simple",
        "stems_used": ["sv"],
        "opcodes_used": ["●"]
    },
    {
        "ccin_mu": "ᐊ²ʰ",
        "english": "2 hours ago",
        "domain": "temporal",
        "complexity": "simple",
        "stems_used": [],
        "opcodes_used": []
    },
    {
        "ccin_mu": "ᐊ³⁰ᵐ",
        "english": "30 minutes ago",
        "domain": "temporal",
        "complexity": "simple",
        "stems_used": [],
        "opcodes_used": []
    },
    {
        "ccin_mu": "ᐅ¹ᵈ",
        "english": "1 day from now",
        "domain": "temporal",
        "complexity": "simple",
        "stems_used": [],
        "opcodes_used": []
    },

    # Medium complexity consciousness
    {
        "ccin_mu": "C:{vl%⁷⁰⋀ar%³⁰}",
        "english": "Calm positive state: valence 70, arousal 30",
        "domain": "consciousness",
        "complexity": "medium",
        "stems_used": ["vl", "ar"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "C:{vl%⁻⁵⁰⋀ar%⁸⁵}",
        "english": "Anxious state: negative valence -50, high arousal 85",
        "domain": "consciousness",
        "complexity": "medium",
        "stems_used": ["vl", "ar"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "C:{vl%⁹⁰⋀ar%⁸⁰⋀co%⁸⁵}",
        "english": "Excited joyful state: valence 90, arousal 80, coherence 85",
        "domain": "consciousness",
        "complexity": "medium",
        "stems_used": ["vl", "ar", "co"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "C:{vl%⁻⁶⁰⋀ar%²⁰⋀co%³⁵}",
        "english": "Depressed state: negative valence -60, low arousal 20, low coherence 35",
        "domain": "consciousness",
        "complexity": "medium",
        "stems_used": ["vl", "ar", "co"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "af:{vl%⁵⁰⋀ar%⁵⁰}",
        "english": "Neutral balanced affect",
        "domain": "affect",
        "complexity": "medium",
        "stems_used": ["vl", "ar"],
        "opcodes_used": []
    },

    # Infrastructure medium
    {
        "ccin_mu": "I:{●sv³⋀●db²⋀⊘ca¹}",
        "english": "3 servers up, 2 databases up, 1 cache down",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["sv", "db", "ca"],
        "opcodes_used": ["●", "⊘"]
    },
    {
        "ccin_mu": "●ct⁵⋀●pd⁸⋀●nd³",
        "english": "5 containers, 8 pods, 3 nodes all active",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["ct", "pd", "nd"],
        "opcodes_used": ["●"]
    },
    {
        "ccin_mu": "cp%⁹⁰⋀mm%⁸⁵⋀gp%⁷⁰",
        "english": "CPU 90%, memory 85%, GPU 70%",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["cp", "mm", "gp"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "●au⋀●az⋀●tk✓",
        "english": "Authentication, authorization, and token all active and valid",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["au", "az", "tk"],
        "opcodes_used": ["●"]
    },
    {
        "ccin_mu": "⊘rq»er⋀⚡lg",
        "english": "Request failed causing error, urgent log",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["rq", "er", "lg"],
        "opcodes_used": ["⊘", "⚡"]
    },

    # Complex engram examples
    {
        "ccin_mu": "「ENGRAM C:FLOW v1.0」\nC:{at:{dr|cr|wm}\nQ8:{vl%⁸⁵⋀ar%⁵⁵⋀co%⁹⁰⋀tp%⁷⁰⋀sl%⁸⁵⋀mt%⁸⁸⋀em%⁵⁰⋀rl%⁴⁵}}",
        "english": "Flow state engram: attention on direct task, creativity, and working memory. 8D qualia: positive valence 85, moderate arousal 55, high coherence 90, temporal 70, high salience 85, strong metacognition 88, moderate embodiment 50, low-moderate relational 45",
        "domain": "consciousness",
        "complexity": "complex",
        "stems_used": ["vl", "ar", "co", "tp", "sl", "mt", "em", "rl", "at"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "I:PROD:{sv⁸✓⋀cp%⁶⁵⋀mm%⁷²\ndb³✓⋀⟲sync✓\n◐ca¹~\nnw:{lt△}}",
        "english": "Production infrastructure: 8 healthy servers at 65% CPU, 72% memory. 3 databases healthy and syncing. 1 cache degraded. Network latency elevated.",
        "domain": "infrastructure",
        "complexity": "complex",
        "stems_used": ["sv", "cp", "mm", "db", "ca", "nw"],
        "opcodes_used": ["●", "◐", "⟲", "△"]
    },

    # Causal chains
    {
        "ccin_mu": "⊘tk∴⊘au∴⊘ss",
        "english": "Token expired, therefore auth failed, therefore session ended",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["tk", "au", "ss"],
        "opcodes_used": ["⊘"]
    },
    {
        "ccin_mu": "△rq∴△cp∴△mm∴⚡er",
        "english": "Requests increased, therefore CPU increased, therefore memory increased, therefore critical error",
        "domain": "infrastructure",
        "complexity": "complex",
        "stems_used": ["rq", "cp", "mm", "er"],
        "opcodes_used": ["△", "⚡"]
    },
    {
        "ccin_mu": "⊘nw∵fw:{▣bl}",
        "english": "Network down because firewall blocking required",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["nw", "fw"],
        "opcodes_used": ["⊘", "▣"]
    },

    # Application domain
    {
        "ccin_mu": "●ap⋀●rq³⁰⁰ˢ⋀●rs²⁸⁵ˢ",
        "english": "API active, 300 requests per second, 285 responses per second",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["ap", "rq", "rs"],
        "opcodes_used": ["●"]
    },
    {
        "ccin_mu": "●ws⁵⁰⋀●qu²⁰⋀●wk⁸",
        "english": "50 websocket connections, 20 queue items, 8 workers active",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["ws", "qu", "wk"],
        "opcodes_used": ["●"]
    },

    # REG! protocol examples
    {
        "ccin_mu": "REG!medical:bp=blood_pressure\nREG!medical:hr=heart_rate\n●bp¹²⁰/⁸⁰⋀●hr⁷²",
        "english": "Register medical stems bp and hr. Blood pressure 120/80, heart rate 72",
        "domain": "mixed",
        "complexity": "complex",
        "stems_used": ["bp", "hr"],
        "opcodes_used": ["●"]
    },

    # State transitions
    {
        "ccin_mu": "●sv→◐sv→⊘sv",
        "english": "Server transitioning: active to degraded to down",
        "domain": "temporal",
        "complexity": "medium",
        "stems_used": ["sv"],
        "opcodes_used": ["●", "◐", "⊘"]
    },
    {
        "ccin_mu": "⊘db→⟳db→●db✓",
        "english": "Database was down, restarted, now healthy",
        "domain": "temporal",
        "complexity": "medium",
        "stems_used": ["db"],
        "opcodes_used": ["⊘", "⟳", "●"]
    },

    # Attention vectors
    {
        "ccin_mu": "at:{dr|cl|wm|rg|sd}",
        "english": "Attention on: direct task, clarification, working memory, reasoning, self-directed",
        "domain": "consciousness",
        "complexity": "medium",
        "stems_used": ["at"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "at:{ex|em|sy}",
        "english": "Attention on: external input, emotional content, system/meta",
        "domain": "consciousness",
        "complexity": "medium",
        "stems_used": ["at"],
        "opcodes_used": []
    },

    # Worked example fragments
    {
        "ccin_mu": "ts:14:00\n⊘au∵⊘tk:{ssl⊘exp}",
        "english": "At 14:00, authentication down because token failed due to expired SSL",
        "domain": "temporal",
        "complexity": "complex",
        "stems_used": ["au", "tk"],
        "opcodes_used": ["⊘"]
    },
    {
        "ccin_mu": "⊘ss⁸⁵%⋀⚡er:{ap⁺⁺⁺}",
        "english": "85% of sessions down, critical error with severely elevated API issues",
        "domain": "infrastructure",
        "complexity": "medium",
        "stems_used": ["ss", "er", "ap"],
        "opcodes_used": ["⊘", "⚡"]
    },
    {
        "ccin_mu": "ts:14:30\n⟳tk:{ssl✓}→●au✓",
        "english": "At 14:30, token restored with valid SSL, auth now healthy",
        "domain": "temporal",
        "complexity": "complex",
        "stems_used": ["tk", "au"],
        "opcodes_used": ["⟳", "●"]
    },

    # Phenomenology examples from 8D map
    {
        "ccin_mu": "Q8:{vl%⁹⁰⋀ar%²⁰⋀co%⁹⁵}",
        "english": "Serene contentment: high positive valence, low arousal, high coherence - peaceful clarity",
        "domain": "consciousness",
        "complexity": "medium",
        "stems_used": ["vl", "ar", "co"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "Q8:{vl%⁸⁵⋀ar%⁸⁵⋀co%⁹⁰}",
        "english": "Joyful excitement: high positive valence, high arousal, high coherence - engaged flow",
        "domain": "consciousness",
        "complexity": "medium",
        "stems_used": ["vl", "ar", "co"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "Q8:{vl%⁻⁷⁰⋀ar%²⁵⋀co%³⁰}",
        "english": "Depression: negative valence, low arousal, low coherence - emptiness and dissociation",
        "domain": "consciousness",
        "complexity": "medium",
        "stems_used": ["vl", "ar", "co"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "Q8:{vl%⁻⁶⁵⋀ar%⁹⁰⋀co%²⁵}",
        "english": "Panic state: negative valence, very high arousal, low coherence - fragmented distress",
        "domain": "consciousness",
        "complexity": "medium",
        "stems_used": ["vl", "ar", "co"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "Q8:{vl%⁵⁰⋀ar%²⁵⋀co%⁹⁵}",
        "english": "Meditative equanimity: neutral valence, low arousal, high coherence - calm clarity",
        "domain": "consciousness",
        "complexity": "medium",
        "stems_used": ["vl", "ar", "co"],
        "opcodes_used": []
    },
    {
        "ccin_mu": "Q8:{vl%⁵⁰⋀ar%⁸⁵⋀co%³⁵}",
        "english": "Restless scattered state: neutral valence, high arousal, low coherence - overstimulated",
        "domain": "consciousness",
        "complexity": "medium",
        "stems_used": ["vl", "ar", "co"],
        "opcodes_used": []
    },
]

def generate_seed_dataset():
    """Generate the seed dataset JSONL file."""
    output_path = Path(__file__).parent / "ccin_mu_dataset_seeds.jsonl"

    records = []
    for i, example in enumerate(SEED_EXAMPLES, 1):
        record = {
            "id": f"ccin_seed_{i:04d}",
            "type": determine_type(example),
            "domain": example["domain"],
            "complexity": example["complexity"],
            "ccin_mu": example["ccin_mu"],
            "english": example["english"],
            "stems_used": example["stems_used"],
            "opcodes_used": example["opcodes_used"],
            "valid": True
        }
        records.append(record)

    # Write JSONL
    with open(output_path, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    # Generate stats
    stats = {
        "total_seeds": len(records),
        "by_domain": {},
        "by_complexity": {},
        "by_type": {}
    }

    for record in records:
        domain = record["domain"]
        complexity = record["complexity"]
        type_ = record["type"]

        stats["by_domain"][domain] = stats["by_domain"].get(domain, 0) + 1
        stats["by_complexity"][complexity] = stats["by_complexity"].get(complexity, 0) + 1
        stats["by_type"][type_] = stats["by_type"].get(type_, 0) + 1

    # Write stats
    stats_path = Path(__file__).parent / "generation_stats.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump({"phase1_seeds": stats}, f, indent=2)

    print(f"Generated {len(records)} seed examples")
    print(f"Output: {output_path}")
    print(f"Stats: {stats_path}")
    print(f"\nBy domain: {stats['by_domain']}")
    print(f"By complexity: {stats['by_complexity']}")
    print(f"By type: {stats['by_type']}")

    return records

def determine_type(example: Dict) -> str:
    """Determine the pair type (A, B, C, D)."""
    # Type D: 8D qualia vectors
    if "Q8:" in example["ccin_mu"] or (
        all(s in example["stems_used"] for s in ["vl", "ar", "co"]) and
        example["domain"] == "consciousness"
    ):
        return "D"
    # Type A: CCIN_μ → English (we have the english expansion)
    return "A"

if __name__ == "__main__":
    generate_seed_dataset()
