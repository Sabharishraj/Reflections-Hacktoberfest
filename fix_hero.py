with open("app.py", "r") as f:
    text = f.read()

old_hero = """    with st.container(border=True):
        st.markdown(f'''
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">
                <h1 style="font-size: 44px; margin: 0; line-height: 1.1;">AI <span class="highlight">Reflection</span> Journal</h1>
                <p style="margin: 8px 0 0 0; color: #6b6b6b; font-size: 17px;">Discover patterns in your daily life.</p>
            </div>
            <div style="display: flex; align-items: center; gap: 24px;">
                {prop_img('marcus.png', height=140)}
                <div style="font-family: 'DM Serif Display', serif; font-style: italic; color: #6b6b6b; font-size: 17px; line-height: 1.3; max-width: 250px;">
                    "Meditations — the original private journal, never meant to be read by anyone else."
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)"""

new_hero = """    st.markdown(f'''
    <div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:24px; color:#1a1a1a;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">
                <h1 style="font-size: 44px; margin: 0; line-height: 1.1;">AI <span style="background-color: #ffd966; padding: 0 4px; border-radius: 2px;">Reflection</span> Journal</h1>
                <p style="margin: 8px 0 0 0; color: #6b6b6b; font-size: 17px;">Discover patterns in your daily life.</p>
            </div>
            <div style="display: flex; align-items: center; gap: 24px;">
                {prop_img('marcus.png', height=140)}
                <div style="font-family: 'DM Serif Display', serif; font-style: italic; color: #6b6b6b; font-size: 17px; line-height: 1.3; max-width: 250px;">
                    "Meditations — the original private journal, never meant to be read by anyone else."
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)"""

text = text.replace(old_hero, new_hero)

with open("app.py", "w") as f:
    f.write(text)
