from __future__ import print_function
import httplib2
import os
import email
import base64
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient import errors

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
    
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials    
    

def ListMessagesWithLabels(service,user_id, label_ids=[]):
	try:
		response = service.users().messages().list(userId='me',labelIds=label_ids).execute()
		messages = []
		if 'messages' in response:
			messages.extend(response['messages'])
			i = 0
			while i < 10:
				identifier = (messages[i]["threadId"])
				GetMimeMessage(service, user_id, identifier)
				i+=1
				continue
		while 'nextPageToken' in response:
			page_token = response['nextPageToken']
			response = service.users().messages().list(userId='me',labelIds=label_ids,pageToken=page_token).execute()
			messages.extend(response['messages'])
			
	except errors.HttpError, error:
		print ('An error occurred:', error)

def GetMimeMessage(service, user_id, msg_id):
	try:
		message = service.users().messages().get(userId=user_id, id=msg_id,format='raw').execute()
		msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
		mime_msg = email.message_from_string(msg_str)
		print ("\n",mime_msg['Subject'], mime_msg['From'], mime_msg['Date'])	
	except errors.HttpError, error:
		print ('An error occurred.', error)
	

def main():		
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)
	list_labels = ListMessagesWithLabels(service,'me')

	
		

if __name__ == '__main__':
	main()