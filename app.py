import streamlit as st
import db
import extract
import search
import json
import seed
from collections import Counter

st.set_page_config(page_title="AI Reflection Journal", layout="wide")

# --- OFFLINE LOGIN SYSTEM ---
def check_password():
    """Returns `True` if the user has the correct PIN."""
    def password_entered():
        if st.session_state["password"] == "1234":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # clear from memory
        else:
            st.session_state["password_correct"] = False

    # First run or after refresh
    if "password_correct" not in st.session_state:
        st.markdown("### 🔒 Privacy-First Local Journal")
        st.text_input(
            "Enter your local PIN to unlock (Hint: type 1234)", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False
    # Incorrect password entered
    elif not st.session_state["password_correct"]:
        st.markdown("### 🔒 Privacy-First Local Journal")
        st.text_input(
            "Enter your local PIN to unlock (Hint: type 1234)", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("Incorrect PIN. Please try again.")
        return False
    # Logged in successfully
    else:
        return True

# Stop the app completely if they haven't logged in
if not check_password():
    st.stop()

# Ensure DB is initialized
db.init_db()

@st.cache_resource
def get_cached_index_and_rows():
    """Cache the FAISS index so it isn't rebuilt on every UI refresh."""
    return search.build_index()

st.title("AI Reflection Journal")
st.markdown("A privacy-first, offline journal that helps you discover patterns in your daily life.")

# --- SIDEBAR & DASHBOARD ---
st.sidebar.header("Dashboard")

if st.sidebar.button("Load Demo Data"):
    success, msg = seed.load_demo_data()
    if success:
        st.sidebar.success(msg)
        get_cached_index_and_rows.clear()
    else:
        st.sidebar.warning(msg)
    st.rerun()

if st.sidebar.button("Clear All Data"):
    seed.clear_all_data()
    st.sidebar.success("All journal entries deleted.")
    get_cached_index_and_rows.clear()
    st.rerun()

# --- Your World (Preferences) ---
st.sidebar.markdown("### Your World")
try:
    prefs = db.get_top_preferences()
    if prefs:
        for p in prefs:
            st.sidebar.caption(f"**{str(p['category']).title()}**: {p['value']} ({p['mention_count']} mentions)")
    else:
        st.sidebar.caption("Preferences will appear as you write.")
except Exception:
    st.sidebar.caption("Preferences loading...")

# --- Event Mindmap ---
st.sidebar.markdown("### Connections")
if "show_map" not in st.session_state:
    st.session_state.show_map = False

if st.sidebar.button("Show mindmap of events"):
    st.session_state.show_map = not st.session_state.show_map

if st.session_state.show_map:
    import graphmap
    fig = graphmap.render_event_map()
    if fig:
        st.sidebar.plotly_chart(fig, use_container_width=True)
        st.sidebar.caption("Connected moments share the same people, exams, or places.")
    else:
        st.sidebar.info("Not enough connected events yet — keep writing.")

all_entries = db.get_all_entries()

if all_entries:
    # Calculate stats
    total_days = len(set(e['created_at'].split(' ')[0] for e in all_entries))
    
    all_emotions = []
    all_triggers = []
    chain_count = 0
    
    for e in all_entries:
        try:
            emotions = json.loads(e['emotions'])
            triggers = json.loads(e['triggers'])
        except:
            emotions = []
            triggers = []
            
        all_emotions.extend(emotions)
        all_triggers.extend(triggers)
        
        # Look for the specific pattern (exams + comparison)
        lower_triggers = [t.lower() for t in triggers]
        has_exam = any("exam" in t for t in lower_triggers)
        has_comparison = any("comparison" in t for t in lower_triggers)
        if has_exam and has_comparison:
            chain_count += 1
            
    most_common_emotion = Counter(all_emotions).most_common(1)[0][0] if all_emotions else "None"
    most_common_trigger = Counter(all_triggers).most_common(1)[0][0] if all_triggers else "None"

    # Dashboard Cards
    st.subheader("Your Patterns Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    
    # Get today's emotion (latest entry)
    today_entry = all_entries[0] # Since it's sorted DESC
    try:
        today_emotion = json.loads(today_entry['emotions'])[0] if json.loads(today_entry['emotions']) else "None"
    except:
        today_emotion = "None"
        
    today_intensity = today_entry['intensity']

    with col1:
        if today_intensity.lower() == "low" or today_intensity == "none":
            st.info(f"**Today**\n\n{today_emotion.capitalize()}")
        else:
            st.info(f"**Today**\n\n{today_emotion.capitalize()}\n\n*intensity: {today_intensity}*")
    with col2:
        st.warning(f"**Top Emotion**\n\n{most_common_emotion.capitalize()}")
    with col3:
        st.error(f"**Top Trigger**\n\n{most_common_trigger.capitalize()}")
    with col4:
        day_word = "day" if total_days == 1 else "days"
        st.success(f"**History**\n\n{total_days} {day_word} this month")
        
    # Evidence-based hedged language
    st.markdown("### Pattern Insights")
    if len(all_entries) < 5:
        st.write("Keep writing — patterns emerge after a few more entries.")
    else:
        st.write(f"Based on your past entries, you frequently mention **{most_common_trigger}** in situations associated with feeling **{most_common_emotion}**.")
            
    import heatmap
    st.html(heatmap.render_heatmap_html())
    
    st.divider()

# --- MAIN INPUT ---
st.subheader("New Entry")
entry_text = st.text_area("What happened today?", height=150)

if st.button("Reflect"):
    if entry_text.strip():
        with st.spinner("Analyzing entry locally (this might take a few seconds)..."):
            # 1. Extract JSON with Ollama
            extracted = extract.extract_structured_data(entry_text)
            
            # 2. Save to DB
            new_id = db.insert_entry(
                raw=entry_text,
                event=extracted.get("event", "Unknown event"),
                situation=extracted.get("situation", "Unknown situation"),
                emotions=extracted.get("emotions", ["numb"]),
                intensity=extracted.get("intensity", "low"),
                triggers=extracted.get("triggers", [])
            )
            
            # Extract and save preferences & entities in the background
            prefs = extract.extract_preferences(entry_text)
            db.upsert_preferences(prefs)
            ents = extract.extract_entities(entry_text)
            db.update_entry_entities(new_id, json.dumps(ents))
            
            st.success("Entry saved and analyzed!")
            
            # 3. Display Extracted Data
            st.subheader("Analysis")
            e_col1, e_col2 = st.columns(2)
            with e_col1:
                st.write(f"**Event:** {extracted.get('event')}")
                st.write(f"**Situation:** {extracted.get('situation')}")
            with e_col2:
                st.write(f"**Emotions:** {', '.join(extracted.get('emotions', []))}")
                st.write(f"**Intensity:** {extracted.get('intensity')}")
                st.write(f"**Triggers:** {', '.join(extracted.get('triggers', []))}")
                
            # Clear cache and rebuild to include the newly saved entry
            get_cached_index_and_rows.clear()
            faiss_index, cached_rows = get_cached_index_and_rows()
            
            if len(cached_rows) < 3:
                st.subheader("Similar Moments in Your Past")
                st.info("Similar moments appear once you have a few entries.")
            else:
                # Search using the updated search.py logic
                query_text = f"{extracted.get('situation', '')} {', '.join(extracted.get('triggers', []))}"
                similar_entries = search.find_similar(
                    index=faiss_index, 
                    rows=cached_rows, 
                    query_text=query_text, 
                    current_id=new_id,
                    k=3,
                    threshold=0.55
                )
                
                # Check for negative entry recovery flow
                import recovery
                current_is_neg = recovery.is_negative({
                    "intensity": extracted.get("intensity", "low"),
                    "emotions": extracted.get("emotions", [])
                })
                
                if current_is_neg:
                    st.subheader("You've been through something like this before")
                    recovery_matches = []
                    for past in similar_entries:
                        nd = recovery.get_next_day(past['created_at'])
                        if nd and not recovery.is_negative(nd):
                            recovery_matches.append((past, nd))
                            
                    if recovery_matches:
                        for past, nd in recovery_matches:
                            with st.container():
                                st.info(f"🕰️ **{past['date']}**\nYou faced: {past['event']}\n\n**How it turned out:** {nd['event']} - {nd['situation']}")
                    else:
                        st.info("This is the first time this has shown up in your journal. How you handle it becomes part of your story.")
                else:
                    st.subheader("Similar Moments in Your Past")
                    # Render the cognitive pattern chain
                    import chain
                    chain.render_pattern_chain(
                        situation=extracted.get("situation", ""),
                        triggers=extracted.get("triggers", []),
                        emotions=extracted.get("emotions", []),
                        intensity=extracted.get("intensity", "low"),
                        similar_entries=similar_entries
                    )
                    
                    if similar_entries:
                        for past in similar_entries:
                            st.info(f"🕰️ **{past['date']} - {past['event']}**\n\nFelt: {past['emotions'].title()} (Intensity: {past['intensity']})")
                            
                            next_entry = db.get_next_day_entry(past['created_at'])
                            if next_entry:
                                afterward_text = next_entry['raw'][:120]
                                if len(next_entry['raw']) > 120:
                                    afterward_text += "..."
                                st.caption(f"**Afterward:** {afterward_text}")
                    else:
                        st.info("No strong match in your past entries.")
    else:
        st.warning("Please write something before reflecting.")
st.write("")
st.caption("All data stays on this device. Nothing is sent to the cloud.")
