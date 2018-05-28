#  -*-  coding:  utf-8  -*-

from __future__ import division

import sys
if sys.version_info[0] == 3:
    from statistics import mean

from collections import Counter
from itertools import islice
from textblob import TextBlob
import textblob
import re
import string
from math import sqrt, log
from scipy.stats import hypergeom


def preprocess(text):
    """ 1. lower case
        2. removes digits
        3. removes variations of dashes and hyphens

        Parameter
        ---------
        text: string

        Returns
        -------
        string
    """
    # lowercase and remove digits
    text = re.sub(r'[0-9]+', '', text.lower())

    # Replace dashes/hyphens
    if sys.version_info[0] == 3:
        text = text.replace('–', '')
        text = text.replace('—', '')
        text = text.replace('-', '')
    else:
        text = text.replace('-', '')
    return text


def tokenize(text):
    """ Tokenize text into a list of tokens using built-in methods.

        Parameter
        ---------
        text: string

        Returns
        -------
        list
        """
    text = preprocess(text)

    for p in list(string.punctuation):
        text = text.replace(p, ' ')

    words = text.split()
    return words


def blobber(text):
    """ Tokenize text into a list of tokens using TextBlob.

        Parameter
        ---------
        text: string

        Return
        ------
        TextBlob list of words
    """
    blob = TextBlob(text)
    return blob.words


def segment_generator(List, segment_size):
    """ Split a list into s segments of size r (segment_size).

        Parameters
        ----------
        List: list
            List of items to be segmented.
        segment_size: int
            Size of each segment.

        Returns
        -------
        Generator
    """
    for i in range(0, len(List), segment_size):
        yield List[i: i + segment_size]


def list_sliding_window(sequence, window_size=2):
    """ Returns a sliding window generator (of size window_size) over a sequence. Taken from
        https://docs.python.org/release/2.3.5/lib/itertools-example.html

        Example
        -------
        List = ['a', 'b', 'c', 'd']
        window_size = 2
        list_sliding_window(List, 2) -> ('a', 'b')
                                        ('b', 'c')
                                        ('c', 'd')

        Parameters
        ----------
        sequence: sequence (string, unicode, list, tuple, etc.)
            Sequence to be iterated over. window_size=1 is just a regular iterator.
        window_size: int
            Size of each window.

        Returns
        -------
        Generator

    """
    iterable = iter(sequence)
    result = tuple(islice(iterable, window_size))
    if len(result) == window_size:
        yield result
    for item in iterable:
        result = result[1:] + (item,)
        yield result


class LexicalRichness(object):
    """ Object containing tokenized text and methods to compute Lexical Richness (also known as
        Lexical Diversity or Vocabulary Diversity.)
    """

    def __init__(self, text, use_TextBlob=False):
        """ Initialise object with basic attributes needed to compute the common lexical diversity measures.

            Parameters
            ----------
            text: string
                String (or unicode) variable containing textual data.
            use_TextBlob: bool
                If True, use TextBlob to tokenize text.
                If False, use built-in string methods.

            Attributes
            ----------
            wordlist: list
                List of tokens from text.
            words: int
                Number of words in text.
            terms: int
                Number of unique terms/vocabb in text.
            tokenizer: string
                Description of tokenizer used.

            Helpers Functions
            -----------------
            preprocess(string):
                Preprocess text before tokenizing
            blobber(string)
                Tokenize text using TextBlob (if use_TextBlob=True)
            tokenize(string)
                Tokenize text using built-in string methods (if use_TextBlob=False)
        """
        self.text = preprocess(text)

        if use_TextBlob:
            self.wordlist = blobber(self.text)
            self.words = len(self.wordlist)
            self.terms = len(set(self.wordlist))
            self.tokenizer = "{} (ver. {})".format(textblob.__name__, textblob.__version__)
        else:
            self.wordlist = tokenize(self.text)
            self.words = len(self.wordlist)
            self.terms = len(set(self.wordlist))
            self.tokenizer = 'default'


    # Lexical richness measures
    @property
    def ttr(self):
        """ Type-token ratio (TTR) computed as t/w, where t is the number of unique terms/vocab,
            and w is the total number of words.
            (Chotlos 1944, Templin 1957)
        """
        return self.terms / self.words


    @property
    def rttr(self):
        """ Root TTR (RTTR) computed as t/sqrt(w), where t is the number of unique terms/vocab,
            and w is the total number of words.
            Also known as Guiraud's R and Guiraud's index.
            (Guiraud 1954, 1960)
        """
        return self.terms / sqrt(self.words)


    @property
    def cttr(self):
        """ Corrected TTR (CTTR) computed as t/sqrt(2 * w), where t is the number of unique terms/vocab,
            and w is the total number of words.
            (Carrol 1964)
        """
        return self.terms / sqrt(2 * self.words)


    @property
    def Herdan(self):
        """ Computed as log(t)/log(w), where t is the number of unique terms/vocab, and w is the
            total number of words.
            Also known as Herdan's C.
            (Herdan 1960, 1964)
        """
        return log(self.terms) / log(self.words)


    @property
    def Summer(self):
        """ Computed as log(log(t)) / log(log(w)), where t is the number of unique terms/vocab, and
            w is the total number of words.
            (Summer 1966)
        """
        return log(log(self.terms)) / log(log(self.words))


    @property
    def Dugast(self):
        """ Computed as (log(w) ** 2) / (log(w) - log(t)), where t is the number of unique terms/vocab,
            and w is the total number of words.
            (Dugast 1978)
        """
        # raise exception if terms and words count are the same
        if self.words == self.terms:
            raise ZeroDivisionError('Word count and term counts are the same.')

        return (log(self.words) ** 2) / (log(self.words) - log(self.terms))


    @property
    def Maas(self):
        """ Maas's TTR, computed as (log(w) - log(t)) / (log(w) * log(w)), where t is the number of
            unique terms/vocab, and w is the total number of words. Unlike the other measures, lower
            maas measure indicates higher lexical richness.
            (Maas 1972)
        """
        return (log(self.words) - log(self.terms)) / (log(self.words) ** 2)


    def msttr(self, segment_window=100, discard=True):
        """ Mean segmental TTR (MSTTR) computed as average of TTR scores for segments in a text.

            Split a text into segments of length segment_window. For each segment, compute the TTR.
            MSTTR score is the sum of these scores divided by the number of segments.
            (Johnson 1944)

            Helper Function
            ---------------
            segment_generator(List, segment_window):
                Split a list into s segments of size r (segment_size).

            Parameters
            ----------
            segment_window: int
                Size of each segment (default=100).
            discard: bool
                If True, discard the remaining segment (e.g. for a text size of 105 and a segment_window
                of 100, the last 5 tokens will be discarded). Default is True.

            Returns
            -------
            float
        """
        if segment_window >= self.words:
            raise ValueError('Window size must be greater than text size of {}. Try a smaller segment_window size.'.format(self.words))

        if segment_window < 1 or type(segment_window) is float:
            raise ValueError('Window size must be a positive integer.')

        scores = list()
        for segment in segment_generator(self.wordlist, segment_window):
            ttr = len(set(segment)) / len(segment)
            scores.append(ttr)

        if discard: # discard remaining words
            del scores[-1]

        if sys.version_info == 3:
            mean_ttr = mean(scores)
        else:
            mean_ttr = sum(scores) / len(scores)
        return mean_ttr


    def mattr(self, window_size=100):
        """ Moving average TTR (MATTR) computed using the average of TTRs over successive segments
            of a text.

            Estimate TTR for tokens 1 to n, 2 to n+1, 3 to n+2, and so on until the end
            of the text (where n is window size), then take the average.
            (Covington 2007, Covington and McFall 2010)

            Helper Function
            ---------------
            list_sliding_window(sequence, window_size):
                Returns a sliding window generator (of size window_size) over a sequence

            Parameter
            ---------
            window_size: int
                Size of each sliding window.

            Returns
            -------
            float
        """
        if window_size > self.words:
            raise ValueError('Window size must not be greater than text size of {}. Try a smaller window size.'.format(self.words))

        if window_size < 1 or type(window_size) is float:
            raise ValueError('Window size must be a positive integer.')

        scores = [len(set(window)) / window_size
                  for window in list_sliding_window(self.wordlist, window_size)]

        if sys.version_info == 3:
            mattr = mean(scores)
        else:
            mattr = sum(scores)/len(scores)

        return mattr


    def mtld(self, threshold=0.72):
        """ Measure of textual lexical diversity, computed as the mean length of sequential words in
            a text that maintains a minimum threshold TTR score.

            Iterates over words until TTR scores falls below a threshold, then increase factor
            counter by 1 and start over. McCarthy and Jarvis (2010, pg. 385) recommends a factor
            threshold in the range of [0.660, 0.750].
            (McCarthy 2005, McCarthy and Jarvis 2010)

            Parameters
            ----------
            threshold: float
                Factor threshold for MTLD. Algorithm skips to a new segment when TTR goes below the
                threshold (default=0.72).

            Returns
            -------
            float
        """

        def sub_mtld(self, threshold, reverse=False):
            """
            Parameters
            ----------
            threshold: float
                Factor threshold for MTLD. Algorithm skips to a new segment when TTR goes below the
                threshold (default=0.72).
            reverse: bool
                If True, compute mtld for the reversed sequence of text (default=False).

            Returns:
                mtld measure (float)
            """
            if reverse:
                word_iterator = iter(reversed(self.wordlist))
            else:
                word_iterator = iter(self.wordlist)

            terms = set()
            word_counter = 0
            factor_count = 0

            for word in word_iterator:
                word_counter += 1
                terms.add(word)
                ttr = len(terms)/word_counter

                if ttr <= threshold:
                    word_counter = 0
                    terms = set()
                    factor_count += 1

            # partial factors for the last segment computed as the ratio of how far away ttr is from
            # unit, to how far away threshold is to unit
            if word_counter > 0:
                factor_count += (1-ttr) / (1 - threshold)

            # ttr never drops below threshold by end of text
            if factor_count == 0:
                ttr = self.terms / self.words
                if ttr == 1:
                    factor_count += 1
                else:
                    factor_count += (1-ttr) / (1 - threshold)

            return len(self.wordlist) / factor_count

        forward_measure = sub_mtld(self, threshold, reverse=False)
        reverse_measure = sub_mtld(self, threshold, reverse=True)

        if sys.version_info[0] == 3:
            mtld = mean((forward_measure, reverse_measure))
        else:
            mtld = (forward_measure + reverse_measure) / 2

        return mtld


    def hdd(self, draws=42):
        """ Hypergeometric distribution diversity (HD-D) score.

            For each term (t) in the text, compute the probabiltiy (p) of getting at least one appearance
            of t with a random draw of size n < N (text size). The contribution of t to the final HD-D
            score is p * (1/n). The final HD-D score thus sums over p * (1/n) with p computed for
            each term t. Described in McCarthy and Javis 2007, p.g. 465-466.
            (McCarthy and Jarvis 2007)

            Parameters
            ----------
            draws: int
                Number of random draws in the hypergeometric distribution (default=42).

            Returns
            -------
            float
        """
        if self.terms < 42:
            suggestion = self.words // 2
        else:
            suggestion = 42
        if self.words < draws:
            raise ValueError('Number of draws should be less than the total sample size of {0}. Try a draw value smaller than {0}, e.g. hdd(draws={1}.)'.format(self.words, suggestion))
        if draws < 1 or type(draws) is float:
            raise ValueError('Number of draws must be a positive integer. E.g. hdd(draws={})'.format(suggestion))

        term_freq = Counter(self.wordlist)

        term_contributions = [(1 - hypergeom.pmf(0, self.words, freq, draws)) / draws
                              for term, freq in term_freq.items()]

        return sum(term_contributions)


    def __str__(self):
        return ' '.join(self.wordlist)


    def __repr__(self):
        return 'String(words={}, terms={}, tokenizer={}, wordlist={}, string="{}")'.format(self.words, self.terms, self.tokenizer, self.wordlist, ' '.join(self.wordlist))
