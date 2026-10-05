import re

with open("app.py", "r") as f:
    text = f.read()

# 1. We need to update the CSS for the nav bar (6. THE TOP NAV CONTAINER SPECIFICS)
old_nav_css = """    /* 6. THE TOP NAV CONTAINER SPECIFICS */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type {
        padding: 12px 24px !important;
        margin-bottom: 24px !important;
        transform: none !important;
    }
    
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Home/Analysis Links */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(2) button {
        font-family: 'DM Serif Display', serif !important;
        font-size: 16px !important;
        color: #1a1a1a !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(2) [data-testid="column"]:nth-child({active_idx}) button {
        color: #2e6fb0 !important;
        text-decoration: underline !important;
        text-decoration-thickness: 2px !important;
        text-underline-offset: 4px !important;
    }
    
    /* Demo/Clear Actions */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(3) button {
        background: #ffffff !important;
        border: 2px solid #1a1a1a !important;
        color: #1a1a1a !important;
        border-radius: 20px !important;
        font-size: 14px !important;
        padding: 4px 12px !important;
        font-family: sans-serif !important;
        box-shadow: 2px 2px 0 rgba(0,0,0,0.15) !important;
        transition: all 0.2s !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(3) button:hover {
        background: #2e6fb0 !important;
        color: #ffffff !important;
    }"""

new_nav_css = """    /* 6. BRUTALIST BLACK NAV BAR */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type {
        background-color: #0a0a0a !important;
        background-image: none !important;
        border: 3px solid #1a1a1a !important;
        border-radius: 999px !important;
        box-shadow: 6px 6px 0 #1a1a1a !important;
        padding: 14px 28px !important;
        margin-bottom: 24px !important;
        transform: none !important;
    }
    
    /* All buttons in the black nav bar */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        font-family: sans-serif !important;
        font-size: 16px !important;
        color: #faf7f0 !important;
        text-transform: uppercase !important;
        font-weight: bold !important;
        padding: 6px 16px !important;
        transition: all 0.15s !important;
    }
    
    /* Inactive Hover */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type button:hover {
        text-decoration: underline !important;
        text-decoration-thickness: 2px !important;
        text-underline-offset: 4px !important;
        color: #faf7f0 !important;
    }
    
    /* Active Link State */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(2) [data-testid="column"]:nth-child({active_idx}) button {
        background-color: #faf7f0 !important;
        color: #0a0a0a !important;
        border-radius: 999px !important;
        transform: rotate(-1deg) !important;
        text-decoration: none !important;
    }
    
    /* 8. FOOTER STICKER BUTTONS */
    .footer-actions [data-testid="baseButton-secondary"] {
        background-color: #ffffff !important;
        border: 2px solid #1a1a1a !important;
        color: #1a1a1a !important;
        border-radius: 4px !important;
        padding: 6px 16px !important;
        font-family: sans-serif !important;
        font-weight: bold !important;
        box-shadow: 3px 3px 0 #1a1a1a !important;
        transition: all 0.1s !important;
    }
    .footer-actions [data-testid="baseButton-secondary"]:active {
        transform: translate(2px, 2px) !important;
        box-shadow: 1px 1px 0 #1a1a1a !important;
    }"""
text = text.replace(old_nav_css, new_nav_css)

# 2. Update the Python structure of render_nav()
old_render_nav_py = """    with st.container(border=True):
        col_title, col_links, col_actions = st.columns([3, 2, 2])
        with col_title:
            st.markdown('<div style="font-family:\\'DM Serif Display\\',serif; font-size:20px; line-height:2.0; color:#1a1a1a;"><span style="color:#2e6fb0;">●</span> AI Reflection Journal</div>', unsafe_allow_html=True)
        with col_links:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Home"):
                    st.session_state.nav = 'home'
                    st.rerun()
            with c2:
                if st.button("Analysis"):
                    st.session_state.nav = 'analysis'
                    st.rerun()
        with col_actions:
            c3, c4 = st.columns(2)
            with c3:
                if st.button("Load Demo"):
                    seed.load_demo_data()
                    st.rerun()
            with c4:
                if st.button("Clear Data"):
                    seed.clear_all_data()
                    st.rerun()"""

# Left side: app title. Right side: home / analysis. The prompt says "28px apart" which we can manage by the columns.
# We have a 2-column layout now for the nav. Let's use [1, 1].
new_render_nav_py = """    with st.container(border=True):
        col_title, col_links = st.columns([2, 1])
        with col_title:
            st.markdown('<div style="font-family:\\'DM Serif Display\\',serif; font-size:20px; line-height:2.0; color:#faf7f0; text-transform:uppercase; font-weight:bold;"><span style="color:#2e6fb0; margin-right:4px;">●</span> AI REFLECTION JOURNAL</div>', unsafe_allow_html=True)
        with col_links:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Home"):
                    st.session_state.nav = 'home'
                    st.rerun()
            with c2:
                if st.button("Analysis"):
                    st.session_state.nav = 'analysis'
                    st.rerun()"""
text = text.replace(old_render_nav_py, new_render_nav_py)

# 3. Add footer buttons above the privacy caption
old_footer = "st.markdown('''<div style=\"text-align:center; color:#6b6b6b; font-family: monospace; font-size:12px; margin-top:80px; margin-bottom:40px;\">* All data stays on this device. Nothing is sent to the cloud.</div>''', unsafe_allow_html=True)"

new_footer = """st.markdown('<div class="footer-actions" style="display:flex; justify-content:center; gap:16px; margin-top:60px;">', unsafe_allow_html=True)
fc1, fc2, fc3, fc4 = st.columns([3, 1, 1, 3])
with fc2:
    if st.button("Load Demo Data"):
        seed.load_demo_data()
        st.rerun()
with fc3:
    if st.button("Clear All Data"):
        seed.clear_all_data()
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
""" + old_footer

text = text.replace(old_footer, new_footer)

with open("app.py", "w") as f:
    f.write(text)
