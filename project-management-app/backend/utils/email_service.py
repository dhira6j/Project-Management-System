from fastapi import BackgroundTasks

# In a real app, this would use SMTP or an email API client
def send_email_background(background_tasks: BackgroundTasks, subject: str, recipient: str, body: str):
    # This is a dummy function for now
    def _send_dummy_email():
        print(f"--- Sending Email (Simulation) ---")
        print(f"To: {recipient}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print(f"--- Email Sent (Simulation) ---")

    background_tasks.add_task(_send_dummy_email)

def send_welcome_email(background_tasks: BackgroundTasks, email_to: str, user_full_name: str):
    subject = "Welcome to Our Platform!"
    body = f"Hi {user_full_name}, Welcome aboard! We are excited to have you.\n\nThanks,\nThe Team"
    send_email_background(background_tasks, subject, email_to, body)
