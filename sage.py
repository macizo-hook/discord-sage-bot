import os
import discord
import openai

openai.api_key = os.environ['OPENAI_API_KEY']

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Create a dictionary to store the context for each user; there are possibly better structures.
context = {}


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Get the context for the current user
    user_context = context.get(message.author.id, {})

    if message.content.startswith("!gpt"):
        prompt = 'Response to: "{}"'.format(message.content[5:]).strip()

    # If the user has a stored context, add it to the prompt
    if user_context:
        prompt += "\n\nContext: {}".format(user_context)

    try:
        # Send prompt to OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        # Store the response as the context for the next message
        if response.choices:
            context[message.author.id] = response.choices[0].text.strip()

        # Send the response to the Discord channel
        if context[message.author.id]:
            await message.channel.send(context[message.author.id])
        else:
            await message.channel.send("I'm sorry, I don't know how to respond to that.")

    except Exception as e:
        print("Error:", e)

client.run(os.environ['DISCORD_BOT_TOKEN'])
