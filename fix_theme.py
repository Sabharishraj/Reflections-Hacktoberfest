import re

with open("app.py", "r") as f:
    content = f.read()

new_css = """    <style>
    /* 0. GLOBAL THEME AND DARK MODE DEFEAT */
    .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background-color: #faf7f0 !important;
        background-image: repeating-linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px), repeating-linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px) !important;
        background-size: 24px 24px !important;
        color: #1a1a1a !important;
    }
    [data-testid="stMarkdownContainer"] { color: #1a1a1a !important; }
    
    /* 1. HIDE SIDEBAR ENTIRELY */
"""

content = content.replace("    <style>\n    /* 1. HIDE SIDEBAR ENTIRELY */\n", new_css)

# Replace textarea background to fdfbf5 as requested and border focus
content = content.replace("background-color: #faf7f0 !important;", "background-color: #fdfbf5 !important;")
content = content.replace("padding-top: 6px !important;\n    }", "padding-top: 6px !important;\n    }\n    [data-testid=\"stTextArea\"] textarea:focus { border-color: #2e6fb0 !important; box-shadow: 0 0 0 1px #2e6fb0 !important; }")

with open("app.py", "w") as f:
    f.write(content)
