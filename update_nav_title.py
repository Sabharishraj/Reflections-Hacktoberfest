with open("app.py", "r") as f:
    text = f.read()

old_line = "st.markdown('<div style=\"font-family:\\'DM Serif Display\\',serif; font-size:20px; line-height:2.0; color:#faf7f0; text-transform:uppercase; font-weight:bold;\"><span style=\"color:#2e6fb0; margin-right:4px;\">●</span> REFLECTIONS</div>', unsafe_allow_html=True)"
new_line = "st.markdown('<div style=\"font-family:\\'DM Serif Display\\',serif; font-size:20px; line-height:2.0; color:#1a1a1a; text-transform:uppercase; font-weight:bold;\">REFLECTIONS</div>', unsafe_allow_html=True)"

text = text.replace(old_line, new_line)

with open("app.py", "w") as f:
    f.write(text)
