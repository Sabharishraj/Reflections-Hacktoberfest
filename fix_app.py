with open("app.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "Analysis</h4>" in line:
        new_lines.append("                    st.markdown('<h4 style=\"font-family: \\'DM Serif Display\\', serif;\">Analysis</h4>', unsafe_allow_html=True)\n")
    else:
        new_lines.append(line)

with open("app.py", "w") as f:
    f.writelines(new_lines)
