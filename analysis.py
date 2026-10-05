import streamlit as st
import db
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from collections import Counter
import heatmap
from props import prop_img, section_header

def render_analysis():
    entries = db.get_all_entries()
    
    st.markdown(f"""
    <div style="background: #ffffff; border: 2px solid #1a1a1a; padding: 32px; border-radius: 4px; box-shadow: 6px 6px 0 rgba(0,0,0,0.15); margin-bottom: 48px; display: flex; justify-content: space-between; align-items: center; position: relative; overflow: hidden;">
        <div style="flex: 1;">
            <h1 style="font-size: 44px; margin: 0; line-height: 1.1;">Mood <span class="highlight">Analytics</span></h1>
            <p style="margin: 8px 0 0 0; color: #6b6b6b; font-size: 17px;">Longitudinal patterns from your reflections.</p>
        </div>
        <div style="display: flex; align-items: center; gap: 24px; border-left: 2px dashed #1a1a1a; padding-left: 24px; max-width: 400px;">
            {prop_img('aristotle.png', rotation=1, height=120)}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    total_reflections = len(entries)
    
    all_emotions = []
    for e in entries:
        try: all_emotions.extend(json.loads(e['emotions']))
        except: pass
    dominant_emotion = Counter(all_emotions).most_common(1)[0][0].upper() if all_emotions else "—"
    
    now = datetime.now()
    this_month_days = set()
    for e in entries:
        try:
            dt = datetime.strptime(e['created_at'][:10], "%Y-%m-%d")
            if dt.year == now.year and dt.month == now.month:
                this_month_days.add(dt.day)
        except: pass
    reflection_days = len(this_month_days) if entries else "—"
    
    intensity_map = {'low': 1, 'medium': 2, 'high': 3}
    intensities = [intensity_map.get(e.get('intensity', 'low').lower(), 1) for e in entries]
    avg_intensity = (sum(intensities) / len(intensities)) / 3 * 100 if intensities else 0
    avg_intensity_str = f"{avg_intensity:.1f}%" if entries else "—"
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a; min-height:120px;"><div style="font-size: 12px; text-transform: uppercase; letter-spacing: 2px; color: #6b6b6b; margin-bottom: 8px; font-weight: bold; font-variant: small-caps;">Total Reflections</div><div style="font-size: 28px; font-family: \'DM Serif Display\', serif; color: #1a1a1a; margin-bottom: 4px;">{total_reflections if entries else "—"}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a; min-height:120px;"><div style="font-size: 12px; text-transform: uppercase; letter-spacing: 2px; color: #6b6b6b; margin-bottom: 8px; font-weight: bold; font-variant: small-caps;">Dominant Emotion</div><div style="font-size: 22px; font-family: \'DM Serif Display\', serif; color: #1a1a1a; margin-bottom: 4px;">{dominant_emotion}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a; min-height:120px;"><div style="font-size: 12px; text-transform: uppercase; letter-spacing: 2px; color: #6b6b6b; margin-bottom: 8px; font-weight: bold; font-variant: small-caps;">Reflection Days</div><div style="font-size: 28px; font-family: \'DM Serif Display\', serif; color: #1a1a1a; margin-bottom: 4px;">{reflection_days}</div><div style="color:#6b6b6b; font-size:13px;">This month</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a; min-height:120px;"><div style="font-size: 12px; text-transform: uppercase; letter-spacing: 2px; color: #6b6b6b; margin-bottom: 8px; font-weight: bold; font-variant: small-caps;">Avg Intensity</div><div style="font-size: 28px; font-family: \'DM Serif Display\', serif; color: #1a1a1a; margin-bottom: 4px;">{avg_intensity_str}</div><div style="color:#6b6b6b; font-size:13px;">Of maximum</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown(section_header("Chronological Mood Timeline"), unsafe_allow_html=True)
    with st.container(border=True):
        if not entries:
            st.markdown('<div style="text-align:center; color:#6b6b6b; padding:40px;">Patterns emerge after your first reflection.</div>', unsafe_allow_html=True)
        else:
            df = pd.DataFrame(entries)
            df['date'] = pd.to_datetime(df['created_at'])
            df['int_val'] = df['intensity'].str.lower().map(intensity_map).fillna(1)
            df = df.sort_values('date')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['date'], y=df['int_val'], mode='lines',
                line=dict(color='#2e6fb0', width=2),
                fill='tozeroy', fillcolor='rgba(46,111,176,0.15)',
                customdata=df[['intensity', 'event']],
                hovertemplate="<b>%{x|%b %d, %Y}</b><br>Intensity: %{customdata[0]}<br>Event: %{customdata[1]}<extra></extra>"
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#fdfbf5',
                font=dict(color='#1a1a1a', family='-apple-system, sans-serif'),
                height=240, margin=dict(l=0, r=0, t=10, b=0),
                hoverlabel=dict(bgcolor="white", font_size=13, font_family="sans-serif")
            )
            fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.08)', zeroline=False)
            fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.08)', zeroline=False, tickvals=[1,2,3], ticktext=['Low', 'Medium', 'High'])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('<br><br>', unsafe_allow_html=True)
    
    c_left, c_right = st.columns(2)
    
    with c_left:
        with st.container(border=True):
            st.markdown(section_header("Emotion Frequency"), unsafe_allow_html=True)
            counts = Counter(all_emotions)
            if sum(counts.values()) < 3:
                st.markdown('<div style="border: 2px dashed #1a1a1a; padding: 32px; text-align: center; color: #6b6b6b; border-radius: 4px;">Patterns emerge after a few more entries.</div>', unsafe_allow_html=True)
            else:
                edf = pd.DataFrame(counts.items(), columns=['Emotion', 'Count'])
                fig2 = px.pie(edf, names='Emotion', values='Count', hole=0.55, color_discrete_sequence=['#bcd4ea', '#6fa3d4', '#2e6fb0', '#1e3a5f', '#8fb8de'])
                fig2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#fdfbf5',
                    font=dict(color='#1a1a1a'), height=260, margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=True, legend=dict(yanchor="middle", y=0.5, xanchor="left", x=1.0)
                )
                fig2.update_traces(hovertemplate="%{label}<br>Count: %{value}<br>%{percent}<extra></extra>", textinfo='none')
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    with c_right:
        with st.container(border=True):
            st.markdown(section_header("Monthly Reflection Calendar"), unsafe_allow_html=True)
            st.html(heatmap.render_heatmap_html().replace('background:#faf7f0;', 'background:#ffffff;'))

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown(section_header("Top Triggers"), unsafe_allow_html=True)
    with st.container(border=True):
        all_triggers = []
        for e in entries:
            try: all_triggers.extend(json.loads(e['triggers']))
            except: pass
            
        triggers_html = ""
        if all_triggers:
            top_triggers = Counter(all_triggers).most_common(5)
            for t, c in top_triggers:
                # No leading spaces inside the HTML block to prevent Markdown code-block escaping
                triggers_html += f'''<div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px dashed rgba(26,26,26,0.2); padding: 12px 0;">
<div style="font-size: 17px; font-weight: bold; color: #1a1a1a; text-transform: capitalize;">{t}</div>
<div style="background: #2e6fb0; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; border: 2px solid #1a1a1a;">{c}</div>
</div>'''
        else:
            triggers_html = '<div style="color: #6b6b6b;">No triggers recorded yet.</div>'

        st.markdown(triggers_html, unsafe_allow_html=True)
