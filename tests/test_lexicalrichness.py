#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `lexicalrichness` package."""


import unittest

from lexicalrichness import *
import textblob


class TestLexicalrichness(unittest.TestCase):
    """Tests for `lexicalrichness` package."""

    def setUp(self):
        self.s1 = "TEST text with some text numbers 42, hyphen-here, and text punctuations."
        self.s2 = "TEST text with some text numbers 42, hyphen–here, and text punctuations."
        self.s3 = "TEST text with some text numbers 42, hyphen—here, and text punctuations."
        self.wordlist = "TEST text with some text numbers hyphenhere and text punctuations".split()
        self.emptystring = ''

        self.obj1 = LexicalRichness(self.s1)
        self.obj2 = LexicalRichness(self.s2)
        self.obj3 = LexicalRichness(self.s3)
        self.emptyobj = LexicalRichness(self.emptystring)
        self.wordlistobj = LexicalRichness(self.wordlist, preprocessor=None, tokenizer=None)

    def tearDown(self):
        pass

    def test_preprocess(self):
        self.assertEqual(preprocess(self.s1), 'test text with some text numbers , hyphenhere, and text punctuations.')
        self.assertEqual(preprocess(self.s2), 'test text with some text numbers , hyphenhere, and text punctuations.')
        self.assertEqual(preprocess(self.s3), 'test text with some text numbers , hyphenhere, and text punctuations.')
        self.assertEqual(preprocess(self.emptystring), '')

    def test_tokenize(self):
        self.assertIs(type(tokenize(self.s1)), list)
        self.assertIs(type(tokenize(self.s2)), list)
        self.assertIs(type(tokenize(self.s3)), list)
        self.assertIs(type(tokenize(self.emptystring)), list)

    def test_blobber(self):
        self.assertIs(type(blobber(self.s1)), textblob.blob.WordList)
        self.assertIs(type(blobber(self.s2)), textblob.blob.WordList)
        self.assertIs(type(blobber(self.s3)), textblob.blob.WordList)
        self.assertIs(type(blobber(self.emptystring)), textblob.blob.WordList)

    def test_list_sliding_window(self):
        test_list = ['a', 'b', 'c', 'd']

        self.assertEqual(list(list_sliding_window(test_list, 1)), [('a',), ('b',), ('c',), ('d',)])
        self.assertEqual(list(list_sliding_window(test_list, 2)), [('a', 'b'), ('b', 'c'), ('c', 'd')])
        self.assertEqual(list(list_sliding_window(test_list, 3)), [('a', 'b', 'c'), ('b', 'c', 'd')])
        self.assertEqual(list(list_sliding_window(test_list, 4)), [('a', 'b', 'c', 'd')])

    def test_segment_generator(self):
        test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.assertEqual(list(segment_generator(test_list, 3)), [[1,2,3], [4,5,6], [7,8,9], [10]])
        self.assertEqual(list(segment_generator(test_list, 5)), [[1,2,3,4,5], [6,7,8,9,10]])
        self.assertEqual(list(segment_generator(test_list, 1)), [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
        self.assertEqual(list(segment_generator(test_list, 10)), [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
        self.assertEqual(list(segment_generator(test_list, 11)), [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])

    def test_words(self):
        self.assertEqual(self.obj1.words, 10)
        self.assertEqual(self.wordlistobj.words, 10)
        self.assertEqual(self.emptyobj.words, 0)

    def test_terms(self):
        self.assertEqual(self.obj1.terms, 8)
        self.assertEqual(self.wordlistobj.terms, 8)
        self.assertEqual(self.emptyobj.terms, 0)

    def test_ttr(self):
        self.assertEqual(self.obj1.ttr, 0.8)

    def test_rttr(self):
        self.assertEqual(self.obj1.rttr, 2.5298221281347035)

    def test_cttr(self):
        self.assertEqual(self.obj1.cttr, 1.7888543819998317)

    def test_Herdan(self):
        self.assertEqual(self.obj1.Herdan, 0.9030899869919434)

    def test_Summer(self):
        self.assertEqual(self.obj1.Summer, 0.8777828395738175)

    def test_Dugast(self):
        self.assertEqual(self.obj1.Dugast, 23.760032854423635)

    def test_Maas(self):
        self.assertEqual(self.obj1.Maas, 0.04208748389057132)

    def test_msttr(self):
        self.assertEqual(self.obj1.msttr(segment_window=5, discard=True), 0.8)
        self.assertEqual(self.obj1.msttr(segment_window=5, discard=False), 0.9)

        with self.assertRaises(ValueError):
            self.obj1.msttr(segment_window=0)
        with self.assertRaises(ValueError):
            self.obj1.msttr(segment_window=-1)
        with self.assertRaises(ValueError):
            self.obj1.msttr(segment_window=1.5)

    def test_mattr(self):
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
        self.assertEqual(self.obj1.mtld(threshold=0.72), 14.000000000000004)

        all_unqiue = LexicalRichness('only unique terms in this little string')
        self.assertEqual(all_unqiue.mtld(threshold=0.72), all_unqiue.words)

    def test_hdd(self):
        self.assertEqual(self.obj1.hdd(draws=5), 0.8833333333333332)

        with self.assertRaises(ValueError):
            self.obj1.hdd(draws=0)
        with self.assertRaises(ValueError):
            self.obj1.hdd(draws=-5)
        with self.assertRaises(ValueError):
            self.obj1.hdd(draws=1.5)


if __name__ == '__main__':
    unittest.main()
