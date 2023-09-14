from wechaty import Wechaty


class MyBot(Wechaty):
    async def on_message(self, msg):
        from_contact = msg.talker()
        text = msg.text()
        await from_contact.say('Echo: ' + text)


bot = MyBot()
bot.start()

if __name__ == '__main__':
    
