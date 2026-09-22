from tokenizer import train_tokenizer, add_padding
from splits import load_splits
from ngram import AddOneSmoothing


def predict_author(passage_ids, hobbit_model, lost_model, ngram=2):
    h_score = hobbit_model.neg_log_prob(passage_ids, ngram)
    l_score = lost_model.neg_log_prob(passage_ids, ngram)
    return "hobbit" if h_score < l_score else "lost"


# this was all messed up and cleaned up by Claude Sonnet 5
def main():
    hobbit, lost = load_splits()
    hobbit_train, hobbit_dev, hobbit_test = hobbit
    lost_train, lost_dev, lost_test = lost

    for vsize in [500, 1000, 2000]:
        tok = train_tokenizer(hobbit_train + lost_train, vocab_size=vsize)
        # rebuild padded ids, retrain models at best (n=2, k=0.1), print dev perplexity
        vocab_size = tok.get_vocab_size()

        hobbit_train_ids = [add_padding(tok, p) for p in hobbit_train]
        hobbit_dev_ids = [add_padding(tok, p) for p in hobbit_dev]
        hobbit_test_ids = [add_padding(tok, p) for p in hobbit_test]

        lost_train_ids = [add_padding(tok, p) for p in lost_train]
        lost_dev_ids = [add_padding(tok, p) for p in lost_dev]
        lost_test_ids = [add_padding(tok, p) for p in lost_test]

        # --- k=1, n=2 cross-author sanity check ---
        hobbit_model = AddOneSmoothing(hobbit_train_ids, vocab_size)
        lost_model = AddOneSmoothing(lost_train_ids, vocab_size)

        print(
            "hobbit model on hobbit dev:",
            hobbit_model.perplexity(hobbit_dev_ids, ngram=2),
        )
        print(
            "hobbit model on lost dev:  ",
            hobbit_model.perplexity(lost_dev_ids, ngram=2),
        )
        print(
            "lost model on lost dev:    ", lost_model.perplexity(lost_dev_ids, ngram=2)
        )
        print(
            "lost model on hobbit dev:  ",
            lost_model.perplexity(hobbit_dev_ids, ngram=2),
        )

        # --- ngram / k grid on dev ---
        print("\nngram/k grid:")
        results = []
        for k in [1, 0.1, 0.01]:
            hmodel = AddOneSmoothing(hobbit_train_ids, vocab_size, k=k)
            lmodel = AddOneSmoothing(lost_train_ids, vocab_size, k=k)
            for n in [2, 3]:
                results.append(
                    {
                        "book": "hobbit",
                        "k": k,
                        "n": n,
                        "perplexity": hmodel.perplexity(hobbit_dev_ids, ngram=n),
                    }
                )
                results.append(
                    {
                        "book": "lost",
                        "k": k,
                        "n": n,
                        "perplexity": lmodel.perplexity(lost_dev_ids, ngram=n),
                    }
                )
        for r in results:
            print(r)

    # --- final chosen config: n=2, k=0.1, vocab_size=1000 author ID sanity check on own test split ---
    hobbit_model = AddOneSmoothing(hobbit_train_ids, 1000, k=0.1)
    lost_model = AddOneSmoothing(lost_train_ids, 1000, k=0.1)

    hobbit_correct = sum(
        predict_author(p, hobbit_model, lost_model) == "hobbit" for p in hobbit_test_ids
    )
    lost_correct = sum(
        predict_author(p, hobbit_model, lost_model) == "lost" for p in lost_test_ids
    )

    print(f"\nhobbit test accuracy: {hobbit_correct}/{len(hobbit_test_ids)}")
    print(f"lost test accuracy:   {lost_correct}/{len(lost_test_ids)}")


if __name__ == "__main__":
    main()
