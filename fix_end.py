with open("app.py", "r") as f:
    text = f.read()

bad = """    elif st.session_state.nav == 'analysis':
    import analysis
    analysis.render_analysis()
    st.markdown('<div style="text-align:center; color:#6b6b6b; font-family: monospace; font-size:12px; margin-top:80px; margin-bottom:40px;">* All data stays on this device. Nothing is sent to the cloud.</div>', unsafe_allow_html=True)
"""
good = """elif st.session_state.nav == 'analysis':
    import analysis
    analysis.render_analysis()
    st.markdown('<div style="text-align:center; color:#6b6b6b; font-family: monospace; font-size:12px; margin-top:80px; margin-bottom:40px;">* All data stays on this device. Nothing is sent to the cloud.</div>', unsafe_allow_html=True)
"""
text = text.replace(bad, good)

# also check if there's any stray EOF newlines
text = text.replace("    elif st.session_state.nav == 'analysis':\n    import analysis\n", "elif st.session_state.nav == 'analysis':\n    import analysis\n")

with open("app.py", "w") as f:
    f.write(text)
