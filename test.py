from narrator.email import Gmail,User

gmail = Gmail()
user = User(gmail)
user.authenticate()
print(user.read_latest_emails())