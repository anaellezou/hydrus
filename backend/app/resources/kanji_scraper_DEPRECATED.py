""" DEPRECATED: This script is no longer used as the data is now stored in a JSON file. It was originally created to scrape kanji data from a website and export it to a JSON file for use in the application."""
""" DO NOT LAUNCH THIS SCRIPT """"
""" Leaving this as an example for future use """"
import requests
from bs4 import BeautifulSoup
import json

#url = "https://hirakan.com/blogs/japanese/kanji-jlpt-n5-list"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

start_section = soup.find("h2", string="Your JLPT N5 Kanji Playbook")

if not start_section:
    raise ValueError("Section 'Your JLPT N5 Kanji Playbook' not found")

tables = start_section.find_all_next("table")

kanji_list = []

for table in tables:
    rows = table.select("tr")[1:]

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        kanji   = cols[0].text.strip()
        meaning_raw = cols[1].text.strip()
        onyomi  = cols[2].text.strip()
        kunyomi = cols[3].text.strip()

        # Format the meaning field into a list of string if there are multiple meaning or a simple string
        meanings = meaning_raw.split(", ") if ", " in meaning_raw else meaning_raw

        kanji_data = {
            "kanji": kanji,
            "onyomi": onyomi,
            "kunyomi": kunyomi,
            "meaning": meanings
        }
        kanji_list.append(kanji_data)

# Export data in a JSON file
#with open("kanji_n5.json", "w", encoding="utf-8") as json_file:
#    json.dump(kanji_list, json_file, ensure_ascii=False, indent=4)

print("Data exported into kanji_n5.json")