import json
import os

def levenshtein_distance(s1, s2):
    """Fast Levenshtein distance for two strings."""
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    if not s2:
        return len(s1)
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (c1 != c2)))
        prev = curr
    return prev[-1]

def min_normalized_levenshtein(vals1, vals2):
    """Compute minimum normalized Levenshtein distance between two lists of values."""
    dists = [
        levenshtein_distance(str(v1), str(v2)) / max(len(str(v1)), len(str(v2)))
        if max(len(str(v1)), len(str(v2))) > 0 else 0.0
        for v1 in vals1 for v2 in vals2
    ]
    return min(dists)

def compute_matrix(ids, values_dict):
    """
    Compute normalized Levenshtein distance between all pairs in ids, using values_dict.
    Supports multiple strings per case (as lists).
    Returns: dict[id][id] = min normalized distance.
    """
    matrix = {}
    for idx1, id1 in enumerate(ids):
        vals1 = values_dict[id1] if isinstance(values_dict[id1], list) else [values_dict[id1]]
        matrix[id1] = {}
        for idx2, id2 in enumerate(ids):
            if idx2 < idx1:
                matrix[id1][id2] = matrix[id2][id1]
            elif id1 == id2:
                matrix[id1][id2] = 0.0
            else:
                vals2 = values_dict[id2] if isinstance(values_dict[id2], list) else [values_dict[id2]]
                matrix[id1][id2] = min_normalized_levenshtein(vals1, vals2)
    return matrix

def main():
    test_case_file = os.path.join("test", "cases.json")
    string_distance_dir = os.path.join("test", "string-distance")
    input_matrix_file = os.path.join(string_distance_dir, "input.json")
    output_matrix_file = os.path.join(string_distance_dir, "output.json")
    print(f"Loading test cases from {test_case_file}...")
    os.makedirs(string_distance_dir, exist_ok=True)

    try:
        with open(test_case_file, "r") as f:
            test_cases = json.load(f)
        if not isinstance(test_cases, dict) or not test_cases:
            print("No test cases found. Exiting.")
            return
    except Exception as e:
        print(f"Error loading {test_case_file}: {e}")
        return

    ids = list(test_cases.keys())
    input_values = {tid: test_cases[tid]["input"] for tid in ids}
    # Only include output if present and not blank/None
    output_values = {tid: test_cases[tid]["output"] for tid in ids if "output" in test_cases[tid] and test_cases[tid]["output"] not in ("", None)}
    has_output = bool(output_values)

    print("Calculating input distance matrix for %d cases..." % len(ids))
    input_matrix = compute_matrix(ids, input_values)
    print(f"Saving input distance matrix to {input_matrix_file}...")
    with open(input_matrix_file, "w") as f:
        json.dump(input_matrix, f, indent=2)

    if has_output:
        print("Calculating output distance matrix for %d cases..." % len(output_values))
        output_matrix = compute_matrix(ids, output_values)
        print(f"Saving output distance matrix to {output_matrix_file}...")
        with open(output_matrix_file, "w") as f:
            json.dump(output_matrix, f, indent=2)
    else:
        print("No valid outputs found. Skipping output distance matrix.")

    print("Successfully created distance matrices for", len(ids), "cases.")

if __name__ == "__main__":
    main()