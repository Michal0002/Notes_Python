from flask import Flask, request, render_template, redirect, send_file
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def init_db():
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        priority TEXT NOT NULL, 
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
    connection.commit()
    connection.close()

init_db()

class Note:
    def __init__(self,title,content, priority):
        self.title = title
        self.content = content
        self.priority = priority
    
    def save(self):
        connection = sqlite3.connect('notes.db')
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO notes (title, content, priority) VALUES (?, ?, ?)''', (self.title, self.content, self.priority))
        connection.commit()
        connection.close()

    def get_all_notes():
        connection = sqlite3.connect('notes.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM notes")
        notes = cursor.fetchall()
        connection.close()
        return notes

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        if 'title' in request.form and 'content' in request.form:
            title = request.form['title']
            content = request.form['content']
            priority = request.form['priority']        
            note = Note(title, content, priority)
            note.save()
            return redirect('/display_notes')
        else:
            return "Error: Missing required data (title or note content)"
    else:
        return render_template('add_note.html')

@app.route('/display_notes')
def display_notes():
    notes = Note.get_all_notes()
    return render_template('display_notes.html', notes=notes)

@app.route('/download_notes', methods=['POST'])
def download_notes():
    notes = Note.get_all_notes()
    with open('notes.txt', 'w') as file:
        for note in notes:
            file.write(f"Title: {note[1]}\nContent: {note[2]}\n\n")
    return send_file('notes.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
