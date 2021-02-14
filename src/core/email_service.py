# -*- coding: utf-8 -*-


import sendgrid
from loguru import logger


def send_user_review(access_id: str):

    subject = "PyNote II Access Request Review"

    message_body = f'<html><p>Admin</p>\
        <p>A new user has requested access. \
        Please check the site and approve or reject access.</p>\
        <p>Access <a href="https://pynoteii.devsetgo.com/admin/approval/{access_id}">PyNote II</a>\
        to review.</p></html>'

    to_email: str = "admin@devsetgo.com"
    result = send_email(to_email=to_email, subject=subject, message_body=message_body)
    logger.info(result)
    return result


def send_user_reject(to_email: str):

    subject = "PyNote II Access Request Rejected"
    message_body = f"<html><p>Dear User,</p>\
        \
        <p>Your access request was reviewed and rejected. If you wish to ask for a review, please respond to this email and we will review your request.</p>\
        \
        </html>"

    to_email: str = to_email
    result = send_email(to_email=to_email, subject=subject, message_body=message_body)
    return result


def send_user_approved(to_email: str):

    subject = "PyNote II Access Request Approved"
    message_body = f'<html><p>Dear User,</p>\
        \
        <p>Your access request was reviewed and approved. You can now access the <a href="https://pynoteii.devsetgo.com/user/login">login page</a>. If you have any questions, please respond to this email.</p>\
        \
        </html>'

    to_email: str = to_email
    result = send_email(to_email=to_email, subject=subject, message_body=message_body)
    return result


def send_email(to_email: str, subject: str, message_body: str):
    sg = sendgrid.SendGridAPIClient(api_key="")
    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": to_email,
                    }
                ],
                "subject": subject,
            }
        ],
        "from": {"email": "admin@devsetgo.com"},
        "content": [{"type": "text/html", "value": message_body}],
    }

    response = sg.client.mail.send.post(request_body=data)

    logger.info("sendgrid response code: {response.status_code}")
    logger.info("sendgrid response body: {response.body}")
    logger.info("sendgrid response body: {response.headers}")

    result = response.headers["X-Message-Id"]
    logger.info("sendgrid response body: {response.headers}")
    return result


if __name__ == "__main__":

    to_email: str = "dannyryan602@gmail.com"
    subject: str = "This is a test of sending from my program"
    message_body: str = "Yo... check this out!"
    send_email(to_email, message_body)
