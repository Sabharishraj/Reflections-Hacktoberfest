import json
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import db
import extract
import search

def build_edges():
    """Builds node and edge lists based on shared entities and embedding similarity."""
    entries = db.get_all_entries()
    nodes = []
    texts = []
    
    # 1. Prepare nodes and migrate missing entities
    for e in entries:
        entities_str = e.get('entities')
        if not entities_str:
            # Extract on demand if missing
            ent_list = extract.extract_entities(e['raw'])
            entities_str = json.dumps(ent_list)
            db.update_entry_entities(e['id'], entities_str)
            
        try:
            ents = set([x.lower() for x in json.loads(entities_str)])
        except Exception:
            ents = set()
            
        # Add to node list
        node = {
            'id': e['id'],
            'date': e['created_at'][:10],
            'event': e['event'],
            'emotions': e['emotions'],
            'intensity': e['intensity'].lower(),
            'entities': ents,
            'text': f"{e['situation']} {e.get('triggers', '')}"
        }
        nodes.append(node)
        texts.append(node['text'])
        
    if not nodes:
        return [], []
        
    # 2. Get embeddings for similarity checks
    embeddings = search.get_embeddings(texts)
    embeddings = np.array(embeddings).astype('float32')
    import faiss
    faiss.normalize_L2(embeddings)
    
    # 3. Build edges (shared entity AND similarity > 0.5, max 2 per node)
    edges = []
    for i in range(len(nodes)):
        node_edges = 0
        for j in range(i + 1, len(nodes)):
            shared = nodes[i]['entities'].intersection(nodes[j]['entities'])
            if shared:
                # Calculate cosine similarity using dot product on normalized vectors
                sim = np.dot(embeddings[i], embeddings[j])
                if sim > 0.5:
                    shared_name = list(shared)[0]
                    edges.append((i, j, shared_name))
                    node_edges += 1
                    if node_edges >= 2:
                        break
                        
    return nodes, edges

def render_event_map():
    """Renders the Plotly network graph."""
    nodes, edges = build_edges()
    if len(nodes) < 2 or len(edges) == 0:
        return None
        
    # Build NetworkX graph for spring layout
    G = nx.Graph()
    for i in range(len(nodes)):
        G.add_node(i)
    for e in edges:
        G.add_edge(e[0], e[1], label=e[2])
        
    pos = nx.spring_layout(G, seed=42)
    
    # Prepare node data for Plotly
    node_x = [pos[i][0] for i in range(len(nodes))]
    node_y = [pos[i][1] for i in range(len(nodes))]
    colors = []
    hover_texts = []
    
    for n in nodes:
        c = {"high": "#e05252", "medium": "#2e6fb0", "low": "#2e8b57"}.get(n['intensity'], "#2e6fb0")
        colors.append(c)
        try:
            emo = ", ".join(json.loads(n['emotions']))
        except:
            emo = "Unknown"
        hover_texts.append(f"{n['date']}<br>{n['event']}<br>{emo}")
        
    # Prepare edge data for Plotly
    edge_x = []
    edge_y = []
    mid_x = []
    mid_y = []
    mid_text = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
        # Midpoint for hover labels
        mid_x.append((x0 + x1) / 2)
        mid_y.append((y0 + y1) / 2)
        mid_text.append(edge[2].get('label', ''))
        
    fig = go.Figure()
    
    # 1. Edge lines
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines'
    ))
    
    # 2. Edge hover targets (invisible markers at midpoints)
    fig.add_trace(go.Scatter(
        x=mid_x, y=mid_y,
        mode='markers',
        marker=dict(size=10, color='rgba(0,0,0,0)'),
        hovertext=mid_text,
        hoverinfo='text'
    ))
    
    # 3. Nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hovertext=hover_texts,
        hoverinfo='text',
        marker=dict(size=14, color=colors, line=dict(width=2, color='white'))
    ))
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    return fig
