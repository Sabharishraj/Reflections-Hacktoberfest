import re

with open("app.py", "r") as f:
    text = f.read()

bad_wildcard = """    /* Ensure no child elements accidentally inherit the transparent/grid background */
    [data-testid="stVerticalBlockBorderWrapper"] * {{
        background-image: none !important;
    }}"""

text = text.replace(bad_wildcard, "")

with open("app.py", "w") as f:
    f.write(text)
