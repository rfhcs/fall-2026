from collections import Counter
import math


class AddOneSmoothing:
    def __init__(self, corpus, vocab_size, k=1):
        self.unigrams = Counter()
        self.bigrams = Counter()
        self.trigrams = Counter()
        self.first_word_bigram = Counter()
        self.first_word_trigram = Counter()
        self.k = k
        self.vocab_size = vocab_size

        self.train(corpus)

    # 90% of this algorithm was found here: https://www.geeksforgeeks.org/nlp/additive-smoothing-techniques-in-language-models/
    def train(self, corpus):
        for passage in corpus:
            for i in range(1, len(passage)):
                # skip position 0 which is just an <s> note that for report.
                self.unigrams[passage[i]] += 1
                if i >= 2:
                    # collecting all bigrams
                    self.bigrams[(passage[i - 1], passage[i])] += 1
                    self.first_word_bigram[passage[i - 1]] += 1

                    # finding all trigrams
                    self.trigrams[(passage[i - 2], passage[i - 1], passage[i])] += 1
                    self.first_word_trigram[(passage[i - 2], passage[i - 1])] += 1

    def bigram_prob(self, prev, cur):
        return (self.bigrams[(prev, cur)] + self.k) / (
            self.first_word_bigram[prev] + (self.k * self.vocab_size)
        )

    def trigram_prob(self, prev2, prev1, cur):
        return (self.trigrams[(prev2, prev1, cur)] + self.k) / (
            self.first_word_trigram[(prev2, prev1)] + (self.k * self.vocab_size)
        )

    def neg_log_prob(self, passage, ngram=2):
        probs = []
        for i in range(2, len(passage)):
            if ngram == 2:
                probs.append(self.bigram_prob(passage[i - 1], passage[i]))
            elif ngram == 3:
                probs.append(
                    self.trigram_prob(passage[i - 2], passage[i - 1], passage[i])
                )
            else:
                raise ValueError("ngram must be 2 or 3")
        return -sum(math.log(p) for p in probs)

    def perplexity(self, passages, ngram=2):
        total = sum(self.neg_log_prob(p, ngram) for p in passages)
        n_tokens = sum(len(p) - 2 for p in passages)
        return math.exp(1 / n_tokens * total)
