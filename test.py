from inarrator.email.email import OutLook, Gmail

outlook = OutLook()
gmail = Gmail()
outlook.authenticate(
    credentials_path="/home/mohtashimkhan/INarrator/outlook_credentials.json",
    authority_url="https://login.microsoftonline.com/consumers/",
    outlook_scope=[
        "User.Read",
        "Mail.ReadWrite",
        "Mail.ReadBasic.Shared",
        "Mail.ReadBasic",
        "Mail.Read.Shared",
        "Mail.Read",
    ],
)
gmail.authenticate(
    credentials_path="/home/mohtashimkhan/INarrator/gmail_credentials.json",
    gmail_scope=["https://www.googleapis.com/auth/gmail.readonly"],
)
print(
    gmail.get_latest_emails(
        gmail_filters="from:(-noreply -no-reply) is:unread -category:social -category:promotions -unsubscribe",
        gmail_max_emails="10",
    )
)
print(outlook.get_latest_emails(outlook_max_emails="10"))
