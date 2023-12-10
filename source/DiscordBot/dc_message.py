from requests import post




def send_discord_message(message
                 , botname='Lego_GCT_Bot'
                 ,webhookurl = 'https://discord.com/api/webhooks/1163820232842956821/v2P4bWjkNpHETdGZgQufhRMg4lcXvNchpl6aIh4grd_NqSYQjECiZZ00DZ4vLn-4vHQ-'):
    """
    Diese Funktion dient dem senden einer Nachricht in einen angegebenen Discordchannel
    :param message: Die Nachricht, die versand werden soll
    :type message: string
    :param botname: Der Name des Discordbots, standard ist hinterlegt
    :type botname: string
    :param webhookurl: eine URL zu einem Weebhook eines Discordbots, standard ist hinterlegt
    :type webhookurl: string
    """

    data = {
        "content": message,
        "username": botname
    }

    post(webhookurl, data)

