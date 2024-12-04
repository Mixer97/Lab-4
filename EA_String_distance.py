import random
import math

# Parameters for genetic algorithm
NPOP = 500
NTOUR = 5
PMUT = 0.10
NITERATIONS = 100
TARGET = "BESTIALEEEEEEEEEEEEEE"
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGJKLMNOPQRSTUVWXYZ"
MAX_LENGTH = 20

# Can be used if it is needed a PMUT that needs to change over the generations 
def calculate_pmut_exponential(gen, max_pmut, min_pmut):
    k = 5 / NITERATIONS  # Adjust rate of decay
    return min_pmut + (max_pmut - min_pmut) * math.exp(-k * gen)

# Levenshtein Distance Implementation
def levenshtein_distance(x, y):
    m, n = len(x), len(y)
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if x[i - 1] != y[j - 1]:
                curr[j] = 1 + min(curr[j - 1], prev[j - 1], prev[j])
            else:
                curr[j] = prev[j - 1]
        prev, curr = curr, prev
    return prev[n]

# Initialized population
def init_population() -> list:
    initialized_population = list()
    for i in range(NPOP):
        tmp = list()
        for j in range(random.randint(2,MAX_LENGTH)):
            tmp.append(random.choice(ALPHABET))
        initialized_population.append(tmp)
    return initialized_population

# fitness function
def fitness_func(current_string: list) -> int:
    distance = levenshtein_distance(TARGET, current_string)
    return distance
            
# Reproduction function
def reproduction(initialized_population:list, counter_population:int) -> list:
    offspring = list()
    while len(offspring) < NPOP:
        # global PMUT
        # PMUT = calculate_pmut_exponential(counter_population, 0.40, 0.10)
        s1 = tournament_selection(initialized_population)
        s2 = tournament_selection(initialized_population)
        child = crossover(s1, s2)
        child_mut = random_mutation(child)
        child_mut = insert_mutation(child_mut)
        child_mut = delete_mutation(child_mut)
        offspring.append(child_mut)
        
    return offspring

# Randomly mutate a random char in to another one        
def random_mutation(child: list) -> list:
    if random.random() < PMUT:
        random_index = random.randint(0, len(child) - 1)
        random_letter = random.choice(ALPHABET)
        child[random_index] = random_letter  # Mutate the character in the list
    return child

# Randomly insert a char in the list
def insert_mutation(child: list) -> list:
    if random.random() < PMUT and len(child) < MAX_LENGTH:
        random_index = random.randint(0, len(child) - 1)
        random_letter = random.choice(ALPHABET)
        child.insert(random_index, random_letter) 
    return child

# Randomly delete a char in the list    
def delete_mutation(child: list) -> list:
    if random.random() < PMUT and len(child) > 2:
        random_index = random.randint(0, len(child) - 1)
        child.pop(random_index)
    return child

# Crossover function (single-point crossover)
def crossover(parent1: list, parent2: list) -> list:
    crossover_point = random.randint(0, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

# get fitness list
def get_fitness_list(str_list: list) -> list:
    fitness_list = list()
    i = 0
    for value in str_list:
        fitness_list.append(fitness_func(str_list[i]))
        i += 1
    return fitness_list

# Tournament selection
def tournament_selection(initialized_population:list) -> list:
    tmp_list = list()
    fitness_list = list()
    best_strings_list = list()
    
    while len(tmp_list) < NTOUR:   # randomly select NTOUR strings from initialized_population and get their fitness
        random_str = random.choice(initialized_population)
        tmp_list.append(random_str)
        fitness_list.append(fitness_func(random_str))

    best_fitness:int = min(fitness_list)  # Get the best fitness value
    i = 0
    for value in fitness_list:    # Get strings corrisponding to the best fitness value
        if fitness_list[i] == best_fitness:
            best_strings_list.append(tmp_list[i])
        i += 1
        
    return random.choice(best_strings_list)

# Evolutionary algorithm
def evolutionary_algorithm():
    
    initialized_population = init_population()
    best_fitness = float('inf')  # Initialize best fitness to infinity
    best_individual = None
    final_best_individuals_list = list()
    
    counter:int = 0
    while counter < NITERATIONS:
        counter += 1
        offspring = reproduction(initialized_population, counter)
        initialized_population += offspring
        current_fitness_list = get_fitness_list(initialized_population)
        while len(initialized_population) > NPOP:
            worst_index = current_fitness_list.index(max(current_fitness_list))
            #print("before" + str(worst_index))
            initialized_population.pop(worst_index)
            current_fitness_list.pop(worst_index)
            #print("after" + str(worst_index))
        
        # Track best individual
        current_best_fitness = min(current_fitness_list)
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_individual = initialized_population[current_fitness_list.index(best_fitness)]
            
        print(f"Generation {counter}, Best Fitness: {best_fitness}, Best String Representative: {''.join(best_individual)}")
        
    current_fitness_list = get_fitness_list(initialized_population)
    
    i = 0
    for value in current_fitness_list:
        if value == best_fitness:
            final_best_individuals_list.append(initialized_population[i])
            i += 1
            
    return final_best_individuals_list

# Run the algorithm
if __name__ == "__main__":
    best_individual_list = evolutionary_algorithm()
    print(len(best_individual_list))
    
    # Using list comprehension to join each inner list into a string
    best_individuals_list_of_strings = [''.join(inner_list) for inner_list in best_individual_list]
    
    # Removing duplicates 
    best_individuals_unique = list(set(best_individuals_list_of_strings))
    
    num_columns = 3
    print(f"Best individuals after {NITERATIONS} generations:")

    # Print in columns, dynamically handling row sizes
    for i in range(0, len(best_individuals_unique), num_columns):
        # Slice the list
        row = best_individuals_unique[i:i + num_columns]
        
        # Format the row depending on its length
        print(" ".join(f"{item:<20}" for item in row))

### COMMENTI ###
# Maybe consider putting a minus sign on the fitness function so we can work with the max and not the min.




# Quadrato
# Quadricipiti
# Trevirato