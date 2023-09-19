# gws-cli-py

Google Workspace Python command-line interface.


Thist script is just to extract informations from Google Workspace email accounts.
User needs enough rights to parse the information.


## Usage
```
./gws-cli.py -c credentials.json -au user@domain.ext

╭─────────────────────┬───────────────┬───────────────┬─────────────┬────────────┬────────────────┬───────────────────┬───────────────────┬───────────┬────────────────────┬─────────────────┬──────────────────┬──────────────────────────┬──────────────────────────┬────────────────────────────╮
│ primaryEmail        │ name_fullName │ orgUnitPath   │ suspended   │ archived   │ changePW_ANL   │ isEnrolledIn2Sv   │ isEnforcedIn2Sv   │ isAdmin   │ isDelegatedAdmin   │ agreedToTerms   │ isMailboxSetup   │ creationTime             │ lastLoginTime            │ organizations_0_title      │
├─────────────────────┼───────────────┼───────────────┼─────────────┼────────────┼────────────────┼───────────────────┼───────────────────┼───────────┼────────────────────┼─────────────────┼──────────────────┼──────────────────────────┼──────────────────────────┼────────────────────────────┤
│ email01@domain.ext  │ User1 User01  │ /Company      │ False       │ False      │ False          │ True              │ True              │ False     │ True               │ True            │ True             │ 2021-08-19T15:16:08.000Z │ 2022-09-07T12:38:31.000Z │ COO                        │
│ email02@domain.ext  │ User2 User02  │ /Company      │ False       │ False      │ False          │ True              │ True              │ False     │ False              │ True            │ True             │ 2011-08-03T13:26:19.000Z │ 2023-09-05T09:20:16.000Z │ Account Manager            │
...

./gws-cli.py -c credentials.json -au user@domain.ext, user2@domain2.ext2
```
