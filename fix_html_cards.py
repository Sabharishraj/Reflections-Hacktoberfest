import re

with open("app.py", "r") as f:
    text = f.read()

# DASHBOARD CARDS
old_dash = """        with col1:
            with st.container(border=True):
                intensity_html = f'<div style="color:#6b6b6b; font-size:13px;">Intensity: {today_intensity}</div>' if today_intensity.lower() not in ['low', 'none'] else ''
                st.markdown(f'<div class="tape"></div><div class="card-label">Today</div><div class="card-value">{today_emotion.capitalize()}</div>{intensity_html}', unsafe_allow_html=True)
        with col2:
            with st.container(border=True):
                st.markdown(f'<div class="card-label">Top Emotion</div><div class="card-value">{most_common_emotion.capitalize()}</div>', unsafe_allow_html=True)
        with col3:
            with st.container(border=True):
                st.markdown(f'<div class="card-label">Top Trigger</div><div class="card-value">{most_common_trigger.capitalize()}</div>', unsafe_allow_html=True)
        with col4:
            with st.container(border=True):
                day_word = "day" if total_days == 1 else "days"
                st.markdown(f'<div class="card-label">History</div><div class="card-value">{total_days}</div><div style="color:#6b6b6b; font-size:13px;">{day_word} this month</div>', unsafe_allow_html=True)"""

new_dash = """        with col1:
            intensity_html = f'<div style="color:#6b6b6b; font-size:13px;">Intensity: {today_intensity}</div>' if today_intensity.lower() not in ['low', 'none'] else ''
            st.markdown(f'<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a; position:relative; min-height:140px;"><div class="tape"></div><div class="card-label">Today</div><div class="card-value">{today_emotion.capitalize()}</div>{intensity_html}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a; position:relative; min-height:140px;"><div class="card-label">Top Emotion</div><div class="card-value">{most_common_emotion.capitalize()}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a; position:relative; min-height:140px;"><div class="card-label">Top Trigger</div><div class="card-value">{most_common_trigger.capitalize()}</div></div>', unsafe_allow_html=True)
        with col4:
            day_word = "day" if total_days == 1 else "days"
            st.markdown(f'<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a; position:relative; min-height:140px;"><div class="card-label">History</div><div class="card-value">{total_days}</div><div style="color:#6b6b6b; font-size:13px;">{day_word} this month</div></div>', unsafe_allow_html=True)"""
text = text.replace(old_dash, new_dash)

# PATTERN INSIGHTS
old_pattern = """        if len(all_entries) < 5:
            with st.container(border=True):
                st.write("Keep writing — patterns emerge after a few more entries.")
        else:
            with st.container(border=True):
                meander_svg = '''<svg width="100%" height="8" style="position:absolute; bottom:0; left:0;"><pattern id="meander" x="0" y="0" width="20" height="8" patternUnits="userSpaceOnUse"><path d="M0,0 h16 v8 h-4 v-4 h-8 v8" fill="none" stroke="#1a1a1a" stroke-width="2"/></pattern><rect width="100%" height="8" fill="url(#meander)"/></svg>'''
                st.markdown(f'''
                <div class="is-sticky"></div>
                <div style="padding: 12px; position:relative; padding-bottom: 24px;">
                    <p style="font-size: 17px; margin: 0 0 16px 0; color: #1a1a1a;">Based on your past entries, you frequently mention <strong style="color:#1a1a1a; background:rgba(255,217,102,0.5); padding:0 4px;">{most_common_trigger}</strong> in situations associated with feeling <strong style="color:#1a1a1a; background:rgba(255,217,102,0.5); padding:0 4px;">{most_common_emotion}</strong>.</p>
                    <div style="font-family: 'DM Serif Display', serif; font-size: 18px; color:#1a1a1a;">"Knowing yourself is the beginning of all wisdom."</div>
                    <div style="font-variant: small-caps; color:#6b6b6b; font-weight:bold; font-size: 12px; margin-top: 4px;">— Aristotle</div>
                    {meander_svg}
                </div>
                ''', unsafe_allow_html=True)"""

new_pattern = """        if len(all_entries) < 5:
            st.markdown('<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a; position:relative;">Keep writing — patterns emerge after a few more entries.</div>', unsafe_allow_html=True)
        else:
            meander_svg = '''<svg width="100%" height="8" style="position:absolute; bottom:0; left:0; border-bottom-left-radius:10px; border-bottom-right-radius:10px; overflow:hidden;"><pattern id="meander" x="0" y="0" width="20" height="8" patternUnits="userSpaceOnUse"><path d="M0,0 h16 v8 h-4 v-4 h-8 v8" fill="none" stroke="#1a1a1a" stroke-width="2"/></pattern><rect width="100%" height="8" fill="url(#meander)"/></svg>'''
            st.markdown(f'''
            <div style="background:#fff3bf; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:24px; color:#1a1a1a; position:relative; transform: rotate(-1deg); margin-bottom: 16px;">
                <div style="position: absolute; top: 8px; left: 50%; transform: translateX(-50%); width: 12px; height: 12px; background: #e05252; border-radius: 50%; border: 2px solid #1a1a1a; box-shadow: 2px 2px 0 rgba(0,0,0,0.1);"></div>
                <div style="position:relative; padding-bottom: 24px;">
                    <p style="font-size: 17px; margin: 0 0 16px 0; color: #1a1a1a;">Based on your past entries, you frequently mention <strong style="color:#1a1a1a; background:rgba(255,217,102,0.5); padding:0 4px;">{most_common_trigger}</strong> in situations associated with feeling <strong style="color:#1a1a1a; background:rgba(255,217,102,0.5); padding:0 4px;">{most_common_emotion}</strong>.</p>
                    <div style="font-family: 'DM Serif Display', serif; font-size: 18px; color:#1a1a1a;">"Knowing yourself is the beginning of all wisdom."</div>
                    <div style="font-variant: small-caps; color:#6b6b6b; font-weight:bold; font-size: 12px; margin-top: 4px;">— Aristotle</div>
                </div>
                {meander_svg}
            </div>
            ''', unsafe_allow_html=True)"""
text = text.replace(old_pattern, new_pattern)

with open("app.py", "w") as f:
    f.write(text)
