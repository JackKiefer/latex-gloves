import sys
import string
import os
import re
import pickle

# all of the preamble material goes in this list
latexPreamble=['\documentclass[convert={outext=.png},  class=exam, border=20pt, varwidth]{standalone}',
'\\usepackage{tikz, multicol, graphicx, etoolbox, enumerate, setspace, relsize}',
'\\usepackage{amsmath, amsfonts, amssymb, amsthm, epsfig, epstopdf, titling, url, esvect, array}',
'\\usepackage{mathrsfs, verbatim, xpatch}',
'\\usepackage[paperwidth=400pt, paperheight=600pt]{geometry}',
'\\usepackage{tikz-3dplot}',
'\\usepackage{pgfplots}',
'\\usepackage{xspace}',
'\\usepackage{comment}',
'\\usepackage{xspace}',
'\\usepackage{adjustbox}',
'\\usepgfplotslibrary{polar}',
'\\usetikzlibrary{shapes.geometric}',
'\\usetikzlibrary{arrows}',
'\\usetikzlibrary[topaths]',
'\\pgfplotsset{compat=1.15}',
'%==================================================================',
'\\newcommand{\\matlab}{\\textsc{Matlab}\\xspace}',
'\\newcommand{\\ds}{\\displaystyle}',
'\\newcommand{\\Z}{\\mathbb{Z}}',
'\\newcommand{\\arc}{\\rightarrow}',
'\\newcommand{\\R}{\\mathbb{R}}',
'\\newcommand{\\spn}{\\textrm{span}}',
'\\newcommand{\\rvec}{\\rule[.5ex]{1em}{0.4pt}}',
'\\begin{document}']
#'\\newcommand{\matlab}{\\textsc{Matlab}\\xspace}',
#'\\begin{document}']

# include all of the closing matter in this list
latexClosure=['\end{document}']

# create an empty list for the bulk of all the and 
latexCode = []

# Keep track of question data
questionData = {}

def convert(inFile):
    infile = open(inFile,"r")
    while infile:
      line = infile.readline()  
      line = line.strip()
      line = line + '\n'
      if '\\question%' in line:

        # Regex the question code 
        questionCode = re.search(r'\%(.*)\.', line).group(1)
        # Add to data dict
        questionData[questionCode] = {}

        outfn = './tex/' + questionCode + '.tex'
        outfile = open(outfn,"w")
        line = infile.readline()
        for k in range(0,len(latexPreamble)):
          outfile.write(latexPreamble[k])
          outfile.write('\n')
        flg = 0
        while not '\\newpage\n' in line:
          # Have a look at stripped lines
          stripped = line.replace(' ', '')

          if '%type:' in stripped:
            questionData[questionCode]['type'] = re.search(r'\:(.*)', stripped).group(1)

          if '%answer' in stripped:
            questionData[questionCode]['answer(s)'] = re.search(r'\:(.*)', stripped).group(1)
 
          if '%margin' in stripped:
            questionData[questionCode]['margin'] = re.search(r'\:(.*)', stripped).group(1)

          if '\\begin{choices}\n' == line:
            flg = 1
          if '\\begin{choices}\n' == line:
            line = '\\begin{enumerate}[A.]\n'
          if '\\end{choices}' in line:
            line = '\\end{enumerate}\n'
          if 'CorrectChoice' in line: 
            line = str.replace(line,'CorrectChoice', 'item')
          if '\\choice' in line:
            line = str.replace(line,'choice', 'item')
          if '\\begin{solution}' in line:
            line = str.replace(line,'\\begin{solution}', '\n\\begin{comment}')     
          if '\\end{solution}' in line:
            line = str.replace(line,'\\end{solution}', '\\end{comment}\n')     
          outfile.write(line)
          line = infile.readline()  
          line = line.strip()
          line = line + '\n'
          if '\\end{questions}' in line:
            flg = 1
            break
    #    if flg:
    #      outfile.write('\\end{enumerate}\n')
        outfile.write('\\end{document}\n')
        outfile.close()
      if '\\end{document}' in line:
        outfile.close()
        break
    print('Written TeX files to ./tex/')
      
      
      
if len(sys.argv) <= 1:
    print('No input file specified')
else:
    convert(str(sys.argv[1]))
 
with open('questionData.pickle', 'wb') as handle:
    pickle.dump(questionData, handle)
