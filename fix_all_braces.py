import re

with open("app.py", "r") as f:
    text = f.read()

# We need to find the f''' block for styles in render_nav()
# and ensure all braces are doubled.
# Note: we have `{active_idx}` which MUST remain `{active_idx}`.

# Strategy: 
# 1. Extract the style block
# 2. Replace {{ with {, }} with } to normalize
# 3. Replace { with {{, } with }} to escape everything
# 4. Replace {{active_idx}} back to {active_idx}
# 5. Put it back into text

start = text.find("<style>")
end = text.find("</style>") + len("</style>")

if start != -1 and end != -1:
    style_block = text[start:end]
    
    # Normalize
    style_block = style_block.replace("{{", "{").replace("}}", "}")
    
    # Escape
    style_block = style_block.replace("{", "{{").replace("}", "}}")
    
    # Restore the python variable substitution
    style_block = style_block.replace("{{active_idx}}", "{active_idx}")
    
    text = text[:start] + style_block + text[end:]

with open("app.py", "w") as f:
    f.write(text)
