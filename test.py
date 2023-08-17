from inarrator.email import Gmail, User

gmail = Gmail()
gmail.authenticate(credentials_path="credentials.json")
gmail2 = Gmail()
gmail2.authenticate(credentials_path="credentials.json")
gmail3 = Gmail()
gmail3.authenticate(credentials_path="credentials.json")
gmail4 = Gmail()
gmail4.authenticate(credentials_path="credentials.json")
gmail5 = Gmail()
gmail5.authenticate(credentials_path="credentials.json")
user = User([gmail,gmail2,gmail3,gmail4,gmail5])
user.authenticate()
emails = user.read_latest_emails(
    gmail_filters="from:(-noreply -no-reply) is:unread -category:social -category:promotions -unsubscribe",
    gmail_max_emails="15",
)
print(emails)
