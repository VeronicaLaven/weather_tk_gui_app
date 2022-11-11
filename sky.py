# #####
# resources:
# api: https://openweathermap.org
# icons: https://openweathermap.org/weather-conditions
# #####

from configparser import ConfigParser
import requests
from tkinter import *
from tkinter import messagebox

# get url from openweathermap.org API current weather call by City Name
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

# for security the api key is stored in the config.ini file so we will need extract values 
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

# create a function to get weather data from api, json
# https requests returns weather data as json response
def get_weather(city):
    req = requests.get(url.format(city, api_key))
    if req:
        json = req.json()
        # set variables to later create a tuple with weather data
        # extract data from json
        city = json['name']
        country = json['sys']['country']
        # UTC Date Time
        lon = json['coord']['lon']
        lat = json['coord']['lat']

        # convert K to C and C to F for Temps and meters per second to miles per hour for Wind Speed below
    
        # current temperature
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9/5 + 32
        # feels like (wind chill factor) temperature
        flike_kelvin = json['main']['feels_like']
        flike_celsius = flike_kelvin - 273.15
        flike_fahrenheit = (flike_kelvin - 273.15) * 9/5 + 32
        # weather icon changes depending on weather
        icon = json['weather'][0]['icon']
        # weather and description
        weather = json['weather'][0]['main']
        desc = json['weather'][0]['description']
        # wind speed in meters per second and miles per hour
        wind_speed = json['wind']['speed']
        wind_speed_mph = wind_speed * 2.23694
        
        # create tuple of weather report details to display
        report = (
            city, 
            country,
            lon,
            lat,
            temp_celsius, 
            temp_fahrenheit, 
            flike_celsius, 
            flike_fahrenheit, 
            icon, 
            weather, 
            desc, 
            wind_speed, 
            wind_speed_mph
            )

        return report


    else:
        return None

# print to test for city like London to make sure weather data for variables in above tuple are returned
# print (get_weather('London'))
 

# create a function to search for city
def search(event):
    city = city_text.get()
    weather = get_weather(city)
    if weather: 
        # location label = {city}, {country}
        location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])  # get [positions] from weather report tuple above
        lonlat_lbl['text'] = 'Longitude: {:.2f}°, Latitude: {:.2f}°'.format(weather[2], weather[3])
        image['bitmap'] = 'images/{}.png'.format(weather[8])
        # express temp 2 digits after decimal place
        # degree symbol on Mac is SHFT+OPTION+8
        temp_lbl['text'] = 'Current Temperature:  {:.2f}°C, {:.2f}°F'.format(weather[4], weather[5])
        feels_lbl['text'] = 'Feels Like: {:.2f}°C, {:.2f}°F'.format(weather[6], weather[7])
        weather_lbl['text'] = 'Weather: {}'.format(weather[9])
        desc_lbl['text'] = 'Description: {}'.format(weather[10])
        # wind speed meters per second and miles per hour
        wind_speed_lbl['text'] = 'Wind Speed: {} mps, {:.2f} mph'.format(weather[11], weather[12]) 
        
    else:
        messagebox.showerror('Error', 'The city term, {}, you entered does not exist'.format(city))


# create gui window
root = Tk()

# Create File Menu with Exit Menu Item to Exit app

menubar = Menu(root)
root.config(menu = menubar)
file_menu = Menu(menubar, tearoff = 0)
file_menu.add_command(label = 'Exit', command = root.destroy)
menubar.add_cascade(label = "File", menu = file_menu)

# Create a frame for city search box at top center of window
frame = LabelFrame(root, text = 'Enter City to Get Weather Report', padx = 10, pady = 10, bd = 0, fg = '#fff', bg = '#1F3B4D', labelanchor="n" )
frame.pack(padx = 40, pady = 40)

# Create app window and set size and background color
bg_color = '#add8e6'
root.title('Sky App')
root.geometry('500x510')
root.configure(background = bg_color)

# display weather report for searched city

# set the textvariable attribute to an instance of StringVar
city_text = StringVar()
# StringVar object in Entry widget
city_entry = Entry(frame, textvariable = city_text, bd = 0, relief = SUNKEN)
city_entry.pack(padx = 5, pady = 5)

search_btn = Button(frame, text = "Get Weather", width = 10, command = search, bd = 0, relief = SUNKEN, highlightthickness=0)
search_btn.pack(padx = 5, pady = 5)

lonlat_lbl = Label(root, text = "", font = ('regular', 14), bg = bg_color)
lonlat_lbl.pack()

location_lbl = Label(root, text = "", font = ('bold', 24), bg = bg_color)
location_lbl.pack()

image = Label(root, bitmap = '', bg = bg_color)
image.pack()

temp_lbl = Label(root, text = '', bg = bg_color, font = ('regular', 14))
temp_lbl.pack()

feels_lbl = Label(root, text = '', bg = bg_color, font = ('regular', 14))
feels_lbl.pack()

weather_lbl = Label(root, text = '', bg = bg_color, font = ('regular', 14))
weather_lbl.pack()

desc_lbl = Label(root, text = '', bg = bg_color, font = ('regular', 14))
desc_lbl.pack()


wind_speed_lbl = Label(root, text = '', bg = bg_color, font = ('regular', 14))
wind_speed_lbl.pack()

wind_speed_mph_lbl = Label(root, text = '', bg = bg_color, font = ('regular', 14))
wind_speed_mph_lbl.pack()

# bind Enter Key to search function so clicking Enter / Return key will exit the app
root.bind('<Return>', search)


root.mainloop()


