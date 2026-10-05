with open("app.py", "r") as f:
    text = f.read()

text = text.replace(
    "padding-top: 6px !important;\n    }\n    [data-testid=\"stTextArea\"] textarea:focus { border-color: #2e6fb0 !important; box-shadow: 0 0 0 1px #2e6fb0 !important; }}",
    "padding-top: 6px !important;\n    }}\n    [data-testid=\"stTextArea\"] textarea:focus {{ border-color: #2e6fb0 !important; box-shadow: 0 0 0 1px #2e6fb0 !important; }}"
)

with open("app.py", "w") as f:
    f.write(text)
