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

## Generate a Canvas API key
1.  Login to Canvas
2.  Go to ``Account > Settings``
3.  Click ``+ New Access Token``. For "Purpose", put ``latex-gloves``, and press ``Generate Token``.
4.  Copy the token.
5.  Create a file called ``key.txt`` in the ``resources/`` directory, paste the token into it, and save. Make sure the file has only one line and that there are no other characters. 

# Usage

## Quick reference

```
python texParser.py main.tex
python convert.py
python gloves.py
```

## User guide

Once the quiz is ready to be uploaded:

### Environment setup
1.  In the Overleaf project, first ensure that the document is compiling with no errors, and that all lines commented out with a ``\begin{comment}`` command have been deleted or converted to the ``%`` comment style.
2.  Click ``Menu > Download > Source`` to download a zip file of the project.
3.  Extract the contents of the zip file to the same directory that latex-gloves is installed (e.g., ``C:\Users\2250\Desktop\latex-gloves-master``
4.  Open up with Windows Command Prompt.
5.  Navigate to the latex-gloves directory within the command prompt using the ``cd`` (change directory) command. E.g., run ``cd C:\Users\2250\Desktop\latex-gloves-master``

### Splitting the master file into individual .tex files
1.  Ensure that all packages you plan on using are indicated in the header file, ``resources/questionPreamble.tex``. This block of TeX is included at the start of all individual tex files. Similarly, ``resources/latexClosure.tex`` is included at the end of each tex file if you need to make any adjustments there.
2.  Pass the main TeX file (e.g., ``main.tex``) into the TeX parser by running ``python texParser.py main.tex``. _Note:_ For this to work, ``main.tex`` and ``texParser.py`` must be in the same folder.
3.  At this time, the TeX parser will inform you of any parsing errors that it encounters. If errors are encountered, they must be fixed within the TeX file by the user. See the section below on question syntax.

### Converting to PNGs
1.  Simply run ``python convert.py`` to begin the conversion process. Hopefully, since your document compiled without error on overleaf, the questions will be compiled without error here, as well. In any case, a bunch of very verbose output will be spit onto the screen by ``pdflatex``, and it will indicate any compiler errors that need be fixed.

### Upload to Canvas
1.  Open up ``gloves.py`` in your favorite text editor.
2.  Change ``folderPath`` to the path in Canvas's file system you'd like to upload the quizz's images to, e.g. ``/quizzes/chapter1``. Make sure this path begins with a leading ``/``.
3.  Create an empty quiz in Canvas, and change ``quizURL`` to the quiz's URL. It should look something like ``https://xxx.instructure.com/courses/xxxxx/quizzes/xxxxx``.
4.  Cross your fingers and run ``python gloves.py``!


# LaTeX Question Syntax

To be written


# Why no fill-in-the-blank questions?

Automating fill-in-the-blank questions is a very, very bad idea. We've tried it before. It was awful. Never do it. Ever. 

Consider the following example:

```
A rectangle is formed on the XY-plane. 
Three of its corners are defined by (0,0), (0, 1/3), and (1/2, 0).
Where is its fourth corner?
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

I'm sure you can imagine even more entries in the above list.

You might think that maybe, _just maybe_, you can provide specific-enough instructions to wrangle students into a consistent answer format. You might think that _your_ students are smart enough to figure it out. You are wrong. You are more wrong than you realize. Never underestimate the creative stupidity of a human being. Okay, you specify, "include parentheses, express all numbers as fractions in their lowest terms, and do not include a space anywhere in the coordinate pair." So, a student complies, and writes ``The fourth corner is located at (1/2,1/3)``. They are marked wrong by the auto-grader. The student is upset. Their parents angrily call the president of the university demanding a grade change _this instant_. Your palm flies through your face. It will happen.

Fill-in-the-blank answers are a bad idea. Don't do it. Don't even think about it.

If you really, _really_, and I mean _really really_ want a fill-in-the-blank question that isn't a math question, like "What city was the Pascal programming language created in?", then, by all means, input it manually into Canvas. Latex-gloves will not be responsible for your blunder. Just be sure to include all of the possible answers of ``Zurich``, ``Zürich``, ``Zurich, Switzerland``, ``Zurich,Switzerland``, ``Zürich, Switzerland``, and ``Zürich,Switzerland``.




