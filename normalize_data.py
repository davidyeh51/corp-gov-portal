# -*- coding: utf-8 -*-
"""
統一正規化 LECTURES_PART1 (00~19) 與 LECTURES_PART2 (20~39) 的資料結構
確保 build_pptx.py 與 build_site.py 在所有 40 講皆能 100% 完整渲染所有欄位。
"""
import copy
from data_part1 import LECTURES_PART1
from data_part2 import LECTURES_PART2


def normalize_lecture(raw_lec):
    lec = copy.deepcopy(raw_lec)
    ltype = lec.get("type", "parallel")

    # 1. Normalize one_to_one
    if ltype == "one_to_one":
        callout_pts = lec.get("callout_points", [])
        bars = lec.get("bars", [])
        for i, b in enumerate(bars):
            if not b.get("desc"):
                if i < len(callout_pts):
                    b["desc"] = callout_pts[i]
                elif callout_pts:
                    b["desc"] = callout_pts[-1]
                else:
                    b["desc"] = f"{b.get('label', '')}：{b.get('display', '')}"

    # 2. Normalize parallel
    elif ltype == "parallel":
        cards = lec.get("cards", [])
        for i, c in enumerate(cards):
            if not c.get("tag"):
                c["tag"] = f"核心支柱 {i+1}"
            if not c.get("desc") and c.get("points"):
                c["desc"] = "；".join([p.replace("\n", " ") for p in c["points"]])
            if "highlight" not in c:
                c["highlight"] = (i == 0)

    # 3. Normalize combined
    elif ltype == "combined":
        pillars = lec.get("pillars", [])
        for i, p in enumerate(pillars):
            if not p.get("points") and p.get("facts"):
                p["points"] = [f.replace("\n", " ") for f in p["facts"]]
            if "highlight" not in p:
                p["highlight"] = (i == 0)
        if not lec.get("synthesis_banner"):
            lec["synthesis_banner"] = lec.get("top_claim", lec.get("conclusion_title", ""))

    # 4. Normalize chain
    elif ltype == "chain":
        steps = lec.get("steps", [])
        for i, s in enumerate(steps):
            if not s.get("phase"):
                stg = s.get("stage", f"階段 {i+1}")
                if "：" in stg:
                    p_part, t_part = stg.split("：", 1)
                    s["phase"] = p_part.replace("③", "").strip()
                    if not s.get("title"):
                        s["title"] = t_part.strip()
                else:
                    s["phase"] = f"STEP {i+1}"
                    if not s.get("title"):
                        s["title"] = stg
            if not s.get("desc") and s.get("items"):
                s["desc"] = " ｜ ".join(s["items"])
            if "highlight" not in s:
                s["highlight"] = (i == len(steps) - 1)

    # 5. Normalize mckinsey_flow
    elif ltype == "mckinsey_flow":
        rows = lec.get("rows", [])
        for r in rows:
            if not r.get("label") and r.get("dimension"):
                r["label"] = r["dimension"].replace("\n", " ")

    # 6. Normalize opposition
    elif ltype == "opposition":
        if not lec.get("left_title") and lec.get("side_a_title"):
            lec["left_title"] = lec["side_a_title"]
        if not lec.get("right_title") and lec.get("side_b_title"):
            lec["right_title"] = lec["side_b_title"]
        dims = lec.get("dimensions", [])
        for d in dims:
            if not d.get("dim") and d.get("name"):
                d["dim"] = d["name"]
            if not d.get("left") and d.get("side_a"):
                d["left"] = d["side_a"]
            if not d.get("right") and d.get("side_b"):
                d["right"] = d["side_b"]

    # 7. Normalize bcg_matrix
    elif ltype == "bcg_matrix":
        if not lec.get("y_axis") and lec.get("y_axis_label"):
            lec["y_axis"] = "資金與抗風險需求（低 ➔ 高）"
        if not lec.get("x_axis") and lec.get("x_axis_label"):
            lec["x_axis"] = "治理約束與控制權稀釋容忍度（低 ➔ 高）"
        quads = lec.get("quadrants", [])
        default_pos = ["左上象限 (高Y / 低X)", "右上象限 (高Y / 高X)", "左下象限 (低Y / 低X)", "右下象限 (低Y / 高X)"]
        for i, q in enumerate(quads[:4]):
            if not q.get("pos"):
                q["pos"] = default_pos[i]

    # 8. Normalize beginner.key_terms -> list of {"term": ..., "def": ...}
    beg = lec.get("beginner", {})
    norm_terms = []
    for t in beg.get("key_terms", []):
        if isinstance(t, dict):
            norm_terms.append({"term": str(t.get("term", "")), "def": str(t.get("def", ""))})
        else:
            s = str(t)
            if "：" in s:
                k, v = s.split("：", 1)
                norm_terms.append({"term": k.strip(), "def": v.strip()})
            else:
                norm_terms.append({"term": s.strip(), "def": ""})
    beg["key_terms"] = norm_terms

    # 9. Normalize advanced.causal_link -> str & advanced.checklist -> list of str
    adv = lec.get("advanced", {})
    cl = adv.get("causal_link", "")
    if isinstance(cl, dict):
        parts = []
        if cl.get("prev"):
            parts.append(f"【承上】{cl['prev']}")
        if cl.get("current"):
            parts.append(f"【本講核心】{cl['current']}")
        if cl.get("next"):
            parts.append(f"【啟下】{cl['next']}")
        adv["causal_link"] = " ➔ ".join(parts)
    else:
        adv["causal_link"] = str(cl)

    norm_chk = []
    for item in adv.get("checklist", []):
        if isinstance(item, dict):
            norm_chk.append(f"**{item.get('check', '')}**：{item.get('action', '')}（預期效益：{item.get('impact', '')}）")
        else:
            norm_chk.append(str(item))
    adv["checklist"] = norm_chk

    return lec


def get_all_normalized_lectures():
    raw_all = LECTURES_PART1 + LECTURES_PART2
    return [normalize_lecture(x) for x in raw_all]
