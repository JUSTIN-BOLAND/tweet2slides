from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import sys
import datetime

SCOPES = "https://www.googleapis.com/auth/presentations"

store = file.Storage('credentials.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
    print('Fetched credentials.')
else:
    print('Got credentials')

service = build('slides', 'v1', http=creds.authorize(Http()))


def init():
    return service.presentations().create(body={'title': str(datetime.datetime.today())[:len('YYYY-MM-DD')]}).execute()


def new_slide(ppt, tweet, i=0):
    q = [
        {
            'createSlide': {
                'objectId': f'pageBoi_{i}',
                'slideLayoutReference': {
                    'predefinedLayout': 'SECTION_TITLE_AND_DESCRIPTION'
                },
                'placeholderIdMappings': [{
                    'layoutPlaceholder': {'type': 'TITLE', 'index': 0},
                    'objectId': f'titleBoi_{i}'
                }, {
                    'layoutPlaceholder': {'type': 'SUBTITLE', 'index': 0},
                    'objectId': f'engagementBoi_{i}'
                }, {
                    'layoutPlaceholder': {'type': 'BODY', 'index': 0},
                    'objectId': f'tweetBoi_{i}'
                }]
            }
        }, {
            'insertText': {
                'objectId': f'titleBoi_{i}',
                'text': tweet['time'].strftime('%A, %-I:%M %p')
            }
        }, {
            'insertText': {
                'objectId': f'tweetBoi_{i}',
                'text': tweet['text']
            }
        }, {
            'insertText': {
                'objectId': f'engagementBoi_{i}',
                'text': f'{tweet["retweets"]} retweets, {tweet["favorites"]} favorites'
            }
        }
    ]
    i += 1
    s = service.presentations().batchUpdate(presentationId=ppt.get(
        'presentationId'), body={'requests': q}).execute()
    return s.get('replies')[0].get('createSlide').get('objectId'), i

def new_slide_plus(ppt, tweet, i=0):
    q = [
        {
            'createSlide': {
                'objectId': f'pageBoi_{i}',
                'slideLayoutReference': {
                    'predefinedLayout': 'SECTION_TITLE_AND_DESCRIPTION'
                },
                'placeholderIdMappings': [{
                    'layoutPlaceholder': {'type': 'TITLE', 'index': 0},
                    'objectId': f'titleBoi_{i}'
                }, {
                    'layoutPlaceholder': {'type': 'SUBTITLE', 'index': 0},
                    'objectId': f'engagementBoi_{i}'
                }, {
                    'layoutPlaceholder': {'type': 'BODY', 'index': 0},
                    'objectId': f'tweetBoi_{i}'
                }]
            }
        }, {
            'insertText': {
                'objectId': f'titleBoi_{i}',
                'text': tweet['time'].strftime('%A, %-I:%M %p')
            }
        }, {
            'insertText': {
                'objectId': f'tweetBoi_{i}',
                'text': tweet['text']
            }
        }, {
            'insertText': {
                'objectId': f'engagementBoi_{i}',
                'text': f'{tweet["retweets"]} retweets, {tweet["favorites"]} favorites\n{tweet["replies"]} replies, {tweet["engagements"]} engagements\n{tweet["impressions"]} total impressions'
            }
        }
    ]
    i += 1
    s = service.presentations().batchUpdate(presentationId=ppt.get(
        'presentationId'), body={'requests': q}).execute()
    return s.get('replies')[0].get('createSlide').get('objectId'), i
