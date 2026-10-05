import re

with open("analysis.py", "r") as f:
    text = f.read()

# MOOD TIMELINE
old_timeline = """    st.markdown(section_header("Chronological Mood Timeline"), unsafe_allow_html=True)
    st.markdown('<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a;">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)"""

new_timeline = """    st.markdown(section_header("Chronological Mood Timeline"), unsafe_allow_html=True)
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
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})"""

text = text.replace(old_timeline, new_timeline)

# EMOTION FREQUENCY
old_pie = """    with c_left:
        st.markdown('<div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a;">', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)"""

new_pie = """    with c_left:
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
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})"""
text = text.replace(old_pie, new_pie)

# TOP TRIGGERS
old_triggers = """    st.markdown(section_header("Top Triggers"), unsafe_allow_html=True)
    all_triggers = []
    for e in entries:
        try: all_triggers.extend(json.loads(e['triggers']))
        except: pass
        
    triggers_html = ""
    if all_triggers:
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

    st.markdown(f'''
    <div style="background:#ffffff; border:2px solid #1a1a1a; border-radius:12px; box-shadow:4px 4px 0 rgba(0,0,0,0.15); padding:20px; color:#1a1a1a;">
        {triggers_html}
    </div>
    ''', unsafe_allow_html=True)"""

new_triggers = """    st.markdown(section_header("Top Triggers"), unsafe_allow_html=True)
    with st.container(border=True):
        all_triggers = []
        for e in entries:
            try: all_triggers.extend(json.loads(e['triggers']))
            except: pass
            
        triggers_html = ""
        if all_triggers:
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

        st.markdown(triggers_html, unsafe_allow_html=True)"""
text = text.replace(old_triggers, new_triggers)

with open("analysis.py", "w") as f:
    f.write(text)
