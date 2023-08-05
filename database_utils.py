import sqlite3

DATABASE_NAME = 'streamlit_app_data.db'

def setup_database():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS api_data (
            id INTEGER PRIMARY KEY,
            content_type TEXT,
            text_input TEXT,
            tone_option TEXT,
            tone_input TEXT,
            generated_text TEXT,
            guidance_option TEXT,
            guidance_input TEXT,
            compliance_result TEXT,
            questions_option TEXT,
            persona_option TEXT,
            persona_result TEXT
        )
    ''')

    conn.commit()
    conn.close()

def store_in_database(data):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute('''
        INSERT INTO api_data (
            content_type, text_input, tone_option, tone_input, generated_text, 
            guidance_option, guidance_input, compliance_result, 
            questions_option, persona_option, persona_result
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('content_type', None), 
        data.get('text_input', None), 
        data.get('tone_option', None), 
        data.get('tone_input', None), 
        data.get('generated_text', None),
        data.get('guidance_option', None), 
        data.get('guidance_input', None), 
        data.get('compliance_result', None),
        data.get('questions_option', None), 
        data.get('persona_option', None), 
        data.get('persona_result', None)
    ))

    conn.commit()
    conn.close()

def fetch_previous_response(id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute('SELECT * FROM api_data WHERE id = ?', (id,))
    record = c.fetchone()
    conn.close()

    if record:
        columns = ["id", "content_type", "text_input", "tone_option", "tone_input", "generated_text", "guidance_option", "guidance_input", "compliance_result", "questions_option", "persona_option", "persona_result"]
        return dict(zip(columns, record))
    return None
