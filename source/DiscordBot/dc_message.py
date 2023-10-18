from requests import post




def send_discord_message(message
                 , botname='Lego_GCT_Bot'
                 ,webhookurl = 'https://discord.com/api/webhooks/1163820232842956821/v2P4bWjkNpHETdGZgQufhRMg4lcXvNchpl6aIh4grd_NqSYQjECiZZ00DZ4vLn-4vHQ-'):
    data = {
        "content": message,
        "username": botname
    }

    post(webhookurl, data)

