import os
from typing import Optional

import httpx


NOTIFICATION_SERVICE_URL = os.getenv(
    "NOTIFICATION_SERVICE_URL",
    "http://localhost:8001"
)

NOTIFICATION_CALLBACK_URL = os.getenv(
    "NOTIFICATION_CALLBACK_URL",
    "http://host.docker.internal:9000/callback"
)


def send_email_notification(
    recipient: str,
    message: str
) -> Optional[dict]:
    """
    Send an EMAIL notification request to the existing
    Event-Driven Notification System.

    The notification service handles the actual
    asynchronous processing.
    """

    payload = {
        "eventType": ["EMAIL"],
        "payload": {
            "recipient": recipient,
            "message": message
        },
        "callbackUrl": NOTIFICATION_CALLBACK_URL
    }

    try:
        response = httpx.post(
            f"{NOTIFICATION_SERVICE_URL}/api/events",
            json=payload,
            timeout=5.0
        )

        response.raise_for_status()

        result = response.json()

        print(
            f"Notification accepted for {recipient}: "
            f"{result}"
        )

        return result

    except httpx.HTTPError as error:
        print(
            f"Notification service HTTP error: {error}"
        )
        return None

    except Exception as error:
        print(
            f"Unexpected notification error: {error}"
        )
        return None


def notify_note_created(
    recipient: str,
    creator_username: str,
    note_title: str
) -> Optional[dict]:

    message = (
        f"A new note titled '{note_title}' "
        f"was created by {creator_username}."
    )

    return send_email_notification(
        recipient=recipient,
        message=message
    )


def notify_comment_added(
    recipient: str,
    commenter_username: str,
    note_title: str
) -> Optional[dict]:

    message = (
        f"{commenter_username} added a new comment "
        f"to your note '{note_title}'."
    )

    return send_email_notification(
        recipient=recipient,
        message=message
    )


def notify_upvote_added(
    recipient: str,
    voter_username: str,
    note_title: str
) -> Optional[dict]:

    message = (
        f"{voter_username} upvoted your note "
        f"'{note_title}'."
    )

    return send_email_notification(
        recipient=recipient,
        message=message
    )