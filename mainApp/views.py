import re
from datetime import datetime, timedelta
import threading
from rest_framework.views import APIView
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from django.shortcuts import render#

def frontend(request):#
    return render(request, 'index.html')#

# Function to parse time from the message
def parse_time_from_message(body_message):
    time_pattern = r"(\d{1,2}:\d{2}[APMapm]{2})"  # Matches time like "12:00PM"
    match = re.search(time_pattern, body_message)
    if match:
        time_str = match.group(1)
        return datetime.strptime(time_str, "%I:%M%p").time()
    raise ValueError("No valid time found in the message.")

# Function to calculate the target time
def get_schedule_time(body_message):
    meeting_time = parse_time_from_message(body_message)
    today = datetime.now().date()
    meeting_datetime = datetime.combine(today, meeting_time)
    return meeting_datetime - timedelta(minutes=10)  # 10 minutes before

class EmailAPI(APIView):
    def get(self, request):
        subject = request.GET.get('subject')
        body_message = request.GET.get('text')  # Dynamic body message
        html_ = request.GET.get('html')
        recipient_list = request.GET.get('recipient_list')
        from_email = settings.EMAIL_HOST_USER

        if not all([subject, body_message, recipient_list]):
            return Response({'msg': 'Subject, body message, and recipient list are required.'}, status=400)

        try:
            # Calculate schedule time
            schedule_time = get_schedule_time(body_message)
            now = datetime.now()

            if schedule_time < now:
                return Response({'msg': 'The scheduled time has already passed.'}, status=400)

            # Schedule email sending
            delay_seconds = (schedule_time - now).total_seconds()

            def send_email_task():
                send_mail(
                    subject,
                    body_message,
                    from_email,
                    recipient_list.split(','),
                    html_message=html_,
                    fail_silently=False,
                )

            threading.Timer(delay_seconds, send_email_task).start()

            return Response({
                'msg': 'Email scheduled successfully.',
                'scheduled_time': schedule_time.strftime('%Y-%m-%d %I:%M:%S %p'),
            }, status=200)

        except ValueError as e:
            return Response({'msg': str(e)}, status=400)
        except Exception as e:
            return Response({'msg': f'An error occurred: {e}'}, status=500)

