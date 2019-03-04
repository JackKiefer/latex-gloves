# First time set-up

1.  Have the following installed on your system:  
    * **MiKTeX** and the corresponding command ``pdflatex``. [Website](https://miktex.org/)  
    * **pdf2svg**, with installation info found at its [GitHub Repository](https://github.com/dawbarton/pdf2svg)  

2.  Generate a Canvas API key and store it in ``resources/key.txt``
    * While logged in to Canvas, go to ``Account > Settings``
    * Under "Approved Integrations," selection ``+ New Access Token``
    * Write something descriptive for the token's purpose and generate it.
    * Create a file named ``key.txt`` in the ``resources/`` directory, paste your token into it, and save. Make sure the file has no whitespace.
    
# Usage

**Quick usage:**
*  Input the proper quiz URL and file path at the top of ``gloves.py``
*  Download the .tex file from Overleaf (in this example, it shall be named ``main.tex``) 
*  Run ``python texParser.py main.tex``. Resolve any parsing errors in the TeX file. 
*  Cross your fingers and run ``./makeQuiz.sh main.tex``

### Understanding and working with LaTeX-gloves

It is important to know how LaTeX gloves operates so that the points of failure can be detected when something goes wrong.

The LaTeX-gloves pipeline can be simply thought of as **Parse TeX -> Convert to SVG -> Construct Quiz -> Upload**. 

*  ``texParser.py`` parses the input TeX file, collects the information of each question, and separates each question out into individual TeX files.
*  ``convert.sh`` converts each individual TeX file to a PDF file and then converts each PDF file to an SVG file. It uses LaTeX preamble
*  ``gloves.py`` uses the question data proved by ``texParser.py`` and the images provided by ``convert.sh`` to construct the quiz and upload it to Canvas. 

``makeQuiz.sh`` is simply a convenience script that strings these individual programs together.

### Potential points of failure

* ``texParser.py`` is written to fail gracefully and give hopefully enough information to you when there's a formatting error in the input TeX file. Sometimes the failure might be so wonky that texParser crashes all-together. In any case, this will happen when your input TeX file is ill-formatted.
* ``convert.sh`` will fail when there is an actual LaTeX syntax error in the individual question .texs. Make sure Overleaf says there are no syntax errors (the PDF in overleaf will often compile anyway). Additionally, if you started using a new package or custom command in the Overleaf document, make sure you also make the proper changes to the preamble in ``resources/``
