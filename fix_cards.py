import re

with open("app.py", "r") as f:
    text = f.read()

# 1. Fix the THEME LOCK to stop applying the grid to inner block-containers
old_theme = "body, .stApp, [data-testid=\"stAppViewContainer\"], [data-testid=\"stAppViewContainer\"] > .main, .block-container {{"
new_theme = "body, .stApp, [data-testid=\"stAppViewContainer\"], [data-testid=\"stAppViewContainer\"] > .main {{"
text = text.replace(old_theme, new_theme)

# 2. Reinforce the white background on the cards and remove any background-image from them and their children
old_card = """    /* 5. ALL BORDERED CONTAINERS BECOME WHITE CARDS */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: #ffffff !important;
        border: 2px solid #1a1a1a !important;
        border-radius: 12px !important;
        box-shadow: 4px 4px 0 rgba(0,0,0,0.15) !important;
        padding: 20px !important;
        margin-bottom: 16px;
        position: relative;
        color: #1a1a1a !important;
    }}"""

new_card = """    /* 5. ALL BORDERED CONTAINERS BECOME WHITE CARDS */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: #ffffff !important;
        background-image: none !important;
        border: 2px solid #1a1a1a !important;
        border-radius: 12px !important;
        box-shadow: 4px 4px 0 rgba(0,0,0,0.15) !important;
        padding: 20px !important;
        margin-bottom: 16px;
        position: relative;
        color: #1a1a1a !important;
        z-index: 1;
    }}
    /* Ensure no child elements accidentally inherit the transparent/grid background */
    [data-testid="stVerticalBlockBorderWrapper"] * {{
        background-image: none !important;
    }}"""
text = text.replace(old_card, new_card)

# But wait, Pattern Insights needs to be yellow! The existing CSS for it is:
# [data-testid="stVerticalBlockBorderWrapper"]:has(.is-sticky) {{ background: #fff3bf !important; ...
# Since we changed new_card to use `background-color`, let's make sure pattern insights uses it too.
text = text.replace("background: #fff3bf !important;", "background-color: #fff3bf !important; background-image: none !important;")

with open("app.py", "w") as f:
    f.write(text)
