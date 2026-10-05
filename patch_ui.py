import re

with open("app.py", "r") as f:
    content = f.read()

# Fix 1: section_header
old_header = """def section_header(num, title):
    wavy_svg = '''<svg width="60" height="8" viewBox="0 0 60 8" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 4 Q 10 0, 20 4 T 40 4 T 60 4" stroke="#1a1a1a" stroke-width="2" stroke-linecap="round"/></svg>'''
    return f'<h3 style="display:flex; align-items:center; margin-bottom:0;"><span class="sec-badge">{num}</span> {title}</h3><div style="margin: 4px 0 24px 44px;">{wavy_svg}</div>'"""
new_header = """def section_header(title):
    wavy_svg = '''<svg width="60" height="8" viewBox="0 0 60 8" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 4 Q 10 0, 20 4 T 40 4 T 60 4" stroke="#1a1a1a" stroke-width="2" stroke-linecap="round"/></svg>'''
    return f'<h3 style="display:flex; align-items:center; margin-bottom:0;">{title}</h3><div style="margin: 4px 0 24px 0;">{wavy_svg}</div>'"""
content = content.replace(old_header, new_header)

content = content.replace('section_header("01", "Dashboard")', 'section_header("Dashboard")')
content = content.replace('section_header("02", "Pattern Insights")', 'section_header("Pattern Insights")')
content = content.replace('section_header("03", "New Entry")', 'section_header("New Entry")')
content = content.replace('section_header("04", "Similar Moments in Your Past")', 'section_header("Similar Moments in Your Past")')
content = content.replace('section_header("04", "You\'ve been through something like this before")', 'section_header("You\'ve been through something like this before")')


# Fix 4: Scaling up CSS
content = content.replace("p, li { font-size: 15px; color: #6b6b6b; }", "p, li { font-size: 17px; color: #6b6b6b; }")
content = content.replace(".stApp {", '[data-testid="block-container"] { max-width: 1400px; width: 95%; margin: 0 auto; padding-top: 2rem; }\n.stApp {')
content = content.replace("h3 { font-size: 24px !important;", "h3 { font-size: 30px !important;")
content = content.replace(".scrap-card {\n    background: #ffffff;", ".scrap-card {\n    background: #ffffff;\n    min-height: 180px;")
content = content.replace("padding: 16px;\n    box-shadow:", "padding: 24px;\n    box-shadow:")
content = content.replace(".card-label { font-size: 11px;", ".card-label { font-size: 12px;")
content = content.replace(".card-value { font-size: 24px;", ".card-value { font-size: 28px;")
content = content.replace("height: 180px !important;", "height: 260px !important;")
content = content.replace("font-size: 15px !important;", "font-size: 17px !important;")
content = content.replace("padding: 12px !important;", "padding: 12px 32px !important;")

content = content.replace("font-size: 42px;", "font-size: 44px;")

# Fix 2 & 3: Hero layout
old_hero = """<div style="background: #ffffff; border: 2px solid #1a1a1a; padding: 32px; border-radius: 4px; box-shadow: 6px 6px 0 rgba(0,0,0,0.15); margin-bottom: 48px; display: flex; justify-content: space-between; align-items: center; position: relative; overflow: hidden;">
    <div>
        <h1 style="font-size: 44px; margin: 0; line-height: 1.1;">AI <span class="highlight">Reflection</span> Journal</h1>
        <p style="margin: 8px 0 0 0; color: #6b6b6b; font-size: 16px;">Discover patterns in your daily life.</p>
    </div>
    <div style="display: flex; align-items: center; gap: 16px; border-left: 2px dashed #1a1a1a; padding-left: 24px; max-width: 320px;">
        {prop_img('marcus.png', rotation=2, height=70)}
        <div style="font-family: 'DM Serif Display', serif; font-style: italic; color: #6b6b6b; font-size: 15px; line-height: 1.3;">
            "Meditations — the original private journal, never meant to be read by anyone else."
        </div>
    </div>
</div>"""

new_hero = """<div style="background: #ffffff; border: 2px solid #1a1a1a; padding: 32px; border-radius: 4px; box-shadow: 6px 6px 0 rgba(0,0,0,0.15); margin-bottom: 48px; display: flex; justify-content: space-between; align-items: center; position: relative; overflow: hidden;">
    <div style="flex: 1;">
        <h1 style="font-size: 44px; margin: 0; line-height: 1.1;">AI <span class="highlight">Reflection</span> Journal</h1>
        <p style="margin: 8px 0 0 0; color: #6b6b6b; font-size: 17px;">Discover patterns in your daily life.</p>
    </div>
    <div style="display: flex; align-items: center; gap: 24px; border-left: 2px dashed #1a1a1a; padding-left: 24px; max-width: 400px;">
        {prop_img('marcus.png', rotation=2, height=140)}
        <div style="font-family: 'DM Serif Display', serif; font-style: italic; color: #6b6b6b; font-size: 17px; line-height: 1.3;">
            "Meditations — the original private journal, never meant to be read by anyone else."
        </div>
    </div>
</div>"""
content = content.replace(old_hero, new_hero)

# Pattern Insights Layout
old_pattern = """<div style="position:relative; margin: 16px 0 32px 0;">
        <div style="position:absolute; top:-30px; right:10px; z-index:10; display:flex; flex-direction:column; align-items:center; gap:4px; max-width:150px; text-align:center;">
            <div style="background: white; border: 2px solid #1a1a1a; padding: 6px 10px; border-radius: 12px; font-size: 11px; box-shadow: 2px 2px 0 rgba(0,0,0,0.15);">"Knowing yourself is the beginning of all wisdom."<br><span style="font-variant: small-caps; color:#6b6b6b; font-weight:bold;">— Aristotle</span></div>
            {prop_img('aristotle.png', rotation=1, height=80)}
        </div>
        <div class="sticky-note" style="transform: rotate(-1deg);">
            <p style="font-size: 16px; margin: 8px 0 16px 0; max-width: 80%;">Based on your past entries, you frequently mention <strong style="color:#1a1a1a;">{most_common_trigger}</strong> in situations associated with feeling <strong style="color:#1a1a1a;">{most_common_emotion}</strong>.</p>
            {meander_svg}
        </div>
    </div>"""

new_pattern = """<div class="sticky-note" style="transform: rotate(-1deg); display: flex; justify-content: space-between; align-items: center; padding: 32px; margin: 16px 0 32px 0;">
        <div style="flex: 1; padding-right: 24px;">
            <p style="font-size: 17px; margin: 0 0 16px 0;">Based on your past entries, you frequently mention <strong style="color:#1a1a1a;">{most_common_trigger}</strong> in situations associated with feeling <strong style="color:#1a1a1a;">{most_common_emotion}</strong>.</p>
            <div style="font-family: 'DM Serif Display', serif; font-size: 18px; color:#1a1a1a;">"Knowing yourself is the beginning of all wisdom."</div>
            <div style="font-variant: small-caps; color:#6b6b6b; font-weight:bold; font-size: 14px; margin-top: 4px;">— Aristotle</div>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
            {prop_img('aristotle.png', rotation=1, height=130)}
        </div>
        {meander_svg}
    </div>"""
content = content.replace(old_pattern, new_pattern)

# New Entry Layout
old_new_entry = """st.markdown(section_header("New Entry"), unsafe_allow_html=True)
st.markdown(f\"\"\"
<div style="position:relative; margin-bottom: 8px;">
    <div style="position:absolute; bottom:-10px; left:-20px; z-index:10; display:flex; flex-direction:column; align-items:center;">
         <div style="background: white; border: 2px solid #1a1a1a; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; box-shadow: 2px 2px 0 rgba(0,0,0,0.15); margin-bottom: 4px;">Think it through.</div>
         {prop_img('thinker.png', rotation=-2, height=80)}
    </div>
</div>
\"\"\", unsafe_allow_html=True)"""

new_new_entry = """st.markdown(f\"\"\"
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
    <div style="flex: 1;">
        {section_header("New Entry")}
    </div>
    <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
        {prop_img('thinker.png', rotation=-2, height=150)}
        <div style="font-size: 12px; color: #6b6b6b; font-style: italic; font-weight: bold;">Think it through.</div>
    </div>
</div>
\"\"\", unsafe_allow_html=True)"""
content = content.replace(old_new_entry, new_new_entry)


with open("app.py", "w") as f:
    f.write(content)

