import random
import re

random.seed(1337)  # set random seed so results are reproducible

TARGET_WORDS = 80


def build_passages(data):
    """Read a normalized book and return a list of short passages."""

    with open(f"../data/processed/normie-{data}.txt", "r", encoding="utf-8") as file:
        text = file.read()

    # splitting paragraphs
    paragraphs = re.split(r"(?:[ \t]*\n\n+)+", text)

    passage_list = []
    current_passage = []
    word_count = 0

    for paragraph in paragraphs:
        current_passage.append(paragraph)
        word_count += len(paragraph.split())

        if word_count >= TARGET_WORDS:
            combined = " ".join(current_passage)
            passage_list.append(re.sub(r"\s+", " ", combined).strip())
            current_passage = []
            word_count = 0

    if current_passage and passage_list:
        leftover = re.sub(r"\s+", " ", " ".join(current_passage)).strip()
        passage_list[-1] = passage_list[-1] + " " + leftover

    return passage_list


# Splitting passages function written by Claude Sonnet 5
def split_passages(passages, block_size=10, dev_frac=0.1, test_frac=0.1):
    """Group consecutive passages into blocks, and split on that."""

    blocks = [passages[i : i + block_size] for i in range(0, len(passages), block_size)]
    random.shuffle(blocks)

    n_dev = max(1, round(len(blocks) * dev_frac))
    n_test = max(1, round(len(blocks) * test_frac))

    dev = [p for b in blocks[:n_dev] for p in b]
    test = [p for b in blocks[n_dev : n_dev + n_test] for p in b]
    train = [p for b in blocks[n_dev + n_test :] for p in b]

    return train, dev, test


def load_splits():
    hobbit = split_passages(build_passages("hobbit"))
    lost = split_passages(build_passages("lostworld"))

    return hobbit, lost
