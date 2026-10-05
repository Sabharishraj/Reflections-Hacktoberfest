import calendar
from datetime import datetime
import json
import db

def render_heatmap_html():
    """Generates a GitHub-style contribution HTML heatmap for emotional intensity."""
    now = datetime.now()
    year, month = now.year, now.month
    
    # Get all entries and map them to their max intensity and first emotion for the day
    entries = db.get_all_entries()
    curr_month_str = now.strftime("%Y-%m")
    day_data = {}
    
    intensity_map = {"low": 1, "medium": 2, "high": 3}
    for e in entries:
        if e['created_at'].startswith(curr_month_str):
            day = int(e['created_at'][8:10])
            val = intensity_map.get(e['intensity'].lower(), 0)
            
            # Extract first emotion for the tooltip
            try:
                emotions = json.loads(e['emotions'])
                first_emo = emotions[0].title() if emotions else "Unknown"
            except:
                first_emo = "Unknown"
                
            # Store the highest intensity entry for the day
            if day not in day_data or val > intensity_map.get(day_data[day]['intensity'], 0):
                day_data[day] = {'intensity': e['intensity'].lower(), 'emotion': first_emo}

    first_weekday, num_days = calendar.monthrange(year, month)
    
    # Colors on a continuous blue scale, dark theme background
    colors = {"none": "#1a1a1a", "low": "#1e3a5f", "medium": "#2e6fb0", "high": "#5aa9e6"}
    
    # We use a CSS grid that flows down the columns (weeks) like GitHub
    html = f"""
    <div style="background-color: #0e1117; color: white; padding: 15px; border-radius: 8px; font-family: sans-serif;">
        <h4 style="margin-top: 0; font-weight: 500;">{now.strftime("%B %Y")} Intensity</h4>
        <div style="display: grid; grid-template-rows: repeat(7, 14px); grid-template-columns: repeat(6, 14px); gap: 3px; grid-auto-flow: column; width: max-content;">
    """
    
    # Pad the start of the month (Monday = 0) with invisible squares
    for _ in range(first_weekday):
        html += '<div style="width: 14px; height: 14px; background: transparent;"></div>'
        
    # Render the actual days of the month
    for day in range(1, num_days + 1):
        data = day_data.get(day)
        color = colors[data['intensity']] if data else colors["none"]
        
        # Tooltip text
        title = f"{now.strftime('%b')} {day}"
        if data:
            title += f" - {data['intensity']} - {data['emotion']}"
            
        html += f'<div title="{title}" style="width: 14px; height: 14px; background-color: {color}; border-radius: 3px;"></div>'
        
    # Close grid and add Legend
    html += f"""
        </div>
        <div style="margin-top: 15px; font-size: 12px; display: flex; align-items: center; gap: 4px; color: #aaa;">
            <span>Intensity:</span>
            <div style="width: 12px; height: 12px; background-color: {colors['low']}; border-radius: 2px; margin-left: 5px;"></div> low
            <div style="width: 12px; height: 12px; background-color: {colors['medium']}; border-radius: 2px; margin-left: 5px;"></div> med
            <div style="width: 12px; height: 12px; background-color: {colors['high']}; border-radius: 2px; margin-left: 5px;"></div> high
        </div>
    </div>
    """
    return html
