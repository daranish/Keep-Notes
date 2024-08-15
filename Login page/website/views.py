from flask import Blueprint, flash,render_template, request,jsonify
from flask_login import login_required,current_user
from .models import Note
from . import db
import json

from website.auth import login


views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note)<1:
            flash('Note is too small!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Created Successfully', category='success')    

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    data = request.get_json()
    noteId = data.get('noteId')
    note = Note.query.get(noteId)
    
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Unauthorized'}), 403
    else:
        return jsonify({'error': 'Note not found'}), 404 