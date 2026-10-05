import base64
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"
_prop_cache = {}

def prop_img(filename, height=140, rotation=-2.0):
    if filename not in _prop_cache:
        p = ASSETS / filename
        _prop_cache[filename] = base64.b64encode(p.read_bytes()).decode() if p.exists() else None
    b64 = _prop_cache[filename]
    if not b64:
        return ""
    return (f'<img src="data:image/png;base64,{b64}" style="height:{height}px; '
            f'transform:rotate({rotation}deg); filter:drop-shadow(3px 3px 2px rgba(0,0,0,0.25)); '
            f'pointer-events:none;" />')

def section_header(title):
    wavy_svg = '''<svg width="60" height="8" viewBox="0 0 60 8" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 4 Q 10 0, 20 4 T 40 4 T 60 4" stroke="#1a1a1a" stroke-width="2" stroke-linecap="round"/></svg>'''
    return f'<h3 style="display:flex; align-items:center; margin-bottom:0; font-size:30px;">{title}</h3><div style="margin: 4px 0 24px 0;">{wavy_svg}</div>'
