with open("app.py", "r") as f:
    text = f.read()

# Replace tape class
old_tape = '<div class="tape"></div>'
new_tape = '<div style="position: absolute; background: rgba(255, 217, 102, 0.6); width: 80px; height: 24px; top: -5px; left: -10px; transform: rotate(35deg); box-shadow: 1px 1px 3px rgba(0,0,0,0.1); border: 1px solid rgba(0,0,0,0.05); z-index: 10; pointer-events: none; clip-path: polygon(0% 5%, 5% 0%, 95% 5%, 100% 15%, 98% 85%, 95% 100%, 5% 95%, 0% 90%);"></div>'
text = text.replace(old_tape, new_tape)

# Replace card-label and card-value classes
text = text.replace('<div class="card-label">', '<div style="font-size: 12px; text-transform: uppercase; letter-spacing: 2px; color: #6b6b6b; margin-bottom: 8px; font-weight: bold; font-variant: small-caps;">')
text = text.replace('<div class="card-value">', '<div style="font-size: 28px; font-family: \\\'DM Serif Display\\\', serif; color: #1a1a1a; margin-bottom: 4px;">')

with open("app.py", "w") as f:
    f.write(text)
