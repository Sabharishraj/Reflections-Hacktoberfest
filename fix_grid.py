import re

with open("app.py", "r") as f:
    text = f.read()

bad_grid = "background-image: repeating-linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px), repeating-linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px) !important;"
good_grid = "background-image: linear-gradient(rgba(0,0,0,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(0,0,0,0.07) 1px, transparent 1px) !important;"

text = text.replace(bad_grid, good_grid)

with open("app.py", "w") as f:
    f.write(text)
