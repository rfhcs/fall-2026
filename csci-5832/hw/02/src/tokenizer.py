from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace


# 100% of this tokenizer code was found at the link: https://huggingface.co/docs/tokenizers/en/quicktour
def train_tokenizer(passages, vocab_size=1000, pre_tokenizer=None):
    # initalize tokenizer
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))

    # if no pre_tokenizer is specified default to Whitespace()
    tokenizer.pre_tokenizer = pre_tokenizer or Whitespace()

    # instantiate BPE trainer
    trainer = BpeTrainer(vocab_size=vocab_size, special_tokens=["[UNK]", "<s>", "</s>"])

    # train and then return
    tokenizer.train_from_iterator(passages, trainer)

    return tokenizer


def add_padding(tokenizer, text):
    bos = tokenizer.token_to_id("<s>")
    eos = tokenizer.token_to_id("</s>")

    return [bos, bos] + tokenizer.encode(text).ids + [eos]
