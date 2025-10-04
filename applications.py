from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import requests
import datetime

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("API Key not found.")

client = genai.Client(api_key=api_key)


# --- Function to get weather of a city
def get_weather(city: str):
    """
    fetches current weather for a given city using API

    args:
    city(str): city name (eg: Dehradun)

    returns:
    dict: weather details in json format
    """

    try:
        api_key = "4e0faf50697f512a3a23bec2b4c6c96f"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        return{"error": str(e)}


# gemini code to use the function to get details of the city
def temperature_of_city(city):
    system_instructions = """
        You are given weather data in JSON format from the OpenWeather API.
        Your job is to convert it into a clear, human-friendly weather update.
        
        Guidelines:
        1. Always mention the city and country.
        2. Convert temperature from Kelvin to Celsius (°C), rounded to 1 decimal.
        3. Include: current temperature, feels-like temperature, main weather description,
           humidity, wind speed, and sunrise/sunset times (converted from UNIX timestamp).
        4. Use natural, conversational language.
        5. Based on the current conditions, suggest what the person should carry or wear.
           - If rain/clouds: suggest umbrella/raincoat.
           - If very hot (>30°C): suggest light cotton clothes, sunglasses, stay hydrated.
           - If cold (<15°C): suggest warm clothes, jacket.
           - If windy: suggest windbreaker, secure loose items.
           - If humid: suggest breathable clothes, water bottle.
        6. If any field is missing, gracefully ignore it.
        """
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = f"Generate a clear, friendly weather report with temperatures in degree celsius, humidity, wind, sunrise/sunset, for the {city} and practical suggestions on what to wear or carry",
        config = types.GenerateContentConfig(system_instruction = system_instructions , tools = [get_weather])
    )

    return(response.candidates[0].content.parts[0].text)


# function to get news of interests

def get_news(topic : str):
    """
    fetches latest news headlines from an api

    args:
    topic(str): topic to search news for (eg. technology, cricket, etc)
    """

    try:
        api_key = "21cb2f70ca16426f9638f82d43f03d7b"
        url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}&pageSize=5&sortBy=publishedAt"
        response = requests.get(url)
        return  response.json().get("articles", [])
    except requests.exceptions.RequestException as e:
        return{"error": str(e)}


# --- function to summarize the news
def news_summarizer(url):
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = f"Summarize the news from the {url}, dont add sentences like - from where the article is, in this article, etc. Just give clear and crisp summary"
    )

    return response.text


# --- function to get forecast of entire day for city and places to visit to smart plan day
def get_forecasted_weather(city : str):
    """
    LLM Tool:- fetches forecasted weather and tourist places to visit for a given city.

    args:
        city(str): city name (eg. delhi, dehradun)
    """

    try:

        grounding_tool = types.Tool(
            google_search= types.GoogleSearch()
        )

        current_date = datetime.date.today().strftime("%B %d, %Y")

        response = client.models.generate_content(
            model = "gemini-2.5-flash-lite",
            contents = f"""
            Provide the detailed weather forecast for {city} on {current_date}.
            Then also list the top recommended places to visit in {city} on the same date.
            Format the response clearly with headings: 'Weather Forecast:' and 'Places to visit:'.
            """,
            config = types.GenerateContentConfig(
                     tools = [grounding_tool]
            )
        )

        return response.text

    except Exception as e:
        return{"error:", str(e)}



# --- function to find local events
def find_local_events(city : str):
    """ 
    find local events for a given city using an api
    
    args:
    city(str): city name (eg. delhi, dehradun)
    """

    try:
        api_key = "a26c3e0f28d941ac797349ee948cb8f2372dce19069b1b1c1aced25cbb68f3cc"
        url = f"https://serpapi.com/search.json?engine=google_events&q=Events in {city}&api_key={api_key}"
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        return{"error:", str(e)}


# --- function for smart calling
def smart_plan(city):
    weather_and_places = get_forecasted_weather(city)
    events_data = find_local_events(city)

    #Extract and format events for the main prompt
    events_list = []
    for event in events_data['events_results']:
        # Create a clean string representation for each event
        title = event.get('title', 'No Title')
        date_time = event.get('date', {}).get('when', 'Date/Time Unknown')
        venue = event.get('address', ['Venue Unknown'])[0]
        link = event.get('link', '#')

        events_list.append(
            f"📅 {title}\n"
            f"⏰ {date_time}\n"
            f"📍 {venue}\n"
            f"🔗 - {link}"
        )
    formatted_events = "\n\n".join(events_list) if events_list else "No major events found for today."

    current_date = datetime.date.today().strftime("%B %d, %Y")

    prompt = f"""                    
            You are a smart travel and event planner assistant.
            Your job is to create personalized day itinerary for the user in a given {city} on **{current_date}**
            
            Use the following PRE-FETCHED data to build the plan. DO NOT call the tools again.
               
            --- PRE-FETCHED DATA ---
            
            {weather_and_places} 
            
            Events:
            {formatted_events}
            
            User's Available Time:
            9:00 AM - 9:00 PM

             --- INSTRUCTIONS ---
            
            1. Always use weather conditions to decide between indoor and outdoor activities.
            2. Organize the plan chronologically (Morning -> Afternoon -> Evening) with clear headings.
            3. Mix tourist attractions + events + leisure breaks so the day feels balanced.
            4. When recommending events, check if the event timings fit the user's availability (9:00 AM - 9:00 PM).
            5. Always include event links (🔗) when mentioning them.
            6. Suggest lunch/dinner breaks with general recommendations (local cuisine or malls).
            7. If multiple good options exist, present them as choices.
            8. Keep the tone friendly and actionable, like a local guide.
            9. The final output must be in a beautifully formatted itinerary style.
            """



    response = client.models.generate_content(
        model = "gemini-2.5-flash-lite",
        contents = prompt
    )

    return response.text
