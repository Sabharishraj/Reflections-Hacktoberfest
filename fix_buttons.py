import re

with open("app.py", "r") as f:
    text = f.read()

# Replace the nav button styling
old_nav_btn = """    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type button {
        box-shadow: none !important;
        border: none !important;
        background: transparent !important;
    }
    
    /* Nav links (Center/Right column) */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(2) button {
        font-family: 'DM Serif Display', serif !important;
        font-size: 16px !important;
        color: #1a1a1a !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(2) [data-testid="column"]:nth-child({active_idx}) button {
        color: #2e6fb0 !important;
        text-decoration: underline !important;
        text-decoration-thickness: 2px !important;
        text-underline-offset: 4px !important;
    }
    
    /* Action buttons (Far Right column) */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(3) button {
        border: 1px solid #2e6fb0 !important;
        color: #2e6fb0 !important;
        border-radius: 20px !important;
        font-size: 14px !important;
        padding: 2px 12px !important;
        font-family: sans-serif !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(3) button:hover {
        background: #2e6fb0 !important;
        color: #ffffff !important;
    }"""

new_nav_btn = """    /* All buttons in nav */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type button {
        background: #ffffff !important;
        border: 2px solid #1a1a1a !important;
        color: #1a1a1a !important;
        border-radius: 20px !important;
        font-size: 14px !important;
        padding: 4px 16px !important;
        box-shadow: 2px 2px 0 rgba(0,0,0,0.1) !important;
        transition: all 0.2s !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type button:hover {
        background: #2e6fb0 !important;
        color: #ffffff !important;
        border-color: #2e6fb0 !important;
    }
    
    /* Home/Analysis Active state */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(2) [data-testid="column"]:nth-child({active_idx}) button {
        background: #2e6fb0 !important;
        color: #ffffff !important;
        border-color: #2e6fb0 !important;
    }"""

text = text.replace(old_nav_btn, new_nav_btn)

with open("app.py", "w") as f:
    f.write(text)
