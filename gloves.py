import requests

######################
## INPUT PARAMETERS ##
######################

# Quiz 2
quizID   = '695476'

# chapterQuizzes/ex2
folderID = '3129143'

# Math 2250 - Spring 2019 
courseID = '528497'

######################
## GLOBAL CONSTANTS ##
######################
baseURL = 'https://usu.instructure.com'
maxQs = 100

def readToken(filename):
    return open(filename,'r').read().strip()

token = readToken('key.txt')
headers = {'Authorization' : 'Bearer ' + token,
	   'Content-Type'  : 'application/json' }

quizURL = baseURL + '/api/v1/courses/' + courseID + '/quizzes/' + quizID

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
    # TODO Error handling
    return requests.get(baseURL + '/api/v1/files/' + fileID + '/public_url',headers=headers).json()['public_url']

# Generates body text with the embedded image of corresponding
# question code.
def getBodyText(questionCode):
    fileID  = findID(questionCode)
    if fileID == 'BAD':
        print('Error on ' + questionCode)
        exit(1)
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

# Create a question object wit specified parameters
def makeQuestion(code='',num=0,groupID=0,qtype='multiple_choice_question',margin=1.0,):
    return {
        "question": {
              "question_name": 'Question ' + str(num),
              "question_text": getBodyText(code),
              "question_type": "multiple_choice_question",
              "points_possible": 1,
              "quiz_group_id" : groupID,
              "answers" : []
              }
    }

# Create a question object and post it
def genQuestion(code='',num=0,groupID=0):
    return postQuestion(makeQuestion(code=code,num=num,groupID=groupID))

def uploadFile(filename):
    return requests.post(quizURL + '/files


############
## SCRIPT ##
############

groupID = createGroup(1)
genQuestion(code=questionCode, num=n, groupID=groupID)
    
