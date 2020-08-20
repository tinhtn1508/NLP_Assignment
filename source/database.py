ruleTable = {
    "ROOT": { "den": "root", "di": "root", "xuat_phat": "root"},
    "xuat_phat": {"nao": "which-query", "tu": "from-to"},
    "tu": {"thanh_pho": "to_loc", "<VAR-LOC>": "<var>name"},
    "den": { "nao": "which-query", "thanh_pho": "to-loc", "luc": "arrive-time", "<VAR-LOC>": "<var>name"},
    "di": {"nao": "which-query", "den": "to-city", "tu": "from-to", "thoi_gian" : "time-query", "xe_bus": "lsubj"},
    "nao": { "xe_bus": "lsubj", "xe": "lsubj", "nhung": "plural"},
    "xe_bus": {"<VAR-BUS>": "<var>name"},
    "thanh_pho": { "<VAR-LOC>": "<var>name" },
    "luc": { "<VAR-TIM>": "<var>time-hour" },
}
