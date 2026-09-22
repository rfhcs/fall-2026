from tokenizer import train_tokenizer, add_padding
from splits import load_splits
from ngram import AddOneSmoothing
from main import predict_author  # reuse the same function

# this is for ease of testing the actual Author ID
# written by Claude Sonnet 5

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

    # TODO: Update if not .txt
    # Currently assumes one passage per line in a plain .txt file.
    with open("../data/test/author_id_test.txt", "r", encoding="utf-8") as f:
        test_passages = [line.strip() for line in f if line.strip()]

    with open("../report/author_id_predictions.txt", "w", encoding="utf-8") as out:
        for passage in test_passages:
            ids = add_padding(tok, passage)
            prediction = predict_author(ids, hobbit_model, lost_model, ngram=2)
            out.write(prediction + "\n")

    print(f"Wrote {len(test_passages)} predictions to author_id_predictions.txt")


if __name__ == "__main__":
    main()
