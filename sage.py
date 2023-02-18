import discord
import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!gpt"):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt='Response to: "{}"'.format(message.content[5:]),
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        await message.channel.send(response.choices[0].text)

client.run(os.environ['DISCORD_BOT_TOKEN'])
