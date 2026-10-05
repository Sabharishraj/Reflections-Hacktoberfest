import re

with open("app.py", "r") as f:
    text = f.read()

bad_footer = """st.markdown('<div class="footer-actions" style="display:flex; justify-content:center; gap:16px; margin-top:60px;">', unsafe_allow_html=True)
fc1, fc2, fc3, fc4 = st.columns([3, 1, 1, 3])
with fc2:
    if st.button("Load Demo Data"):
        seed.load_demo_data()
        st.rerun()
with fc3:
    if st.button("Clear All Data"):
        seed.clear_all_data()
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)"""

good_footer = """st.markdown('<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="is-footer"></div>', unsafe_allow_html=True)
    fc1, fc2, fc3, fc4 = st.columns([3, 1, 1, 3])
    with fc2:
        if st.button("Load Demo Data"):
            seed.load_demo_data()
            st.rerun()
    with fc3:
        if st.button("Clear All Data"):
            seed.clear_all_data()
            st.rerun()"""
text = text.replace(bad_footer, good_footer)

bad_css = """    /* 8. FOOTER STICKER BUTTONS */
    .footer-actions [data-testid="baseButton-secondary"] {"""
good_css = """    /* 8. FOOTER STICKER BUTTONS */
    [data-testid="stVerticalBlock"]:has(.is-footer) [data-testid="baseButton-secondary"] {"""
text = text.replace(bad_css, good_css)

bad_css2 = """    .footer-actions [data-testid="baseButton-secondary"]:active {"""
good_css2 = """    [data-testid="stVerticalBlock"]:has(.is-footer) [data-testid="baseButton-secondary"]:active {"""
text = text.replace(bad_css2, good_css2)

with open("app.py", "w") as f:
    f.write(text)
