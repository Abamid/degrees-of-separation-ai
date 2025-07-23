# streamlit_app.py

import streamlit as st
import csv

# ==== Data Structures ====

people = {}
movies = {}
names = {}

# ==== Load Data ====

def load_data(directory):
    """
    Load people, movies, and stars from CSV files into memory.
    """
    # Load people.csv
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            names.setdefault(row["name"].lower(), set()).add(row["id"])

    # Load movies.csv
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars.csv
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

# ==== Helper Functions ====

def person_id_for_name(name):
    person_ids = list(names.get(name.lower(), set()))
    if not person_ids:
        return None
    elif len(person_ids) == 1:
        return person_ids[0]
    else:
        return person_ids[0]  # just return the first match for simplicity

def neighbors_for_person(person_id):
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for star_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, star_id))
    return neighbors

# ==== Breadth-First Search ====

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class QueueFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        return self.frontier.pop(0)

def shortest_path(source, target):
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    explored = set()

    while not frontier.empty():
        node = frontier.remove()
        if node.state == target:
            path = []
            while node.parent:
                path.append((node.action, node.state))
                node = node.parent
            return path[::-1]

        explored.add(node.state)

        for movie_id, person_id in neighbors_for_person(node.state):
            if not frontier.contains_state(person_id) and person_id not in explored:
                child = Node(state=person_id, parent=node, action=movie_id)
                frontier.add(child)

    return None

# ==== Streamlit UI ====

st.set_page_config(page_title="Degrees of Separation", layout="centered")
st.title("🎬 Degrees of Separation")
st.write("Find how two actors are connected through shared movies using AI search!")

# Load data
load_data("small")
st.success(f"✅ Dataset loaded: {len(people)} people, {len(movies)} movies")

# User input
name1 = st.text_input("🔍 Enter the first actor’s name:")
name2 = st.text_input("🎯 Enter the second actor’s name:")

if name1 and name2:
    source = person_id_for_name(name1)
    target = person_id_for_name(name2)

    if source is None:
        st.error(f"❌ Actor '{name1}' not found.")
    elif target is None:
        st.error(f"❌ Actor '{name2}' not found.")
    else:
        with st.spinner("🔎 Searching for connection..."):
            path = shortest_path(source, target)

        if path is None:
            st.warning("⚠️ No connection found between the two actors.")
        else:
            st.success(f"✅ {len(path)} degrees of separation found!")
            current = source
            for i, (movie_id, person_id) in enumerate(path):
                movie = movies[movie_id]["title"]
                person1 = people[current]["name"]
                person2 = people[person_id]["name"]
                st.write(f"**{i + 1}:** {person1} and {person2} starred in *{movie}*")
                current = person_id
