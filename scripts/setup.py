import json
import os
import numpy as np

def levenshtein_distance(s1, s2):
    """
    Calculates the Levenshtein distance between two strings.
    A simple, pure-Python implementation.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def calculate_distance_matrix(test_cases):
    """
    Calculates and normalizes the Levenshtein distance matrix for test case inputs.
    """
    input_strings = [tc['inputs']['rawString'] for tc in test_cases]
    num_cases = len(input_strings)
    
    # Initialize an empty matrix with numpy
    dist_matrix = np.zeros((num_cases, num_cases))

    print("Calculating distance matrix...")
    for i in range(num_cases):
        for j in range(i, num_cases):
            if i == j:
                dist_matrix[i, j] = 0.0
            else:
                s1 = input_strings[i]
                s2 = input_strings[j]
                
                # Calculate Levenshtein distance
                distance = levenshtein_distance(s1, s2)
                
                # Normalize the distance to a value between 0 and 1
                max_len = max(len(s1), len(s2))
                normalized_distance = distance / max_len if max_len > 0 else 0.0
                
                # Matrix is symmetric
                dist_matrix[i, j] = normalized_distance
                dist_matrix[j, i] = normalized_distance
    
    print("Matrix calculation complete.")
    return dist_matrix.tolist() # Convert numpy array to list for JSON serialization

def main():
    """
    Main function to load data, run calculation, and save results.
    """
    data_dir = "data"
    input_file = os.path.join(data_dir, "test_cases.json")
    output_file = os.path.join(data_dir, "input_distance_matrix.json")

    # --- 1. Load test cases ---
    print(f"Loading test cases from {input_file}...")
    try:
        with open(input_file, "r") as f:
            test_data = json.load(f)
        test_cases = test_data.get("testCases", [])
        if not test_cases:
            print("No test cases found. Exiting.")
            return
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Exiting.")
        return

    # --- 2. Calculate distance matrix ---
    matrix = calculate_distance_matrix(test_cases)
    test_case_ids = [tc["id"] for tc in test_cases]

    # --- 3. Prepare and save the output file ---
    output_data = {
        "testCaseIds": test_case_ids,
        "matrix": matrix
    }

    print(f"Saving distance matrix to {output_file}...")
    os.makedirs(data_dir, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print("Successfully created input_distance_matrix.json.")

if __name__ == "__main__":
    main()
