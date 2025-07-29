import re

BlackListWord = [
    "porn", "sex", "nude", "boobs", "pussy", "ass", "fuck", "bitch", "dick", "cock",
    "hentai", "xxx", "milf", "anal", "blowjob", "fap", "naked", "cum", "nsfw", "deepfake",
    "scam", "phishing", "grabify", "iplogger", "malware", "trojan", "virus", "rat", "keylogger",
    "discord.gg", "invite", "dm me", "free nitro", "steam gift", "robux", "nitro generator",
    "click here", "giveaway", "win", "bitcoin", "crypto", "cheap", "promotion", "limited offer",
    "earn money", "onlyfans", "telegram", "telegram group", "snapchat", "whatsapp", "adult",
    "suck", "rape", "slut", "horny", "s3x", "seggs", "breast", "kys", "kill yourself"
]

def filterBlackListWord(message):
    for char in BlackListWord:
        if char.lower() in message.lower():
            message = re.sub(re.escape(char), "***", message, flags=re.IGNORECASE)
    return message

def filter(content):
    content = content.replace("@everyone", "``@everyone``").replace('@here', '``@here``')
    content = filterBlackListWord(content)
    content = re.sub(r'(https?:\/\/)?(www\.)?(discord\.gg|discordapp\.com\/invite)\/[a-zA-Z0-9]+', '`[INVITE BLOCKED]`',content)
    content = re.sub(r'<@&(\d+)>', r'``<@&\1>``', content)
    content = re.sub(r'<@!?(\d+)>', r'``<@\1>``', content)
    return content
