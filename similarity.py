def tokenize(text):
    cleaned = ""
    for ch in text.lower():
        if ch.isalnum():
            cleaned += ch
        else:
            cleaned += " "
    return cleaned.split()


def checksum(text):
    total = 0
    for i, ch in enumerate(text):
        total = (total + (i + 1) * ord(ch)) % 1000000007
    return total


def exact_duplicate(text, seen_hashes):
    h = checksum(text)
    if h in seen_hashes:
        return True
    seen_hashes.add(h)
    return False


def make_ngrams(words, n=3):
    if len(words) < n:
        return words
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]


def fingerprints(text):
    words = tokenize(text)
    ngrams = make_ngrams(words, 3)

    fp = set()
    for ng in ngrams:
        h = checksum(ng)
        if h % 4 == 0:   
            fp.add(h)
    return fp


def similarity(fp1, fp2):
    if not fp1 or not fp2:
        return 0.0
    return len(fp1 & fp2) / len(fp1 | fp2)


def near_duplicate(text, seen_fps, threshold=0.9):
    fp = fingerprints(text)

    for old_fp in seen_fps:
        if similarity(fp, old_fp) >= threshold:
            return True

    seen_fps.append(fp)
    return False