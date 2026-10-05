import re

with open("analysis.py", "r") as f:
    text = f.read()

bad_block = """        
    with c_right:
        with st.container(border=True):
            st.markdown(section_header("Monthly Reflection Calendar"), unsafe_allow_html=True)
            st.html(heatmap.render_heatmap_html().replace('background:#faf7f0;', 'background:#ffffff;'))"""

text = text.replace(bad_block, "")

with open("analysis.py", "w") as f:
    f.write(text)
