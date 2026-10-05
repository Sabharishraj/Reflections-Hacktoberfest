with open("analysis.py", "r") as f:
    text = f.read()

text = text.replace(
    'st.markdown(\'<h4 style="margin:0 0 8px 0; font-family:\\\'DM Serif Display\\\', serif;">Emotion Frequency</h4>\', unsafe_allow_html=True)',
    'st.markdown(section_header("Emotion Frequency"), unsafe_allow_html=True)'
)
text = text.replace(
    'st.markdown(\'<h4 style="margin:0 0 16px 0; font-family:\\\'DM Serif Display\\\', serif;">Monthly Reflection Calendar</h4>\', unsafe_allow_html=True)',
    'st.markdown(section_header("Monthly Reflection Calendar"), unsafe_allow_html=True)'
)

with open("analysis.py", "w") as f:
    f.write(text)
