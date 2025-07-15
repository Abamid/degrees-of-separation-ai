import csv
from util import Node, QueueFrontier

names = {}
people = {}
movies = {}

def load_data(directory):
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            lower_name = row["name"].lower()
            if lower_name in names:
                names[lower_name].add(row["id"])
            else:
                names[lower_name] = {row["id"]}

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
    return person_ids[0]

def neighbors_for_person(person_id):
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for star_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, star_id))
    return neighbors

def shortest_path(source, target):
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)
    explored = set()

    while True:
        if frontier.empty():
            return None

        node = frontier.remove()

        if node.state == target:
            path = []
            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            return path

        explored.add(node.state)

        for movie_id, person_id in neighbors_for_person(node.state):
            if not frontier.contains_state(person_id) and person_id not in explored:
                child = Node(state=person_id, parent=node, action=movie_id)
                frontier.add(child)