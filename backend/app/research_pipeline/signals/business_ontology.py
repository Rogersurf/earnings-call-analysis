# ============================================================
# FILE:
# backend/app/research_pipeline/signals/business_ontology.py
# ============================================================

SIGNAL_DEFINITIONS = {

    "pc_demand": {
        "keywords": [
            "pc",
            "pcs",
            "notebook",
            "desktop",
            "laptop",
            "commercial pc",
            "consumer pc",
            "ai pc",
        ],
        "context_terms": [
            "commercial",
            "consumer",
            "windows",
            "refresh",
            "devices",
        ],
    },

    "server_cpu_demand": {
        "keywords": [
            "server",
            "servers",
            "cpu",
            "cpus",
            "xeon",
            "processor",
            "processors",
            "compute",
            "data center",
            "datacenter",
        ],
        "context_terms": [
            "enterprise",
            "cloud",
            "infrastructure",
            "ai",
            "gpu",
        ],
    },

    "cloud_capacity": {
        "keywords": [
            "cloud",
            "data center",
            "datacenter",
            "infrastructure",
            "capacity",
            "buildout",
            "build-out",
            "capex",
            "capital expenditure",
        ],
        "context_terms": [
            "ai",
            "gpu",
            "compute",
            "server",
            "cluster",
        ],
    },

    "foundry_manufacturing": {
        "keywords": [
            "foundry",
            "fab",
            "wafer",
            "advanced packaging",
            "process node",
            "18a",
            "20a",
            "semiconductor manufacturing",
        ],
        "context_terms": [
            "manufacturing",
            "yield",
            "capacity",
            "chip",
        ],
    },

    "supply_pressure": {
        "keywords": [
            "shortage",
            "constraint",
            "constraints",
            "inventory",
            "component",
            "supply",
            "allocation",
        ],
        "context_terms": [
            "semiconductor",
            "chip",
            "server",
            "cpu",
            "memory",
        ],
    },

    "margin_pressure": {
        "keywords": [
            "margin",
            "gross margin",
            "pricing",
            "cost pressure",
            "cost",
            "price",
        ],
        "context_terms": [
            "semiconductor",
            "server",
            "cloud",
            "cpu",
            "infrastructure",
        ],
    },
}


BUSINESS_TARGET_MAP = {

    "pc_demand": "Intel_CCG",

    "server_cpu_demand": "Intel_DCAI",

    "cloud_capacity": "Intel_DCAI",

    "foundry_manufacturing": "Intel_Foundry",

    "supply_pressure": "Intel_CCG_or_DCAI",

    "margin_pressure": "Intel_Margin",
}