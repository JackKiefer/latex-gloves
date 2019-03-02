import numpy as np
import pandas as pd
import sys
import re

def find(regex, tex, msg='Undefined'):
    matches = re.findall(regex, tex, re.DOTALL)
    if len(matches) == 0:
        print(tex)
        print("********")
        print("Parse error in above LaTeX block while locating: " + msg)
        exit(1)
    return matches

# Given the input file, grab question codes and corresponding LaTeX
def getCodesAndRawTex(infile):
    questionData = {}
    # Match all raw TeX between the question command and newpage command
    rawTex = find(r'\\question%(.*?)newpage', infile.read(), msg='questions')
    for questionTex in rawTex:
        # Find the filename in the TeX
        questionCode = re.search(r'(.*?).tex', questionTex).group(0)
        # Drop the '.tex' extension
        questionCode = questionCode[:-4]
        # Add to data dictionary
        questionData[questionCode] = {}
        questionData[questionCode]['raw_tex'] = questionTex
    return questionData

def getQuestionType(tex):
    stripped = tex.replace(' ','')
    return re.search(r'(?<=type:).*?(?=\s)', stripped).group(0)

def getRawSolutionsTex(tex):
    return find(r'begin\{solution\}(.*?)end\{solution\}', tex, msg='solution')[0]

def parseMatrixSolution(tex):
    # Regex to grab between \begin{array} and \end{array}
    rawMatrix = find(r'\\begin{array}{.*?}(.*?)\\end{array}', tex, msg='matrix solution')[0]
    # Berid newline characters
    rawMatrix = rawMatrix.replace('\n','')
    # Super rad (super ugly) double list comprehension
    return [np.matrix([[int(x) for x in row.split('&')] for row in rawMatrix.split('\\\\')])]
   

def parseMultipleChoiceSolution(tex):
    rawChoices = find(r'\\begin{choices}(.*?)\\end{choices}',tex, msg='multiple choice options')[0]
    choiceList = find('[C-c]hoice', rawChoices, msg='correct multiple choice response')
    correctNum = choiceList.index('Choice')
    return 'ABCDE'[correctNum]

def getEquation(tex):
    eq = re.findall(r'\$(.*?)\$', tex, re.DOTALL)
    return eq[0] if len(eq) > 0 else tex
 
def parseNumericSolutions(tex):
    eq = getEquation(tex)
    return [
            [ 
                float(values.replace('\n','').replace('\\','')) for values in answer.split('\pm')
            ]
            for answer in eq.split(',')
           ]

def getQuestionSolutions(tex, questionType):
    # First handle types without defined {solution} tags
    if questionType == 'essay':
       return []
    elif questionType == 'multiplechoice' or questionType == 'multiple_choice':
       return parseMultipleChoiceSolution(tex)

    solutionTex = getRawSolutionsTex(tex)

    if questionType == 'matrix':
        return parseMatrixSolution(solutionTex)
    elif questionType == 'numeric':
        return parseNumericSolutions(solutionTex)

def parseAttributes(questionData):
    for question in questionData.keys():
        tex = questionData[question]['raw_tex']
        questionType = getQuestionType(tex)
        questionData[question]['type'] = questionType
        questionData[question]['solutions'] = getQuestionSolutions(tex, questionType)
    return questionData

def getQuestionData(inFile):
    questionData = getCodesAndRawTex(inFile)
    questionData = parseAttributes(questionData)
    return questionData

def sanitizeSolution(code, questionData):
    qType = questionData[code]['type']
    tex   = questionData[code]['raw_tex']
    if qType == 'multiple_choice' or qType == 'multiplechoice':
        return tex.replace('CorrectChoice','choice')[:-1]
    else:
        ret = re.sub(r'\\begin{solution}.*?\\end{solution}', '', tex, flags=re.DOTALL)
        return ret[:-1]

def generateQuestionTex(code, questionData):
    questionTex = sanitizeSolution(code, questionData)
    preamble = open('resources/questionPreamble.tex').read()
    closure  = open('resources/latexClosure.tex').read()
    return preamble + '%' + questionTex + closure

def writeToTexFile(questionCode, tex):
    file = open('tex/' + questionCode + '.tex', 'w')
    file.write(tex)
    file.close()

def convert(inFile):
    questionData = getQuestionData(inFile)
    for questionCode in questionData.keys():
        tex = generateQuestionTex(questionCode, questionData)
        writeToTexFile(questionCode, tex)

def main():
    if len(sys.argv) <= 1:
        print('No input file specified')
        exit(1)
    else:
        inFile = open(str(sys.argv[1]),"r")
        convert(inFile)

if __name__ == '__main__':
    main()
