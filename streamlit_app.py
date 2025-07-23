import streamlit as st
import csv

# === Load the dataset ===
people = {}
movies = {}
names = {}

def load_data(directory):
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            lower = row["name"].lower()
            names.setdefault(lower, set()).add(row["id"])

    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

def person_id_for_name(name):
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    return person_ids[0]  # Assume first match for simplicity

def neighbors_for_person(person_id):
    return set(
        (movie_id, star_id)
        for movie_id in people[person_id]["movies"]
        for star_id in movies[movie_id]["stars"]
    )

def shortest_path(source, target):
    from collections import deque

    frontier = deque()
    frontier.append((source, []))
    explored = set()

    while frontier:
        current_person, path = frontier.popleft()
        explored.add(current_person)

        for movie_id, neighbor in neighbors_for_person(current_person):
            if neighbor not in explored:
                new_path = path + [(movie_id, neighbor)]
                if neighbor == target:
                    return new_path
                frontier.append((neighbor, new_path))

    return None

# === Streamlit App ===
st.set_page_config(page_title="🎬 Degrees of Separation AI", layout="centered")
st.title("🎬 Degrees of Separation")
st.write("Find how two actors are connected through shared movies using AI search!")

load_data("small")

name1 = st.text_input("Enter the first actor’s name:")
name2 = st.text_input("Enter the second actor’s name:")

if st.button("🔍 Find Connection"):
    source = person_id_for_name(name1)
    target = person_id_for_name(name2)

    if source is None or target is None:
        st.error("⚠️ One or both names were not found in the dataset.")
    else:
        path = shortest_path(source, target)
        if path is None:
            st.warning("❌ No connection found.")
        else:
            st.success(f"✅ {len(path)} degrees of separation found!")
            current = source
            for i, (movie_id, person_id) in enumerate(path):
                movie = movies[movie_id]["title"]
                p1 = people[current]["name"]
                p2 = people[person_id]["name"]
                st.write(f"{i + 1}: {p1} and {p2} starred in *{movie}*")
                current = person_id
