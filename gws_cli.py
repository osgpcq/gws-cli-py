#!/usr/bin/env python

from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import argparse
import os
from apiclient import discovery
from tabulate import tabulate

# oauth2client complains about not having logging, we need this
# set to critical to avoid nonsense debug messages
import logging
logging.basicConfig(level=logging.CRITICAL)

# Define scopes of the script
scopes = [
  'https://www.googleapis.com/auth/admin.directory.user.readonly',
]

# Parse script arguments
parser = argparse.ArgumentParser('Updates user signatures')
parser.add_argument(
  '-c', '--credentials-file',
  action='store',
  required=True,
  help='Location of the credentials file.'
)
parser.add_argument(
  '-au', '--admin-user',
  action='store',
  required=True,
  help='User with admin privileges that will be used to get domain info (read-only).'
)
parser.add_argument(
  '-v', '--verbose',
  action='store_true',
  default=False,
  help='Print actions taken.'
)

args = parser.parse_args()

if args.admin_user.__contains__(','):
    admin_users = args.admin_user.split(',')
else:
    admin_users = [args.admin_user]


table = []
for admin in admin_users:
  if (args.verbose):
    print('-----------------------------------------------------------------')
    print('>',admin.split('@')[1],'<')
  # Get the path where the script is being executed
  script_path = os.path.dirname(os.path.realpath(__file__))

  # Credentials with Service accounts  (https://gist.github.com/salrashid123/de891486b5b595f561cbcdcdcb2c7b4a)
  #credentials = ServiceAccountCredentials.from_p12_keyfile('adminapi@fabled-ray-104117.iam.gserviceaccount.com',
  #                                                         'project1-5fc7d442817b.p12',
  #                                                         scopes=scope)
  #credentials = credentials.create_delegated('admin@demoapp2.com')
  #http = httplib2.Http()
  #http_auth = credentials.authorize(http)

  # Credentials with client_secrets and login as domain admin
  #flow  = flow_from_clientsecrets('client_secret.json',
  #                                scope=scope,
  #                                redirect_uri='urn:ietf:wg:oauth:2.0:oob')
  #auth_uri = flow.step1_get_authorize_url()
  #print 'goto the following url ' +  auth_uri
  #code = raw_input('Enter token:')
  #credentials = flow.step2_exchange(code)
  #http = httplib2.Http()
  #http_auth = credentials.authorize(http)

  # Service accounts
  #  Load the credentials file
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
    script_path + '/' + args.credentials_file, scopes=scopes)
  #  Create the http client with the admin user
  delegated_credentials = credentials.create_delegated(admin)
  http_auth = delegated_credentials.authorize(Http())

  # Create service objects
  directory = discovery.build('admin', 'directory_v1', http=http_auth)

  # Loop through all users
  response = directory.users().list(customer='my_customer', maxResults=500, orderBy='email').execute()
  users = response.get('users', [])
  nextPageToken = response.get('nextPageToken', '')
  while nextPageToken:
    response = service.users().list(customer='my_customer', maxResults=500, orderBy='email', pageToken=nextPageToken).execute()
    nextPageToken = response.get('nextPageToken', '')
    users.extend(response.get('users', []))
  if not users:
    print('No users in the domain.')
  else:
    for user in users:
      if (args.verbose):
        print(user['primaryEmail'])
      # 'organizations': [{'title': 'Client Care Specialist', 'primary': True, 'customType': ''}],
      title=''
      if 'organizations' in user: 
        if 'title' in user['organizations'][0]:
          title=user['organizations'][0]['title']
      table.append([
        user['primaryEmail'],
        user['name']['fullName'],
        user['orgUnitPath'],
        user['suspended'],
        user['archived'],
        user['changePasswordAtNextLogin'],
        user['isEnrolledIn2Sv'],
        user['isEnforcedIn2Sv'],
        user['isAdmin'],
        user['isDelegatedAdmin'],
        user['agreedToTerms'],
        user['isMailboxSetup'],
        user['creationTime'],
        user['lastLoginTime'],
        #user['phones'][0]['value'],
        #user['customSchemas']['Extra_fields']['skypeid'],
        title,
      ])
tablefmt='rounded_outline' # 'simple': 'github', 'rounded_outline'
headers=['primaryEmail', 'name_fullName', 'orgUnitPath', 'suspended', 'archived', 'changePW_ANL', 'isEnrolledIn2Sv', 'isEnforcedIn2Sv', 'isAdmin', 'isDelegatedAdmin', 'agreedToTerms', 'isMailboxSetup', 'creationTime', 'lastLoginTime', 'organizations_0_title']
print(tabulate(table, headers=headers, tablefmt=tablefmt))
