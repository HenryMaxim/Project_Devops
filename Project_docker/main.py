from urllib import response
from flask import Flask
from flask import render_template
import datetime
import json
import random
import time
import requests

microweb_app = Flask(__name__)

# Lijst van Duitse Provincies
provinces = ["Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen", "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"]

# Lijst van liedjes
songs = ["Your Grounds", "Relaxing Moment", "Captain Coda", "Gypsy Shit", "New Wonders", "Soul Mate"]



# gebruikte telefoonnummers setten
used_phone_numbers = set()

def generate_random_data(num_votes):
    # een lege lijst aanmaken voor al de data
    data_list = []

    # Aanmaken van lijst voor de stemmen per lied bij te houden
    song_votes = {}

    # Aanmaken van lijst voor de stemmen per provincie bij te houden
    province_song_votes = {}
    
    # De vote counter op 0 zetten
    for song in songs:
        song_votes[song] = 0

    # Generate the specified number of votes
    for i in range(num_votes):
        # Een random nummer genereren in het Duitse formaat "+49XXX XX XX XX"
        phone_number = f"+49{random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}"

        # Een telefoonnummer blijven genereren totdat er een ongebruikte bestaat
        while phone_number in used_phone_numbers:
            phone_number = f"+49{random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}"

        # Het gemaakte telefoonnummer bij de gebruikte toevoegen zodat deze niet tweemaal gebruikt wordt
        used_phone_numbers.add(phone_number)

        # Een random provincie van de lijst kiezen
        province = random.choice(provinces)

        # De tijd tot op de seconde precies bepalen
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Een random lied van de lijst kiezen
        song = random.choice(songs)

        # Bijtellen votes per song
        song_votes[song] += 1

        #Bijtellen van votes per regio
        if province not in province_song_votes:
            province_song_votes[province]={}
        if song not in province_song_votes[province]:
            province_song_votes[province][song] = 0
        province_song_votes[province][song] +=1

        # de aangemaakte data samenvoegen
        data = {
            "timestamp": timestamp,
            "phone_number": phone_number,
            "province": province,
            "song": song
        }

        # Toevoegen van de data aan de lijst
        data_list.append(data)

        song_votes = dict(sorted(song_votes.items(), key=lambda item: item[1], reverse=True))

        most_voted_song = max(song_votes, key=song_votes.get)

        most_voted_province_song = {}
        for province in province_song_votes:
            most_voted_province_song[province] = max(province_song_votes[province], key=province_song_votes[province].get)

    return data_list, song_votes, most_voted_song, most_voted_province_song

@microweb_app.route("/")
def main():
    num_votes = 3000
    data_list, song_votes, most_voted_song, most_voted_province_song = generate_random_data(num_votes)
    return render_template("index.html", datetime_now=datetime.datetime.now(), data_list=data_list, song_votes=song_votes, most_voted_song=most_voted_song, most_voted_province_song=most_voted_province_song)
    """
    In veronderstelling dat post link online was
    #converteren data naar json
    data = json.dumps(data_list)
    #api parameters instellen
    url = "http://127.0.0.1:8080/districts/in?country=Germany"
    headers ={"Content-Type": "application/json"}
    #Posten van data
    response = requests.post(url, data=data, headers=headers)
    #printen van antwoord
    print(response.status_code)
    #nakijken van response
    if response.status_code == 200:
        print("Post succesvol")
    else:
        print("Post failed")
    """

if __name__ == "__main__":
    microweb_app.run(host="0.0.0.0", port=5151)