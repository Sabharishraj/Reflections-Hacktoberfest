import re

with open("app.py", "r") as f:
    content = f.read()

old_block = r'<div style="position:relative; margin: 16px 0 32px 0;">\s*<div style="position:absolute.*?{prop_img\(\'aristotle\.png\', rotation=1, height=80\)}\s*</div>\s*<div class="sticky-note"[^>]*>\s*<p.*?</p>\s*{meander_svg}\s*</div>\s*</div>'

new_block = """<div class="sticky-note" style="transform: rotate(-1deg); display: flex; justify-content: space-between; align-items: center; padding: 32px; margin: 16px 0 32px 0;">
    <div style="flex: 1; padding-right: 24px;">
        <p style="font-size: 17px; margin: 0 0 16px 0; color: #6b6b6b;">Based on your past entries, you frequently mention <strong style="color:#1a1a1a;">{most_common_trigger}</strong> in situations associated with feeling <strong style="color:#1a1a1a;">{most_common_emotion}</strong>.</p>
        <div style="font-family: 'DM Serif Display', serif; font-size: 18px; color:#1a1a1a;">"Knowing yourself is the beginning of all wisdom."</div>
        <div style="font-variant: small-caps; color:#6b6b6b; font-weight:bold; font-size: 14px; margin-top: 4px;">— Aristotle</div>
    </div>
    <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
        {prop_img('aristotle.png', rotation=1, height=130)}
    </div>
    {meander_svg}
</div>"""

content = re.sub(old_block, new_block, content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)
