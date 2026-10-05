import re

with open("app.py", "r") as f:
    content = f.read()

# Remove imports and old helpers up to st.markdown("""
# Let's locate the st.cache_resource def
start_idx = content.find("@st.cache_resource")
style_idx = content.find('st.markdown("""\n<style>')

if start_idx != -1 and style_idx != -1:
    new_top = """@st.cache_resource
def get_cached_index_and_rows():
    return search.build_index()

from props import prop_img, section_header

if 'nav' not in st.session_state:
    st.session_state.nav = 'home'

def render_nav():
    active_idx = 1 if st.session_state.nav == 'home' else 2
    st.markdown(f'''
    <style>
    /* Nav bar styling */
    [data-testid="stHorizontalBlock"]:first-of-type {{
        justify-content: center;
        gap: 16px;
        margin-bottom: 24px;
        padding-top: 10px;
    }}
    [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] {{
        width: auto !important;
        flex: 0 1 auto !important;
    }}
    [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] [data-testid="baseButton-secondary"] {{
        background: #ffffff !important;
        color: #1a1a1a !important;
        font-family: 'DM Serif Display', serif !important;
        font-size: 18px !important;
        border: 2px solid #1a1a1a !important;
        border-radius: 40px !important;
        padding: 8px 32px !important;
        box-shadow: none !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
        width: auto !important;
    }}
    [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:nth-child({active_idx}) [data-testid="baseButton-secondary"] {{
        background: #2e6fb0 !important;
        color: #ffffff !important;
        box-shadow: 3px 3px 0 #1a1a1a !important;
    }}
    [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] [data-testid="baseButton-secondary"]:hover {{
        transform: translate(-2px, -2px) !important;
        box-shadow: 3px 3px 0 #1a1a1a !important;
    }}
    </style>
    ''', unsafe_allow_html=True)
    
    cols = st.columns([1, 1])
    with cols[0]:
        if st.button("Home"):
            st.session_state.nav = 'home'
            st.rerun()
    with cols[1]:
        if st.button("Analysis"):
            st.session_state.nav = 'analysis'
            st.rerun()

"""
    content = content[:start_idx] + new_top + content[style_idx:]

# Now, right after db.init_db() and before rendering anything, wait.
# The layout starts with styles, then all_entries, then rendering.
# We need to render_nav() BEFORE the first element on the main page.
# The first element is the hero: st.markdown(f""" <div style="background: #ffffff;...
hero_idx = content.find('st.markdown(f"""\n<div style="background: #ffffff; border: 2px solid #1a1a1a; padding: 32px;')
if hero_idx != -1:
    content = content[:hero_idx] + "render_nav()\n\nif st.session_state.nav == 'home':\n    " + content[hero_idx:].replace('\n', '\n    ')
    # This indented EVERYTHING below. But wait, st.markdown('<div style="text-align:center; ... at the very end shouldn't be inside the if if we want it global. Let's just indent it all.

with open("app.py", "w") as f:
    f.write(content)

