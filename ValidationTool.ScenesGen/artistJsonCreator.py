import random
import uuid


TEAMS = [
    {"name": "Animators", "prob": 0.30, "lead": "Carles Prenafeta"},
    {"name": "Modelers", "prob": 0.30, "lead": "Omar Model"},
    {"name": "SurfaceArtists", "prob": 0.20, "lead": "Miki Surfa"},
    {"name": "ConceptArtists", "prob": 0.10, "lead": "Antonio Santamaria"},
    {"name": "TechArtists", "prob": 0.05, "lead": "Esteve Garriga"},
    {"name": "HHRRs", "prob": 0.05, "lead": "Gemma Dols"},
]
LEVELS = [
    ("Senior", 0.10),
    ("Mid", 0.40),
    ("Junior", 0.30),
    ("Intern", 0.20),
]

def get_random_level():
    r = random.random()
    cumulative = 0

    for level, prob in LEVELS:
        cumulative += prob
        if r <= cumulative:
            return level

    return LEVELS[-1][0]


def get_random_team_with_lead():
    r = random.random()
    cumulative = 0

    for team_data in TEAMS:
        cumulative += team_data["prob"]
        if r <= cumulative:
            return team_data

    return TEAMS[-1]  # fallback

def format_name_for_display(name: str):
    parts = name.split()
    
    if len(parts) == 1:
        return name

    # Convert "Stepan Batllori Martinez" -> "Stepan BM"
    return f"{parts[0]} {' '.join(p[0] for p in parts[1:])}"


def generate_id():
    return uuid.uuid4().hex[:12]

import json


def create_artist_json(artist_name: str, artist_dir):
    team_data = get_random_team_with_lead()

    data = {
        "name": format_name_for_display(artist_name),
        "id": generate_id(),
        "level": get_random_level(),
        "lead": team_data["lead"],
        "team": team_data["name"],
        "project": "ValidationTool",
        "slack_id": "U0BAQ7DS0L8",
        "teams_id": "ZXCVZXCV",
        "gmail": "stepanbatllorigt@gmail.com"
    }

    json_path = artist_dir / "artistLog.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"[JSON CREATED] {json_path}")


