with open("app.py", "r") as f:
    text = f.read()

text = text.replace(
    '[data-testid="stMarkdownContainer"] { color: #1a1a1a !important; }',
    '[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] * { color: #1a1a1a !important; }'
)

with open("app.py", "w") as f:
    f.write(text)
