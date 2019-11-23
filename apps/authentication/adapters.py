from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class AccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        ctx = {
            "user": emailconfirmation.email_address.user,
            "base_url": settings.WEB_APP_BASE_URL,
            "key": emailconfirmation.key,
            "link": settings.WEB_APP_ROUTES["account_activation"].format(
                key=emailconfirmation.key
            ),
        }

        email_template = "account/email/email_confirmation_signup"

        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)

    def respond_email_verification_sent(self, request, user):
        """ We need to prevent the default behavior from allauth app."""
        pass
