ALPHABET = list("abcdefghijklmnopqrstuvwxyz")

def get_variable_name_from_int(index: int) -> str:
    parts = []
    temp_index = index
    first_round = True

    while first_round or temp_index > 0:
        idx = temp_index % len(ALPHABET)
        parts.append(ALPHABET[idx])

        temp_index = int(temp_index / len(ALPHABET))
        first_round = 0

    return "".join(parts)