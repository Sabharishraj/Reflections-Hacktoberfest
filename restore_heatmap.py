import re

with open("analysis.py", "r") as f:
    text = f.read()

old_c_left_end = """        st.markdown('</div>', unsafe_allow_html=True)


    st.markdown("<br><br>", unsafe_allow_html=True)"""

new_c_right = """        st.markdown('</div>', unsafe_allow_html=True)

    with c_right:
        st.markdown('<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a;">', unsafe_allow_html=True)
        st.markdown(section_header("Monthly Reflection Calendar"), unsafe_allow_html=True)
        st.html(heatmap.render_heatmap_html().replace('background:#faf7f0;', 'background:#ffffff;'))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)"""

text = text.replace(old_c_left_end, new_c_right)

with open("analysis.py", "w") as f:
    f.write(text)
