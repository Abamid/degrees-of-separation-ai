import streamlit as st
import csv
import sys

# ==== DATA STRUCTURES ====
names = {}      # Maps names to a set of corresponding person_ids
people = {}     # Maps person_ids to a dict of: name, birth, movies they've starred in
movies = {}     # Maps movie_ids to a dict of: title, year, stars (a set of person_ids)

# ==== Load Data ====
def load_data(directory):
    # Load people.csv
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            name_key = row["name"].lower()
            if name_key not in names:
                names[name_key] = {row["id"]}
            else:
                names[name_key].add(row["id"])

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
                pass  # Skip if person/movie ID not found

# ==== Helper Functions ====
def person_id_for_name(name):
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        st.warning("Multiple people found. Using the first match.")
    return person_ids[0]

def neighbors_for_person(person_id):
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for star_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, star_id))
    return neighbors

# ==== Search Algorithm ====
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
        else:
            return self.frontier.pop(0)

def shortest_path(source, target):
    frontier = QueueFrontier()
    start = Node(state=source, parent=None, action=None)
    frontier.add(start)

    explored = set()

    while True:
        if frontier.empty():
            return None

        node = frontier.remove()

        if node.state == target:
            # Reconstruct path
            path = []
            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            return path

        explored.add(node.state)

        for movie_id, person_id in neighbors_for_person(node.state):
            if person_id not in explored and not frontier.contains_state(person_id):
                child = Node(state=person_id, parent=node, action=movie_id)
                frontier.add(child)

# ==== STREAMLIT APP ====

st.set_page_config(page_title="Degrees of Separation", page_icon="🎬")
st.title("🎬 Degrees of Separation")
st.write("Find how two actors are connected through shared movies using AI search (BFS).")

# Load data
load_data("degrees_project_colab/small")
st.success(f"Dataset loaded: {len(people)} people, {len(movies)} movies.")

# User input
name1 = st.text_input("Enter the first actor’s name:", "Michael Fassbender")
name2 = st.text_input("Enter the second actor’s name:", "Jennifer Lawrence")

if st.button("Find Connection"):
    source = person_id_for_name(name1)
    target = person_id_for_name(name2)

    if source is None or target is None:
        st.error("Actor not found in the dataset.")
    else:
        path = shortest_path(source, target)
        if path is None:
            st.error("No connection found between the two actors.")
        else:
            st.success(f"{len(path)} degrees of separation found!")
            current = source
            for i, (movie_id, person_id) in enumerate(path):
                movie = movies[movie_id]["title"]
                person1 = people[current]["name"]
                person2 = people[person_id]["name"]
                st.write(f"{i+1}: {person1} and {person2} starred in *{movie}*")
                current = person_id
