"""XLLM6 Short - Main program for end-users.

This program reads pre-created tables and returns results to user queries.
"""

import requests
from autocorrect import Speller

from . import xllm6_util as llm6

try:
    from pattern.text.en import singularize
except ImportError:
    try:
        from pattern3.text.en import singularize
    except ImportError:
        def singularize(word):
            return word

# Unlike xllm6.py, xllm6_short.py does not process the (huge) crawled data.
# Instead, it uses the much smaller summary tables produced by xllm6.py

# --- [1] get tables if not present already

# First, get xllm6_util.py from GitHub and save it locally as xllm6_util.py
#     note: this python code does that automatically for  you
# Then import everything from that library with 'from xllm6_util import *'
# Now you can call the read_xxx() functions from that library
# In addition, the tables stopwords and utf_map are also loaded
#
# Notes:
#    - On first use, dowload all locally with overwrite = True
#    - On next uses, please use local copies: set overwrite = False

# Table description:
#
# unless otherwise specified, a word consists of 1, 2, 3, or 4 tokens
# word_pairs is used in xllm6.py, not in xllm6_short.py
#
# dictionary = {}      words with counts: core (central) table
# word_pairs = {}      pairs of 1-token words found in same word, with count
# word2_pairs = {}     pairs of multi-token words found on same URL, with count
# url_map = {}         URL IDs attached to words in dictionary
# arr_url = []         maps URL IDs to URLs (one-to-one)
# hash_category = {}   categories attached to a word
# hash_related = {}    related topics attached to a word
# hash_see = {}        topics from "see also" section, attached to word
# ngrams_table = {}    ngrams of word found when crawling
# compressed_ngrams_table = {}     only keep ngram with highest count
# utf_map = {}         map accented characters to non-accented version
# stopwords = ()       words (1 or more tokens) not accepted in dictionary
# word_hash = {}       list of 1-token words associated to a 1-token word
# word2_hash = {}      list of multi-token words associated to a multi-token word
# compressed_word2_hash = {}      shorter version of word2_hash
# embeddings = {}      key is a 1-token word; value is hash of 1-token:weight
# embeddings2 = {}     key is a word; value is hash of word:weight


# Define data paths
DATA_PATH = "../../data/xllm6/"

class XLLM6Short:
    """XLLM6 Short - Main program for end-users that reads pre-created tables."""

    def __init__(self, data_path=DATA_PATH):
        """Initialize the XLLM6Short class."""
        self.DATA_PATH = data_path
        self.dictionary = {}
        self.compressed_ngrams_table = {}
        self.compressed_word2_hash = {}
        self.embeddings = {}
        self.embeddings2 = {}
        self.hash_related = {}
        self.hash_see = {}
        self.hash_category = {}
        self.url_map = {}
        self.arr_url = []
        self.stopwords = ()
        self.spell = Speller(lang="en")

    def load_data(self, overwrite=False):
        """Load data from files or GitHub."""
        # Get local copies if needed
        if overwrite:
            self._download_files()

        # Load data
        try:
            self.arr_url = llm6.read_arr_url(self.DATA_PATH + "xllm6_arr_url.txt", path="")
            self.dictionary = llm6.read_dictionary(self.DATA_PATH + "xllm6_dictionary.txt", path="")
            self.stopwords = llm6.read_stopwords(self.DATA_PATH + "stopwords.txt", path="")

            self.compressed_ngrams_table = llm6.read_table(
                self.DATA_PATH + "xllm6_compressed_ngrams_table.txt", type="list", path=""
            )
            self.compressed_word2_hash = llm6.read_table(
                self.DATA_PATH + "xllm6_compressed_word2_hash.txt", type="hash", path=""
            )
            self.embeddings = llm6.read_table(
                self.DATA_PATH + "xllm6_embeddings.txt", type="hash", path="", format="float"
            )
            self.embeddings2 = llm6.read_table(
                self.DATA_PATH + "xllm6_embeddings2.txt", type="hash", path="", format="float"
            )
            self.hash_related = llm6.read_table(
                self.DATA_PATH + "xllm6_hash_related.txt", type="hash", path=""
            )
            self.hash_see = llm6.read_table(
                self.DATA_PATH + "xllm6_hash_see.txt", type="hash", path=""
            )
            self.hash_category = llm6.read_table(
                self.DATA_PATH + "xllm6_hash_category.txt", type="hash", path=""
            )
            self.url_map = llm6.read_table(
                self.DATA_PATH + "xllm6_url_map.txt", type="hash", path=""
            )
            return True
        except FileNotFoundError as e:
            print(f"Warning: Could not load data files: {e}")
            return False

    def _download_files(self):
        """Download files from GitHub."""
        path = (
            "https://raw.githubusercontent.com/VincentGranville/Large-Language-Models/main/xllm6/"
        )

        # Get utility file
        response = requests.get(path + "xllm6_util.py")
        python_code = response.text

        local_copy = "xllm6_util"
        file = open(local_copy + ".py", "w")
        file.write(python_code)
        file.close()

        # Get data files
        files = [
            "xllm6_arr_url.txt",
            "xllm6_compressed_ngrams_table.txt",
            "xllm6_compressed_word2_hash.txt",
            "xllm6_dictionary.txt",
            "xllm6_embeddings.txt",
            "xllm6_embeddings2.txt",
            "xllm6_hash_related.txt",
            "xllm6_hash_category.txt",
            "xllm6_hash_see.txt",
            "xllm6_url_map.txt",
            "stopwords.txt",
        ]

        for name in files:
            response = requests.get(path + name)
            content = response.text
            file = open(self.DATA_PATH + name, "w")
            file.write(content)
            file.close()

    def singular(self, data, mode="Internal"):
        """Convert words to their singular form."""
        stem_table = {}

        for word in data:
            if mode == "Internal":
                n = len(word)
                if (
                    n > 2
                    and "~" not in word
                    and word[0 : n - 1] in self.dictionary
                    and word[n - 1] == "s"
                ):
                    stem_table[word] = word[0 : n - 1]
                else:
                    stem_table[word] = word
            else:
                # the instruction below changes 'hypothesis' to 'hypothesi'
                word = singularize(word)

                # the instruction below changes 'hypothesi' back to 'hypothesis'
                # however it changes 'feller' to 'seller'
                # solution: create 'do not singularize' and 'do not autocorrect' lists
                stem_table[word] = self.spell(word)

        return stem_table

    def fformat(self, value, item, format):
        """Format a value and item according to the given format."""
        format = format.split(" ")
        fmt1 = format[0].replace("%", "")
        fmt2 = format[1].replace("%", "")
        string = "{:{fmt1}} {:{fmt2}}".format(value, item, fmt1=fmt1, fmt2=fmt2)
        return string

    def hprint(self, title, hash, maxprint, output_file, format="%3d %s"):
        """Print a hash table with sorting."""
        print("\n%s\n" % (title))
        output_file.write("\n%s\n\n" % (title))
        hash_sorted = dict(sorted(hash.items(), key=lambda item: item[1], reverse=True))
        printcount = 0
        for item in hash_sorted:
            value = hash[item]
            if "URL" in title:
                item = self.arr_url[int(item)]
            if item != "" and printcount < maxprint and value > 0:
                print(format % (value, item))
                string = self.fformat(value, item, format)
                output_file.write(string + "\n")
                printcount += 1

        return

    def word_summary(self, word, ccnt1, ccnt2, maxprint, output_file):
        """Generate a summary for a word."""
        if word not in self.dictionary:
            print("No result")
            output_file.write("No result\n")
            cnt = 0
        else:
            cnt = self.dictionary[word]

        if cnt > ccnt1:
            dashes = "-" * 60
            print(dashes)
            output_file.write(dashes + "\n")
            print(word, self.dictionary[word])
            output_file.write(word + " " + str(self.dictionary[word]) + "\n")

            self.hprint("ORGANIC URLs", self.url_map[word], maxprint, output_file)
            self.hprint("CATEGORIES & LEVELS", self.hash_category[word], maxprint, output_file)
            self.hprint("RELATED", self.hash_related[word], maxprint, output_file)
            self.hprint("ALSO SEE", self.hash_see[word], maxprint, output_file)
            if word in self.compressed_word2_hash:
                self.hprint("LINKED WORDS", self.compressed_word2_hash[word], maxprint, output_file)
            if word in self.embeddings:
                self.hprint("EMBEDDINGS", self.embeddings[word], maxprint, output_file, "%8.2f %s")
            if word in self.embeddings2:
                self.hprint(
                    "X-EMBEDDINGS", self.embeddings2[word], maxprint, output_file, "%8.2f %s"
                )

        print()
        return

    def process_query(self, query, ccnt1=0, ccnt2=0, maxprint=10, output_file=""):
        """Process a user query and return relevant results."""
        # Split the query and process each part
        queries = query.split(",")
        token_list = []
        token_clean_list = []

        for q in queries:
            tokens = q.split(" ")
            for token in tokens:
                # note: spell('feller') = 'seller', should not be autocorrected
                token = token.lower()
                if token not in self.dictionary:
                    token = self.spell(token)
                token_list.append(token)

            stemmed = self.singular(token_list, mode="Internal")

            for old_token in stemmed:
                token = stemmed[old_token]
                if token in self.dictionary:
                    token_clean_list.append(token)
            token_clean_list.sort()

            if not token_clean_list:
                if q != "":
                    print("No match found")
                    if output_file:
                        output_file.write("No match found\n")
            else:
                print("Found: ", token_clean_list)
                if output_file:
                    output_file.write("Found: " + str(token_clean_list) + "\n")
                self._process_clean_query(token_clean_list, ccnt1, ccnt2, maxprint, output_file)

    def _process_clean_query(self, query, ccnt1, ccnt2, maxprint, output_file=""):
        """Process a cleaned query (list of tokens) and return relevant results."""
        # query is a sorted word, each token is in dictionary
        # retrieve all sub-ngrams with a dictionary entry, print results for each one

        def get_bin(x, n):
            return format(x, "b").zfill(n)

        n = len(query)

        for k in range(1, 2**n):
            binary = get_bin(k, n)
            sorted_word = ""
            for j in range(0, len(binary)):
                if binary[j] == "1":
                    if sorted_word == "":
                        sorted_word = query[j]
                    else:
                        sorted_word += "~" + query[j]

            if sorted_word in self.compressed_ngrams_table:
                ngram_list = self.compressed_ngrams_table[sorted_word]
                # the word below (up to 4 tokens) is in the dictionary
                word = ngram_list[0]
                print("Found:", word)
                if output_file:
                    output_file.write("Found:" + word + "\n")
                self.word_summary(word, ccnt1, ccnt2, maxprint, output_file)

    def run(self):
        """Run the XLLM6 Short program interactively."""
        print("\n")
        output_file = open(self.DATA_PATH + "xllm6_results.txt", "w", encoding="utf-8")

        # Hyperparameters
        ccnt1 = 0
        ccnt2 = 0  # 2
        maxprint = 10  # up to maxprint rows shown per word/section

        query = " "
        while query != "":
            # Ask for user input
            query = input("Enter queries (ex: Gaussian distribution, central moments): ")
            if not query:
                break

            self.process_query(query, ccnt1, ccnt2, maxprint, output_file)

        output_file.close()


# Only run this when the module is executed directly
if __name__ == "__main__":
    xllm6_short = XLLM6Short()
    if xllm6_short.load_data():
        xllm6_short.run()
