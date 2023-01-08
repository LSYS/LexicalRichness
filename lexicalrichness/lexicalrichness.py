#  -*-  coding:  utf-8  -*-

from __future__ import division

import sys

if sys.version_info[0] == 3:
    from statistics import mean

from collections import Counter
from itertools import islice
import re
import string
from math import sqrt, log
import numpy as np
from scipy.stats import hypergeom
from scipy.optimize import curve_fit
import random
import matplotlib.pyplot as plt

try:
    from textblob import TextBlob
except ImportError:
    pass
else:

    def blobber(text):
        """Tokenize text into a list of tokens using TextBlob.

        Parameter
        ---------
        text: string

        Return
        ------
        TextBlob list of words
        """
        blob = TextBlob(text)
        return blob.words


def preprocess(text):
    """1. lower case
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
    text = re.sub(r"[0-9]+", "", text.lower())

    # Replace dashes/hyphens
    if sys.version_info[0] == 3:
        text = text.replace("–", "")
        text = text.replace("—", "")
        text = text.replace("-", "")
    else:
        text = text.replace("-", "")
    return text


def tokenize(text):
    """Tokenize text into a list of tokens using built-in methods.

    Parameter
    ---------
    text: string

    Returns
    -------
    list
    """
    text = preprocess(text)

    for p in list(string.punctuation):
        text = text.replace(p, " ")

    words = text.split()
    return words


def segment_generator(List, segment_size):
    """Split a list into s segments of size r (segment_size).

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
        yield List[i : i + segment_size]


def list_sliding_window(sequence, window_size=2):
    """Returns a sliding window generator (of size window_size) over a sequence. Taken from
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


def ttr_nd(N, D):
    """McKee, Mavern, and Richard 2000's formulation of how the type token ratio (TTR) depends
    on the number of tokens (N) and a parameter D (a construct of the unobserved lexical diversity).
    Predicted values of D is in the order of 10 to 100.

    Directly referenced from McKee, Mavern, and Richard 2000.

    Used to compute vocd(self, ntokens=50, within_sample=100, iterations=3, seed=42).
    """
    return (D / N) * (np.sqrt(1 + 2 * (N / D)) - 1)


class LexicalRichness(object):
    """Object containing tokenized text and methods to compute Lexical Richness (also known as
    Lexical Diversity or Vocabulary Diversity.)
    """

    def __init__(self, text, preprocessor=preprocess, tokenizer=tokenize):
        """Initialise object with basic attributes needed to compute the common lexical diversity measures.

        Parameters
        ----------
        text: string or list
            String (or unicode) variable containing textual data, or a list
            of tokens if the text is already tokenized.
        preprocessor: callable or None
            A callable for preprocessing the text. Default is the built-in
            `preprocess` function. If None, no preprocessing is applied.
        tokenizer: callable or None
            A callable for tokenizing the text. Default is the built-in
            `tokenize` function. If None, the text parameter should be a list.

        Attributes
        ----------
        wordlist: list
            List of tokens from text.
        words: int
            Number of words in text.
        terms: int
            Number of unique terms/vocabb in text.
        preprocessor: callable
            The preprocessor used.
        tokenizer: callable
            The tokenizer used.

        Helpers Functions
        -----------------
        preprocess(string):
            Preprocess text before tokenizing (if preprocessor=preprocess)
        blobber(string)
            Tokenize text using TextBlob (if tokenizer=blobber)
        tokenize(string)
            Tokenize text using built-in string methods (if tokenizer=tokenize)
        """
        self.preprocessor = preprocessor
        self.tokenizer = tokenizer

        if self.tokenizer:
            if self.preprocessor:
                text = self.preprocessor(text)
            self.wordlist = self.tokenizer(text)
        else:
            assert (
                type(text) == list
            ), "If tokenizer is None, then input should be a list of words."
            self.wordlist = text

        self.words = len(self.wordlist)
        self.terms = len(set(self.wordlist))

    # Lexical richness measures as properties
    @property
    def ttr(self):
        """Type-token ratio (TTR) computed as t/w, where t is the number of unique terms/vocab,
        and w is the total number of words.
        (Chotlos 1944, Templin 1957)
        """
        return self.terms / self.words

    @property
    def rttr(self):
        """Root TTR (RTTR) computed as t/sqrt(w), where t is the number of unique terms/vocab,
        and w is the total number of words.
        Also known as Guiraud's R and Guiraud's index.
        (Guiraud 1954, 1960)
        """
        return self.terms / sqrt(self.words)

    @property
    def cttr(self):
        """Corrected TTR (CTTR) computed as t/sqrt(2 * w), where t is the number of unique terms/vocab,
        and w is the total number of words.
        (Carrol 1964)
        """
        return self.terms / sqrt(2 * self.words)

    @property
    def Herdan(self):
        """Computed as log(t)/log(w), where t is the number of unique terms/vocab, and w is the
        total number of words.
        Also known as Herdan's C.
        (Herdan 1960, 1964)
        """
        return log(self.terms) / log(self.words)

    @property
    def Summer(self):
        """Computed as log(log(t)) / log(log(w)), where t is the number of unique terms/vocab, and
        w is the total number of words.
        (Summer 1966)
        """
        return log(log(self.terms)) / log(log(self.words))

    @property
    def Dugast(self):
        """Computed as (log(w) ** 2) / (log(w) - log(t)), where t is the number of unique terms/vocab,
        and w is the total number of words.
        (Dugast 1978)
        """
        # raise exception if terms and words count are the same
        if self.words == self.terms:
            raise ZeroDivisionError("Word count and term counts are the same.")

        return (log(self.words) ** 2) / (log(self.words) - log(self.terms))

    @property
    def Maas(self):
        """Maas's TTR, computed as (log(w) - log(t)) / (log(w) * log(w)), where t is the number of
        unique terms/vocab, and w is the total number of words. Unlike the other measures, lower
        maas measure indicates higher lexical richness.
        (Maas 1972)
        """
        return (log(self.words) - log(self.terms)) / (log(self.words) ** 2)

    # Lexical richness measures as methods
    def msttr(self, segment_window=100, discard=True):
        """Mean segmental TTR (MSTTR) computed as average of TTR scores for segments in a text.

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
            raise ValueError(
                "Window size must be greater than text size of {}. Try a smaller segment_window size.".format(
                    self.words
                )
            )

        if segment_window < 1 or type(segment_window) is float:
            raise ValueError("Window size must be a positive integer.")

        scores = list()
        for segment in segment_generator(self.wordlist, segment_window):
            ttr = len(set(segment)) / len(segment)
            scores.append(ttr)

        if discard:  # discard remaining words
            del scores[-1]

        if sys.version_info == 3:
            mean_ttr = mean(scores)
        else:
            mean_ttr = sum(scores) / len(scores)
        return mean_ttr

    def mattr(self, window_size=100):
        """Moving average TTR (MATTR) computed using the average of TTRs over successive segments
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
            raise ValueError(
                "Window size must not be greater than text size of {}. Try a smaller window size.".format(
                    self.words
                )
            )

        if window_size < 1 or type(window_size) is float:
            raise ValueError("Window size must be a positive integer.")

        scores = [
            len(set(window)) / window_size
            for window in list_sliding_window(self.wordlist, window_size)
        ]

        if sys.version_info == 3:
            mattr = mean(scores)
        else:
            mattr = sum(scores) / len(scores)

        return mattr

    def mtld(self, threshold=0.72):
        """Measure of textual lexical diversity, computed as the mean length of sequential words in
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
                ttr = len(terms) / word_counter

                if ttr <= threshold:
                    word_counter = 0
                    terms = set()
                    factor_count += 1

            # partial factors for the last segment computed as the ratio of how far away ttr is from
            # unit, to how far away threshold is to unit
            if word_counter > 0:
                factor_count += (1 - ttr) / (1 - threshold)

            # ttr never drops below threshold by end of text
            if factor_count == 0:
                ttr = self.terms / self.words
                if ttr == 1:
                    factor_count += 1
                else:
                    factor_count += (1 - ttr) / (1 - threshold)

            return len(self.wordlist) / factor_count

        forward_measure = sub_mtld(self, threshold, reverse=False)
        reverse_measure = sub_mtld(self, threshold, reverse=True)

        if sys.version_info[0] == 3:
            mtld = mean((forward_measure, reverse_measure))
        else:
            mtld = (forward_measure + reverse_measure) / 2

        return mtld

    def hdd(self, draws=42):
        """Hypergeometric distribution diversity (HD-D) score.

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
            raise ValueError(
                "Number of draws should be less than the total sample size of {0}. Try a draw value smaller than {0}, e.g. hdd(draws={1}.)".format(
                    self.words, suggestion
                )
            )
        if draws < 1 or type(draws) is float:
            raise ValueError(
                "Number of draws must be a positive integer. E.g. hdd(draws={})".format(
                    suggestion
                )
            )

        term_freq = Counter(self.wordlist)

        term_contributions = [
            (1 - hypergeom.pmf(0, self.words, freq, draws)) / draws
            for term, freq in term_freq.items()
        ]

        return sum(term_contributions)

    def vocd(self, ntokens=50, within_sample=100, iterations=3, seed=42):
        """Vocd score of lexical diversity derived from a series of TTR samplings and curve fittings.

        Vocd is meant as a measure of lexical diversity robust to varying text lengths. See also hdd.
        The vocd is computed in 4 steps as follows.

        Step 1: Take 100 random samples of 35 words from the text. Compute the mean TTR from the 100 samples.
        Step 2: Repeat this procedure for samples of 36 words, 37 words, and so on, all the way to ntokens
            (recommended as 50 [default]). In each iteration, compute the TTR. Then get the mean TTR over
            the different number of tokens. So now we have an array of averaged TTR values for ntoken=35,
            ntoken=36,..., and so on until ntoken=50.
        Step 3: Find the best-fitting curve from the empirical function of TTR to word size (ntokens).
            The value of D that provides the best fit is the vocd score.
        Step 4: Repeat steps 1 to 3 for x number (default=3) of times before averaging D, which is the
            returned value.

        Helper Function
        ---------------
        ttr_nd
            TTR as a function of latent lexical diversity (d) and text length (n).

        Parameters
        ----------
        ntokens: int
            Maximum number for the token/word size in the random samplings (default=50).
        within_sample: int
            Number of samples for each token/word size (default=100).
        iterations: int
            Number of times to repeat steps 1 to 3 before averaging (default=3).
        seed: int
            Seed for the pseudo-random number generator in ramdom.sample() (default=42).

        Returns
        -------
        float
        """
        try:
            assert self.words > ntokens
        except Exception:
            raise ValueError(
                "Number of tokens in text smaller than number of tokens to sample."
            )

        random.seed(seed)
        adapted_d = []
        for _ in range(iterations):
            mean_ttr_results = []
            for ntoken in range(35, 1 + ntokens):
                ttr_results = []
                for _ in range(100):
                    sample_of_tokens = random.sample(self.wordlist, k=ntoken)
                    n_unique = len(set(sample_of_tokens))
                    ttr = n_unique / ntoken
                    ttr_results.append(ttr)
                mean_ttr = np.mean(ttr_results)
                mean_ttr_results.append(mean_ttr)
            # Step 3
            xdata = list(range(35, 1 + ntokens))
            ydata = mean_ttr_results
            popt, _ = curve_fit(ttr_nd, xdata, ydata)
            adapted_d.append(popt[0])
        return np.mean(adapted_d)

    def vocd_fig(
        self,
        ntokens=50,
        within_sample=100,
        seed=42,
        return_data=False,
        color1="darkslategray",
        color2="black",
        leglabel1="Random-sampling TTR curve",
        leglabel2="Best-fitting theoretical curve",
        lwidth1=3,
        lwidth2=1.5,
        lpattern1="-",
        lpattern2="--",
        xlabel="Sample size",
        ylabel="TTR",
        figsize=None,
        title="",
    ):
        """ Plots the empirical function of TTR to word sampling and the best-fitting curve in the 
            vocd measure. Vocd is meant as a measure of lexical diversity robust to varying text lengths. 
            See also vocd and hdd.

            The horizontal axis is the token/word size of the random samplings (e.g. token size=50 means 
            that each of the 100 samples consists of 50 words).
            The vertical axis is the mean TTR score from the 100 samples computed in 2 steps as follows. 
            First, take 100 random samples of 35 words from the text. Compute the mean TTR from the 100 
            samples. Second, repeat this procedure for samples of 36 words, 37 words, and so on, all the 
            way to ntokens (recommended as 50 [default]).

            Helper Function
            ---------------
            ttr_nd 
                TTR as a function of latent lexical diversity (d) and text length (n).

            Parameters
            ----------
            ntokens: int
                Maximum number for the token/word size in the random samplings (default=50).
            within_sample: int
                Number of samples for each token/word size (default=100).
            iterations: int
                Number of times to repeat steps 1 to 3 before averaging (default=3).
            seed: int
                Seed for the pseudo-random number generator in ramdom.sample() (default=42).
            return_data: boolean
                If True, returns a tuple (figure, xvalues, empirical_TTR, fitted_TTR). Default is False.
                xvalues, empirical_TTR, and fitted_TTR are lists of numbers.

            Returns
            -------
            matplotlib.figure.Figure            
        """
        try:
            assert self.words > ntokens
        except Exception:
            raise ValueError(
                "Number of tokens in text smaller than number of tokens to sample."
            )

        random.seed(seed)
        ydata = []
        for ntoken in range(35, 1 + ntokens):
            ttr_results = []
            for _ in range(100):
                sample_of_tokens = random.sample(self.wordlist, k=ntoken)

                n_unique = len(set(sample_of_tokens))

                ttr = n_unique / ntoken

                ttr_results.append(ttr)

            mean_ttr = np.mean(ttr_results)
            ydata.append(mean_ttr)

        xdata = list(range(35, 1 + ntokens))
        assert len(xdata) == len(ydata)

        popt, _ = curve_fit(ttr_nd, xdata, ydata)

        # Plot
        fig = plt.figure(figsize=figsize)
        plt.plot(
            xdata,
            ydata,
            color=color1,
            linewidth=lwidth1,
            linestyle=lpattern1,
            label=leglabel1,
        )
        plt.plot(
            xdata,
            ttr_nd(xdata, popt),
            color=color2,
            linewidth=lwidth2,
            linestyle=lpattern2,
            label=leglabel2,
            alpha=0.6,
        )
        plt.locator_params(axis="y", nbins=5)
        plt.xlabel(xlabel, fontweight="bold", loc="right", size=12)
        plt.ylabel(ylabel, fontweight="bold", loc="top", size=12)
        plt.title(title, fontweight="bold", loc="left", size=12)
        plt.legend(
            loc="best", fontsize=11, frameon=False, fancybox=True, framealpha=0.8,
        )

        if return_data:
            return fig, xdata, ydata, list(ttr_nd(xdata, popt))
        else:
            return fig
            
    def __str__(self):
        return " ".join(self.wordlist)

    def __repr__(self):
        return 'LexicalRichness(words={}, terms={}, preprocessor={}, tokenizer={}, wordlist={}, string="{}")'.format(
            self.words,
            self.terms,
            self.preprocessor,
            self.tokenizer,
            self.wordlist,
            " ".join(self.wordlist),
        )
