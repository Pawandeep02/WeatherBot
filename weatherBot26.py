# import the necessary libraries
import discord 
import requests

# set the OpenWeatherMap API key and Discord bot token
api_key = "c703795f4023a7a4a5d765a7c9bbbd5f"
token='MTA5NDAzMzc0NTcxNzI0NDAyNQ.G7NC8c.mJ4906g98P2YxyMOVtNggdkE5oJ0XXDnf6eLhA'

# create a new Discord client instance with default intents
client = discord.Client(intents=discord.Intents.default())

# event handler for when the bot is connected to the Discord server
@client.event
async def on_ready():
    print('Bot is active on the server')

# event handler for when a message is sent to the Discord channel
@client.event
async def on_message(message):
    # ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # check if the message starts with the weather command
    if message.content.startswith(('!weather-', '!w-')):
        # extract the city name from the message
        city = message.content.split('-', 1)[-1]
        try:
            # make a request to the OpenWeatherMap API for the weather data of the city
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}')
            data = response.json()

            # extract the relevant weather information from the API response
            temp = round(data['main']['temp'] - 273.15, 2)
            feels_like = round(data['main']['feels_like'] - 273.15, 2)
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            weather_desc = data['weather'][0]['description']
            city_name = data['name']
            country_code = data['sys']['country']

            # send a message to the Discord channel with the weather information
            await message.channel.send(f'Temperature in {city_name}{country_code} is {temp}°C.It feels like {feels_like}°C.Humidity is {humidity}%. Wind speed is {wind_speed} m/s. {weather_desc}.')
        except:
            # if the city is not found in the API, send an error message to the Discord channel
            await message.channel.send('City not found, please rewrite the city name')

    # if the message starts with the weather help command, send a help message to the Discord channel
    if message.content.startswith(('!weather?', '!w?')):
        await message.channel.send('To get the weather information of a city, type "!weather-" or "!w-" followed by the city name. For example, "!weather-tokyo" or "!w-Toronto"')

# start the Discord client with the bot token
client.run(token)