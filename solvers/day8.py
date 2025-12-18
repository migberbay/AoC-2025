# PART 1
# INSTRUCTIONS

# EXAMPLE

# PART 2

# INSTRUCTIONS

# EXAMPLE

from tqdm import tqdm
from .base_solver import solver
import math

def precalculate_distances(points_dict):
    """Precalculate all pairwise distances and return sorted list"""
    distances = []
    keys = list(points_dict.keys())
    
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            id1 = keys[i]
            id2 = keys[j]
            p1 = points_dict[id1]
            p2 = points_dict[id2]
            dist = math.dist(p1, p2)
            distances.append((dist, (id1, id2)))
    
    # Sort by distance
    distances.sort(key=lambda x: x[0])
    return distances

def connections_to_circuits(connections):
    circuits = []
    for conn in connections:
        # Find all circuits that contain either endpoint
        matching_circuits = []
        for circuit in circuits:
            if conn[0] in circuit or conn[1] in circuit:
                matching_circuits.append(circuit)
        
        if len(matching_circuits) == 0:
            # No existing circuit, create a new one
            circuits.append(set(conn))
        elif len(matching_circuits) == 1:
            # Add to existing circuit
            matching_circuits[0].update(conn)
        else:
            # Multiple circuits need to be merged
            merged = set(conn)
            for circuit in matching_circuits:
                merged.update(circuit)
                circuits.remove(circuit)
            circuits.append(merged)
            
    return circuits

# solver class has a self.parser to read the file for the day.
class solve(solver):
    def part1(self):
        num_conns = 1000
        
        data = self.parser.file_to_matrix_sep(',', to_type=int)
        data_dict = {i+1:d for i, d in enumerate(data)}
        
        # Precalculate and sort all distances
        sorted_distances = precalculate_distances(data_dict)
        
        connections = set()
        used_pairs = set()
        
        for dist, pair in sorted_distances:
            if len(connections) >= num_conns:
                break
            
            # Normalize pair to avoid duplicates
            normalized_pair = (min(pair), max(pair))
            if normalized_pair not in used_pairs:
                connections.add(pair)
                used_pairs.add(normalized_pair)

        circuits = connections_to_circuits(connections)
        circuits.sort(key=lambda x: len(x), reverse=True)
        
        return math.prod([len(c) for c in circuits[:3]])
    
    def part2(self):
        data = self.parser.file_to_matrix_sep(',', to_type=int)
        data_dict = {i+1:d for i, d in enumerate(data)}
        
        # Precalculate and sort all distances
        sorted_distances = precalculate_distances(data_dict)
        
        connections = []
        last_connection = None
        
        for _, pair in tqdm(sorted_distances):
            connections.append(pair)
            
            # Build circuits incrementally
            circuits = connections_to_circuits(connections)
            
            # Check if we have only one circuit (all connected)
            if len(circuits) == 1 and len(circuits[0]) == len(data_dict):
                last_connection = pair
                break
            
        # last_connection now contains the connection that joined everything
        print(f"Last connection that merged all: {last_connection}")
        
        # get the coordinates for the last connection
        p1 = data_dict[last_connection[0]]
        p2 = data_dict[last_connection[1]]
        
        print(f"Coordinates: {p1} <-> {p2}")
        
        return p1[0] * p2[0]