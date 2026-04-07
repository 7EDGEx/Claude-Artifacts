#!/usr/bin/env python3
"""
Fetches all observability data from Supabase and generates a beautiful HTML report.
Opens the report in the default browser automatically.
"""
import json, os, sys, webbrowser, tempfile
from urllib import request
from datetime import datetime

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://uwrttdldcuzwczvaihwb.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def fetch(endpoint):
    req = request.Request(
        f"{SUPABASE_URL}/rest/v1/{endpoint}",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Accept": "application/json"},
    )
    with request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def get_data():
    return {
        "skills":   fetch("skill_usage_summary?select=skill,total_uses,last_used&order=total_uses.desc"),
        "tools":    fetch("tool_call_summary?select=tool_name,total_calls,failed_calls,avg_duration_ms,last_used&order=total_calls.desc"),
        "mcp":      fetch("mcp_usage_summary?select=mcp_server,mcp_tool,total_calls,failed_calls,avg_duration_ms&order=total_calls.desc"),
        "agents":   fetch("agent_usage_summary?select=agent_type,total_runs,unique_users,avg_duration_ms&order=total_runs.desc"),
        "commands": fetch("command_usage_summary?select=command,total_uses,unique_users,last_used&order=total_uses.desc"),
        "sessions": fetch("session_summary?select=user,total_sessions,avg_duration_ms,total_tokens,total_cost_usd,last_seen&order=total_sessions.desc"),
        "dau":      fetch("daily_active_users?select=day,active_users,total_sessions&order=day.desc&limit=14"),
        "turns":    fetch("turn_token_summary?select=user,total_turns,total_input_tokens,total_output_tokens,total_tokens,total_cost_usd&order=total_tokens.desc"),
        "models":   fetch("model_usage_summary?select=model,total_turns,total_tokens,total_cost_usd&order=total_tokens.desc"),
        "traces":   fetch("turn_tokens?select=uuid,parent_uuid,session_id,model,total_tokens,estimated_cost_usd,timestamp,user&order=timestamp.asc&limit=200"),
        "skill_cost":    fetch("skill_cost_estimate?select=skill,total_uses,avg_cost_per_use,total_estimated_cost&order=total_estimated_cost.desc"),
        "cooccurrence":  fetch("skill_cooccurrence?select=skill_a,skill_b,sessions_together&order=sessions_together.desc&limit=20"),
        "depth":         fetch("session_depth?select=session_id,user,turn_count,total_tokens,estimated_cost_usd,started_at&order=started_at.desc&limit=30"),
        "depth_summary": fetch("session_depth_summary?select=avg_turns_per_session,max_turns,min_turns,deep_sessions,shallow_sessions,total_sessions"),
        "mcp_latency":   fetch("mcp_latency_comparison?select=mcp_server,total_calls,avg_latency_ms,min_latency_ms,max_latency_ms,p95_latency_ms"),
    }

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

def bar(value, max_val, width=120):
    if not max_val: return ""
    pct = min(100, int(value / max_val * 100))
    return f'<div class="bar-wrap"><div class="bar" style="width:{pct}%"></div><span>{pct}%</span></div>'

def skill_chart_data(skills):
    labels = json.dumps([s["skill"] for s in skills[:10]])
    values = json.dumps([s["total_uses"] for s in skills[:10]])
    return labels, values

def tool_chart_data(tools):
    labels = json.dumps([t["tool_name"] for t in tools[:10]])
    values = json.dumps([t["total_calls"] for t in tools[:10]])
    return labels, values

def dau_chart_data(dau):
    labels = json.dumps([d["day"][:10] for d in reversed(dau)])
    values = json.dumps([d["total_sessions"] for d in reversed(dau)])
    return labels, values

def generate_html(d):
    from datetime import timezone, timedelta
    now = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M IST")
    total_skills   = sum(s["total_uses"] for s in d["skills"])
    total_tools    = sum(t["total_calls"] for t in d["tools"])
    total_cost     = sum(float(s.get("total_cost_usd") or 0) for s in d["sessions"])
    total_tokens   = sum(int(s.get("total_tokens") or 0) for s in d["sessions"])
    total_sessions = sum(int(s.get("total_sessions") or 0) for s in d["sessions"])
    total_commands = sum(int(c.get("total_uses") or 0) for c in d["commands"])
    trace_json     = json.dumps(d.get("traces", []))
    skill_labels, skill_vals   = skill_chart_data(d["skills"])
    tool_labels,  tool_vals    = tool_chart_data(d["tools"])
    dau_labels,   dau_vals     = dau_chart_data(d["dau"])
    max_skill = max((s["total_uses"] for s in d["skills"]), default=1)
    max_tool  = max((t["total_calls"] for t in d["tools"]), default=1)

    # MCP latency chart data
    mcp_lat_labels = json.dumps([m["mcp_server"] for m in d["mcp_latency"]])
    mcp_lat_avg    = json.dumps([int(m["avg_latency_ms"] or 0) for m in d["mcp_latency"]])
    mcp_lat_p95    = json.dumps([int(m["p95_latency_ms"] or 0) for m in d["mcp_latency"]])

    # Depth summary
    ds = d["depth_summary"][0] if d["depth_summary"] else {}
    avg_turns = ds.get("avg_turns_per_session") or "—"
    max_turns = ds.get("max_turns") or "—"
    deep_sessions = ds.get("deep_sessions") or 0
    shallow_sessions = ds.get("shallow_sessions") or 0

    def skill_rows():
        rows = ""
        for s in d["skills"]:
            last = (s.get("last_used") or "")[:16].replace("T"," ")
            rows += f"""<tr>
              <td><span class="tag">{s['skill']}</span></td>
              <td class="num">{s['total_uses']}</td>
              <td>{bar(s['total_uses'], max_skill)}</td>
              <td class="dim">{last}</td>
            </tr>"""
        return rows

    def tool_rows():
        rows = ""
        for t in d["tools"]:
            last = (t.get("last_used") or "")[:16].replace("T"," ")
            failed = t.get("failed_calls") or 0
            fail_cls = ' class="red"' if failed > 0 else ""
            rows += f"""<tr>
              <td><code>{t['tool_name']}</code></td>
              <td class="num">{t['total_calls']}</td>
              <td{fail_cls} class="num">{failed}</td>
              <td class="num">{fmt_ms(t.get('avg_duration_ms'))}</td>
              <td>{bar(t['total_calls'], max_tool)}</td>
              <td class="dim">{last}</td>
            </tr>"""
        return rows

    def mcp_rows():
        rows = ""
        for m in d["mcp"]:
            rows += f"""<tr>
              <td><span class="badge cyan">{m['mcp_server']}</span></td>
              <td><code>{m['mcp_tool']}</code></td>
              <td class="num">{m['total_calls']}</td>
              <td class="num">{m.get('failed_calls') or 0}</td>
              <td class="num">{fmt_ms(m.get('avg_duration_ms'))}</td>
            </tr>"""
        return rows

    def agent_rows():
        rows = ""
        for a in d["agents"]:
            rows += f"""<tr>
              <td><span class="badge violet">{a['agent_type']}</span></td>
              <td class="num">{a['total_runs']}</td>
              <td class="num">{a.get('unique_users') or '—'}</td>
              <td class="num">{fmt_ms(a.get('avg_duration_ms'))}</td>
            </tr>"""
        return rows

    def cmd_rows():
        rows = ""
        for c in d["commands"]:
            last = (c.get("last_used") or "")[:16].replace("T"," ")
            rows += f"""<tr>
              <td><code>/{c['command']}</code></td>
              <td class="num">{c['total_uses']}</td>
              <td class="num">{c.get('unique_users') or '—'}</td>
              <td class="dim">{last}</td>
            </tr>"""
        return rows

    def session_rows():
        rows = ""
        for s in d["sessions"]:
            last = (s.get("last_seen") or "")[:16].replace("T"," ")
            rows += f"""<tr>
              <td><span class="badge rose">{s['user']}</span></td>
              <td class="num">{s['total_sessions']}</td>
              <td class="num">{fmt_ms(s.get('avg_duration_ms'))}</td>
              <td class="num">{fmt_tokens(s.get('total_tokens'))}</td>
              <td class="num green">{fmt_cost(s.get('total_cost_usd'))}</td>
              <td class="dim">{last}</td>
            </tr>"""
        return rows

    def model_rows():
        rows = ""
        for m in d["models"]:
            rows += f"""<tr>
              <td><span class="badge cyan">{m['model'] or '—'}</span></td>
              <td class="num">{m['total_turns']}</td>
              <td class="num">{fmt_tokens(m.get('total_tokens'))}</td>
              <td class="num green">{fmt_cost(m.get('total_cost_usd'))}</td>
            </tr>"""
        return rows

    def turn_rows():
        rows = ""
        for t in d["turns"]:
            rows += f"""<tr>
              <td><span class="badge rose">{t['user']}</span></td>
              <td class="num">{t['total_turns']}</td>
              <td class="num">{fmt_tokens(t.get('total_input_tokens'))}</td>
              <td class="num">{fmt_tokens(t.get('total_output_tokens'))}</td>
              <td class="num">{fmt_tokens(t.get('total_tokens'))}</td>
              <td class="num green">{fmt_cost(t.get('total_cost_usd'))}</td>
            </tr>"""
        return rows

    def skill_cost_rows():
        rows = ""
        max_cost = max((float(s.get("total_estimated_cost") or 0) for s in d["skill_cost"]), default=0.0001)
        for s in d["skill_cost"]:
            cost = float(s.get("total_estimated_cost") or 0)
            avg  = float(s.get("avg_cost_per_use") or 0)
            rows += f"""<tr>
              <td><span class="tag">{s['skill']}</span></td>
              <td class="num">{s['total_uses']}</td>
              <td class="num green">{fmt_cost(avg)}</td>
              <td class="num green">{fmt_cost(cost)}</td>
              <td>{bar(cost, max_cost)}</td>
            </tr>"""
        return rows

    def cooccurrence_rows():
        rows = ""
        for c in d["cooccurrence"][:15]:
            rows += f"""<tr>
              <td><span class="tag">{c['skill_a']}</span></td>
              <td><span class="tag">{c['skill_b']}</span></td>
              <td class="num">{c['sessions_together']}</td>
            </tr>"""
        return rows

    def depth_rows():
        rows = ""
        for s in d["depth"][:15]:
            turns = s.get("turn_count") or 0
            depth_color = "#f43f5e" if turns >= 10 else "#a855f7" if turns >= 5 else "#00e5ff"
            rows += f"""<tr>
              <td><span class="badge rose">{s.get('user','—')}</span></td>
              <td class="num" style="color:{depth_color};font-weight:700">{turns}</td>
              <td class="num">{fmt_tokens(s.get('total_tokens'))}</td>
              <td class="num green">{fmt_cost(s.get('estimated_cost_usd'))}</td>
            </tr>"""
        return rows

    def mcp_latency_rows():
        rows = ""
        max_lat = max((int(m.get("avg_latency_ms") or 0) for m in d["mcp_latency"]), default=1)
        for m in d["mcp_latency"]:
            avg = int(m.get("avg_latency_ms") or 0)
            p95 = int(m.get("p95_latency_ms") or 0)
            rows += f"""<tr>
              <td><span class="badge cyan">{m['mcp_server']}</span></td>
              <td class="num">{m['total_calls']}</td>
              <td class="num">{fmt_ms(m.get('avg_latency_ms'))}</td>
              <td class="num">{fmt_ms(m.get('min_latency_ms'))}</td>
              <td class="num">{fmt_ms(m.get('max_latency_ms'))}</td>
              <td class="num" style="color:#f43f5e">{fmt_ms(m.get('p95_latency_ms'))}</td>
              <td>{bar(avg, max_lat)}</td>
            </tr>"""
        return rows

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>7EDGE · Claude Observability Report</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --bg: #07080d;
    --surface: #0e1018;
    --surface2: #141720;
    --border: #1e2130;
    --cyan: #00e5ff;
    --violet: #a855f7;
    --rose: #f43f5e;
    --green: #22c55e;
    --text: #e2e8f0;
    --dim: #64748b;
    --font: 'Inter', system-ui, sans-serif;
    --mono: 'JetBrains Mono', monospace;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: var(--font); font-size: 14px; line-height: 1.6; }}
  a {{ color: var(--cyan); text-decoration: none; }}

  /* Layout */
  .wrap {{ max-width: 1400px; margin: 0 auto; padding: 40px 24px 80px; }}

  /* Header */
  .header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 48px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }}
  .logo {{ display: flex; align-items: center; gap: 12px; }}
  .logo-icon {{ width: 40px; height: 40px; border-radius: 10px; background: linear-gradient(135deg, var(--cyan), var(--violet)); display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; color: #000; }}
  .logo-text {{ font-size: 22px; font-weight: 700; letter-spacing: -0.5px; }}
  .logo-text span {{ background: linear-gradient(135deg, var(--cyan), var(--violet)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
  .header-meta {{ text-align: right; color: var(--dim); font-size: 12px; font-family: var(--mono); }}

  /* KPI cards */
  .kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 48px; }}
  .kpi {{ background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 20px 24px; position: relative; overflow: hidden; }}
  .kpi::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: var(--accent, var(--cyan)); }}
  .kpi-label {{ font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: var(--dim); margin-bottom: 8px; }}
  .kpi-value {{ font-size: 32px; font-weight: 800; letter-spacing: -1px; color: var(--text); }}
  .kpi-sub {{ font-size: 11px; color: var(--dim); margin-top: 4px; font-family: var(--mono); }}

  /* Charts row */
  .charts {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 48px; }}
  .chart-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 24px; }}
  .chart-title {{ font-size: 13px; font-weight: 600; color: var(--dim); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 20px; }}
  .chart-wrap {{ position: relative; height: 220px; }}

  /* Sections */
  .section {{ margin-bottom: 40px; }}
  .section-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }}
  .section-icon {{ width: 28px; height: 28px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 14px; }}
  .section-title {{ font-size: 16px; font-weight: 700; }}
  .section-count {{ font-size: 12px; color: var(--dim); font-family: var(--mono); background: var(--surface2); padding: 2px 8px; border-radius: 20px; }}

  /* Tables */
  .table-wrap {{ background: var(--surface); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; }}
  table {{ width: 100%; border-collapse: collapse; }}
  thead tr {{ background: var(--surface2); }}
  th {{ padding: 12px 16px; text-align: left; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: var(--dim); white-space: nowrap; transition: color 0.15s; }}
  th:hover {{ color: var(--cyan); }}
  td {{ padding: 11px 16px; border-top: 1px solid var(--border); vertical-align: middle; }}
  tr:hover td {{ background: var(--surface2); }}
  .num {{ text-align: right; font-family: var(--mono); font-size: 13px; }}
  .dim {{ color: var(--dim); font-size: 12px; font-family: var(--mono); }}
  .red {{ color: var(--rose); }}
  .green {{ color: var(--green); }}

  /* Bar */
  .bar-wrap {{ display: flex; align-items: center; gap: 8px; min-width: 120px; }}
  .bar {{ height: 6px; border-radius: 3px; background: linear-gradient(90deg, var(--cyan), var(--violet)); min-width: 2px; }}
  .bar-wrap span {{ font-size: 11px; color: var(--dim); font-family: var(--mono); white-space: nowrap; }}

  /* Badges */
  .badge {{ display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }}
  .badge.cyan {{ background: rgba(0,229,255,0.1); color: var(--cyan); }}
  .badge.violet {{ background: rgba(168,85,247,0.1); color: var(--violet); }}
  .badge.rose {{ background: rgba(244,63,94,0.1); color: var(--rose); }}
  .tag {{ display: inline-block; padding: 2px 10px; border-radius: 6px; font-size: 12px; background: var(--surface2); border: 1px solid var(--border); font-family: var(--mono); }}
  code {{ font-family: var(--mono); font-size: 12px; background: var(--surface2); padding: 2px 6px; border-radius: 4px; }}

  /* Footer */
  .footer {{ margin-top: 60px; padding-top: 24px; border-top: 1px solid var(--border); text-align: center; color: var(--dim); font-size: 12px; font-family: var(--mono); }}

  /* Glow effects */
  .glow-cyan {{ box-shadow: 0 0 30px -10px rgba(0,229,255,0.2); }}
  .glow-violet {{ box-shadow: 0 0 30px -10px rgba(168,85,247,0.2); }}
</style>
</head>
<body>
<div class="wrap">

  <!-- Header -->
  <div class="header">
    <div class="logo">
      <div class="logo-icon">7E</div>
      <div>
        <div class="logo-text">7EDGE <span>Observability</span></div>
        <div style="font-size:12px;color:var(--dim);font-family:var(--mono)">Claude Code Analytics Dashboard</div>
      </div>
    </div>
    <div class="header-meta">
      Generated: {now}<br>
      Project: Claude-Artifacts<br>
      Supabase: uwrttdldcuzwczvaihwb
      <br><br>
      <button id="refreshBtn" style="background:rgba(0,229,255,0.1);border:1px solid rgba(0,229,255,0.3);color:var(--cyan);padding:6px 14px;border-radius:8px;cursor:pointer;font-size:12px;font-family:var(--mono)">⟳ Refresh</button>
    </div>
  </div>

  <!-- Search bar -->
  <div style="margin-bottom:32px">
    <input id="globalSearch" type="text" placeholder="🔍  Filter all tables..." style="width:100%;background:var(--surface);border:1px solid var(--border);color:var(--text);padding:12px 18px;border-radius:12px;font-size:14px;outline:none;font-family:var(--font);transition:border 0.2s" onfocus="this.style.borderColor='var(--cyan)'" onblur="this.style.borderColor='var(--border)'">
  </div>

  <!-- KPIs -->
  <div class="kpis">
    <div class="kpi" style="--accent:var(--cyan)">
      <div class="kpi-label">Skill Invocations</div>
      <div class="kpi-value" data-target="{total_skills}">{total_skills}</div>
      <div class="kpi-sub">{len(d['skills'])} distinct skills</div>
    </div>
    <div class="kpi" style="--accent:var(--violet)">
      <div class="kpi-label">Tool Calls</div>
      <div class="kpi-value" data-target="{total_tools}">{total_tools}</div>
      <div class="kpi-sub">0 failures</div>
    </div>
    <div class="kpi" style="--accent:var(--rose)">
      <div class="kpi-label">Sessions</div>
      <div class="kpi-value" data-target="{total_sessions}">{total_sessions}</div>
      <div class="kpi-sub">{len(d['dau'])} active days</div>
    </div>
    <div class="kpi" style="--accent:var(--green)">
      <div class="kpi-label">Total Tokens</div>
      <div class="kpi-value" data-target="{total_tokens}" data-suffix="">{fmt_tokens(total_tokens)}</div>
      <div class="kpi-sub">across all sessions</div>
    </div>
    <div class="kpi" style="--accent:var(--cyan)">
      <div class="kpi-label">Est. Cost</div>
      <div class="kpi-value" style="color:var(--green)" data-target="{total_cost:.4f}" data-float="1" data-prefix="$">{fmt_cost(total_cost)}</div>
      <div class="kpi-sub">Claude Sonnet 4.6</div>
    </div>
    <div class="kpi" style="--accent:var(--violet)">
      <div class="kpi-label">Commands Used</div>
      <div class="kpi-value" data-target="{total_commands}">{total_commands}</div>
      <div class="kpi-sub">{len(d['commands'])} distinct commands</div>
    </div>
  </div>

  <!-- Charts -->
  <div class="charts">
    <div class="chart-card glow-cyan">
      <div class="chart-title">⚡ Top Skills</div>
      <div class="chart-wrap"><canvas id="skillChart"></canvas></div>
    </div>
    <div class="chart-card glow-violet">
      <div class="chart-title">🔧 Top Tools</div>
      <div class="chart-wrap"><canvas id="toolChart"></canvas></div>
    </div>
    <div class="chart-card" style="box-shadow:0 0 30px -10px rgba(244,63,94,0.2)">
      <div class="chart-title">📅 Daily Sessions</div>
      <div class="chart-wrap"><canvas id="dauChart"></canvas></div>
    </div>
  </div>

  <!-- Skills -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:rgba(0,229,255,0.1)">⚡</div>
      <div class="section-title">Skills Usage</div>
      <div class="section-count">{len(d['skills'])} skills · {total_skills} total uses</div>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Skill</th><th>Uses</th><th>Distribution</th><th>Last Used</th></tr></thead>
        <tbody>{skill_rows()}</tbody>
      </table>
    </div>
  </div>

  <!-- Tools -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:rgba(168,85,247,0.1)">🔧</div>
      <div class="section-title">Tool Calls</div>
      <div class="section-count">{total_tools} calls · 0 failures</div>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Tool</th><th>Calls</th><th>Failed</th><th>Avg Duration</th><th>Distribution</th><th>Last Used</th></tr></thead>
        <tbody>{tool_rows()}</tbody>
      </table>
    </div>
  </div>

  <!-- MCP + Agents side by side -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:40px">
    <div class="section" style="margin:0">
      <div class="section-header">
        <div class="section-icon" style="background:rgba(0,229,255,0.1)">🔌</div>
        <div class="section-title">MCP Usage</div>
        <div class="section-count">{len(d['mcp'])} tools</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Server</th><th>Tool</th><th>Calls</th><th>Failed</th><th>Avg ms</th></tr></thead>
          <tbody>{mcp_rows()}</tbody>
        </table>
      </div>
    </div>
    <div class="section" style="margin:0">
      <div class="section-header">
        <div class="section-icon" style="background:rgba(168,85,247,0.1)">🤖</div>
        <div class="section-title">Agent Usage</div>
        <div class="section-count">{len(d['agents'])} agent types</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Type</th><th>Runs</th><th>Users</th><th>Avg Duration</th></tr></thead>
          <tbody>{agent_rows()}</tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Commands -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:rgba(244,63,94,0.1)">/</div>
      <div class="section-title">Commands Usage</div>
      <div class="section-count">{len(d['commands'])} commands · {total_commands} uses</div>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Command</th><th>Uses</th><th>Unique Users</th><th>Last Used</th></tr></thead>
        <tbody>{cmd_rows()}</tbody>
      </table>
    </div>
  </div>

  <!-- Sessions + Model side by side -->
  <div style="display:grid;grid-template-columns:2fr 1fr;gap:20px;margin-bottom:40px">
    <div class="section" style="margin:0">
      <div class="section-header">
        <div class="section-icon" style="background:rgba(34,197,94,0.1)">📊</div>
        <div class="section-title">Session Analytics</div>
        <div class="section-count">{total_sessions} sessions</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>User</th><th>Sessions</th><th>Avg Duration</th><th>Tokens</th><th>Cost</th><th>Last Seen</th></tr></thead>
          <tbody>{session_rows()}</tbody>
        </table>
      </div>
    </div>
    <div class="section" style="margin:0">
      <div class="section-header">
        <div class="section-icon" style="background:rgba(0,229,255,0.1)">🧠</div>
        <div class="section-title">Model Usage</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Model</th><th>Turns</th><th>Tokens</th><th>Cost</th></tr></thead>
          <tbody>{model_rows()}</tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Token Usage -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:rgba(34,197,94,0.1)">💰</div>
      <div class="section-title">Token Usage per User</div>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>User</th><th>Turns</th><th>Input Tokens</th><th>Output Tokens</th><th>Total Tokens</th><th>Est. Cost</th></tr></thead>
        <tbody>{turn_rows()}</tbody>
      </table>
    </div>
  </div>

  <!-- Analytics Row: Skill Cost + Co-occurrence -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:40px">
    <div class="section" style="margin:0">
      <div class="section-header">
        <div class="section-icon" style="background:rgba(34,197,94,0.1)">💸</div>
        <div class="section-title">Cost per Skill</div>
        <div class="section-count">estimated</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Skill</th><th>Uses</th><th>Avg Cost</th><th>Total Cost</th><th>Distribution</th></tr></thead>
          <tbody>{skill_cost_rows()}</tbody>
        </table>
      </div>
    </div>
    <div class="section" style="margin:0">
      <div class="section-header">
        <div class="section-icon" style="background:rgba(168,85,247,0.1)">🔀</div>
        <div class="section-title">Skill Co-occurrence</div>
        <div class="section-count">used together</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Skill A</th><th>Skill B</th><th>Sessions</th></tr></thead>
          <tbody>{cooccurrence_rows()}</tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Analytics Row: Session Depth + MCP Latency -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:40px">
    <div class="section" style="margin:0">
      <div class="section-header">
        <div class="section-icon" style="background:rgba(0,229,255,0.1)">📏</div>
        <div class="section-title">Session Depth</div>
        <div class="section-count">avg {avg_turns} turns · max {max_turns} · {deep_sessions} deep (≥10) · {shallow_sessions} shallow (&lt;5)</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>User</th><th>Turns</th><th>Tokens</th><th>Cost</th></tr></thead>
          <tbody>{depth_rows()}</tbody>
        </table>
      </div>
    </div>
    <div class="section" style="margin:0">
      <div class="section-header">
        <div class="section-icon" style="background:rgba(244,63,94,0.1)">⏱</div>
        <div class="section-title">MCP Latency</div>
        <div class="section-count">by server</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Server</th><th>Calls</th><th>Avg</th><th>Min</th><th>Max</th><th>P95</th><th>Bar</th></tr></thead>
          <tbody>{mcp_latency_rows()}</tbody>
        </table>
      </div>
      <div style="padding:16px 20px 4px">
        <div class="chart-wrap" style="height:160px"><canvas id="mcpLatencyChart"></canvas></div>
      </div>
    </div>
  </div>

  <!-- Chain Execution Traces -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:rgba(0,229,255,0.1)">🔗</div>
      <div class="section-title">Chain Execution Traces</div>
      <div class="section-count">{len(d['traces'])} turns recorded</div>
    </div>
    <div style="background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:20px;margin-bottom:12px">
      <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:20px">
        <span style="font-size:12px;color:var(--dim)">Session:</span>
        <select id="sessionFilter" style="background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:8px;font-size:12px;cursor:pointer;flex:1;max-width:320px"></select>
        <div style="display:flex;gap:16px;font-size:11px;color:var(--dim);font-family:var(--mono)">
          <span>🟦 Low cost</span><span>🟪 Medium</span><span>🟥 High cost</span>
          <span>Width = tokens used</span>
        </div>
      </div>
      <div id="traceTimeline"></div>
      <div id="traceSummary" style="margin-top:16px;padding:12px 16px;background:var(--surface2);border-radius:10px;font-size:12px;font-family:var(--mono);color:var(--dim);display:none"></div>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    7EDGE Technologies &nbsp;·&nbsp; Claude Code Observability &nbsp;·&nbsp; {now}
    &nbsp;·&nbsp; <span style="color:var(--cyan)">{total_sessions} sessions tracked</span>
    &nbsp;·&nbsp; <span style="color:var(--green)">{fmt_cost(total_cost)} total spend</span>
  </div>

</div>

<script>
// ── Animated counters ──────────────────────────────────────────────────────
function animateCounter(el) {{
  const target = parseFloat(el.dataset.target);
  const isFloat = el.dataset.float === '1';
  const prefix = el.dataset.prefix || '';
  const suffix = el.dataset.suffix || '';
  const duration = 1200;
  const start = performance.now();
  function step(now) {{
    const p = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - p, 3);
    const val = target * ease;
    el.textContent = prefix + (isFloat ? val.toFixed(4) : Math.round(val).toLocaleString()) + suffix;
    if (p < 1) requestAnimationFrame(step);
  }}
  requestAnimationFrame(step);
}}
document.querySelectorAll('[data-target]').forEach(animateCounter);

// ── Sortable tables ────────────────────────────────────────────────────────
document.querySelectorAll('table').forEach(table => {{
  const headers = table.querySelectorAll('th');
  headers.forEach((th, col) => {{
    th.style.cursor = 'pointer';
    th.style.userSelect = 'none';
    th.title = 'Click to sort';
    let asc = true;
    th.addEventListener('click', () => {{
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.querySelectorAll('tr'));
      rows.sort((a, b) => {{
        const av = a.cells[col]?.textContent.trim().replace(/[,$%ms]/g,'') || '';
        const bv = b.cells[col]?.textContent.trim().replace(/[,$%ms]/g,'') || '';
        const an = parseFloat(av), bn = parseFloat(bv);
        if (!isNaN(an) && !isNaN(bn)) return asc ? an - bn : bn - an;
        return asc ? av.localeCompare(bv) : bv.localeCompare(av);
      }});
      rows.forEach(r => tbody.appendChild(r));
      headers.forEach(h => h.textContent = h.textContent.replace(' ↑','').replace(' ↓',''));
      th.textContent += asc ? ' ↑' : ' ↓';
      asc = !asc;
    }});
  }});
}});

// ── Global search filter ───────────────────────────────────────────────────
document.getElementById('globalSearch').addEventListener('input', function() {{
  const q = this.value.toLowerCase();
  document.querySelectorAll('tbody tr').forEach(row => {{
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  }});
}});

// ── Section toggle ─────────────────────────────────────────────────────────
document.querySelectorAll('.section-header').forEach(header => {{
  header.style.cursor = 'pointer';
  header.addEventListener('click', () => {{
    const section = header.closest('.section, [data-section]');
    const content = section?.querySelector('.table-wrap, .chart-card');
    if (content) {{
      const hidden = content.style.display === 'none';
      content.style.display = hidden ? '' : 'none';
      const icon = header.querySelector('.toggle-icon');
      if (icon) icon.textContent = hidden ? '▾' : '▸';
    }}
  }});
  const icon = document.createElement('span');
  icon.className = 'toggle-icon';
  icon.textContent = '▾';
  icon.style.cssText = 'margin-left:auto;color:var(--dim);font-size:12px;';
  header.appendChild(icon);
}});

// ── Tooltip on table cells ─────────────────────────────────────────────────
const tooltip = document.createElement('div');
tooltip.style.cssText = 'position:fixed;background:#1e2130;border:1px solid #2d3348;color:#e2e8f0;padding:6px 12px;border-radius:8px;font-size:12px;pointer-events:none;opacity:0;transition:opacity 0.15s;z-index:9999;font-family:monospace;';
document.body.appendChild(tooltip);
document.querySelectorAll('td').forEach(td => {{
  td.addEventListener('mouseenter', e => {{
    const full = td.textContent.trim();
    if (full.length > 3) {{
      tooltip.textContent = full;
      tooltip.style.opacity = '1';
    }}
  }});
  td.addEventListener('mousemove', e => {{
    tooltip.style.left = (e.clientX + 12) + 'px';
    tooltip.style.top  = (e.clientY - 28) + 'px';
  }});
  td.addEventListener('mouseleave', () => {{ tooltip.style.opacity = '0'; }});
}});

// ── Charts ─────────────────────────────────────────────────────────────────
const chartDefaults = {{
  plugins: {{ legend: {{ display: false }}, tooltip: {{ backgroundColor: '#1e2130', titleColor: '#e2e8f0', bodyColor: '#94a3b8', borderColor: '#2d3348', borderWidth: 1, padding: 10, cornerRadius: 8 }} }},
  scales: {{
    x: {{ ticks: {{ color: '#64748b', font: {{ size: 11 }} }}, grid: {{ color: '#1e2130' }} }},
    y: {{ ticks: {{ color: '#64748b', font: {{ size: 11 }} }}, grid: {{ color: '#1e2130' }} }}
  }}
}};

new Chart(document.getElementById('skillChart'), {{
  type: 'bar',
  data: {{
    labels: {skill_labels},
    datasets: [{{ data: {skill_vals}, backgroundColor: ctx => `rgba(0,229,255,${{0.4 + ctx.dataIndex * 0.06}})`, borderRadius: 6, borderSkipped: false }}]
  }},
  options: {{ ...chartDefaults, indexAxis: 'y', responsive: true, maintainAspectRatio: false,
    onClick: (e, els) => {{ if(els.length) {{ const i = els[0].index; document.querySelectorAll('tbody tr').forEach(r => {{ r.style.background = r.textContent.includes({skill_labels}[i]) ? 'rgba(0,229,255,0.05)' : ''; }}); }} }}
  }}
}});

new Chart(document.getElementById('toolChart'), {{
  type: 'bar',
  data: {{
    labels: {tool_labels},
    datasets: [{{ data: {tool_vals}, backgroundColor: ctx => `rgba(168,85,247,${{0.4 + ctx.dataIndex * 0.06}})`, borderRadius: 6, borderSkipped: false }}]
  }},
  options: {{ ...chartDefaults, indexAxis: 'y', responsive: true, maintainAspectRatio: false }}
}});

// MCP Latency chart
if (document.getElementById('mcpLatencyChart')) {{
  new Chart(document.getElementById('mcpLatencyChart'), {{
    type: 'bar',
    data: {{
      labels: {mcp_lat_labels},
      datasets: [
        {{ label: 'Avg ms', data: {mcp_lat_avg}, backgroundColor: 'rgba(0,229,255,0.6)', borderRadius: 4 }},
        {{ label: 'P95 ms', data: {mcp_lat_p95}, backgroundColor: 'rgba(244,63,94,0.5)', borderRadius: 4 }}
      ]
    }},
    options: {{
      ...chartDefaults,
      responsive: true, maintainAspectRatio: false,
      plugins: {{ ...chartDefaults.plugins, legend: {{ display: true, labels: {{ color: '#64748b', font: {{ size: 10 }} }} }} }}
    }}
  }});
}}

new Chart(document.getElementById('dauChart'), {{
  type: 'line',
  data: {{
    labels: {dau_labels},
    datasets: [{{
      data: {dau_vals},
      borderColor: '#f43f5e',
      backgroundColor: 'rgba(244,63,94,0.1)',
      fill: true, tension: 0.4,
      pointBackgroundColor: '#f43f5e', pointRadius: 5, pointHoverRadius: 8
    }}]
  }},
  options: {{ ...chartDefaults, responsive: true, maintainAspectRatio: false }}
}});

// ── IST timezone helper (UTC+5:30) ─────────────────────────────────────────
function toIST(utcStr) {{
  if (!utcStr) return '—';
  const d = new Date(utcStr);
  // Add 5h 30m offset
  const ist = new Date(d.getTime() + (5.5 * 60 * 60 * 1000));
  const pad = n => String(n).padStart(2,'0');
  return `${{ist.getUTCFullYear()}}-${{pad(ist.getUTCMonth()+1)}}-${{pad(ist.getUTCDate())}} ${{pad(ist.getUTCHours())}}:${{pad(ist.getUTCMinutes())}} IST`;
}}
function toISTTime(utcStr) {{
  if (!utcStr) return '—';
  const d = new Date(utcStr);
  const ist = new Date(d.getTime() + (5.5 * 60 * 60 * 1000));
  const pad = n => String(n).padStart(2,'0');
  return `${{pad(ist.getUTCHours())}}:${{pad(ist.getUTCMinutes())}}`;
}}

// Convert all .dim cells that look like timestamps
document.querySelectorAll('td.dim').forEach(td => {{
  const txt = td.textContent.trim();
  if (/^\\d{{4}}-\\d{{2}}-\\d{{2}}/.test(txt)) {{
    td.textContent = toIST(txt.replace(' ','T') + (txt.includes('T') ? '' : 'Z'));
  }}
}});
document.getElementById('refreshBtn').addEventListener('click', () => {{
  document.getElementById('refreshBtn').textContent = '⟳ Refreshing...';
  setTimeout(() => location.reload(), 300);
}});

// ── Chain Execution Trace Timeline ─────────────────────────────────────────
const traceData = {trace_json};

function renderTimeline(sessionId) {{
  const container = document.getElementById('traceTimeline');
  const summary   = document.getElementById('traceSummary');
  const turns = sessionId === 'all' ? traceData : traceData.filter(t => t.session_id === sessionId);

  if (!turns.length) {{
    container.innerHTML = '<div style="text-align:center;padding:40px;color:#64748b;font-family:monospace">No trace data yet — turns are logged after each Claude response.</div>';
    summary.style.display = 'none';
    return;
  }}

  const maxTokens = Math.max(...turns.map(t => t.total_tokens || 1));
  const totalCost = turns.reduce((s,t) => s + parseFloat(t.estimated_cost_usd||0), 0);
  const totalToks = turns.reduce((s,t) => s + (t.total_tokens||0), 0);

  const bySession = {{}};
  turns.forEach(t => {{
    const sid = t.session_id || 'unknown';
    if (!bySession[sid]) bySession[sid] = [];
    bySession[sid].push(t);
  }});

  let html = '';
  Object.entries(bySession).forEach(([sid, sessionTurns]) => {{
    const sessionCost = sessionTurns.reduce((s,t) => s + parseFloat(t.estimated_cost_usd||0), 0);
    const sessionToks = sessionTurns.reduce((s,t) => s + (t.total_tokens||0), 0);
    html += `<div style="margin-bottom:28px">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
        <span style="font-size:11px;font-family:monospace;color:#64748b;background:#141720;padding:3px 10px;border-radius:6px;border:1px solid #1e2130">SESSION ${{sid.slice(0,8)}}…</span>
        <span style="font-size:11px;color:#64748b;font-family:monospace">${{sessionTurns.length}} turns · ${{(sessionToks/1000).toFixed(1)}}k tokens · $${{sessionCost.toFixed(4)}} · ${{toIST(sessionTurns[0]?.timestamp)}} → ${{toISTTime(sessionTurns[sessionTurns.length-1]?.timestamp)}} IST</span>
      </div>
      <div style="display:flex;gap:3px;align-items:flex-end;height:90px;padding:0 4px">`;
    sessionTurns.forEach((t, i) => {{
      const tokens = t.total_tokens || 0;
      const cost   = parseFloat(t.estimated_cost_usd || 0);
      const maxC   = Math.max(...sessionTurns.map(x => parseFloat(x.estimated_cost_usd||0)), 0.0001);
      const ratio  = cost / maxC;
      const color  = ratio > 0.7 ? '#f43f5e' : ratio > 0.3 ? '#a855f7' : '#00e5ff';
      const barH   = Math.max(14, Math.round((tokens / maxTokens) * 76));
      const ts     = toISTTime(t.timestamp);
      html += `<div style="display:flex;flex-direction:column;align-items:center;gap:2px;cursor:pointer;flex:1;min-width:24px"
        onclick="selectTurn(${{JSON.stringify(t)}}, this)"
        onmouseenter="this.querySelector('.tb').style.opacity='1'"
        onmouseleave="this.querySelector('.tb').style.opacity='0.7'">
        <div style="font-size:8px;color:#475569;font-family:monospace">${{ts}}</div>
        <div class="tb" style="width:100%;height:${{barH}}px;background:${{color}};border-radius:4px 4px 0 0;opacity:0.7;transition:all 0.15s;position:relative">
          <div style="position:absolute;bottom:2px;left:0;right:0;text-align:center;font-size:8px;color:rgba(0,0,0,0.8);font-family:monospace;font-weight:700">${{tokens>=1000?(tokens/1000).toFixed(0)+'k':tokens}}</div>
        </div>
        <div style="font-size:8px;color:#475569;font-family:monospace">#${{i+1}}</div>
      </div>`;
    }});
    html += `</div></div>`;
  }});

  container.innerHTML = html;
  summary.style.display = 'block';
  summary.innerHTML = `<span style="color:#00e5ff">${{turns.length}} turns</span> &nbsp;·&nbsp;
    <span style="color:#a855f7">${{(totalToks/1000).toFixed(1)}}k tokens</span> &nbsp;·&nbsp;
    <span style="color:#22c55e">$${{totalCost.toFixed(4)}} cost</span> &nbsp;·&nbsp;
    Avg ${{Math.round(totalToks/turns.length).toLocaleString()}} tokens/turn &nbsp;·&nbsp;
    Avg $${{(totalCost/turns.length).toFixed(5)}}/turn`;
}}

function selectTurn(t, el) {{
  document.querySelectorAll('#traceTimeline [onclick]').forEach(e => {{ e.style.background=''; e.style.borderRadius=''; }});
  el.style.background = 'rgba(0,229,255,0.06)'; el.style.borderRadius = '6px';
  const ts = toIST(t.timestamp);
  const s = document.getElementById('traceSummary');
  s.style.display = 'block';
  s.innerHTML = `<b style="color:#00e5ff">Turn selected</b> &nbsp;·&nbsp;
    UUID: <span style="color:#a855f7">${{(t.uuid||'').slice(0,12)}}…</span> &nbsp;·&nbsp;
    Parent: <span style="color:#64748b">${{t.parent_uuid ? t.parent_uuid.slice(0,12)+'…' : 'root (first turn)'}}</span> &nbsp;·&nbsp;
    Model: <span style="color:#00e5ff">${{t.model||'—'}}</span> &nbsp;·&nbsp;
    Tokens: <span style="color:#a855f7">${{(t.total_tokens||0).toLocaleString()}}</span> &nbsp;·&nbsp;
    Cost: <span style="color:#22c55e">$${{parseFloat(t.estimated_cost_usd||0).toFixed(6)}}</span> &nbsp;·&nbsp;
    Time: ${{ts}}`;
}}

const sessions = [...new Set(traceData.map(t => t.session_id).filter(Boolean))];
const sel = document.getElementById('sessionFilter');
const allOpt = document.createElement('option');
allOpt.value = 'all'; allOpt.textContent = `All sessions (${{traceData.length}} turns)`;
sel.appendChild(allOpt);
sessions.forEach(s => {{
  const opt = document.createElement('option');
  opt.value = s;
  const count = traceData.filter(t => t.session_id === s).length;
  const cost  = traceData.filter(t => t.session_id === s).reduce((a,t) => a + parseFloat(t.estimated_cost_usd||0), 0);
  opt.textContent = `${{s.slice(0,8)}}… · ${{count}} turns · $${{cost.toFixed(4)}}`;
  sel.appendChild(opt);
}});
sel.addEventListener('change', () => renderTimeline(sel.value));
renderTimeline('all');
</script>
</body>
</html>"""


def main():
    print("Fetching observability data...", flush=True)
    try:
        data = get_data()
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

    html = generate_html(data)

    # Write to a fixed path so it can be reopened
    report_path = os.path.expanduser("~/.claude/observability-report.html")
    with open(report_path, "w") as f:
        f.write(html)

    print(f"Report generated: {report_path}")
    webbrowser.open(f"file://{report_path}")
    print("Opened in browser.")

if __name__ == "__main__":
    main()
