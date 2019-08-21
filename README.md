**latex-gloves** is a command-line software suite for the automatic creation of auto-graded Canvas quizzes for mathematics courses. 

latex-gloves allows an entire quiz to be defined in a collaborative Overleaf document. The program automates: generating individual images for each question; uploading the images to Canvas; creating question groups; and creating multiple-choice, numeric-answer, matrix, and essay quiz questions.

# First-time setup

## Step 1: Install (Windows / Mac OS)
### i) Install Python
1. Download the latest version of Python 3.7 from [the Python website.](https://www.python.org/)
2. Run the installer. Check "Add Python 3.7 to PATH" and press "Install Now"

### ii) Install Python dependencies

1. Open up a command console.
    *  **Windows:** Hit the Windows key (``⊞ Win``) to open the start menu, type ``cmd``, press enter.
    *  **Mac OS:** Launch the Terminal application found in ``Applications > Utilities``
2. In the console, run the command ``pip install numpy sympy``

### iii) Install MiKTeX

1.  Navigate to the [MiKTeX download page](https://miktex.org/download) and nab the installer.
2.  When installing, be sure to let it check for updates.

### iv) Install latex-gloves
1. Download ``latex-gloves-master.zip`` from [here](https://github.com/JackMiranda/latex-gloves/archive/master.zip)
2. Extract ``latex-gloves-master.zip`` to a folder you can easily find. In this example, we'll use ``C:\Users\2250\Desktop\latex-gloves-master``

## Step 1: Install (Linux)

For Debian-based systems:

```
sudo apt install texlive-latex-base texlive-fonts-recommended texlive-latex-extra
pip install numpy sympy
git clone https://github.com/JackMiranda/latex-gloves
cd latex-gloves
```

For other systems: 

```
You know what you're doing. 
```

## Step 2: Generate a Canvas API key (all systems)
1.  Login to Canvas
2.  Go to ``Account > Settings``
3.  Click ``+ New Access Token``. For "Purpose", put ``latex-gloves``, and press ``Generate Token``.
4.  Copy the token.
5.  Create a file called ``key.txt`` in the ``resources/`` directory, paste the token into it, and save. Make sure the file has only one line and that there are no other characters. 

# User guide

## Step 1: Structuring the quiz and formatting questions

Each quiz should be contained in a single master TeX file (usually in Overleaf to allow for collaboration) consisting of a **master header**, any number of **questions**, and a **master footer**. 

### Master headers and question headers
The each header is simply a LaTeX preamble consisting of the document declaration, package includes, and any custom declarations. 

The **master header** is the preamble of the master TeX file containing every question. The following is an example of a fairly minimal master header; note the document class  and environment begins:

```latex
%%% Document class for the master TeX file
\documentclass[answers]{exam}

%%% Package includes
\usepackage{amsmath}
%%% Custom commands
\renewcommand{\vec}[1]{\boldsymbol{#1}}

%%% Begin questions environment
\begin{document}
\raggedright
\begin{questions}
```

The **question header** is the preamble that is used to generate each individual question image. It is defined in ``resources/questionPreamble.tex``. It is of a different document class and geometry, but the package-includes and custom commands should be the same. Like so:

```latex
%%% Document class for each question file
\documentclass[convert={outext=.png}, class=exam, border=20pt, varwidth]{standalone}

%%% Package includes
\usepackage{amsmath}
%%% Custom commands
\renewcommand{\vec}[1]{\boldsymbol{#1}}

%%% Begin single question environment
\begin{document}
```

### Master footers and question footers

Similar to the headers, the **master footer** and **question footer** are simply the LaTeX footers of the master and question TeX files, respectively. 

The master footer is usually just:

```latex
\end{questions}
\end{document}
```

while the question footer, defined in ``resources/questionPreamble.tex``, is usually simply:

```latex
\end{document}
```

### Formatting questions

All questions have several standard components. Consider the following example of a numeric question:

```latex
\question%c01s02n08b.tex
%type: numeric

\hfill \today
\hfill c01s02n08b
\vspace{1em}

Given $x^2 = 81$, solve for $x$.

\vspace{1em}
{\rule{\linewidth}{0.4pt}}

\begin{solution}
$9, -9$
\end{solution}

\newpage
```

Let's break down each component.

```latex
\question%c01s02n08b.tex
%type: numeric
```

This is the question declaration. It says we're creating a numeric-answer question with the unique ID ``c01s02n08b``, code for "chapter 1, section 2, problem number 8, variant b." Except for the "variant" indicator, it doesn't matter what the code itself is; you are free to use whatever system you like.

The inclusion of the lower-case "variant" letter at the end of the code indicates that the question is a member of a group. That is, should there also exist questions ``c01s02n08a`` and ``c01s02n08c``, all three questions will be placed into a question group from which only one will be randomly selected and shown to the quiz-taking student. 

```latex
\hfill \today
\hfill c01s02n08b
\vspace{1em}
```

These are simply some graphical elements that place today's date, the question ID, and some spacing before the content of the question. It is generally handy to include this to keep track of each question as the semesters go by. Feel free to edit or delete this. 


```latex
Given $x^2 = 81$, solve for $x$.
```

The seitan of the question! Any and all LaTeX is valid here. That's right, throw in all the equations, tables, matrices, graphs, and cat pictures that your heart desires. If it compiles, it works!

```latex
\vspace{1em}
{\rule{\linewidth}{0.4pt}}
```

This is more graphical fiddling that adds a horizontal line to separate the question body from the solutions. Again: handy, but not strictly neccesarry. Modify to your content.



```latex
\begin{solution}
$9, -9$
\end{solution}
```

The solution! The format of this changes depending on which question type we're dealing with (see below), but the solutions always show up after the question body. 

```latex
\newpage
```

The all-important ``\newpage``! This _must_ go at the end of all question blocks (including the last one) in order for latex-gloves to know to stop grabbing lines for the current question. 

#### Numeric-answer questions
Numeric-answer questions support multiple correct answers and allow for an acceptable margin of error. Each correct answer should be separated by a comma (,). The ``\pm`` operator (±) allows each answer to be given an appropriate bound. 

```latex
\question%c01s02n08c.tex
%type: numeric

\hfill \today
\hfill c01s02n08c
\vspace{1em}

Given $x^2 = 81$, solve for $x$.

\vspace{1em}
{\rule{\linewidth}{0.4pt}}

\begin{solution}
$9, -9$
\end{solution}

\newpage
```

Let's break down each component.

```latex
\question%c01s02n08b.tex
%type: numeric
```


#### Multiple-choice questions
#### Matrix-answer questions
#### Essay questions

## Step 2: Parsing and uploading the quiz to Canvas

### Quick command reference
```
python texParser.py main.tex
python convert.py
python gloves.py
```

### i) Environment setup
1.  In the Overleaf project, first ensure that the document is compiling with no errors, and that all lines commented out with a ``\begin{comment}`` command have been deleted or converted to the ``%`` comment style.
2.  Click ``Menu > Download > Source`` to download a zip file of the project.
3.  Extract the contents of the zip file to the same directory that latex-gloves is installed (e.g., ``C:\Users\2250\Desktop\latex-gloves-master``
4.  Open up with Windows Command Prompt.
5.  Navigate to the latex-gloves directory within the command prompt using the ``cd`` (change directory) command. E.g., run ``cd C:\Users\2250\Desktop\latex-gloves-master``

### ii) Splitting the master file into individual .tex files
1.  Ensure that all packages you plan on using are indicated in the header file, ``resources/questionPreamble.tex``. This block of TeX is included at the start of all individual tex files. Similarly, ``resources/latexClosure.tex`` is included at the end of each tex file if you need to make any adjustments there.
2.  Pass the main TeX file (e.g., ``main.tex``) into the TeX parser by running ``python texParser.py main.tex``. _Note:_ For this to work, ``main.tex`` and ``texParser.py`` must be in the same folder.
3.  At this time, the TeX parser will inform you of any parsing errors that it encounters. If errors are encountered, they must be fixed within the TeX file by the user. See the section above on question syntax.

### iii) Converting to PNGs
1.  Simply run ``python convert.py`` to begin the conversion process. Hopefully, since your document compiled without error on overleaf, the questions will be compiled without error here, as well. In any case, a bunch of very verbose output will be spit onto the screen by ``pdflatex``, and it will indicate any compiler errors that need be fixed.

### iv) Upload to Canvas
1.  Open up ``gloves.py`` in your favorite text editor.
2.  Change ``folderPath`` to the path in Canvas's file system you'd like to upload the quizz's images to, e.g. ``/quizzes/chapter1``. Make sure this path begins with a leading ``/``.
3.  Create an empty quiz in Canvas, and change ``quizURL`` to the quiz's URL. It should look something like ``https://xxx.instructure.com/courses/xxxxx/quizzes/xxxxx``.
4.  Cross your fingers and run ``python gloves.py``!



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




