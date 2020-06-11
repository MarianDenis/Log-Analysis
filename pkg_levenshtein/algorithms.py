def compute_distance(first_string, second_string):
    if first_string == '-' and second_string == '-':
        return 0
    elif first_string == '-':
        return len(second_string)
    elif second_string == '-':
        return len(first_string)
    else:
        rows = len(first_string) + 1
        cols = len(second_string) + 1
        dist = [[0 for x in range(cols)] for x in range(rows)]

        for i in range(1, rows):
            dist[i][0] = i

        for i in range(1, cols):
            dist[0][i] = i

        for col in range(1, cols):
            for row in range(1, rows):
                if first_string[row - 1] == second_string[col - 1]:
                    cost = 0
                else:
                    cost = 1
                dist[row][col] = min(dist[row - 1][col] + 1,  # deletion
                                     dist[row][col - 1] + 1,  # insertion
                                     dist[row - 1][col - 1] + cost)  # substitution

        return dist[row][col]


def compute_similarity(s1: str, s2: str):
    if not s1 or not s2:
        return 1.0
    if len(s1) == 0 or len(s2) == 0:
        return 1.0
    s1 = s1.lower()
    s2 = s2.lower()
    if s1 == s2:
        return 0.0

    steps_for_match = compute_distance(s1, s2)

    result = steps_for_match / max(len(s1), len(s2)) # 1 - inseamna complet diferite; 0 - inseamna exact la fel

    return result


if __name__ == '__main__':
    print(compute_similarity("PUT", "POST"))
