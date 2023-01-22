from pydoc import plain
from flask import Flask
from flask import render_template
import datetime
import json
import random
import time

microweb_app = Flask(__name__)

# List of provinces in Germany
provinces = ["Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen", "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"]

# List of songs
songs = ["Your Grounds", "Relaxing Moment", "Captain Coda", "Gypsy Shit", "New Wonders", "Soul Mate"]



# Set to store used phone numbers
used_phone_numbers = set()

def generate_random_data(num_votes):
    # Create an empty list to store the data
    data_list = []

    # Create a dictionary to store the count of votes for each song
    song_votes = {}
    
    # Initialize the vote count for each song to 0
    for song in songs:
        song_votes[song] = 0

    # Generate the specified number of votes
    for i in range(num_votes):
        # Generate random phone number in the format "0XXX XX XX XX"
        phone_number = f"+49{random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}"

        # Keep generating a new phone number until we get one that has not been used
        while phone_number in used_phone_numbers:
            phone_number = f"+49{random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}"

        # Add the generated phone number to the set of used phone numbers
        used_phone_numbers.add(phone_number)

        # Select a random province from the list
        province = random.choice(provinces)

        # Get current timestamp (precise to the second)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Select a random song from the list
        song = random.choice(songs)

        # Increment the vote count for the selected song
        song_votes[song] += 1

        # Create a dictionary with the generated data
        data = {
            "timestamp": timestamp,
            "phone_number": phone_number,
            "province": province,
            "song": song
        }

        # Append the data dictionary to the list
        data_list.append(data)

        song_votes = dict(sorted(song_votes.items(), key=lambda item: item[1], reverse=True))

        most_voted_song = max(song_votes, key=song_votes.get)

    return data_list, song_votes, most_voted_song

@microweb_app.route("/")
def main():
    num_votes = 3000
    data_list, song_votes, most_voted_song = generate_random_data(num_votes)
    return render_template("index.html", datetime_now=datetime.datetime.now(), data_list=data_list, song_votes=song_votes, most_voted_song=most_voted_song)

if __name__ == "__main__":
    microweb_app.run(host="0.0.0.0", port=5151)