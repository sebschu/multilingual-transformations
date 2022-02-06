import sys
import spacy
import argparse
from datasets import load_dataset
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("num_examples", type=int, help="Number of examples to analyze.")
parser.add_argument("-l", "--language", type=str, default="en",
                    help="Language on which we perform the corpus analysis.")
parser.add_argument("-m", "--metric", type=str, default="jaccard_sim",
                    help="Similarity metric for comparing sentences.")
parser.add_argument("-i", "--ignore-case", action="store_true", default=False,
                    help="Whether to ignore casing in input text.")
args = parser.parse_args()

# calculate proportion of word set overlap across two sentences
# TODO: take into account words that appear multiple times (use Counter?)
def jaccard_sim(sent_1, sent_2):
    wordset_1 = set(sent_1)
    wordset_2 = set(sent_2)
    shared_words = wordset_1.intersection(wordset_2)
    jaccard_sim = len(shared_words) / \
            (len(wordset_1) + len(wordset_2) - len(shared_words))
    return jaccard_sim

def dependency_sim(sent_1, sent_2):
    pass

METRIC_FUNCTIONS = {
    "jaccard_sim": jaccard_sim,
    "dependency_sim": dependency_sim
}

en_mc4 = load_dataset("mc4", args.language, split="train", streaming=True)
# make it iterable using `next`
en_mc4 = iter(en_mc4)

# for this to work, you'll have to run `python -m spacy download en_core_web_sm
if args.language == "en":
    nlp = spacy.load("en_core_web_sm")
else:
    raise NotImplementedError(f"Language \"{args.language}\" not supported.")

skipped = 0
max_sim = 0
max_sim_sents = [None, None]

# iterate through mC4 documents looking for disambiguating sentence pairs
for _ in tqdm(range(args.num_examples)):
    example = next(en_mc4)["text"]
    if args.ignore_case:
        example = example.lower()
    doc = nlp(example)
    sentences = list(doc.sents)
    # skip document if only 1 sentence is present
    if len(sentences) < 2:
        skipped += 1
        continue
    # compare adjacent sentences in the training example
    prev_sent = None
    for idx in range(1, len(sentences)):
        if not prev_sent:
            sent_1 = [token.text for token in sentences[idx-1]]
        else:
            sent_1 = prev_sent
        # sentences are stored as lists of tokens (incl. punctuation)
        sent_2 = [token.text for token in sentences[idx]]
        prev_sent = sent_2

        sent_sim = METRIC_FUNCTIONS[args.metric](sent_1, sent_2)
        if sent_sim > max_sim:
            max_sim = sent_sim
        max_sim_sents = [sent_1, sent_2]

print(f"maximally similar sentences:\n{max_sim_sents[0]}\n-------\n{max_sim_sents[1]}\n")
print(f"# skipped documents: {skipped}")
