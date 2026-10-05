import re

for folder in ["hackathon_journal", "hackathon_journal copy"]:
    path = f"../{folder}/analysis.py"
    try:
        with open(path, "r") as f:
            text = f.read()
            
        old_code = "st.markdown(triggers_html, unsafe_allow_html=True)"
        new_code = "st.html(triggers_html)"
        
        text = text.replace(old_code, new_code)
        
        with open(path, "w") as f:
            f.write(text)
    except Exception as e:
        print(f"Failed for {folder}: {e}")

