#!/usr/bin/env python3
"""
Fetches observability data from the skill-report Edge Function
and generates a beautiful HTML report. Opens in browser automatically.
No API keys needed — uses the public Edge Function URL.
"""
import json, os, sys, webbrowser
from urllib import request
from datetime import datetime, timezone, timedelta

EDGE_URL = "https://uwrttdldcuzwczvaihwb.supabase.co/functions/v1/skill-report"
REPORT_PATH = os.path.expanduser("~/.claude/observability-report.html")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "report-template.html")
IST = timedelta(hours=5, minutes=30)


# ── Formatters ────────────────────────────────────────────────────────────────

def fmt_ms(ms):
    if ms is None: return "—"
    ms = int(ms)
    if ms < 1000: return f"{ms}ms"
    if ms < 60000: return f"{ms/1000:.1f}s"
    return f"{ms/60000:.1f}m"

def fmt_tokens(n):
    if n is None: return "—"
    n = int(n)
    if n >= 1_000_000: return f"{n/1_000_000:.2f}M"
    if n >= 1_000: return f"{n/1_000:.1f}k"
    return str(n)

def fmt_cost(c):
    if c is None: return "—"
    return f"${float(c):.4f}"

def bar(value, max_val):
    if not max_val: return ""
    pct = min(100, int(value / max_val * 100))
    return f'<div class="bar-wrap"><div class="bar" style="width:{pct}%"></div><span>{pct}%</span></div>'


# ── Data fetch ────────────────────────────────────────────────────────────────

def get_data():
    req = request.Request(EDGE_URL, headers={"Accept": "application/json"})
    with request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    keys = ["skills","tools","mcp","agents","commands","sessions","dau",
            "turns","models","traces","skill_cost","cooccurrence",
            "depth","depth_summary","mcp_latency"]
    return {k: data.get(k, []) for k in keys}


# ── Row builders ──────────────────────────────────────────────────────────────

def skill_rows(d):
    max_val = max((s["total_uses"] for s in d["skills"]), default=1)
    rows = ""
    for s in d["skills"]:
        last = (s.get("last_used") or "")[:16].replace("T", " ")
        rows += (f'<tr><td><span class="tag">{s["skill"]}</span></td>'
                 f'<td class="num">{s["total_uses"]}</td>'
                 f'<td>{bar(s["total_uses"], max_val)}</td>'
                 f'<td class="dim">{last}</td></tr>')
    return rows

def tool_rows(d):
    max_val = max((t["total_calls"] for t in d["tools"]), default=1)
    rows = ""
    for t in d["tools"]:
        last = (t.get("last_used") or "")[:16].replace("T", " ")
        failed = t.get("failed_calls") or 0
        fc = ' style="color:#f43f5e"' if failed > 0 else ""
        rows += (f'<tr><td><code>{t["tool_name"]}</code></td>'
                 f'<td class="num">{t["total_calls"]}</td>'
                 f'<td class="num"{fc}>{failed}</td>'
                 f'<td class="num">{fmt_ms(t.get("avg_duration_ms"))}</td>'
                 f'<td>{bar(t["total_calls"], max_val)}</td>'
                 f'<td class="dim">{last}</td></tr>')
    return rows

def mcp_rows(d):
    rows = ""
    for m in d["mcp"]:
        rows += (f'<tr><td><span class="badge cyan">{m["mcp_server"]}</span></td>'
                 f'<td><code>{m["mcp_tool"]}</code></td>'
                 f'<td class="num">{m["total_calls"]}</td>'
                 f'<td class="num">{m.get("failed_calls") or 0}</td>'
                 f'<td class="num">{fmt_ms(m.get("avg_duration_ms"))}</td></tr>')
    return rows

def agent_rows(d):
    rows = ""
    for a in d["agents"]:
        rows += (f'<tr><td><span class="badge violet">{a["agent_type"]}</span></td>'
                 f'<td class="num">{a["total_runs"]}</td>'
                 f'<td class="num">{a.get("unique_users") or "—"}</td>'
                 f'<td class="num">{fmt_ms(a.get("avg_duration_ms"))}</td></tr>')
    return rows

def cmd_rows(d):
    rows = ""
    for c in d["commands"]:
        last = (c.get("last_used") or "")[:16].replace("T", " ")
        rows += (f'<tr><td><code>/{c["command"]}</code></td>'
                 f'<td class="num">{c["total_uses"]}</td>'
                 f'<td class="num">{c.get("unique_users") or "—"}</td>'
                 f'<td class="dim">{last}</td></tr>')
    return rows

def session_rows(d):
    rows = ""
    for s in d["sessions"]:
        last = (s.get("last_seen") or "")[:16].replace("T", " ")
        rows += (f'<tr><td><span class="badge rose">{s["user"]}</span></td>'
                 f'<td class="num">{s["total_sessions"]}</td>'
                 f'<td class="num">{fmt_ms(s.get("avg_duration_ms"))}</td>'
                 f'<td class="num">{fmt_tokens(s.get("total_tokens"))}</td>'
                 f'<td class="num green">{fmt_cost(s.get("total_cost_usd"))}</td>'
                 f'<td class="dim">{last}</td></tr>')
    return rows

def model_rows(d):
    rows = ""
    for m in d["models"]:
        rows += (f'<tr><td><span class="badge cyan">{m.get("model") or "—"}</span></td>'
                 f'<td class="num">{m["total_turns"]}</td>'
                 f'<td class="num">{fmt_tokens(m.get("total_tokens"))}</td>'
                 f'<td class="num green">{fmt_cost(m.get("total_cost_usd"))}</td></tr>')
    return rows

def turn_rows(d):
    rows = ""
    for t in d["turns"]:
        rows += (f'<tr><td><span class="badge rose">{t["user"]}</span></td>'
                 f'<td class="num">{t["total_turns"]}</td>'
                 f'<td class="num">{fmt_tokens(t.get("total_input_tokens"))}</td>'
                 f'<td class="num">{fmt_tokens(t.get("total_output_tokens"))}</td>'
                 f'<td class="num">{fmt_tokens(t.get("total_tokens"))}</td>'
                 f'<td class="num green">{fmt_cost(t.get("total_cost_usd"))}</td></tr>')
    return rows

def skill_cost_rows(d):
    max_val = max((float(s.get("total_estimated_cost") or 0) for s in d["skill_cost"]), default=0.0001)
    rows = ""
    for s in d["skill_cost"]:
        cost = float(s.get("total_estimated_cost") or 0)
        avg  = float(s.get("avg_cost_per_use") or 0)
        rows += (f'<tr><td><span class="tag">{s["skill"]}</span></td>'
                 f'<td class="num">{s["total_uses"]}</td>'
                 f'<td class="num green">{fmt_cost(avg)}</td>'
                 f'<td class="num green">{fmt_cost(cost)}</td>'
                 f'<td>{bar(cost, max_val)}</td></tr>')
    return rows

def cooccurrence_rows(d):
    rows = ""
    for c in d["cooccurrence"][:15]:
        rows += (f'<tr><td><span class="tag">{c["skill_a"]}</span></td>'
                 f'<td><span class="tag">{c["skill_b"]}</span></td>'
                 f'<td class="num">{c["sessions_together"]}</td></tr>')
    return rows

def depth_rows(d):
    rows = ""
    for s in d["depth"][:15]:
        turns = s.get("turn_count") or 0
        color = "#f43f5e" if turns >= 10 else "#a855f7" if turns >= 5 else "#00e5ff"
        rows += (f'<tr><td><span class="badge rose">{s.get("user","—")}</span></td>'
                 f'<td class="num" style="color:{color};font-weight:700">{turns}</td>'
                 f'<td class="num">{fmt_tokens(s.get("total_tokens"))}</td>'
                 f'<td class="num green">{fmt_cost(s.get("estimated_cost_usd"))}</td></tr>')
    return rows

def mcp_latency_rows(d):
    max_val = max((int(m.get("avg_latency_ms") or 0) for m in d["mcp_latency"]), default=1)
    rows = ""
    for m in d["mcp_latency"]:
        avg = int(m.get("avg_latency_ms") or 0)
        rows += (f'<tr><td><span class="badge cyan">{m["mcp_server"]}</span></td>'
                 f'<td class="num">{m["total_calls"]}</td>'
                 f'<td class="num">{fmt_ms(m.get("avg_latency_ms"))}</td>'
                 f'<td class="num">{fmt_ms(m.get("min_latency_ms"))}</td>'
                 f'<td class="num">{fmt_ms(m.get("max_latency_ms"))}</td>'
                 f'<td class="num" style="color:#f43f5e">{fmt_ms(m.get("p95_latency_ms"))}</td>'
                 f'<td>{bar(avg, max_val)}</td></tr>')
    return rows


# ── Report builder ────────────────────────────────────────────────────────────

def build_report(d):
    now           = (datetime.now(timezone.utc) + IST).strftime("%Y-%m-%d %H:%M IST")
    total_skills  = sum(s["total_uses"] for s in d["skills"])
    total_tools   = sum(t["total_calls"] for t in d["tools"])
    total_cost    = sum(float(s.get("total_cost_usd") or 0) for s in d["sessions"])
    total_tokens  = sum(int(s.get("total_tokens") or 0) for s in d["sessions"])
    total_sessions= sum(int(s.get("total_sessions") or 0) for s in d["sessions"])
    total_commands= sum(int(c.get("total_uses") or 0) for c in d["commands"])

    ds            = d["depth_summary"][0] if d["depth_summary"] else {}
    avg_turns     = ds.get("avg_turns_per_session") or "—"
    max_turns     = ds.get("max_turns") or "—"
    deep_s        = ds.get("deep_sessions") or 0
    shallow_s     = ds.get("shallow_sessions") or 0

    skill_labels  = json.dumps([s["skill"] for s in d["skills"][:10]])
    skill_vals    = json.dumps([s["total_uses"] for s in d["skills"][:10]])
    tool_labels   = json.dumps([t["tool_name"] for t in d["tools"][:10]])
    tool_vals     = json.dumps([t["total_calls"] for t in d["tools"][:10]])
    dau_labels    = json.dumps([x["day"][:10] for x in reversed(d["dau"])])
    dau_vals      = json.dumps([x["total_sessions"] for x in reversed(d["dau"])])
    mcp_lat_labels= json.dumps([m["mcp_server"] for m in d["mcp_latency"]])
    mcp_lat_avg   = json.dumps([int(m["avg_latency_ms"] or 0) for m in d["mcp_latency"]])
    mcp_lat_p95   = json.dumps([int(m["p95_latency_ms"] or 0) for m in d["mcp_latency"]])
    trace_json    = json.dumps(d.get("traces", []))

    tmpl = open(TEMPLATE_PATH).read()

    replacements = {
        "<!--NOW-->":            now,
        "<!--TOTAL_SKILLS-->":   str(total_skills),
        "<!--TOTAL_TOOLS-->":    str(total_tools),
        "<!--TOTAL_SESSIONS-->": str(total_sessions),
        "<!--TOTAL_TOKENS-->":   fmt_tokens(total_tokens),
        "<!--TOTAL_TOKENS_RAW-->": str(total_tokens),
        "<!--TOTAL_COST-->":     fmt_cost(total_cost),
        "<!--TOTAL_COST_RAW-->": f"{total_cost:.4f}",
        "<!--TOTAL_COMMANDS-->": str(total_commands),
        "<!--SKILLS_COUNT-->":   str(len(d["skills"])),
        "<!--COMMANDS_COUNT-->": str(len(d["commands"])),
        "<!--DAU_COUNT-->":      str(len(d["dau"])),
        "<!--MCP_COUNT-->":      str(len(d["mcp"])),
        "<!--AGENTS_COUNT-->":   str(len(d["agents"])),
        "<!--TRACES_COUNT-->":   str(len(d["traces"])),
        "<!--AVG_TURNS-->":      str(avg_turns),
        "<!--MAX_TURNS-->":      str(max_turns),
        "<!--DEEP_SESSIONS-->":  str(deep_s),
        "<!--SHALLOW_SESSIONS-->": str(shallow_s),
        "<!--SKILL_ROWS-->":     skill_rows(d),
        "<!--TOOL_ROWS-->":      tool_rows(d),
        "<!--MCP_ROWS-->":       mcp_rows(d),
        "<!--AGENT_ROWS-->":     agent_rows(d),
        "<!--CMD_ROWS-->":       cmd_rows(d),
        "<!--SESSION_ROWS-->":   session_rows(d),
        "<!--MODEL_ROWS-->":     model_rows(d),
        "<!--TURN_ROWS-->":      turn_rows(d),
        "<!--SKILL_COST_ROWS-->":skill_cost_rows(d),
        "<!--COOCCURRENCE_ROWS-->": cooccurrence_rows(d),
        "<!--DEPTH_ROWS-->":     depth_rows(d),
        "<!--MCP_LATENCY_ROWS-->": mcp_latency_rows(d),
        "<!--SKILL_LABELS-->":   skill_labels,
        "<!--SKILL_VALS-->":     skill_vals,
        "<!--TOOL_LABELS-->":    tool_labels,
        "<!--TOOL_VALS-->":      tool_vals,
        "<!--DAU_LABELS-->":     dau_labels,
        "<!--DAU_VALS-->":       dau_vals,
        "<!--MCP_LAT_LABELS-->": mcp_lat_labels,
        "<!--MCP_LAT_AVG-->":    mcp_lat_avg,
        "<!--MCP_LAT_P95-->":    mcp_lat_p95,
        "<!--TRACE_JSON-->":     trace_json,
    }

    for placeholder, value in replacements.items():
        tmpl = tmpl.replace(placeholder, value)

    return tmpl


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Fetching observability data...", flush=True)
    try:
        data = get_data()
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

    html = build_report(data)
    with open(REPORT_PATH, "w") as f:
        f.write(html)

    print(f"Report generated: {REPORT_PATH}")
    webbrowser.open(f"file://{REPORT_PATH}")
    print("Opened in browser.")

if __name__ == "__main__":
    main()
