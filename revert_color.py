with open("app.py", "r") as f:
    text = f.read()

text = text.replace(
    '[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] * { color: #1a1a1a !important; }',
    '[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] span, [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3, [data-testid="stMarkdownContainer"] h4, [data-testid="stMarkdownContainer"] div { color: #1a1a1a; }'
)

with open("app.py", "w") as f:
    f.write(text)
