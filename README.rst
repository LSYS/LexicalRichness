===============
LexicalRichness
===============
.. image:: https://badge.fury.io/py/lexicalrichness.svg
        :target: https://pypi.org/project/lexicalrichness/
.. image:: https://badgen.net/github/release/Naereen/Strapdown.js
        :target: https://github.com/LSYS/LexicalRichness.js/releases
.. image:: https://www.codefactor.io/repository/github/lsys/lexicalrichness/badge
        :target: https://www.codefactor.io/repository/github/lsys/lexicalrichness  


.. image:: https://img.shields.io/lgtm/grade/python/g/LSYS/LexicalRichness.svg?logo=lgtm&logoWidth=18)
        :target: https://lgtm.com/projects/g/LSYS/LexicalRichness/context:python
.. image:: https://img.shields.io/pypi/pyversions/lexicalrichness   
	:target: https://img.shields.io/pypi/pyversions/lexicalrichness  

.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity

.. |Maintenance yes| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity
	

.. image:: https://img.shields.io/badge/PRs-welcome-brightgreen.svg
        :target: http://makeapullrequest.com
.. image:: https://img.shields.io/badge/License-MIT-blue.svg
        :target: https://lbesson.mit-license.org
.. image:: https://mybinder.org/badge_logo.svg
        :target: https://mybinder.org/v2/gh/LSYS/lexicaldiversity-example/main?labpath=example.ipynb
	
	
A small python module to compute textual lexical richness (aka lexical diversity) measures.

Lexical richness refers to the range and variety of vocabulary deployed in a text by a speaker/writer (McCarthy and Jarvis 2007). Lexical richness is used interchangeably with lexical diversity, lexical variation, lexical density, and vocabulary richness and is measured by a wide variety of indices. Uses include (but not limited to) measuring writing quality, vocabulary knowledge (Šišková 2012), speaker competence, and socioeconomic status (McCarthy and Jarvis 2007).

.. image:: http://ForTheBadge.com/images/badges/made-with-python.svg
   :target: https://www.python.org/

Installation
------------
**Install using PIP**

.. code-block:: bash

	pip install lexicalrichness

If you encounter, 


.. code-block:: python

	ModuleNotFoundError: No module named 'textblob'

install textblob:

.. code-block:: bash

	pip install textblob
	
**Install manually from GitHub**

.. code-block:: bash

	git clone https://github.com/LSYS/LexicalRichness.git
	cd LexicalRichness
	pip install .


**Run from the cloud**

Try the package on the cloud (without setting anything up on your local machine) by clicking the icon here:  

|mybinder|

.. |mybinder| image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/LSYS/lexicaldiversity-example/main?labpath=example.ipynb

Quickstart
----------

.. code-block:: python

	>>> from lexicalrichness import LexicalRichness

	# text example
	>>> text = """Measure of textual lexical diversity, computed as the mean length of sequential words in
            		a text that maintains a minimum threshold TTR score.

            		Iterates over words until TTR scores falls below a threshold, then increase factor
            		counter by 1 and start over. McCarthy and Jarvis (2010, pg. 385) recommends a factor
            		threshold in the range of [0.660, 0.750].
            		(McCarthy 2005, McCarthy and Jarvis 2010)"""

	# instantiate new text object (use the tokenizer=blobber argument to use the textblob tokenizer)
	>>> lex = LexicalRichness(text)

	# Return word count.
	>>> lex.words
	57

	# Return (unique) word count.
	>>> lex.terms
	39

	# Return type-token ratio (TTR) of text.
	>>> lex.ttr
	0.6842105263157895

	# Return root type-token ratio (RTTR) of text.
	>>> lex.rttr
	5.165676192553671

	# Return corrected type-token ratio (CTTR) of text.
	>>> lex.cttr
	3.6526846651686067

	# Return mean segmental type-token ratio (MSTTR).
	>>> lex.msttr(segment_window=25)
	0.88

	# Return moving average type-token ratio (MATTR).
	>>> lex.mattr(window_size=25)
	0.8351515151515151

	# Return Measure of Textual Lexical Diversity (MTLD).
	>>> lex.mtld(threshold=0.72)
	46.79226361031519

	# Return hypergeometric distribution diversity (HD-D) measure.
	>>> lex.hdd(draws=42)
	0.7468703323966486

	# Return Herdan's lexical diversity measure.
	>>> lex.Herdan
	0.9061378160786574

	# Return Summer's lexical diversity measure.
	>>> lex.Summer
	0.9294460323356605

	# Return Dugast's lexical diversity measure.
	>>> lex.Dugast
	43.074336212149774

	# Return Maas's lexical diversity measure.
	>>> lex.Maas
	0.023215679867353005

Attributes and properties
+++++++++++++++++++++++++

+-------------------------+-----------------------------------------------------------------------------------+
| ``wordlist``            | list of words                                                   		      |
+-------------------------+-----------------------------------------------------------------------------------+
| ``words``  		  | number of words (w) 				   			      |
+-------------------------+-----------------------------------------------------------------------------------+
| ``terms``		  | number of unique terms (t)			                                      |
+-------------------------+-----------------------------------------------------------------------------------+
| ``preprocessor``        | preprocessor used		                                                      |
+-------------------------+-----------------------------------------------------------------------------------+
| ``tokenizer``           | tokenizer used		                                                      |
+-------------------------+-----------------------------------------------------------------------------------+
| ``ttr``		  | type-token ratio computed as t / w (Chotlos 1944, Templin 1957)         	      |
+-------------------------+-----------------------------------------------------------------------------------+
| ``rttr``	          | root TTR computed as t / sqrt(w) (Guiraud 1954, 1960)                             |
+-------------------------+-----------------------------------------------------------------------------------+
| ``cttr``	          | corrected TTR computed as t / sqrt(2w) (Carrol 1964)		              |
+-------------------------+-----------------------------------------------------------------------------------+
| ``Herdan`` 	          | log(t) / log(w) (Herdan 1960, 1964)                                               |
+-------------------------+-----------------------------------------------------------------------------------+
| ``Summer``    	  | log(log(t)) / log(log(w)) Summer (1966)                                           |
+-------------------------+-----------------------------------------------------------------------------------+
| ``Dugast``          	  | (log(w) ** 2) / (log(w) - log(t) Dugast (1978)				      |
+-------------------------+-----------------------------------------------------------------------------------+
| ``Maas`` 	          | (log(w) - log(t)) / (log(w) ** 2) Maas (1972)                                     |
+-------------------------+-----------------------------------------------------------------------------------+

Methods
+++++++

+-------------------------+-----------------------------------------------------------------------------------+
| ``msttr``            	  | Mean segmental TTR (Johnson 1944)						      |
+-------------------------+-----------------------------------------------------------------------------------+
| ``mattr``  		  | Moving average TTR (Covington 2007, Covington and McFall 2010)		      |
+-------------------------+-----------------------------------------------------------------------------------+
| ``mtld``		  | Measure of Lexical Diversity (McCarthy 2005, McCarthy and Jarvis 2010)            |
+-------------------------+-----------------------------------------------------------------------------------+
| ``hdd``                 | HD-D (McCarthy and Jarvis 2007)                                                   |
+-------------------------+-----------------------------------------------------------------------------------+

Assessing method docstrings
---------------------------
.. code-block:: python

	>>> import inspect

	# docstring for hdd (HD-D)
	>>> print(inspect.getdoc(LexicalRichness.hdd))

	Hypergeometric distribution diversity (HD-D) score.

	For each term (t) in the text, compute the probabiltiy (p) of getting at least one appearance
	of t with a random draw of size n < N (text size). The contribution of t to the final HD-D
	score is p * (1/n). The final HD-D score thus sums over p * (1/n) with p computed for
	each term t. Described in McCarthy and Javis 2007, p.g. 465-466.
	(McCarthy and Jarvis 2007)

	Parameters
	__________
	draws: int
	    Number of random draws in the hypergeometric distribution (default=42).

	Returns
	_______
	float
	
Alternatively, just do

.. code-block:: python

	>>> print(lex.hdd.__doc__)
	
	Hypergeometric distribution diversity (HD-D) score.

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

Contributing
------------
Author
++++++
Lucas Shen

Contributors
++++++++++++
* `Christophe Bedetti <https://github.com/cbedetti>`__
* `David Lesieur <https://github.com/davidlesieur>`__

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given. 
See here for `how to contribute  <./CONTRIBUTING.rst>`__ to this project.
See here for `Contributor Code of
Conduct <http://contributor-covenant.org/version/1/0/0/>`__.

License
-------

The package is released under the `MIT
License <https://opensource.org/licenses/MIT>`__.
