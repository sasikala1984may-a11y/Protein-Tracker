# Protein Tracker — Streamlit UI

This workspace contains a simple Streamlit front-end for the existing protein tracker MySQL database.

Setup

1. Create (or ensure) the MySQL database `protien_tracker` with table `pro_content` matching the original project.
2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run

```bash
streamlit run "streamlit_app.py"
```

Notes
- The app connects using the same credentials used in the original script (host=localhost, user=root, passwd=ridhan). Update `streamlit_app.py` if you need different credentials.
- For eggs the database is expected to store protein per egg (the original console app treats eggs as per-unit).
