'''
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
'''

import sys
import irc.bot
import requests
import random

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # get useful channel info using the id
        url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
        headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.info = r

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)
        return
        

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)
        return

    def on_pubmsg(self, c, e):
        msg = e.arguments[0]
        sender = e.source.split('!')[0]
        # print message
        print((sender, msg))

        # If a chat message starts with an exclamation point, try to run it as a command
        if msg[:1] == '!':
            toks = e.arguments[0].split(' ')
            cmd = toks[0][1:]
            rest = toks[1:]
            print('Received command: ' + cmd)
            self.do_command(sender, cmd, rest)
        return
    
    def send(self, msg):
        self.connection.privmsg(self.channel, msg)
        return

    def do_command(self, sender, cmd, arg_toks):
        c = self.connection
        info = self.info
        channel_name = info['display_name']

        try:
            # Poll the API to get current game.
            if cmd == "roll":
                sides = int(arg_toks[0])
                roll = random.randint(1, sides)
                msg = f"{sender} you rolled a {roll} from a {sides}-sided die"

            # Poll the API the get the current status of the stream
            elif cmd == "title":
                msg = f'{channel_name} the channel title is currently "{info["status"]}"'
            
            # The command was not recognized
            else:
                msg = f"Did not recognize command: {cmd}"
        except:
            msg = f"{sender}, your {cmd} command was malformed"
        self.send(msg)
        return

def main():
    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <client id> <token> <channel>")
        sys.exit(1)

    username  = sys.argv[1]
    client_id = sys.argv[2]
    token     = sys.argv[3]
    channel   = sys.argv[4]

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()
    return

if __name__ == "__main__":
    main()