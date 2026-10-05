with open("analysis.py", "r") as f:
    text = f.read()

# Update X axes
text = text.replace("fig.update_xaxes(showgrid=False, zeroline=False)", 
                    "fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.08)', zeroline=False)")
# Update Y axes
text = text.replace("fig.update_yaxes(showgrid=False, zeroline=False, tickvals=[1,2,3], ticktext=['Low', 'Medium', 'High'])",
                    "fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.08)', zeroline=False, tickvals=[1,2,3], ticktext=['Low', 'Medium', 'High'])")

with open("analysis.py", "w") as f:
    f.write(text)
