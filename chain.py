import streamlit as st
import db
import json
from collections import Counter

def render_pattern_chain(situation, triggers, emotions, intensity, similar_entries):
    """
    Renders a 6-box horizontal chain showing the cognitive pattern.
    """
    # --- 1. Situation ---
    box_situation = situation if situation else "Unknown situation"
    
    # --- 2. Thought ---
    if triggers:
        # Simple inference: joining the triggers as thoughts
        box_thought = f"Thoughts about {', '.join(triggers)}"
    else:
        box_thought = "Unclear triggers"
        
    # --- 3. Emotion ---
    box_emotion = ", ".join(emotions).title() if emotions else "Unknown"
    
    # --- 4. Reaction ---
    if intensity.lower() == "high":
        box_reaction = "Felt it strongly"
    elif intensity.lower() == "medium":
        box_reaction = "Felt it moderately"
    else:
        box_reaction = "Felt it mildly"
        
    # --- 5 & 6. Response and Outcome (inferred from past similar entries) ---
    past_actions = []
    positive_outcomes = 0
    total_next_days = 0
    
    if similar_entries:
        for past in similar_entries:
            next_entry = db.get_next_day_entry(past['created_at'])
            if next_entry:
                total_next_days += 1
                # Extract actions (events) from next day
                past_actions.append(next_entry['event'])
                
                # Check for positive emotions next day
                try:
                    next_emotions = json.loads(next_entry['emotions'])
                    positive_set = {"calm", "happy", "excited"}
                    if any(e in positive_set for e in next_emotions):
                        positive_outcomes += 1
                except Exception:
                    pass
                    
    if past_actions:
        most_common_action = Counter(past_actions).most_common(1)[0][0]
        box_response = most_common_action
    else:
        box_response = "Unclear response"
        
    if total_next_days > 0 and (positive_outcomes / total_next_days) >= 0.5:
        box_outcome = "Mood often improved"
    elif total_next_days > 0:
        box_outcome = "Mood varied"
    else:
        box_outcome = "Not enough data"

    # --- Render UI ---
    st.markdown("### Your Behavioral Pattern")
    
    # Use CSS to make simple boxes
    st.markdown("""
        <style>
        .pattern-box {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            text-align: center;
            height: 100%;
            background-color: #f9f9f9;
        }
        .pattern-label {
            font-size: 0.7em;
            text-transform: uppercase;
            color: #666;
            margin-bottom: 5px;
            font-weight: bold;
            letter-spacing: 0.5px;
        }
        .pattern-value {
            font-size: 0.9em;
            color: #333;
        }
        /* Dark mode compatibility */
        @media (prefers-color-scheme: dark) {
            .pattern-box {
                background-color: #1e1e1e;
                border-color: #444;
            }
            .pattern-label { color: #aaa; }
            .pattern-value { color: #eee; }
        }
        </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(6)
    boxes = [
        ("Situation", box_situation),
        ("Thought", box_thought),
        ("Emotion", box_emotion),
        ("Reaction", box_reaction),
        ("Response", box_response),
        ("Outcome", box_outcome)
    ]
    
    for i, col in enumerate(cols):
        label, value = boxes[i]
        with col:
            st.markdown(f"""
            <div class="pattern-box">
                <div class="pattern-label">{label}</div>
                <div class="pattern-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)
            
    # Caption (hedged language requirement)
    st.write("") # spacing
    match_count = len(similar_entries)
    if match_count > 0:
        st.caption(f"*This sequence appeared in {match_count} of your past entries.*")
    else:
        st.caption("*This sequence is new; no past entries matched strongly enough to infer a response pattern.*")
    st.divider()
