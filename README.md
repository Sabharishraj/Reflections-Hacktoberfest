# Reflections

**Reflections** is a privacy-first, offline AI journaling application that analyzes personal journal entries, identifies recurring patterns, retrieves similar past experiences, and highlights previous instances of recovery.

The application combines local language models, semantic search, structured data extraction, and longitudinal analysis to provide context based on the user's own journal history.

---

## Key Features

### Journal Analysis

Users can enter free-form journal entries. The application uses a locally hosted LLM to extract structured information including:

- Event
- Situation
- Emotions
- Emotional intensity
- Triggers

Structured output is generated in JSON format and stored locally for further analysis.

### Semantic Similarity Search

Journal entries are converted into vector embeddings using:

- `sentence-transformers`
- `all-MiniLM-L6-v2`

FAISS is used for efficient similarity search across previous entries.

This allows the application to identify experiences that are semantically similar even when different words are used.

### Recovery-Based Retrieval

Reflections does not simply retrieve previous negative experiences.

For difficult entries, the retrieval system prioritizes similar past situations that were followed by recovery. This is intended to provide useful historical context without unnecessarily reinforcing negative experiences.

### Pattern Detection

The application identifies recurring themes across journal entries, including repeated situations, emotions, and triggers.

Pattern descriptions use cautious, evidence-based language rather than presenting interpretations as psychological diagnoses.

### Analytics Dashboard

The analysis dashboard provides:

- Summary metrics
- Mood and intensity timeline
- Emotion frequency analysis
- Top triggers
- Monthly journal activity

### Monthly Activity Heatmap

A GitHub-style calendar visualizes journal activity by day.

The calendar supports:

- Correct month alignment
- One cell per day
- Entry-count-based intensity
- Monthly activity visualization

### Local Authentication

The application includes a lightweight authentication system with:

- User login
- Encrypted credential storage
- Default test account
- Administrative user creation
- Access-request workflow

Credentials are stored separately using Fernet encryption.

---

## Privacy

Privacy is a core design consideration of Reflections.

The primary processing pipeline runs locally:

```text
Journal Entry
     |
     v
Local LLM
     |
     v
Structured Data
     |
     v
Local SQLite Database
     |
     +----> Local Embeddings
     |
     +----> FAISS Search
     |
     +----> Pattern Analysis
```

The application does not require an external AI API for its core journal analysis workflow.

---

## Responsible AI

Reflections is designed as a personal reflection and journaling tool rather than a medical or psychological diagnostic system.

The project follows several principles:

### No Diagnosis

The application does not attempt to diagnose mental health conditions.

### Evidence-Based Insights

Pattern detection is based on information contained in the user's journal history.

### Uncertainty-Aware Language

Insights use qualified statements instead of presenting interpretations as definitive facts.

### Recovery-Focused Retrieval

Similar negative experiences are not surfaced solely because they are negative. Retrieval prioritizes experiences associated with subsequent recovery.

### Privacy by Design

Local models, local storage, and local semantic search reduce unnecessary transmission of personal journal data.

---

## Architecture

```text
                         +------------------+
                         |       User       |
                         |  Journal Entry   |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |    Streamlit     |
                         |   Application    |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |  Ollama / Llama  |
                         |   3.2 3B Model  |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         | Structured JSON  |
                         |    Extraction    |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |      SQLite      |
                         |     Storage      |
                         +--------+---------+
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
          +------------------+        +------------------+
          | Sentence         |        | Pattern Analysis |
          | Transformers     |        |                  |
          +--------+---------+        +------------------+
                   |
                   v
          +------------------+
          |      FAISS       |
          | Semantic Search  |
          +--------+---------+
                   |
                   v
          +------------------+
          | Recovery Filter  |
          +--------+---------+
                   |
                   v
          +------------------+
          | Contextual       |
          | Reflection       |
          +------------------+
```

---

## Technology Stack

| Component | Technology |
|---|---|
| Application | Streamlit |
| Programming Language | Python |
| Local LLM Runtime | Ollama |
| Language Model | Llama 3.2 3B |
| Database | SQLite |
| Embedding Model | all-MiniLM-L6-v2 |
| Embedding Framework | Sentence Transformers |
| Vector Search | FAISS |
| Authentication Encryption | Fernet |
| Visualization | Plotly |
| UI | HTML / CSS |
| Version Control | Git / GitHub |

---

## Project Structure

```text
Reflections/
│
├── app.py              # Main application
├── analysis.py         # Analytics and visualizations
├── extract.py          # LLM-based structured extraction
├── search.py           # Semantic similarity search
├── recovery.py         # Recovery-focused retrieval
├── patterns.py         # Pattern detection
├── heatmap.py          # Monthly activity heatmap
├── db.py               # SQLite database operations
├── auth.py             # Authentication
├── seed.py             # Demo data generation
│
├── assets/             # Application assets
│
├── README.md
└── requirements.txt
```

---

## Installation

### Requirements

- Python 3.10 or later
- Ollama
- Git

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/reflections.git
cd reflections
```

### Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install the Local LLM

Install Ollama and pull the required model:

```bash
ollama pull llama3.2:3b
```

Ensure Ollama is running before starting the application.

### Run the Application

```bash
streamlit run app.py
```

The application will be available through the local Streamlit server.

---

## Demo Dataset

The project includes seeded demonstration data to make the application immediately usable during demonstrations.

The dataset contains representative student journal entries covering areas such as:

- Academic examinations
- GPA concerns
- Friendships
- Comparison
- Travel
- Academic stress
- Personal interests
- Recovery from difficult situations

The seed data allows similarity search, recovery retrieval, pattern analysis, and visualizations to be demonstrated without requiring a large amount of initial user data.

---

## Example Workflow

A typical processing pipeline is:

```text
Free-form Journal Entry
          |
          v
Structured Extraction
          |
          v
SQLite Storage
          |
          v
Embedding Generation
          |
          v
FAISS Similarity Search
          |
          v
Recovery Filtering
          |
          v
Pattern Detection
          |
          v
Contextual Reflection
```

For example, an entry describing poor academic performance may be analyzed for:

```text
Event:
CAT examination

Emotions:
Stress
Disappointment
Anxiety

Intensity:
8/10

Triggers:
Academic performance
Comparison
GPA
```

The system can then search previous entries for semantically similar situations and identify cases where the user subsequently recovered.

---

## Design Principles

### Privacy First

Personal journal information should remain local whenever practical.

### Journal First

Users can write naturally without manually selecting multiple categories.

### Context Over Isolation

Individual entries are analyzed in relation to the user's previous experiences.

### Recovery Over Rumination

The system prioritizes useful evidence of recovery rather than repeatedly surfacing negative experiences.

### Patterns Over Diagnoses

The application identifies recurring observations without attempting clinical interpretation.

---

## Limitations

Reflections is currently a prototype and has several limitations:

- Local LLM output quality depends on the selected model.
- Structured extraction may occasionally produce incorrect or incomplete information.
- Semantic similarity does not guarantee that two experiences are psychologically equivalent.
- Pattern detection can produce false correlations.
- Recovery detection depends on evidence available in the journal history.
- The current authentication implementation is intended for a prototype and should not be considered production-grade security.
- SQLite is primarily suitable for local and small-scale deployments.
- The application is not a substitute for professional mental health support.

---

## Future Improvements

Potential future development includes:

- Improved temporal analysis
- More robust recovery detection
- User-controlled memory management
- Explainable pattern evidence
- Improved retrieval ranking
- Larger local language models
- Encrypted database storage
- Long-term trend analysis
- Improved personalization
- Exportable reflection reports

---

## Project Objective

The objective of Reflections is to demonstrate how local AI, semantic search, structured information extraction, and longitudinal personal data can be combined to create a privacy-conscious journaling system.

Rather than providing generic responses, the system uses the user's own history as the primary source of context.

---

## License

This project is currently intended for educational and experimental use.

Add an appropriate open-source license before public distribution, such as:

```text
MIT License
```

---

## Acknowledgements

This project uses the following open-source technologies:

- Ollama
- Llama 3.2
- Sentence Transformers
- all-MiniLM-L6-v2
- FAISS
- SQLite
- Streamlit
- Plotly
