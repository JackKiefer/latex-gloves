# First-time setup

## Install Python
1. Download the latest version of Python 3.7 for Windows from [the Python website.](https://www.python.org/) The file is called ``python-3.7.x.exe`` where ``x`` is the minor version number.
2. Run ``python-3.7.x.exe``. Check "Add Python 3.7 to PATH" and press "Install Now"

## Install Python dependencies
1. Open up the Windows Command Prompt:
    1.  Hit the Windows key (``⊞ Win``) to open the start menu
    2.  Type ``cmd`` and press enter
2. In the command prompt, run the command ``pip install numpy sympy``

## Install MiKTeX

1.  Navigate to the [MiKTeX download page](https://miktex.org/download)and nab the executable. 
2.  When installing, be sure to let it check for updates.

## Install latex-gloves
1. Download ``latex-gloves-master.zip`` from [here](https://github.com/JackMiranda/latex-gloves/archive/master.zip)
2. Extract ``latex-gloves-master.zip`` to a folder you can easily find. In this example, we'll use ``C:\Users\2250\Desktop\latex-gloves-master``


# Usage
Once the quiz is ready to be uploaded:

## Environment setup
1.  In the Overleaf project, click ``Menu > Download > Source`` to download a zip file of the project.
2.  Extract the contents of the zip file to the same directory that latex-gloves is installed (e.g., ``C:\Users\2250\Desktop\latex-gloves-master``
3.  Open up with Windows Command Prompt.
4.  Navigate to the latex-gloves directory within the command prompt using the ``cd`` (change directory) command. E.g., run ``cd C:\Users\2250\Desktop\latex-gloves-master``

## Parsing the TeX
1.  Pass the main TeX file (e.g., ``main.tex``) into the TeX parser by running ``python texParser.py main.tex``. _Note:_ For this to work, ``main.tex`` and ``texParser.py`` must be in the same folder.
2.  At this time, the TeX parser will inform you of any parsing errors that it encounters. If errors are encountered, they must be fixed within the TeX file by the user. See the section below on question formatting and parsing.









# Why no fill-in-the-blank questions?

Automating fill-in-the-blank questions is a very, very bad idea. We've tried it before. It was awful. Never do it. Ever. 

Consider the following example:

```
A rectangle is formed on the XY-plane. Three of its corners are defined by (0,0), (0, 1/3), and (1/2, 0). Where is its fourth corner?
```

Clearly, the answer is simply ``(1/2, 1/3)``. Now, this is a fine answer format for a handwritten test. Unfortunately, this is a veritable nightmare trying to encode into Canvas. 

Fill-in-the-blank questions in Canvas are not "smart;" to get the answer correct, what the student inputs must match one of the possible answers _character-for-character_. This quickly explodes into a huge variety of different possible answers that are all correct and mathematically equivalent, but using different characters (and yes, _spaces_ count as characters, too):

* ``(1/2, 1/3)``
* ``(0.5, 0.33)``
* ``(0.50, 0.333)``
* ``1/2, 1/3``
* ``0.5, 0.33``
* ``0.50, 0.333``
* ``x=1/2, y=1/3``
* ``x = 1/2, y = 1/3``
* ``(1/2,1/3)``
* ``(0.5,0.33)``
* ``(0.50,0.333)``
* ``1/2,1/3``
* ``0.5,0.33``
* ``0.50,0.333``
* ``x=1/2,y=1/3``
* ``x = 1/2,y = 1/3``
* `` (1/2, 1/3)``
* `` (0.5, 0.33)``
* `` (0.50, 0.333)``
* `` 1/2, 1/3``
* `` 0.5, 0.33``
* `` 0.50, 0.333``
* `` x=1/2, y=1/3``
* `` x = 1/2, y = 1/3``
* `` (1/2,1/3)``
* `` (0.5,0.33)``
* `` (0.50,0.333)``
* `` 1/2,1/3``
* `` 0.5,0.33``
* `` 0.50,0.333``
* `` x=1/2,y=1/3``
* `` x = 1/2,y = 1/3``


I'm sure you can imagine even more entries in the above list.

You might think that maybe, _just maybe_, you can provide specific-enough instructions to wrangle students into a consistent answer format. You might think that _your_ students are smart enough to figure it out. You are wrong. You are more wrong than you realize. Never underestimate the creative stupidity of a human being. Okay, you specify, "include parentheses, express all numbers as fractions in their lowest terms, and do not include a space anywhere in the coordinate pair." So, a student complies, and writes ``The fourth corner is located at (1/2,1/3)``. They are marked wrong by the auto-grader. The student is upset. Their parents angrily call the president of the university demanding a grade change _this instant_. Your palm flies through your face. It will happen.

Fill-in-the-blank answers are a bad idea. Don't do it. Don't even think about it.

If you really, _really_, and I mean _really really_ want a fill-in-the-blank question that isn't a math question, like "What city was the Pascal programming language created in?", then, by all means, input it manually into Canvas. Latex-gloves will not be responsible for your blunder. Just be sure to include all of the possible answers of ``Zurich``, ``Zürich``, ``Zurich, Switzerland``, ``Zurich,Switzerland``, ``Zürich, Switzerland``, and ``Zürich,Switzerland``.




