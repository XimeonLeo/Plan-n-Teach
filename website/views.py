""" Standard routes for Plan'N'Teach """

from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note, User
from . import db
from os import path, makedirs


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def landing_page():
  return render_template("landing_page.html")


@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def homePage():
  if request.method == 'POST':
    note = request.form.get('note')

    if len(note) < 1:
      flash('Empty note cannot be saved!', category='error')
    else:
      new_note = Note(data=note, user_id=current_user.id)
      db.session.add(new_note)
      db.session.commit()
      flash('Note added!', category='success')
    
  return render_template("home.html", user=current_user)


def ensure_dir_exists(directory_name=''):
  if not path.exists(directory_name):
    makedirs(directory_name)

# Route for admin to upload files
@views.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
  if not current_user.is_admin:
    flash('Access Denied: Admin privilege required', category='error')
    return render_template('home.html', user=current_user)
 
  if request.method == 'POST' and 'file' in request.files:
    ensure_dir_exists('uploads')
    file = request.files['file']
    file.save('uploads/' + file.filename)
    flash('File uploaded successfully', category='success')
    return render_template('upload.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
def deleteNote():
  note = json.loads(request.data)
  note_id = note['note_id']
  note = Note.query.get(note_id)
  if note:
    if note.user_id == current_user.id:
      db.session.delete(note)
      db.session.commit()
      return jsonify({})
