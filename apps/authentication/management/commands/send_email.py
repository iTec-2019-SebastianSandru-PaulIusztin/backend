import logging

from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--message", type=str)
        parser.add_argument("--to", type=str, required=True)

    def handle(self, *args, **options):
        message = options.get("message", "Test email from Servicing API.")
        to_email = options.get("to")

        send_mail(
            "Test email",
            message,
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=False,
        )

        logger.info("Email sent")
