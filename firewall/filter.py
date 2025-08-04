import re



def filterBlackListWord(message,BlackListWord):
    for char in BlackListWord:
        if char.lower() in message.lower():
            message = re.sub(re.escape(char), "***", message, flags=re.IGNORECASE)
    return message

def filter(content,BlackListWord):
    content = content.replace("@everyone", "``@everyone``").replace('@here', '``@here``')
    content = filterBlackListWord(content, BlackListWord=BlackListWord)
    content = re.sub(r'(https?:\/\/)?(www\.)?(discord\.gg|discordapp\.com\/invite)\/[a-zA-Z0-9]+', '`[INVITE BLOCKED]`',content)
    content = re.sub(r'<@&(\d+)>', r'``<@&\1>``', content)
   #content = re.sub(r'<@!?(\d+)>', r'``<@\1>``', content)
    return content
