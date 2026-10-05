import re

with open("app.py", "r") as f:
    content = f.read()

# Replace the imports and old helper
old_helper = """# Helper for props
def prop_img(path, rotation, size=90):
    return f'<img src="{path}" class="prop-img" style="transform: rotate({rotation}deg); max-height: {size}px;" onerror="this.style.display=\\'none\\'">'"""

new_helper = """import base64
import os
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"

@st.cache_data
def get_cached_b64(filename: str) -> str:
    path = ASSETS / filename
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()

# Helper for props
def prop_img(filename: str, rotation: float = -2.0, height: int = 90) -> str:
    b64 = get_cached_b64(filename)
    if not b64:
        return ""
    return (
        f'<img src="data:image/png;base64,{b64}" '
        f'class="prop-img" '
        f'style="height:{height}px; transform:rotate({rotation}deg); '
        f'filter:drop-shadow(3px 3px 2px rgba(0,0,0,0.25)); '
        f'pointer-events:none; margin:4px;" />'
    )"""

content = content.replace(old_helper, new_helper)

# Replace the calls
content = content.replace("prop_img('./assets/marcus.png', 2, 70)", "prop_img('marcus.png', rotation=2, height=70)")
content = content.replace("prop_img('./assets/marcus.png', 0, 50)", "prop_img('marcus.png', rotation=0, height=50)")
content = content.replace("prop_img('./assets/aristotle.png', 1, 80)", "prop_img('aristotle.png', rotation=1, height=80)")
# Wait, thinker in New Entry is hardcoded as an <img src="./assets/thinker.png"...
content = re.sub(
    r"<img src=\"\./assets/thinker\.png\".*?>",
    r"{prop_img('thinker.png', rotation=-2, height=80)}",
    content
)
# Check if thinker was called via helper or hardcoded
content = content.replace("prop_img('./assets/diogenes.png', 1.5, 70)", "prop_img('diogenes.png', rotation=1.5, height=70)")

with open("app.py", "w") as f:
    f.write(content)
