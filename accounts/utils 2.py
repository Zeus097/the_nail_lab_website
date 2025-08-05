from django.conf import settings
from django.template.loader import render_to_string

from mailjet_rest import Client



def send_mailjet_email(subject, to_email, template_name, context):
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
                        "Email": to_email,
                        "Name": "Client"
                    }
                ],
                "Subject": subject,
                "HTMLPart": html_content,
            }
        ]
    }

    result = mailjet.send.create(data=data)
    return result.status_code == 200


