import numpy as np
import random


class ACO_TSP:
    def __init__(
        self,
        distance_matrix,
        num_ants,
        num_iterations=50,
        alpha=1,
        beta=5,
        evaporation_rate=0.5,
        Q=100,
    ):
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.Q = Q

        self.pheromone_matrix = np.ones((self.num_cities, self.num_cities))
        self.heuristic_matrix = 1 / (
            self.distance_matrix + np.eye(self.num_cities)
        )  # avoid division by zero

    def run(self):
        best_cost = float("inf")
        best_path = None
        pheromone_history = {
            edge: [] for edge in [(0, 1), (1, 2), (2, 3)]
        }  # example edges
        cost_history = []

        for iteration in range(self.num_iterations):
            all_paths = []
            all_costs = []

            for _ in range(self.num_ants):
                path = self.construct_solution()
                cost = self.calculate_path_cost(path)
                all_paths.append(path)
                all_costs.append(cost)

                if cost < best_cost:
                    best_cost = cost
                    best_path = path

            self.update_pheromones(all_paths, all_costs)

            if (iteration + 1) % 10 == 0:
                cost_history.append(best_cost)
                for edge in pheromone_history:
                    pheromone_history[edge].append(
                        self.pheromone_matrix[edge[0]][edge[1]]
                    )

        return best_path, best_cost

    def construct_solution(self):
        path = []
        visited = set()
        current_city = random.randint(0, self.num_cities - 1)
        path.append(current_city)
        visited.add(current_city)

        for _ in range(self.num_cities - 1):
            probabilities = self.calculate_transition_probabilities(
                current_city, visited
            )
            next_city = self.roulette_selection(probabilities)
            path.append(next_city)
            visited.add(next_city)
            current_city = next_city

        path.append(path[0])  # Return to start
        return path

    def calculate_transition_probabilities(self, current_city, visited):
        probabilities = []
        total = 0
        for j in range(self.num_cities):
            if j not in visited:
                pheromone = self.pheromone_matrix[current_city][j] ** self.alpha
                heuristic = self.heuristic_matrix[current_city][j] ** self.beta
                prob = pheromone * heuristic
                probabilities.append((j, prob))
                total += prob

        probabilities = [(city, prob / total) for city, prob in probabilities]
        return probabilities

    def roulette_selection(self, probabilities):
        r = random.random()
        cumulative = 0.0
        for city, prob in probabilities:
            cumulative += prob
            if r <= cumulative:
                return city
        return probabilities[-1][0]  # fallback

    def calculate_path_cost(self, path):
        return sum(
            self.distance_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1)
        )

    def update_pheromones(self, paths, costs):
        self.pheromone_matrix *= 1 - self.evaporation_rate

        for path, cost in zip(paths, costs):
            for i in range(len(path) - 1):
                a, b = path[i], path[i + 1]
                self.pheromone_matrix[a][b] += self.Q / cost
                self.pheromone_matrix[b][a] += self.Q / cost  # Symmetric


def generate_distance_matrix(num_cities, seed=42):
    np.random.seed(seed)
    mat = np.random.randint(3, 51, size=(num_cities, num_cities))
    mat = (mat + mat.T) // 2
    np.fill_diagonal(mat, 0)
    return mat


def print_matrix(mat):
    for row in mat:
        print(row)


# === Generate distances for 10 and 20 cities ===
distance_10 = generate_distance_matrix(10, seed=1)
distance_20 = generate_distance_matrix(20, seed=2)

print("Distance Matrix for 10 Cities:")
print_matrix(distance_10)
print("\nDistance Matrix for 20 Cities:")
print_matrix(distance_20)


# === Run ACO for different ant counts ===
def run_aco_on_config(distance_matrix, city_count):
    for ants in [1, 5, 10, 20]:
        print(f"\n=== Running ACO on {city_count} cities with {ants} ants ===")
        aco = ACO_TSP(distance_matrix, num_ants=ants)
        best_path, best_cost = aco.run()
        print(f"Best Path: {best_path}")
        print(f"Best Cost: {best_cost}")


print("\n\n=== ACO on 10 Cities ===")
run_aco_on_config(distance_10, 10)

print("\n\n=== ACO on 20 Cities ===")
run_aco_on_config(distance_20, 20)
