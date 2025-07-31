import sqlite3

conn = sqlite3.connect('qa.db')
c = conn.cursor()

#create tables
c.execute("""
    CREATE TABLE IF NOT EXISTS questions(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          question_text TEXT NOT NULL
          )
""")
c.execute(
    """
    CREATE TABLE IF NOT EXISTS answer(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        answer_text TEXT NOT NULL,
        FOREIGN KEY(question_id) REFERENCES questions(id) 
    )
"""
)


# Optional: Add sample questions and answers
c.execute("INSERT INTO questions (question_text) VALUES ('What is Python?')")
c.execute("INSERT INTO answers (question_id, answer_text) VALUES (1, 'A programming language.')")

conn.commit()
conn.close()