from mailjet_rest import Client
from django.conf import settings
from django.template.loader import render_to_string

def send_mailjet_email(subject, client_email,employee_email, template_name, context):
    mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version='v3.1')

    html_content = render_to_string(template_name, context)

    data = {
        'Messages': [
            {
                "From": {
                    "Email": settings.DEFAULT_FROM_EMAIL,
                    "Name": "The Nail Lab PetqG"
                },
                "To": [
                    {
                        "Email": client_email,
                    },
                    {
                        "Email": employee_email,
                    }
                ],
                "Subject": subject,
                "HTMLPart": html_content,
            }
        ]
    }

    result = mailjet.send.create(data=data)

    print("STATUS:", result.status_code)
    print("RESPONSE:", result.json())

    return result.status_code == 200
