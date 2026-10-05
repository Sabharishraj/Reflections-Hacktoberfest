import re

with open("app.py", "r") as f:
    content = f.read()

# Add h3 size
content = content.replace("h1, h2, h3, h4 { font-family:", "h3 { font-size: 30px !important; margin-bottom: 8px !important; }\nh1, h2, h3, h4 { font-family:")

# Add font-size 19px to button
old_btn = 'padding: 12px 32px !important; font-weight: bold'
new_btn = 'padding: 12px 32px !important; font-size: 19px !important; font-weight: bold'
content = content.replace(old_btn, new_btn)

with open("app.py", "w") as f:
    f.write(content)
