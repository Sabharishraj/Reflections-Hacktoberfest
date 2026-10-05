import re

for folder in ["hackathon_journal", "hackathon_journal copy"]:
    path = f"../{folder}/analysis.py"
    try:
        with open(path, "r") as f:
            text = f.read()
            
        old_code = """        if all_triggers:
            top_triggers = Counter(all_triggers).most_common(5)
            for t, c in top_triggers:
                triggers_html += f'''
                <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px dashed rgba(26,26,26,0.2); padding: 12px 0;">
                    <div style="font-size: 17px; font-weight: bold; color: #1a1a1a; text-transform: capitalize;">{t}</div>
                    <div style="background: #2e6fb0; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; border: 2px solid #1a1a1a;">{c}</div>
                </div>
                '''
        else:
            triggers_html = '<div style="color: #6b6b6b;">No triggers recorded yet.</div>'

        st.html(triggers_html)"""

        new_code = """        if all_triggers:
            top_triggers = Counter(all_triggers).most_common(5)
            for t, c in top_triggers:
                # No leading spaces inside the HTML block to prevent Markdown code-block escaping
                triggers_html += f'''<div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px dashed rgba(26,26,26,0.2); padding: 12px 0;">
<div style="font-size: 17px; font-weight: bold; color: #1a1a1a; text-transform: capitalize;">{t}</div>
<div style="background: #2e6fb0; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; border: 2px solid #1a1a1a;">{c}</div>
</div>'''
        else:
            triggers_html = '<div style="color: #6b6b6b;">No triggers recorded yet.</div>'

        st.markdown(triggers_html, unsafe_allow_html=True)"""
        
        # If it already had st.markdown(triggers_html, unsafe_allow_html=True) but indented...
        text = text.replace(old_code, new_code)
        
        with open(path, "w") as f:
            f.write(text)
    except Exception as e:
        print(f"Failed for {folder}: {e}")

