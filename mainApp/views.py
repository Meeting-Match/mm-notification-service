from rest_framework.views import APIView
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from datetime import datetime, timedelta
import threading
import logging

logger = logging.getLogger('notification')

def get_correlation_id(request):
    return getattr(request, 'correlation_id', 'N/A')


class EmailAPI(APIView):
    def post(self, request):
        """
        Schedule an email to be sent at a specified time.

        Expected request body:
        {
            "subject": "Email Subject",
            "body": "Email body content",
            "recipient_list": "recipient1@example.com,recipient2@example.com",
            "time": "2024-01-15 14:30",
            "html": "<p>Optional HTML content</p>" (optional)
        }
        """
        correlation_id = get_correlation_id(request)
        logger.info('Incoming POST request to schedule an email.', extra={'correlation_id': correlation_id})

        data = request.data

        # Extract data from the request body
        subject = data.get('subject')
        body = data.get('body')
        html = data.get('html')
        recipient_list = data.get('recipient_list')
        time_str = data.get('time')

        # Validate required fields
        if not all([subject, body, recipient_list, time_str]):
            logger.warning('Missing required fields in request.', extra={'correlation_id': correlation_id})
            return Response(
                {'msg': 'Subject, body, recipient list, and time are required.'},
                status=400
            )

        # Validate time
        try:
            target_time = self.parse_datetime(time_str)
        except ValueError as e:
            logger.error(f'Error parsing time: {e}', extra={'correlation_id': correlation_id})
            return Response({'msg': str(e)}, status=400)

        # Prepare email details
        from_email = settings.EMAIL_HOST_USER
        recipients = recipient_list.split(',')

        # Schedule the email
        delay_seconds = (target_time - datetime.now()).total_seconds()

        if delay_seconds > 0:
            logger.info(f"Scheduling email '{subject}' to {recipient_list} at {target_time}.", extra={'correlation_id': correlation_id})
            threading.Timer(
                delay_seconds,
                self.send_email,
                args=(subject, body, html, recipients, from_email, correlation_id)
            ).start()

            return Response(
                {'msg': f"Email scheduled to be sent at {
                    target_time.strftime('%Y-%m-%d %H:%M:%S')}."},
                status=200
            )
        else:
            logger.warning('Failed to schedule email: Target time already passed.', extra={'correlation_id': correlation_id})
            return Response({'msg': 'The specified time has already passed.'}, status=400)

    def send_email(self, subject, body, html, recipient_list, from_email, correlation_id):
        """
        Send an email with optional HTML content.

        Args:
            subject (str): Email subject
            body (str): Plain text email body
            html (str, optional): HTML version of the email
            recipient_list (list): List of recipient email addresses
            from_email (str): Sender's email address
        """
        try:
            logger.info(f"Sending email '{subject}' to {recipient_list}.", extra={'correlation_id': correlation_id})
            send_mail(
                subject,
                body,
                from_email,
                recipient_list,
                html_message=html,
                fail_silently=False,
            )
            logger.info(f'Email successfully sent to {recipient_list}.', extra={'correlation_id': correlation_id})
        except Exception as e:
            logger.error(f'Error sending email: {e}', extra={'correlation_id': correlation_id})

    @staticmethod
    def parse_datetime(time_str):
        """
        Parse a datetime string in the format 'YYYY-MM-DD HH:MM'.

        Args:
            time_str (str): Datetime string to parse

        Returns:
            datetime: Parsed datetime object

        Raises:
            ValueError: If the datetime string is invalid
        """
        try:
            # Parse the datetime string
            target_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")

            # Check if the time is in the future
            now = datetime.now()
            if target_time <= now:
                raise ValueError("The specified date and time have already passed.")
            return target_time
        except ValueError:
            raise ValueError("Invalid datetime format. Use 'YYYY-MM-DD HH:MM'.")
