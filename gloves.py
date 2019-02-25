import requests
import os
import pickle

######################
## INPUT PARAMETERS ##
######################

# Quiz 2
quizID     = '695454'
folderPath = '/chapterQuizzes/ex3'


# Math 2250 - Spring 2019 
courseID = '528497'

folderID = '3129140'
maxQs = 100

#################################
## GLOBAL CONSTANTS AND TABLES ##
#################################

baseURL = 'https://usu.instructure.com'

def readToken(filename):
    return open(filename,'r').read().strip()

token = readToken('key.txt')
headers = {'Authorization' : 'Bearer ' + token,
	   'Content-Type'  : 'application/json' }

quizURL  = baseURL + '/api/v1/courses/' + courseID + '/quizzes/' + quizID
filesURL = baseURL + '/api/v1/courses/' + courseID + '/files'

questionData = {}
with open('questionData.pickle', 'rb') as handle:
    questionData = pickle.load(handle)

canvasQuestionType = {
        'multiple_choice' : 'multiple_choice_question',
        'essay' : 'essay_question',
        'numeric' : 'numerical_question',
        'fill_in_the_blank' : 'short_answer_question'
        }

###############
## FUNCTIONS ##
###############

# Locate the internal canvas ID of an SVG file
def findID(questionCode):
    files = requests.get(baseURL + '/api/v1/folders/'+folderID+'/files?per_page=' + str(maxQs),headers=headers).json()
    for fileJson in files:
        if (questionCode + '.svg') in fileJson.values():
            return str(fileJson['id'])
    return 'BAD'

# Return the public preview URL given a fileID
def getPublicUrl(fileID):
    r =  requests.get(baseURL + '/api/v1/files/' + fileID + '/public_url',headers=headers)
    r.raise_for_status()
    return r.json()['public_url']

# Generates body text with the embedded image of corresponding
# question code.
def getBodyText(questionCode):
#    fileID  = questionData[questionCode]['fileID']
    fileID = findID(questionCode)
    fileURL = 'https://usu.instructure.com/files/' + fileID
    publicURL = getPublicUrl(fileID)
    return '<link rel=\"stylesheet\" href=\"'+publicURL+'\"><p><img src=\"'+fileURL+'/preview\" alt=\"'+questionCode+'\" width=\"800\" data-api-endpoint=\"https://usu.instructure.com/api/v1/courses/528497/files/'+fileID+'\" data-api-returntype=\"File\"></p><script src=\"https://instructure-uploads-2.s3.amazonaws.com/account_10090000000000015/attachments/64592351/canvas_global_app.js\"></script>'

# POST a given question and return status
def postQuestion(question):
    return requests.post(quizURL + '/questions', json=question, headers=headers)

# Create a group with name "Group n" and return its ID
def createGroup(n):
    group = {"quiz_groups" : [{
                "name" : 'Group ' + str(n),
                "pick_count" : 1,
                "question_points" : 1
            }]}
    return requests.post(quizURL + '/groups', json=group, headers=headers).json()['quiz_groups'][0]['id']

def makeMultipleChoiceAnswer(letter, correct):
    weight = 0
    if correct:
        weight = 100
    return {
            'answer_text' : letter,
            'answer_weight' : weight
            }

def getMultipleChoiceAnswers(code):
    correctAnswer = questionData[code]['answer(s)']
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

def getNumericAnswers(code):
    # Split the answers 
    answerStrings = questionData[code]['answer(s)'].split(',')

    answers = []
    # Default to 0 margin if no margin specified
    margin = 0
    if 'margin' in questionData[code].keys():
        margin  = questionData[code]['margin']

    for a in answerStrings:
        answers.append(makeNumericAnswer(float(a), float(margin)))

    return answers

def getFillInTheBlankAnswers(code):
    # Split the answers 
    answerStrings = questionData[code]['answer(s)'].split(',')
    answers = []
    for a in answerStrings:
        answers.append(makeStringAnswer(a))

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

    elif questionData[code]['type'] == 'fill_in_the_blank':
        return getFillInTheBlankAnswers(code)

    else:
        print('Bad question type for '+code+'!')
        exit(1)


# Create a question object wit specified parameters
def makeQuestion(code='',num=0,groupID=0):
    return {
        "question": {
              "question_name": 'Question ' + str(num),
              "question_text": getBodyText(code),
              "question_type": canvasQuestionType[questionData[code]['type']],
              "points_possible": 1,
              "quiz_group_id" : groupID,
              "answers" : getAnswers(code)
              }
    }

# Create a question object and post it
def genQuestion(code='',num=0,groupID=0):
    return postQuestion(makeQuestion(code=code,num=num,groupID=groupID))

# Upload a file and return the file ID
def uploadFile(filename):
    # Step 1: Ask canvas nicely to upload a file

    size = os.path.getsize('svg/'+filename)
    data = { 'name' : filename,
             'size' : str(size),
             'content_type' : 'image/svg+xml',
             'parent_folder_path' : folderPath }
    r = requests.post(filesURL, json=data, headers=headers)
    r.raise_for_status()
    r = r.json()

    print(r)
    # Step 2: Wrap up the file and gift it to canvas :)
    gift = list(r['upload_params'].items())
    file_content = open('svg/'+filename, 'rb').read()
#    gift.append((u'file', '@svg/'+filename))
    r = requests.post(r['upload_url'], files=gift)
    r.raise_for_status()
    return str(r.json()['id'])

def sameBase(code1, code2):
    return code1[:-1] == code2[:-1]

# Place codes into appropriate groups based on their base.
# Relies on the codes being in sorted order.
def groupCodes():
    groups   = []
    groupNum = 0
    codes = list(questionData.keys())
    groups.append([codes[0]])
    for i in range(1,len(codes)):
        if sameBase(codes[i],codes[i-1]):
            groups[groupNum].append(codes[i])
        else:
            groups.append([codes[i]])
            groupNum += 1
    return groups
		 


############
## SCRIPT ##
############

groups = groupCodes()

for i,group in enumerate(groups):
    n = i + 1
    if n == n:
        print('')
        print('Creating group %s...' % n)
        groupID = createGroup(n)

        for code in group:
    #        print('---- Uploading '+code+'.svg...')
    #        questionData[code]['fileID'] = uploadFile(code + '.svg')

            print('---- Creating question ' + code + '...')
            genQuestion(code=code, num=n, groupID=groupID)
