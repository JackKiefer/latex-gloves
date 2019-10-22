############################
## DUMMY INPUT PARAMETERS ##
############################

# Folder path to place question images
FOLDER_PATH = '/test'
# URL of the quiz to create
QUIZ_URL = 'https://usu.instructure.com/courses/528497/quizzes/695468'

#################################
## GLOBAL CONSTANTS AND TABLES ##
#################################
import requests
import os
import pickle
import re
import sys
import numpy as np
import texParser as tp

def parseIDs():
    components = QUIZ_URL.split('/')
    return components[4], components[6]


courseID, quizID = parseIDs()


### For use when automatic uploading to Canvas 
### isn't working
folderID = '3129129'
maxQs = 100

baseURL = 'https://usu.instructure.com'

def readToken(filename):
    return open(filename,'r').read().strip()

token = readToken('resources/key.txt')
headers = {'Authorization' : 'Bearer ' + token,
	   'Content-Type'  : 'application/json' }

quizAPI_URL  = baseURL + '/api/v1/courses/' + courseID + '/quizzes/' + quizID
filesURL = baseURL + '/api/v1/courses/' + courseID + '/files'

questionData = {}
with open('questionData.pickle', 'rb') as handle:
    questionData = pickle.load(handle)

canvasQuestionType = {
        'multiple_choice' : 'multiple_choice_question',
        'essay' : 'essay_question',
        'numeric' : 'numerical_question',
        'fill_in_the_blank' : 'short_answer_question',
        'matrix' : 'fill_in_multiple_blanks_question'
        }

###############
## FUNCTIONS ##
###############

# Locate the internal canvas ID of an png file
def findID(questionCode):
    files = requests.get(baseURL + '/api/v1/folders/'+folderID+'/files?per_page=' + str(maxQs),headers=headers).json()
    for fileJson in files:
        if (questionCode + '.png') in fileJson.values():
            return str(fileJson['id'])
    raise Exception("File not located in specified Canvas folder: " + questionCode + ".png")
    exit(1)

# Return the public preview URL given a fileID
def getPublicUrl(fileID):
    r =  requests.get(baseURL + '/api/v1/files/' + fileID + '/public_url',headers=headers)
    r.raise_for_status()
    return r.json()['public_url']

def rowColCode(r, c):
    return 'row' + str(r) + 'col' + str(c)

def makeHTMLmatrix(rows, cols):
    html = ''
    for row in range(rows):
        for col in range(cols):
            html += '[' + rowColCode(row,col) + '] '
        html += '<br />'
    return html

def matrixBodyText(code):
    if questionData[code]['type'] != 'matrix':
        return ''

    matrix = questionData[code]['solution(s)']
    rows, cols = matrix.shape

    body = '<br />'
    body += 'Enter matrix below:'
    body = '<br />'
    body += makeHTMLmatrix(rows, cols)
    return body

# Generates body text with the embedded image of corresponding
# question code.
def getBodyText(questionCode):
    fileID  = questionData[questionCode]['fileID']
#    fileID = findID(questionCode)
    fileURL = 'https://usu.instructure.com/files/' + fileID
    publicURL = getPublicUrl(fileID)
    base = '<link rel=\"stylesheet\" href=\"'+publicURL+'\"><p><img src=\"'+fileURL+'/preview\" alt=\"'+questionCode+'\" width=\"800\" data-api-endpoint=\"https://usu.instructure.com/api/v1/courses/528497/files/'+fileID+'\" data-api-returntype=\"File\"></p><script src=\"https://instructure-uploads-2.s3.amazonaws.com/account_10090000000000015/attachments/64592351/canvas_global_app.js\"></script>'
    return base + matrixBodyText(questionCode)

# POST a given question and return status
def postQuestion(question):
    return requests.post(quizAPI_URL + '/questions', json=question, headers=headers)

# Create a group with name "Group n" and return its ID
def createGroup(n):
    group = {"quiz_groups" : [{
                "name" : 'Group ' + str(n),
                "pick_count" : 1,
                "question_points" : 1
            }]}
    return requests.post(quizAPI_URL + '/groups', json=group, headers=headers).json()['quiz_groups'][0]['id']

def makeMultipleChoiceAnswer(letter, correct):
    weight = 0
    if correct:
        weight = 100
    return {
            'answer_text' : letter,
            'answer_weight' : weight
            }

def getMultipleChoiceAnswers(code):
    correctAnswer = questionData[code]['solution(s)']
    A = makeMultipleChoiceAnswer('A', False)
    B = makeMultipleChoiceAnswer('B', False)
    C = makeMultipleChoiceAnswer('C', False)
    D = makeMultipleChoiceAnswer('D', False)
    E = makeMultipleChoiceAnswer('E', False)

    if   correctAnswer == 'A':
        A = makeMultipleChoiceAnswer('A', True)
    elif correctAnswer == 'B':
        B = makeMultipleChoiceAnswer('B', True)
    elif correctAnswer == 'C':
        C = makeMultipleChoiceAnswer('C', True)
    elif correctAnswer == 'D':
        D = makeMultipleChoiceAnswer('D', True)
    elif correctAnswer == 'E':
        E = makeMultipleChoiceAnswer('E', True)

    return [A,B,C,D,E]


def makeNumericAnswer(exactAnswer, margin):
    start = exactAnswer - margin
    end   = exactAnswer + margin
    return {
            'numerical_answer_type' : 'range_answer',
	    'answer_exact' : exactAnswer,
	    'answer_error_margin': margin,
 	    'answer_range_start': start,
 	    'answer_range_end': end
            }

def makeStringAnswer(text):
    return {
            'answer_text': text
            }

def hasMargin(s):
    return len(s) > 1

def getNumericAnswers(code):
    solutions = questionData[code]['solution(s)']

    answers = []
    for s in solutions:
        exact  = s[0]
        # Default to 0 margin if no margin specified
        margin = 0
        if hasMargin(s):
            margin = s[1]
        answers.append(makeNumericAnswer(exact, margin))

    return answers

def makeMatrixAnswer(matrix, row, col):
    return {
            'answer_text': matrix[row,col],
            'blank_id' : rowColCode(row,col)
           }

def getMatrixAnswers(code):
    answers = []

    matrix = questionData[code]['solution(s)']
    rows, cols = matrix.shape

    for row in range(rows):
        for col in range(cols):
            answers.append(makeMatrixAnswer(matrix, row, col))

    return answers


# Generate the list of answers given a question code
def getAnswers(code):
    # Nothing needed if essay question
    if questionData[code]['type'] == 'essay':
        return []

    # Process multiple choice type
    if questionData[code]['type'] == 'multiple_choice':
        return getMultipleChoiceAnswers(code) 

    elif questionData[code]['type'] == 'numeric':
        return getNumericAnswers(code)

    elif questionData[code]['type'] == 'matrix':
        return getMatrixAnswers(code)

    else:
        print('Bad question type for '+code+'!')
        exit(1)


def numericToString(n):
    if len(n) > 1:
        return str(n[0]) + '±' + str(n[1])
    else:
        return str(n[0])

def solutionString(code):
    qType = questionData[code]['type']
    if qType == 'matrix':
        return ' of shape ' + str(questionData[code]['solution(s)'].shape)
    elif qType == 'numeric':
        return '(s): ' + str([numericToString(n) for n in questionData[code]['solution(s)']])
    elif qType == 'multiple_choice':
        return ': ' + questionData[code]['solution(s)']

def printQuestionSuccess(code):
    qType = questionData[code]['type']
    if qType == 'essay':
        print('Created question of type \'essay\'')
    else:
        print('Created question of type \'' + qType + '\' with solution' + solutionString(code))

# Create a question object wit specified parameters
def makeQuestion(code='',num=0,groupID=0):
    q = {
        "question": {
              "question_name": 'Question ' + str(num),
              "question_text": getBodyText(code),
              "question_type": canvasQuestionType[questionData[code]['type']],
              "points_possible": 1,
              "quiz_group_id" : groupID,
              "answers" : getAnswers(code)
              }
    }
    printQuestionSuccess(code)
    return q

# Create a question object and post it
def genQuestion(code='',num=0,groupID=0):
    return postQuestion(makeQuestion(code=code,num=num,groupID=groupID))

# Upload a file and return the file ID
def uploadFile(filename):
    # Step 1: Ask canvas nicely to upload a file
    size = os.path.getsize('png/'+filename)
    data = { 'name' : filename,
             'size' : str(size),
             'content_type' : 'image/png',
             'parent_folder_path' : FOLDER_PATH }
    response = requests.post(filesURL, json=data, headers=headers)
    response.raise_for_status()
    response = response.json()

    # Step 2: Wrap up the file and gift it to canvas :)
    files = [(key, (None, val)) for key, val in response['upload_params'].items()] # Get all upload params
    file_content = open('png/'+filename, 'rb').read()
    files.append((u'file', file_content))
    response = requests.post(response['upload_url'], files=files)
    response.raise_for_status()
    return str(response.json()['id'])

def sameBase(code1, code2):
    return (code1[:-1] == code2[:-1]) and (not code1[-1].isdigit()) and (not code2[-1].isdigit())

# Place codes into appropriate groups based on their base.
# Relies on the codes being in sorted order.
def groupCodes():
    groups   = []
    groupNum = 0
    codes = list(questionData.keys())
    codes.sort()
    groups.append([codes[0]])
    for i in range(1,len(codes)):
        if sameBase(codes[i],codes[i-1]):
            groups[groupNum].append(codes[i])
        else:
            groups.append([codes[i]])
            groupNum += 1
    return groups


# Ensure that sufficient arguments have been supplied
def checkArgs():
    # If there are not three arguments
    if len(sys.argv) != 3:
        # Print a usage message and exit
        print('Usage: python gloves.py <FOLDER_PATH> <QUIZ_URL>,\n\
                Where <FOLDER_PATH> is the path to place images in and\n\
                <QUIZ_URL> is the URL of the Canvas quiz.')
        exit()
		 
############
## SCRIPT ##
############

def main():
    # Handle command-line arguments
    global FOLDER_PATH, QUIZ_URL
    checkArgs()
    FOLDER_PATH = sys.argv[1]
    QUIZ_URL    = sys.argv[2]

    # Group the codes together based on their naming schema
    groups = groupCodes()

    # Begin creating groups
    for i,group in enumerate(groups):
        n = i + 1
        if n == n:
            print('')
            print('Creating group %s...' % n)
            groupID = createGroup(n)

            for code in group:
                print('---- Uploading '+code+'.png...')
                questionData[code]['fileID'] = uploadFile(code + '.png')

                print('---- Creating question ' + code + '...')
                genQuestion(code=code, num=n, groupID=groupID)
                print('')

if __name__ == '__main__':
    main()
