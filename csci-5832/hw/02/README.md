# Homework 2: Language Models and Author Identification

## AI assistance disclosure

Development of `ngram.py` and `main.py` was done with guidance from Claude (Anthropic), used in a Socratic/tutoring mode — Claude did not write the core algorithm or model logic directly, but helped debug syntax issues, walk through the math behind add-k smoothing and perplexity, and clean up code structure. All AI code is documented within the code itself with comments on if it wrote a specific function or not.

## How everything is formatted 

The structure of my code is as follows:

```
data/
    processed/
        normie-hobbit.txt
        normie-lostworld.txt
    raw/
        hobbit.txt
        lostworld.txt
report/
    report.pdf
    report.tex
src/
    main.py
    ngram.py
    normalize.py
    splits.py
    tokenizer.py
```

## Running the whole thing

Everything is driven from `src/main.py` From inside `src/`:

```
python main.py
```
This will:

1. Load the pre-built train/dev/test splits for both books (via `splits.py`).
2. Train a shared BPE tokenizer across both books (via `tokenizer.py`).
3. Loop over a few vocabulary sizes (500 / 1000 / 2000), and for each:
   - build padded token-ID sequences for every split,
   - train bigram/trigram models with a few values of `k` (1, 0.1, 0.01),
   - print dev-set perplexity for each configuration, plus a cross-author check (each model scored on both books' dev sets).

All commands assume you're running from `src/`, since data paths (`../data/...`) are relative to that directory.

## Re-running normalization (optional)

The processed text files are already included in `data/processed/`, so this step is **not required** to run `main.py`. If you want to regenerate them from the raw Gutenberg files:

```
python normalize.py
```

This overwrites `data/processed/normie-hobbit.txt` and `data/processed/normie-lostworld.txt`. Rerunning this will just replace it with the same thing.

## Notes on other files

- `splits.py`, `tokenizer.py`, and `ngram.py` are not meant to be run directly — they're imported by `main.py`. Each exposes the reusable pieces of the pipeline (passage splitting, tokenizer training + padding, and the n-gram model class, respectively).
- The tokenizer is trained once per vocabulary size on **both books combined**, so the two author-specific models (Hobbit/Tolkien and Lost World/Doyle) always index into the same vocabulary and are directly comparable.
- `random.seed(1337)` in `splits.py` makes the train/dev/test split reproducible.

## Running author identification on a new test set

`predict_test.py` retrains a bigram model (vocab_size=1000, k=0.1) on the
full training data for each book, then classifies each passage in a test
file as "hobbit" (Tolkien) or "lost" (Doyle) using `predict_author` from
`main.py`.

**Note:** this script currently assumes the test file is plain text with
one passage per line, at `data/test/author_id_test.txt`. If the instructor
provides a different format, only the file-reading block in `predict_test.py`
needs to change — the tokenizer, model, and prediction logic are unaffected.

Run with:
```
python predict_test.py
```
