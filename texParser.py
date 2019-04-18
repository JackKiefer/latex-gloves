import numpy as np
import pandas as pd
import pickle
import sys
import re

def niceFloatFormat(x):
    s = str('%.2f' % float(x))
    if s[-1] == '0':
        s = s[:-1]
    if s[-1] == '0':
        s = s[:-1]
    if s[-1] == '.':
        s = s[:-1]
    return s

# Perform a find-all regex on the provided TeX code,
# and throw an error with the provided message
# if the find-all fails to find a match.
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

# Parse question TeX to determine type
def getQuestionType(tex):
    stripped = tex.replace(' ','')
    return find(r'(?<=type:).*?(?=\s)', stripped, msg='question type')[0]

# Extract solution TeX from question TeX
def getRawSolutionsTex(tex):
    return find(r'begin\{solution\}(.*?)end\{solution\}', tex, msg='solution')[0]

# Turn a LaTeX matrix into a numpy matrix!
def parseMatrixSolution(tex):
    # Regex to grab between \begin{array} and \end{array}
    rawMatrix = find(r'\\begin{array}{.*?}(.*?)\\end{array}', tex, msg='matrix solution')[0]
    # Berid newline characters
    rawMatrix = rawMatrix.replace('\n','')
    # Super rad (super ugly) double list comprehension is all there is to it
    return np.matrix([[niceFloatFormat(x) for x in row.split('&')] for row in rawMatrix.split('\\\\')])
   

# Figure out the correct multiple choice solution from question TeX
def parseMultipleChoiceSolution(tex):
    rawChoices = find(r'\\begin{choices}(.*?)\\end{choices}',tex, msg='multiple choice options')[0]
    choiceList = find('[C-c]hoice', rawChoices, msg='correct multiple choice response')
    correctNum = choiceList.index('Choice')
    return 'ABCDE'[correctNum]

# Grab the TeX in an equation (unless there are no $s,
# in which case just return the original TeX)
def getEquation(tex):
    eq = re.findall(r'\$(.*?)\$', tex, re.DOTALL)
    return eq[0] if len(eq) > 0 else tex
 
# Fetch the list of numeric answers and their margins 
# from the given solution TeX
def parseNumericSolutions(tex):
    eq = getEquation(tex)
    return [
            [ 
                float(values.replace('\n','').replace('\\','')) for values in answer.split('\pm')
            ]
            for answer in eq.split(',')
           ]


# Check to see if we have a valid question type and throw an error if we don't.
# Add in a cheeky message if they forgot the underscore in 'multiple_choice'
def checkQuestionType(questionType, question):
    if questionType not in ['essay', 'multiple_choice', 'matrix', 'numeric']:
        # Add a helpful message for common errors
        helpfulMessage = ''
        if questionType == 'multiplechoice':
            helpfulMessage = '. Did you mean \"multiple_choice\"?'
        raise Exception(
                "Unsupported/bad question type \"" 
                + questionType + "\" for question " + question + helpfulMessage)
        # Die!
        exit(1)
 
# Parse the solution to a question according to its question type
def getQuestionSolutions(question, tex, questionType):
    # Make sure we have a valid question type
    checkQuestionType(questionType, question)
    # First handle types without defined {solution} tags
    if questionType == 'essay':
       return []
    elif questionType == 'multiple_choice':
       return parseMultipleChoiceSolution(tex)
    # Now, fetch the {solution} content for the other types
    solutionTex = getRawSolutionsTex(tex)
    if questionType == 'matrix':
        return parseMatrixSolution(solutionTex)
    elif questionType == 'numeric':
        return parseNumericSolutions(solutionTex)

# Parse all question attributes and the attributes to
# the questionData structure
def parseAttributes(questionData):
    for question in questionData.keys():
        tex = questionData[question]['raw_tex']
        questionType = getQuestionType(tex)
        questionData[question]['type'] = questionType
        questionData[question]['solution(s)'] = getQuestionSolutions(question, tex, questionType)
    return questionData

# Generate complete question data from a given input file
def getQuestionData(inFile):
    questionData = getCodesAndRawTex(inFile)
    questionData = parseAttributes(questionData)
    return questionData

# Delete the solution information from question TeX
# so that the solution doesn't render for students
def sanitizeSolution(code, questionData):
    qType = questionData[code]['type']
    tex   = questionData[code]['raw_tex']
    if qType == 'multiple_choice':
        return tex.replace('CorrectChoice','choice')[:-1]
    else:
        ret = re.sub(r'\\begin{solution}.*?\\end{solution}', '', tex, flags=re.DOTALL)
        return ret[:-1]

# Generate the complete TeX file content for a given question
def generateQuestionTex(code, questionData):
    questionTex = sanitizeSolution(code, questionData)
    preamble = open('resources/questionPreamble.tex').read()
    closure  = open('resources/latexClosure.tex').read()
    return preamble + '%' + questionTex + closure

# Write a TeX file to tex/ given a questionCode and the TeX to write
def writeToTexFile(questionCode, tex):
    file = open('tex/' + questionCode + '.tex', 'w')
    file.write(tex)
    file.close()

# Write out every question's TeX file given the question data
def makeQuestionTexFiles(questionData):
    for questionCode in questionData.keys():
        tex = generateQuestionTex(questionCode, questionData)
        writeToTexFile(questionCode, tex)

# Save the question data to disk for other scripts' usage
def pickleDump(questionData):
    with open('questionData.pickle', 'wb') as handle:
        pickle.dump(questionData, handle)


# Running the script will generate individual TeX files for
# each question in the input TeX file and write out the parsed
# question data to a pickle.
def main():
    if len(sys.argv) <= 1:
        print('No input file specified')
        exit(1)
    else:
        inFile = open(str(sys.argv[1]),"r")
        questionData = getQuestionData(inFile)
        makeQuestionTexFiles(questionData)
        pickleDump(questionData)
    print('Successfully parsed TeX file.')

if __name__ == '__main__':
    main()
