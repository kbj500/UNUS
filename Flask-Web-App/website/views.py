from flask import Blueprint, render_template, request, flash, jsonify, session
from flask_login import login_required, current_user
from .models import Note
from . import db
import json, requests
from website.spotify_client import SpotifyClient


client_id = 'cfeac2b1230c4ab9b1644d339efbb9ff'
client_secret = '4f936090b2604b4cabc4382c24289089'

spotify_client = SpotifyClient(client_id, client_secret, port=5000)

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')
    
    # Fetch and display the verified Spotify user's library
    authorization_header = session.get('authorization_header')
    if authorization_header:
        headers = {'Authorization': authorization_header['Authorization']}

        access_token = spotify_client._access_token

        library_response = requests.get(spotify_client.SPOTIFY_API_URL + '/me', headers=headers)
        print("\nStatus Code \me:",library_response.status_code, "\n")
        library_response = requests.get(spotify_client.SPOTIFY_API_URL + '/me/tracks', headers=headers)
        print("\nStatus Code:",library_response.status_code, "\n")
        if library_response.status_code == 200:
            library_data = library_response.json()
            print("\n JSON: \n",json.dumps(library_data, indent = 4),"\n")
            #print("\n JSON: \n",pretty_json,"\n")
            library_items = library_data.get('items', [])
            library_tracks = [item['track'] for item in library_items]
            library_tracks_ids = [track['id'] for track in library_tracks]
            print("\ntrack_id:",library_tracks_ids[1:3],"\n")
            print("\ntype track_id:",type(library_tracks_ids))
            #print("\nLT:",type(library_tracks),"\n")
            # Process and pass the library tracks to the template
            return render_template("home.html", user=current_user, library_tracks_ids = library_tracks_ids, access_token=access_token, scope = spotify_client.SCOPE)

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

