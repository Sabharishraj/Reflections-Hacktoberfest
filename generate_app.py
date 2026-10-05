import urllib.request
# Just copy from the previous successful generation and fix the single quote escape issue.
code = """import streamlit as st
import db
import search
import extract
import json
import seed
from collections import Counter
from props import prop_img, section_header
import heatmap

st.set_page_config(page_title="AI Reflection Journal", layout="wide")
db.init_db()

@st.cache_resource
def get_cached_index_and_rows():
    return search.build_index()

if 'nav' not in st.session_state:
    st.session_state.nav = 'home'

def render_nav():
    active_idx = 1 if st.session_state.nav == 'home' else 2
    st.markdown(f'''
    <style>
    /* =========================================================
       THEME LOCK (Cream Background + Grid + Ink Text)
       Do not remove or alter this block. It prevents dark mode.
       ========================================================= */
    body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main, .block-container {{
        background-color: #faf7f0 !important;
        background-image: repeating-linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px), repeating-linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px) !important;
        background-size: 24px 24px !important;
        color: #1a1a1a !important;
    }}
    [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] span, [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3, [data-testid="stMarkdownContainer"] h4, [data-testid="stMarkdownContainer"] div {{
        color: #1a1a1a;
    }}
    /* ========================================================= */
    
    /* 1. HIDE SIDEBAR ENTIRELY */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {{ display: none !important; }}
    
    /* 2. SCALE CONTAINER */
    [data-testid="block-container"] {{ max-width: 1400px; width: 95%; margin: 0 auto; padding-top: 2rem; }}
    
    /* 3. GLOBAL SCRAPBOOK FONTS */
    p, li {{ font-size: 17px; color: #6b6b6b; }}
    h3 {{ font-size: 30px !important; margin-bottom: 8px !important; }}
    h1, h2, h3, h4 {{ font-family: 'DM Serif Display', Georgia, serif !important; color: #1a1a1a !important; font-weight: normal !important; }}
    .card-label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 2px; color: #6b6b6b; margin-bottom: 8px; font-weight: bold; font-variant: small-caps; }}
    .card-value {{ font-size: 28px; font-family: 'DM Serif Display', serif; color: #1a1a1a; margin-bottom: 4px; }}
    .highlight {{ background-color: #ffd966; padding: 0 4px; border-radius: 2px; }}
    
    /* 4. TAPE AND CHIPS */
    .tape {{ position: absolute; background: rgba(255, 217, 102, 0.6); width: 80px; height: 24px; top: -5px; left: -10px; transform: rotate(35deg); box-shadow: 1px 1px 3px rgba(0,0,0,0.1); border: 1px solid rgba(0,0,0,0.05); z-index: 10; pointer-events: none; clip-path: polygon(0% 5%, 5% 0%, 95% 5%, 100% 15%, 98% 85%, 95% 100%, 5% 95%, 0% 90%); }}
    .tape.pink {{ background: rgba(244, 167, 195, 0.85); transform: translateX(-50%) rotate(2deg); width: 80px; top: -10px; left: 50%; clip-path: none; }}
    .emo-chip {{ display: inline-block; background: #ffffff; color: #1a1a1a; padding: 4px 10px; border-radius: 16px; font-size: 12px; font-weight: bold; border: 2px solid #1a1a1a; box-shadow: 2px 2px 0 rgba(0,0,0,0.1); margin: 2px 4px 2px 0; }}
    .timeline {{ position: relative; margin-left: 10px; margin-top: 16px; padding-bottom: 20px; color: #1a1a1a !important; }}
    .timeline-dot {{ position: absolute; left: -14px; top: -10px; width: 28px; height: 100%; }}
    .timeline-dot svg {{ display: block; overflow: visible; }}
    .recovery-block {{ border: 2px dashed #1a1a1a; margin-top: 16px; background: rgba(244, 167, 195, 0.15); padding: 16px; border-radius: 4px; position: relative; color: #1a1a1a !important; }}

    /* 5. ALL BORDERED CONTAINERS BECOME WHITE CARDS */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: #ffffff !important;
        border: 2px solid #1a1a1a !important;
        border-radius: 12px !important;
        box-shadow: 4px 4px 0 rgba(0,0,0,0.15) !important;
        padding: 20px !important;
        margin-bottom: 16px;
        position: relative;
        color: #1a1a1a !important;
    }}
    
    /* Pattern Insights: sticky note style */
    [data-testid="stVerticalBlockBorderWrapper"]:has(.is-sticky) {{
        background: #fff3bf !important;
        transform: rotate(-1deg);
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:has(.is-sticky)::before {{
        content: ''; position: absolute; top: 6px; left: 50%; transform: translateX(-50%);
        width: 10px; height: 10px; background: #e05252; border-radius: 50%;
        border: 2px solid #1a1a1a; box-shadow: 2px 2px 0 rgba(0,0,0,0.1);
    }}
    
    /* 6. THE TOP NAV CONTAINER SPECIFICS */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type {{
        padding: 12px 24px !important;
        margin-bottom: 24px !important;
        transform: none !important;
    }}
    
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type button {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}
    
    /* Home/Analysis Links */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(2) button {{
        font-family: 'DM Serif Display', serif !important;
        font-size: 16px !important;
        color: #1a1a1a !important;
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(2) [data-testid="column"]:nth-child({active_idx}) button {{
        color: #2e6fb0 !important;
        text-decoration: underline !important;
        text-decoration-thickness: 2px !important;
        text-underline-offset: 4px !important;
    }}
    
    /* Demo/Clear Actions */
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(3) button {{
        background: #ffffff !important;
        border: 2px solid #1a1a1a !important;
        color: #1a1a1a !important;
        border-radius: 20px !important;
        font-size: 14px !important;
        padding: 4px 12px !important;
        font-family: sans-serif !important;
        box-shadow: 2px 2px 0 rgba(0,0,0,0.15) !important;
        transition: all 0.2s !important;
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:first-of-type [data-testid="column"]:nth-child(3) button:hover {{
        background: #2e6fb0 !important;
        color: #ffffff !important;
    }}
    
    /* 7. WIDGET OVERRIDES */
    [data-testid="stTextArea"] textarea {{ 
        height: 260px !important; 
        background-color: #fdfbf5 !important;
        background-image: repeating-linear-gradient(transparent, transparent 31px, rgba(46,111,176,0.2) 31px, rgba(46,111,176,0.2) 32px) !important;
        line-height: 32px !important;
        border: 2px solid #1a1a1a !important; 
        color: #1a1a1a !important; 
        font-size: 17px !important; 
        border-radius: 4px !important;
        box-shadow: inset 2px 2px 5px rgba(0,0,0,0.05) !important;
        padding-top: 6px !important;
    }}
    [data-testid="stTextArea"] textarea:focus {{ border-color: #2e6fb0 !important; box-shadow: 0 0 0 1px #2e6fb0 !important; }}
    [data-testid="stTextArea"] textarea::placeholder {{ font-style: italic; color: #6b6b6b; }}
    
    .reflect-btn [data-testid="baseButton-secondary"] {{
        background: linear-gradient(135deg, #2e6fb0, #5aa9e6) !important;
        color: #ffffff !important;
        border: 2px solid #1a1a1a !important;
        border-radius: 40px !important;
        padding: 12px 32px !important;
        font-size: 19px !important;
        font-weight: bold !important;
        box-shadow: 4px 4px 0 rgba(0,0,0,0.15) !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
        width: 100% !important;
    }}
    .reflect-btn [data-testid="baseButton-secondary"]:hover {{
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0 rgba(0,0,0,0.15) !important;
    }}
    
    /* Slight rotations for columns containing cards */
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(1) > [data-testid="stVerticalBlockBorderWrapper"] {{ transform: rotate(-1.5deg); }}
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) > [data-testid="stVerticalBlockBorderWrapper"] {{ transform: rotate(1deg); }}
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(3) > [data-testid="stVerticalBlockBorderWrapper"] {{ transform: rotate(-0.5deg); }}
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(4) > [data-testid="stVerticalBlockBorderWrapper"] {{ transform: rotate(2deg); }}
    </style>
    ''', unsafe_allow_html=True)
    
    with st.container(border=True):
        col_title, col_links, col_actions = st.columns([3, 2, 2])
        with col_title:
            st.markdown('<div style="font-family:\'DM Serif Display\',serif; font-size:20px; line-height:2.0; color:#1a1a1a;"><span style="color:#2e6fb0;">●</span> AI Reflection Journal</div>', unsafe_allow_html=True)
        with col_links:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Home"):
                    st.session_state.nav = 'home'
                    st.rerun()
            with c2:
                if st.button("Analysis"):
                    st.session_state.nav = 'analysis'
                    st.rerun()
        with col_actions:
            c3, c4 = st.columns(2)
            with c3:
                if st.button("Load Demo"):
                    seed.load_demo_data()
                    st.rerun()
            with c4:
                if st.button("Clear Data"):
                    seed.clear_all_data()
                    st.rerun()

render_nav()

if st.session_state.nav == 'home':
    all_entries = db.get_all_entries()

    with st.container(border=True):
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
        ''', unsafe_allow_html=True)
        
    if all_entries:
        total_days = len(set(e['created_at'].split(' ')[0] for e in all_entries))
        all_emotions = []
        all_triggers = []
        
        for e in all_entries:
            try:
                emotions = json.loads(e['emotions'])
                triggers = json.loads(e['triggers'])
            except:
                emotions = []; triggers = []
            all_emotions.extend(emotions)
            all_triggers.extend(triggers)
                
        most_common_emotion = Counter(all_emotions).most_common(1)[0][0] if all_emotions else "None"
        most_common_trigger = Counter(all_triggers).most_common(1)[0][0] if all_triggers else "None"

        st.markdown(section_header("Dashboard"), unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        today_entry = all_entries[0]
        try: today_emotion = json.loads(today_entry['emotions'])[0] if json.loads(today_entry['emotions']) else "None"
        except: today_emotion = "None"
        today_intensity = today_entry['intensity']

        with col1:
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
                st.markdown(f'<div class="card-label">History</div><div class="card-value">{total_days}</div><div style="color:#6b6b6b; font-size:13px;">{day_word} this month</div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        c_title, c_prop = st.columns([3, 1])
        with c_title:
            st.markdown(section_header("Pattern Insights"), unsafe_allow_html=True)
        with c_prop:
            st.markdown(f'<div style="display:flex; justify-content:flex-end;">{prop_img("aristotle.png", height=130)}</div>', unsafe_allow_html=True)
        
        if len(all_entries) < 5:
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
                ''', unsafe_allow_html=True)
                
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('<h4 style="margin:0 0 16px 0; font-family:\'DM Serif Display\', serif;">Monthly Reflection Calendar</h4>', unsafe_allow_html=True)
            st.html(heatmap.render_heatmap_html())
        
        st.markdown("<br><br>", unsafe_allow_html=True)

    # --- NEW ENTRY ---
    c_new, c_thinker = st.columns([3, 1])
    with c_new:
        st.markdown(section_header("New Entry"), unsafe_allow_html=True)
    with c_thinker:
        st.markdown(f'''
        <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 4px;">
            {prop_img('thinker.png', rotation=-2, height=150)}
            <div style="font-size: 12px; color: #6b6b6b; font-style: italic; font-weight: bold; margin-right: 20px;">Think it through.</div>
        </div>
        ''', unsafe_allow_html=True)

    with st.container(border=True):
        entry_text = st.text_area("What happened today?", height=260, label_visibility="collapsed")
        
        st.markdown('<div class="reflect-btn" style="margin-top:16px;">', unsafe_allow_html=True)
        if st.button("Reflect"):
            st.markdown('</div>', unsafe_allow_html=True)
            if entry_text.strip():
                with st.spinner("Analyzing entry locally..."):
                    extracted = extract.extract_structured_data(entry_text)
                    new_id = db.insert_entry(raw=entry_text, event=extracted.get("event", "Unknown event"), situation=extracted.get("situation", "Unknown situation"), emotions=extracted.get("emotions", ["numb"]), intensity=extracted.get("intensity", "low"), triggers=extracted.get("triggers", []))
                    
                    prefs = extract.extract_preferences(entry_text)
                    db.upsert_preferences(prefs)
                    
                    st.markdown('<div style="color:#2e6fb0; font-weight:bold; margin-bottom:16px;">Entry saved and analyzed!</div>', unsafe_allow_html=True)
                    
                    st.markdown('<h4 style="font-family: \\'DM Serif Display\\', serif;">Analysis</h4>'.replace("\\'", "'"), unsafe_allow_html=True)
                    e_col1, e_col2 = st.columns(2)
                    with e_col1:
                        st.write(f"**Event:** {extracted.get('event')}")
                        st.write(f"**Situation:** {extracted.get('situation')}")
                    with e_col2:
                        emo_html = "".join([f'<span class="emo-chip">{{e.title()}}</span>' for e in extracted.get('emotions', [])])
                        st.markdown(f"**Emotions:** {{emo_html}}", unsafe_allow_html=True)
                        st.write(f"**Intensity:** {extracted.get('intensity')}")
                        st.write(f"**Triggers:** {', '.join(extracted.get('triggers', []))}")
                        
                    get_cached_index_and_rows.clear()
                    faiss_index, cached_rows = get_cached_index_and_rows()
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    if len(cached_rows) < 3:
                        st.markdown(section_header("Similar Moments in Your Past"), unsafe_allow_html=True)
                        st.markdown('<div style="color:#6b6b6b; font-size:15px;">Similar moments appear once you have a few entries.</div>', unsafe_allow_html=True)
                    else:
                        query_text = f"{extracted.get('situation', '')} {', '.join(extracted.get('triggers', []))}"
                        similar_entries = search.find_similar(
                            index=faiss_index, 
                            rows=cached_rows, 
                            query_text=query_text, 
                            current_id=new_id,
                            k=3,
                            threshold=0.55
                        )
                        
                        import recovery
                        current_is_neg = recovery.is_negative({"intensity": extracted.get("intensity", "low"), "emotions": extracted.get("emotions", [])})
                        
                        wavy_line_svg = '''<svg width="24" height="100%" style="position:absolute; top:0; left:0; height:100%;"><path d="M12,0 Q24,20 12,40 T12,80 T12,120 T12,160 T12,200 T12,240 T12,280 T12,320 T12,360 T12,400 T12,440 T12,480 T12,520 T12,560 T12,600 T12,640 T12,680 T12,720 T12,760 T12,800 T12,840 T12,880 T12,920 T12,960 T12,1000" fill="none" stroke="#2e6fb0" stroke-width="2"/></svg>'''
                        
                        if current_is_neg:
                            c_sim, c_dio = st.columns([3, 1])
                            with c_sim:
                                st.markdown(section_header("You've been through something like this before"), unsafe_allow_html=True)
                            with c_dio:
                                st.markdown(f'''
                                <div style="display:flex; flex-direction:column; align-items:flex-end;">
                                    {prop_img('diogenes.png', height=110)}
                                    <div style="color:#6b6b6b; font-size:12px; font-style:italic;">"Searching your past for what helped."</div>
                                </div>
                                ''', unsafe_allow_html=True)
                                
                            recovery_matches = []
                            for past in similar_entries:
                                nd = recovery.get_next_day(past['created_at'])
                                if nd and not recovery.is_negative(nd):
                                    recovery_matches.append((past, nd))
                                    
                            if recovery_matches:
                                st.markdown('<div class="timeline">', unsafe_allow_html=True)
                                st.markdown(f'<div class="timeline-dot">{{wavy_line_svg}}</div>', unsafe_allow_html=True)
                                for past, nd in recovery_matches:
                                    emo_html = "".join([f'<span class="emo-chip">{{e.strip().title()}}</span>' for e in past['emotions'].split(',')]) if isinstance(past['emotions'], str) else "".join([f'<span class="emo-chip">{{e.title()}}</span>' for e in past['emotions']])
                                    
                                    st.markdown(f'''
                                    <div style="position: relative; margin-bottom: 24px; margin-left: 24px;">
                                        <div style="position:absolute; top:-12px; left:-24px; background:#fff; border:2px solid #1a1a1a; padding:4px 12px; font-family:'DM Serif Display',serif; font-size:14px; transform:rotate(-4deg); box-shadow:3px 3px 0 rgba(0,0,0,0.15); z-index:5;">{{past['date']}}</div>
                                    ''', unsafe_allow_html=True)
                                    with st.container(border=True):
                                        st.markdown(f'''
                                        <div class="card-value" style="margin-top: 8px;">{{past['event']}}</div>
                                        <div style="margin-bottom:12px;">{{emo_html}}</div>
                                        <div class="recovery-block">
                                            <div class="tape pink"></div>
                                            <div style="font-size:11px; text-transform:uppercase; color:#6b6b6b; margin-bottom:4px; font-weight:bold;">How it turned out</div>
                                            <div style="color:#1a1a1a; font-family:'DM Serif Display', serif; font-size:18px;">{{nd['event']}} - <span style="font-family:sans-serif; font-size:15px; color:#1a1a1a;">{{nd['situation']}}</span></div>
                                        </div>
                                        ''', unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div style="color:#6b6b6b; font-size:15px;">This is the first time this has shown up in your journal. How you handle it becomes part of your story.</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(section_header("Similar Moments in Your Past"), unsafe_allow_html=True)
                            
                            if similar_entries:
                                st.markdown('<div class="timeline">', unsafe_allow_html=True)
                                st.markdown(f'<div class="timeline-dot">{{wavy_line_svg}}</div>', unsafe_allow_html=True)
                                for past in similar_entries:
                                    next_entry = db.get_next_day_entry(past['created_at'])
                                    afterward_html = ""
                                    if next_entry:
                                        afterward_text = next_entry['raw'][:120]
                                        if len(next_entry['raw']) > 120: afterward_text += "..."
                                        afterward_html = f'''
                                        <div class="recovery-block">
                                            <div class="tape pink"></div>
                                            <div style="font-size:11px; text-transform:uppercase; color:#6b6b6b; margin-bottom:4px; font-weight:bold;">Afterward</div>
                                            <div style="color:#1a1a1a; font-family:'DM Serif Display', serif; font-size:16px;">{{afterward_text}}</div>
                                        </div>
                                        '''
                                        
                                    emo_html = "".join([f'<span class="emo-chip">{{e.strip().title()}}</span>' for e in past['emotions'].split(',')]) if isinstance(past['emotions'], str) else "".join([f'<span class="emo-chip">{{e.title()}}</span>' for e in past['emotions']])
                                    
                                    st.markdown(f'''
                                    <div style="position: relative; margin-bottom: 24px; margin-left: 24px;">
                                        <div style="position:absolute; top:-12px; left:-24px; background:#fff; border:2px solid #1a1a1a; padding:4px 12px; font-family:'DM Serif Display',serif; font-size:14px; transform:rotate(-4deg); box-shadow:3px 3px 0 rgba(0,0,0,0.15); z-index:5;">{{past['date']}}</div>
                                    ''', unsafe_allow_html=True)
                                    with st.container(border=True):
                                        st.markdown(f'''
                                        <div class="card-value" style="margin-top: 8px;">{{past['event']}}</div>
                                        <div style="margin-bottom:12px;">{{emo_html}}</div>
                                        {{afterward_html}}
                                        ''', unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div style="color:#6b6b6b; font-size:15px;">No strong match in your past entries.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="color:#e05252; font-size:15px; margin-top:10px;">Please write something before reflecting.</div>', unsafe_allow_html=True)
        else:
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.nav == 'analysis':
    import analysis
    analysis.render_analysis()

st.markdown('''<div style="text-align:center; color:#6b6b6b; font-family: monospace; font-size:12px; margin-top:80px; margin-bottom:40px;">* All data stays on this device. Nothing is sent to the cloud.</div>''', unsafe_allow_html=True)
"""

with open("app.py", "w") as f:
    f.write(code)
