from flask import Blueprint, render_template, request, flash, jsonify, session
from flask_login import login_required, current_user
from .models import User
from . import db
import json, requests
from website.spotify_client import SpotifyClient


client_id = '8e2db28f21e749d797722f5dc351e65a'
client_secret = '38269d3f577d4c34a67e2b2978f8a9e6'

spotify_client = SpotifyClient(client_id, client_secret, port=5000)

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():    
    soundcloud_id_entered = False
    #if(current_user.sound_c):
    if request.method == 'POST':
        sound_cloud_id = request.form['SoundCloudID']
        # Process the username or perform any other action with the data
        print("sound_cloud_id")
        soundcloud_id_entered = True
    # Fetch and display the verified Spotify user's library
    authorization_header = session.get('authorization_header')
    if authorization_header:
        headers = {'Authorization': authorization_header['Authorization']}
       
        access_token = spotify_client._access_token

        library_response = requests.get(spotify_client.SPOTIFY_API_URL + '/me', headers=headers)
        print("\nStatus Code \me:",library_response.status_code, "\n")     
        library_data = library_response.json()
        local_counter = 0
        library_tracks_ids_total = []
        #below in the url is a limit where you can change how much each pull will grab from your library 
        library_tracks_url = f"/me/tracks?offset={local_counter}&limit=50"
        while(True):
            
            # change this number to increase amount of songs show 
            #currently it will be very slow with anything above 20-30 due to that fact
                #that it is loading all those imaiges at once
            if(local_counter >= 20):
                break
            library_response = requests.get(spotify_client.SPOTIFY_API_URL + library_tracks_url, headers=headers) 
            print("\nStatus Code \me \ tracks:",library_response.status_code, "\n")
            
            if library_response.status_code == 200:
                library_data = library_response.json()
                #print("\n JSON: \n",json.dumps(library_data, indent = 4),"\n")
                #print("\n JSON: \n",pretty_json,"\n")
                library_items = library_data.get('items', [])
                library_tracks = [item['track'] for item in library_items]
                library_tracks_ids = [track['id'] for track in library_tracks]
                local_counter += len(library_tracks_ids)
                #print("\ntrack_id:",library_tracks_ids[1:3],"\n")
                #print("\ntype track_id:",type(library_tracks_ids))
                #print("\nLT:",type(library_tracks),"\n")
                # Process and pass the library tracks to the template
                library_tracks_ids_total.extend(library_tracks_ids)
            else:
                print(library_response.content)
                break
        
    ##souncloud entered and spotify entered    
    if (soundcloud_id_entered == True and authorization_header):
        print("soundcloud id entered is true")
        return render_template("home.html", user=current_user, library_tracks_ids = library_tracks_ids_total, access_token=access_token, scope = spotify_client.SCOPE,sound_cloud_id = sound_cloud_id)
    ##souncloud not entered and spotify entered
    elif (soundcloud_id_entered == False and authorization_header):
        print("soundcloud id entered is false")
        return render_template("home.html", user=current_user, library_tracks_ids = library_tracks_ids_total, access_token=access_token, scope = spotify_client.SCOPE)
    ##souncloud entered and spotify not entered
    if (soundcloud_id_entered == True):
        if(authorization_header == None):
            print("soundcloud id entered is true")
            return render_template("home.html", user=current_user,sound_cloud_id = sound_cloud_id)
    ##souncloud not entered and spotify not entered
    elif (soundcloud_id_entered == False and authorization_header == None):
        print("soundcloud id entered is false")
        return render_template("home.html", user=current_user)
