from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
from splits import hobbit_train, lost_train


# I am literally just following https://huggingface.co/docs/tokenizers/en/quicktour
def train_tokenizer(passages, vocab_size=1000, pre_tokenizer=None):
    # initalize tokenizer
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))

    # using a pre-tokenizer "ensures no token is bigger than a word returned by the pre-tokenizer"
    tokenizer.pre_tokenizer = pre_tokenizer or Whitespace()

    # instantiate BPE trainer
    trainer = BpeTrainer(vocab_size=vocab_size, special_tokens=["[UNK]"])

    # train and save to a json file
    tokenizer.train_from_iterator(passages, trainer)
    # tokenizer.save("../data/results/tokenizer.json")
    return tokenizer


# for size in [500, 1000, 2000, 5000]:
#     tok = train_tokenizer(hobbit_train + lost_train, vocab_size=size)
