import os


def build_request(phone: str, message: str) -> dict:
    # Mantém o código internacional informado nos dados de origem.
    digits = ""
    for char in phone:
        if char.isdigit():
            digits += char

    token = os.environ.get("BOTMAKER_TOKEN")
    if token:
        token_display = "[TOKEN CONFIGURADO]"
    else:
        token_display = "[TOKEN DE EXEMPLO]"

    channel = os.environ.get("BOTMAKER_CHANNEL_ID")
    if not channel:
        channel = "CANAL_DE_EXEMPLO"

    return {
        "method": "POST",
        "url": "https://api.botmaker.com/v2.0/chats-actions/send-messages",
        "headers": {
            "Content-Type": "application/json",
            "access-token": token_display,
        },
        "body": {
            "chat": {
                "channelId": channel,
                "contactId": digits,
            },
            "messages": [{"text": message}],
        },
    }
