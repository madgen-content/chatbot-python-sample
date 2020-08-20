# MADGEN'S UPDATED simple chatbot
I took the rough implementation from [twitchdev](https://github.com/twitchdev/chatbot-python-sample), converted it to python 3, took out some unnecessary api requests, and made it easier to create more interesting commands.  

I'll continue to update this in the future. For now, there is no form of caching or rate limiting

## Setup
After you have cloned this repository, use pip or easy_install to install the IRC library.

```sh
$ pip install irc
```

you also need to do some pre-work before using this project.
1. Using your main account, log in to https://dev.twitch.tv and create an application with the category 'Chat Bot'. Give it an OAuth Redirect URL of http://localhost. Save it and copy the generated **client ID**
2. go to your twitch settings and enable multiple account creation (so you can reuse your email for the chatbot's account)
3. create a new chatbot account on twitch (using your channel email for convenience)
4. go to the [Twitch Chat OAuth Password Generator](http://twitchapps.com/tmi/) **while logged in as your chatbot account**. Copy the generated token **without the initial 'oauth:' prefix**.

## Usage
```sh
$ python chatbot.py <username> <client id> <token> <channel>
```
* Username - The username of the chatbot
* Client ID - Your registered application's Client ID to allow API calls by the bot
* Token - Your OAuth Token *without the 'oauth:' prefix
* Channel - the name of your 'main' channel (the one the bot will send chats to)

I recommend sticking this command in a bash file (first line should be `!#/bin/sh`) that you alter to be executable but not writable or readable for safety. 

## Next Steps
You can customize the `do_command` function in `chatbot.py`.
for every chat that is sent, this function will run if the chat begins with an exclamation point. In this function you have access to several pieces of information...
1. The 'cmd' is the first word after the exclamation point (space delimited)
2. the 'sender' is the username of who sent the message
3. the 'arg_toks' is a list of the rest of the words in the message after the command in order (space delimited)
4. the 'channel_name' is your channel name. 

you can add if-else statements inside of the try-except block and use whatever python code you want to fill in the 'msg' variable.  
once the block finishes, the 'msg' will be sent.  

take a look at the code for some examples.  

If your msg takes arguments, you can assume the user put in well-formed arguments (otherwise it'll error and the try-except block will take care of telling them for you)  

**If you want to see my more fleshed-out personal version of this improved bot, check out the madgen-bot branch!**