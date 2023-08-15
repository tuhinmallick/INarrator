from inarrator.email import Gmail, User

gmail = Gmail()
gmail.authenticate(credentials_path="credentials.json")
user = User([gmail])
user.authenticate()
emails = user.read_latest_emails(
    gmail_filters="from:(-noreply -no-reply) is:unread -category:social -category:promotions -unsubscribe",
    gmail_max_emails="15",
)
print(emails)
