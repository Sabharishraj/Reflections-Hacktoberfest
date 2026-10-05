with open("app.py", "r") as f:
    text = f.read()

# We only want to replace {{ and }} with { and } in the latter half of the file (after line 300)
# because the first half contains the CSS block which genuinely needs {{ }}.
lines = text.split('\n')
for i in range(300, len(lines)):
    lines[i] = lines[i].replace('{{', '{').replace('}}', '}')

text = '\n'.join(lines)

with open("app.py", "w") as f:
    f.write(text)
