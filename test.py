from inarrator.email import Gmail,User

gmail = Gmail()
gmail.authenticate(credentials_path="credentials.json")
user = User([gmail])
user.authenticate()
user.read_latest_emails()