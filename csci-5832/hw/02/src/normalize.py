import re


def normalize(raw, processed):
    with open(
        f"../data/raw/{raw}.txt", "r", encoding="utf-8"
    ) as file:  # open raw text passed in here
        text = file.read()

    # 1. Remove end of Gutenberg
    end_pattern = r"\*\*\* END OF TH(E|IS) PROJECT GUTENBERG EBOOK .* \*\*\*"

    end_match = re.search(end_pattern, text)

    start_idx = 0
    end_idx = end_match.start() if end_match else len(text)

    normalized = text[start_idx:end_idx].strip()

    # 1. Remove all front matter and start at "chapter 1"
    pattern = r"\bchapter i\b"
    match = re.search(pattern, normalized, flags=re.IGNORECASE)

    start_pos = 0

    if match:
        start_pos = match.start()

    normalized = normalized[start_pos:]

    # 2. Remove chapter headers and titles

    chapter_pattern = r"^[ \t]*chapter [IVXLC ]+[ \t]*$[\n]*[ \t]*.*$"

    normalized = re.sub(
        chapter_pattern, "", normalized, flags=re.IGNORECASE | re.MULTILINE
    )

    # 3.1 Standardize quotations
    # create a mapping dictionary of character codepoints to their escaped string notation
    quote_mapping = str.maketrans(
        {
            "’": "'",  # Right single quote / Apostrophe
            "‘": "'",  # Left single quote
            "“": '"',  # Left double quote
            "”": '"',  # Right double quote
        }
    )
    normalized = normalized.translate(quote_mapping)

    # 3.2 Standardize em dashes
    normalized = re.sub(r"--", "—", normalized).strip()
    normalized = re.sub(r"----", "——", normalized).strip()

    # 3.3 Misisng apostrophes
    normalized = re.sub(r"\s[s]\s", "'s ", normalized)

    # write to processed file
    with open(f"../data/processed/{processed}.txt", "w", encoding="utf-8") as f:
        f.write(normalized)
        print(
            f"Normalized text {raw}. Processed data can be found in text file {processed}"
        )


# call normalize on the hobbit and lost world
normalize("hobbit", "normie-hobbit")
normalize("lostworld", "normie-lostworld")
