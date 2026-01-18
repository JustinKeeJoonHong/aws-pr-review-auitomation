def word_count(file_path: str) -> dict:
    """
    Count the frequency of each word in a file.
    """
    counts = {}
    with open(file_path, 'r') as f:
        for line in f:
            words = line.split()
            for w in words:
                word = w.lower()
                counts[word] = counts.get(word, 0) + 1

    return counts