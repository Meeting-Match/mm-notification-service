from rest_framework.views import APIView
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from datetime import datetime, timedelta
import threading
import re

class EmailAPI(APIView):
    def get(self, request):
        subject = self.request.GET.get('subject')
        txt_ = self.request.GET.get('text')
        html_ = self.request.GET.get('html')
        recipient_list = self.request.GET.get('recipient_list')
        from_email = settings.EMAIL_HOST_USER

        if not subject or not recipient_list or (not txt_ and not html_):
            return Response(
                {'msg': 'Subject, recipient list, and either HTML or Text are required.'},
                status=400
            )
        if html_ and txt_:
            return Response(
                {'msg': 'You can either use HTML or Text, not both.'},
                status=400
            )

        # Parse the time from the body message if exists
        try:
            target_time = self.get_schedule_time(txt_ or html_)
        except ValueError as e:
            return Response({'msg': str(e)}, status=400)

        # Schedule the email
        delay_seconds = (target_time - datetime.now()).total_seconds()
        if delay_seconds > 0:
            threading.Timer(
                delay_seconds,
                self.send_email,
                args=(subject, txt_, html_, recipient_list.split(','), from_email)
            ).start()
            return Response(
                {'msg': f"Email scheduled to be sent at {target_time.strftime('%Y-%m-%d %H:%M:%S')}."},
                status=200
            )
        else:
            return Response({'msg': 'The specified time has already passed.'}, status=400)

    def send_email(self, subject, text, html, recipient_list, from_email):
        try:
            send_mail(
                subject,
                text,
                from_email,
                recipient_list,
                html_message=html,
                fail_silently=False,
            )
            print(f"Email sent successfully to {recipient_list}")
        except Exception as e:
            print(f"Error sending email: {e}")

    @staticmethod
    def parse_time_from_message(body_message):
        time_pattern = r"(\d{1,2}:\d{2}[APMapm]{2})"
        match = re.search(time_pattern, body_message)
        if match:
            time_str = match.group(1)
            return datetime.strptime(time_str, "%I:%M%p").time()
        else:
            raise ValueError("No valid time found in the message.")

    def get_schedule_time(self, body_message):
        meeting_time = self.parse_time_from_message(body_message)
        today = datetime.now().date()
        now = datetime.now()

        meeting_datetime = datetime.combine(today, meeting_time)

        # If the calculated time has already passed today, move to the next day
        if meeting_datetime <= now:
            meeting_datetime += timedelta(days=1)

        # Calculate 10 minutes before the scheduled time
        target_time = meeting_datetime - timedelta(minutes=10)
        return target_time

