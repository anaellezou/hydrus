import json

with open("app/resources/kanji_n5.json", "r", encoding="utf-8") as f:
    kanji_data = json.load(f)

corrected = []
for entry in kanji_data:
    corrected.append({
        "kanji":   entry["kanji"],
        "onyomi":  entry["meaning"],   
        "kunyomi": entry["onyomi"],    
        "meaning": entry["kunyomi"],   
    })

with open("app/resources/kanji_n5.json", "w", encoding="utf-8") as f:
    json.dump(corrected, f, ensure_ascii=False, indent=4)

print("JSON corrigé.")