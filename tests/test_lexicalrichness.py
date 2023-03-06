#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `lexicalrichness` package."""


import unittest

import matplotlib
import numpy as np
import pytest

from lexicalrichness.lexicalrichness import (
    LexicalRichness,
    frequency_wordfrequency_table,
    list_sliding_window,
    preprocess,
    segment_generator,
    tokenize,
    ttr_nd,
)


class TestLexicalrichness(unittest.TestCase):
    """Tests for `lexicalrichness` package."""

    def setUp(self):
        print("setting up")
        self.s1 = (
            "TEST text with some text numbers 42, hyphen-here, and text punctuations."
        )
        self.s2 = (
            "TEST text with some text numbers 42, hyphen–here, and text punctuations."
        )
        self.s3 = (
            "TEST text with some text numbers 42, hyphen—here, and text punctuations."
        )
        self.emptystring = ""
        self.longtext = """Measure of textual lexical diversity, computed as the mean length of sequential words in
                a text that maintains a minimum threshold TTR score.

                Iterates over words until TTR scores falls below a threshold, then increase factor
                counter by 1 and start over. McCarthy and Jarvis (2010, pg. 385) recommends a factor
                threshold in the range of [0.660, 0.750].
                (McCarthy 2005, McCarthy and Jarvis 2010)"""

        self.obj1 = LexicalRichness(self.s1)
        self.obj2 = LexicalRichness(self.s2)
        self.obj3 = LexicalRichness(self.s3)
        self.emptyobj = LexicalRichness(self.emptystring)
        self.longtext = LexicalRichness(self.longtext)

    def tearDown(self):
        print("tearing down\n")

    def test_preprocess(self):
        print("testing preprocess")

        self.assertEqual(
            preprocess(self.s1),
            "test text with some text numbers , hyphenhere, and text punctuations.",
        )
        self.assertEqual(
            preprocess(self.s2),
            "test text with some text numbers , hyphenhere, and text punctuations.",
        )
        self.assertEqual(
            preprocess(self.s3),
            "test text with some text numbers , hyphenhere, and text punctuations.",
        )
        self.assertEqual(preprocess(self.emptystring), "")

    def test_tokenize(self):
        print("testing tokenize")

        self.assertIs(type(tokenize(self.s1)), list)
        self.assertIs(type(tokenize(self.s2)), list)
        self.assertIs(type(tokenize(self.s3)), list)
        self.assertIs(type(tokenize(self.emptystring)), list)

    def test_tokenize_str_error(self):
        """Ensures error is raised if tokenizer is set to None and input is a string."""
        with pytest.raises(AssertionError) as err:
            LexicalRichness(self.s1, tokenizer=None)
        assert (
            str(err.value)
            == "If tokenizer is None, then input should be a list of words."
        )

    def test_list_sliding_window(self):
        print("testing list_sliding_window")

        test_list = ["a", "b", "c", "d"]

        self.assertEqual(
            list(list_sliding_window(test_list, 1)),
            [("a",), ("b",), ("c",), ("d",)],
        )
        self.assertEqual(
            list(list_sliding_window(test_list, 2)),
            [("a", "b"), ("b", "c"), ("c", "d")],
        )
        self.assertEqual(
            list(list_sliding_window(test_list, 3)),
            [("a", "b", "c"), ("b", "c", "d")],
        )
        self.assertEqual(
            list(list_sliding_window(test_list, 4)), [("a", "b", "c", "d")]
        )

    def test_segment_generator(self):
        print("testing segment_generator")

        test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.assertEqual(
            list(segment_generator(test_list, 3)),
            [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]],
        )
        self.assertEqual(
            list(segment_generator(test_list, 5)),
            [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]],
        )
        self.assertEqual(
            list(segment_generator(test_list, 1)),
            [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]],
        )
        self.assertEqual(
            list(segment_generator(test_list, 10)),
            [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],
        )
        self.assertEqual(
            list(segment_generator(test_list, 11)),
            [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],
        )

    def test_words(self):
        print("testing words")
        self.assertEqual(self.obj1.words, 10)
        self.assertEqual(self.emptyobj.words, 0)

    def test_terms(self):
        print("testing terms")
        self.assertEqual(self.obj1.terms, 8)
        self.assertEqual(self.emptyobj.terms, 0)

    def test_ttr(self):
        print("testing ttr")
        self.assertEqual(self.obj1.ttr, 0.8)

    def test_rttr(self):
        print("testing rttr")
        self.assertEqual(self.obj1.rttr, 2.5298221281347035)

    def test_cttr(self):
        print("testing cttr")
        self.assertEqual(self.obj1.cttr, 1.7888543819998317)

    def test_Herdan(self):
        print("testing Herdan")
        self.assertEqual(self.obj1.Herdan, 0.9030899869919434)

    def test_Summer(self):
        print("testing Summer")
        self.assertEqual(self.obj1.Summer, 0.8777828395738175)

    def test_Dugast(self):
        print("testing Dugast")
        self.assertEqual(self.obj1.Dugast, 23.760032854423635)

    def test_Maas(self):
        print("testing Maas")
        self.assertEqual(self.obj1.Maas, 0.04208748389057132)

    def test_yulek(self):
        print("testing Yule's K")
        self.assertEqual(self.obj1.yulek, 600.0)

    def test_yulei(self):
        print("testing Yule's I")
        self.assertEqual(self.obj1.yulei, 8.0)

    def test_herdanvm(self):
        print("testing Herdan's Vm")
        self.assertEqual(self.obj1.herdanvm, 0.18708286933869708)

    def test_simpsond(self):
        print("testing Simpson's D")
        self.assertEqual(self.obj1.simpsond, 0.06666666666666667)

    def test_msttr(self):
        print("testing msttr")

        self.assertEqual(self.obj1.msttr(segment_window=5, discard=True), 0.8)
        self.assertEqual(self.obj1.msttr(segment_window=5, discard=False), 0.9)

        with self.assertRaises(ValueError):
            self.obj1.msttr(segment_window=0)
        with self.assertRaises(ValueError):
            self.obj1.msttr(segment_window=-1)
        with self.assertRaises(ValueError):
            self.obj1.msttr(segment_window=1.5)

    def test_mattr(self):
        print("testing mattr")

        self.assertEqual(self.obj1.mattr(window_size=5), 0.9)
        self.assertEqual(self.obj1.mattr(window_size=1), 1)
        self.assertEqual(self.obj1.mattr(window_size=self.obj1.words), self.obj1.ttr)

        with self.assertRaises(ValueError):
            self.obj1.mattr(window_size=0)
        with self.assertRaises(ValueError):
            self.obj1.mattr(window_size=-1)
        with self.assertRaises(ValueError):
            self.obj1.mattr(window_size=1.5)

    def test_mtld(self):
        print("testing mtld")

        self.assertEqual(self.obj1.mtld(threshold=0.72), 14.000000000000004)

        all_unqiue = LexicalRichness("only unique terms in this little string")
        self.assertEqual(all_unqiue.mtld(threshold=0.72), all_unqiue.words)

    def test_hdd(self):
        print("testing hdd")

        self.assertEqual(self.obj1.hdd(draws=5), 0.8833333333333332)

        with self.assertRaises(ValueError):
            self.obj1.hdd(draws=0)
        with self.assertRaises(ValueError):
            self.obj1.hdd(draws=-5)
        with self.assertRaises(ValueError):
            self.obj1.hdd(draws=1.5)

    def test_ttr_nd(self):
        self.assertEqual(ttr_nd(N=100, D=2), 0.1809975124224178)

    def test_vocd(self):
        print("testing voc-D")
        self.assertIs(type(self.longtext.vocd()), np.float64)

        # Gently raise exception if text size is small
        with pytest.raises(ValueError) as err:
            self.obj1.vocd()
        assert (
            str(err.value)
            == "Number of tokens in text smaller than number of tokens to sample."
        )

        # Test that random seed works (for reproducibility)
        first_seed42 = self.longtext.vocd()
        second_seed42 = self.longtext.vocd()
        third_seed0 = self.longtext.vocd(seed=0)
        assert first_seed42 == second_seed42
        assert first_seed42 != third_seed0
        assert second_seed42 != third_seed0

    def test_vocd_fig(self):
        print("testing voc-D figure")
        assert isinstance(self.longtext.vocd_fig(), matplotlib.pyplot.Axes)

        # Gently raise exception if text size is small
        with pytest.raises(ValueError) as err:
            self.obj1.vocd_fig()
        assert (
            str(err.value)
            == "Number of tokens in text smaller than number of tokens to sample."
        )

    def test_frequency_wordfrequency_table(self):
        tab = frequency_wordfrequency_table(self.longtext.wordlist)
        assert tab.shape[1] == 3
        assert tab.columns.tolist() == ["freq", "fv_i_N", "sum_element"]
        assert tab.freq.min() >= 0
        assert tab.fv_i_N.min() >= 0
        assert tab.sum_element.min() >= 0


if __name__ == "__main__":
    unittest.main()
