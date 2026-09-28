from tokenizer import train_tokenizer, add_padding
from splits import load_splits
from ngram import AddOneSmoothing

QUOTE_MAPPING = str.maketrans(
    {
        "\u2019": "'",
        "\u2018": "'",
        "\u201c": '"',
        "\u201d": '"',
    }
)

LABEL = {"hobbit": "Tolkien", "lost": "Doyle"}


def light_normalize(text):
    """Character-level cleanup matching training normalization, without
    the Gutenberg-specific front matter/chapter stripping."""
    text = text.translate(QUOTE_MAPPING)
    text = text.replace("--", "\u2014")
    return text


def predict_author(passage_ids, hobbit_model, lost_model, ngram=2):
    h_score = hobbit_model.neg_log_prob(passage_ids, ngram)
    l_score = lost_model.neg_log_prob(passage_ids, ngram)
    return "hobbit" if h_score < l_score else "lost"


def main():
    hobbit, lost = load_splits()
    hobbit_train, _, _ = hobbit
    lost_train, _, _ = lost

    tok = train_tokenizer(hobbit_train + lost_train, vocab_size=1000)
    vocab_size = tok.get_vocab_size()

    hobbit_train_ids = [add_padding(tok, p) for p in hobbit_train]
    lost_train_ids = [add_padding(tok, p) for p in lost_train]

    hobbit_model = AddOneSmoothing(hobbit_train_ids, vocab_size, k=0.1)
    lost_model = AddOneSmoothing(lost_train_ids, vocab_size, k=0.1)

    with open("../data/test/author_id_test.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    output_lines = []
    for line in lines:
        item_id, text = line.split("\t", 1)
        text = light_normalize(text)
        ids = add_padding(tok, text)
        prediction = predict_author(ids, hobbit_model, lost_model, ngram=2)
        output_lines.append(f"{item_id}\t{LABEL[prediction]}")

    with open("../report/author_id_predictions.txt", "w", encoding="utf-8") as out:
        out.write("\n".join(output_lines) + "\n")

    print(f"Wrote {len(output_lines)} predictions.")


if __name__ == "__main__":
    main()
