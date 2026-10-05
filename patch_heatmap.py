with open("heatmap.py", "r") as f:
    content = f.read()

content = content.replace("repeat(7, 14px)", "repeat(7, 18px)")
content = content.replace("width:14px; height:14px", "width:18px; height:18px")
content = content.replace("line-height:14px", "line-height:18px")

with open("heatmap.py", "w") as f:
    f.write(content)
