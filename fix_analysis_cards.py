import re

with open("analysis.py", "r") as f:
    text = f.read()

old_metrics = """    with col1:
        with st.container(border=True):
            st.markdown(f'<div class="card-label">Total Reflections</div><div class="card-value">{total_reflections if entries else "—"}</div>', unsafe_allow_html=True)
    with col2:
        with st.container(border=True):
            st.markdown(f'<div class="card-label">Dominant Emotion</div><div class="card-value" style="font-size:22px;">{dominant_emotion}</div>', unsafe_allow_html=True)
    with col3:
        with st.container(border=True):
            st.markdown(f'<div class="card-label">Reflection Days</div><div class="card-value">{reflection_days}</div><div style="color:#6b6b6b; font-size:13px;">This month</div>', unsafe_allow_html=True)
    with col4:
        with st.container(border=True):
            st.markdown(f'<div class="card-label">Avg Intensity</div><div class="card-value">{avg_intensity_str}</div><div style="color:#6b6b6b; font-size:13px;">Of maximum</div>', unsafe_allow_html=True)"""

new_metrics = """    with col1:
        st.markdown(f'<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a; min-height:120px;"><div style="font-size: 12px; text-transform: uppercase; letter-spacing: 2px; color: #6b6b6b; margin-bottom: 8px; font-weight: bold; font-variant: small-caps;">Total Reflections</div><div style="font-size: 28px; font-family: \\\'DM Serif Display\\\', serif; color: #1a1a1a; margin-bottom: 4px;">{total_reflections if entries else "—"}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a; min-height:120px;"><div style="font-size: 12px; text-transform: uppercase; letter-spacing: 2px; color: #6b6b6b; margin-bottom: 8px; font-weight: bold; font-variant: small-caps;">Dominant Emotion</div><div style="font-size: 22px; font-family: \\\'DM Serif Display\\\', serif; color: #1a1a1a; margin-bottom: 4px;">{dominant_emotion}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a; min-height:120px;"><div style="font-size: 12px; text-transform: uppercase; letter-spacing: 2px; color: #6b6b6b; margin-bottom: 8px; font-weight: bold; font-variant: small-caps;">Reflection Days</div><div style="font-size: 28px; font-family: \\\'DM Serif Display\\\', serif; color: #1a1a1a; margin-bottom: 4px;">{reflection_days}</div><div style="color:#6b6b6b; font-size:13px;">This month</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a; min-height:120px;"><div style="font-size: 12px; text-transform: uppercase; letter-spacing: 2px; color: #6b6b6b; margin-bottom: 8px; font-weight: bold; font-variant: small-caps;">Avg Intensity</div><div style="font-size: 28px; font-family: \\\'DM Serif Display\\\', serif; color: #1a1a1a; margin-bottom: 4px;">{avg_intensity_str}</div><div style="color:#6b6b6b; font-size:13px;">Of maximum</div></div>', unsafe_allow_html=True)"""

text = text.replace(old_metrics, new_metrics)

with open("analysis.py", "w") as f:
    f.write(text)
