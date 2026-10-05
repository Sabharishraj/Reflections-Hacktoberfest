import re

# 1. HEATMAP.PY
heatmap_code = """import calendar
from datetime import datetime
import db

def render_heatmap_html(con=None):
    now = datetime.now()
    month_name = now.strftime("%b")
    
    counts = {}
    for e in db.get_all_entries():
        dt = datetime.strptime(e['created_at'][:10], "%Y-%m-%d")
        if dt.year == now.year and dt.month == now.month:
            counts[(dt.year, dt.month, dt.day)] = counts.get((dt.year, dt.month, dt.day), 0) + 1
            
    weeks = calendar.monthcalendar(now.year, now.month)
    colors = {1: "#bcd4ea", 2: "#6fa3d4", 3: "#2e6fb0"}
    
    html = '<div style="width:100%; color:#1a1a1a; box-sizing:border-box;">'
    
    html += '<div style="display:grid; grid-template-rows:repeat(7, 18px); grid-auto-flow:column; gap:4px; width:max-content; margin:0 auto;">'
    
    for lbl in ["Mon", "", "Wed", "", "Fri", "", ""]:
        html += f'<div style="font-size:10px; line-height:18px; padding-right:6px; color:#6b6b6b;">{lbl}</div>'
        
    for week in weeks:
        for day in week:
            if day == 0:
                html += '<div style="width:18px; height:18px;"></div>'
            else:
                c = counts.get((now.year, now.month, day), 0)
                color = colors[min(c, 3)] if c > 0 else "#ece5d8"
                txt = "no entry" if c == 0 else f"{c} entries" if c > 1 else "1 entry"
                title = f"{month_name} {day} — {txt}"
                html += f'<div title="{title}" style="width:18px; height:18px; background:{color}; border-radius:2px; border: 1px solid rgba(0,0,0,0.05);"></div>'
                
    html += '</div><div style="margin-top:20px; font-size:11px; display:flex; gap:10px; align-items:center; justify-content:center; color:#6b6b6b; font-weight:bold;">'
    html += '<span>ENTRIES:</span>'
    html += f'<div style="display:flex; align-items:center; gap:4px;"><div style="width:18px; height:18px; background:#ece5d8; border-radius:2px; border: 1px solid rgba(0,0,0,0.05);"></div>0</div>'
    for k, v in colors.items():
        html += f'<div style="display:flex; align-items:center; gap:4px;"><div style="width:18px; height:18px; background:{v}; border-radius:2px; border: 1px solid rgba(0,0,0,0.05);"></div>{"3+" if k==3 else k}</div>'
    html += '</div>'
    
    laurel = '''<svg style="margin: 24px auto 0 auto; display:block;" width="120" height="20" viewBox="0 0 120 20" fill="none" stroke="#1a1a1a" stroke-width="1.5"><path d="M10,10 Q30,0 60,10 T110,10"/><path d="M30,5 C35,2 40,8 30,10"/><path d="M50,7 C55,4 60,10 50,12"/><path d="M70,7 C65,4 60,10 70,12"/><path d="M90,5 C85,2 80,8 90,10"/></svg>'''
    html += laurel
    
    return html + '</div>'
"""
with open("heatmap.py", "w") as f:
    f.write(heatmap_code)
