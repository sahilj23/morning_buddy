import streamlit as st
import random
from applications import temperature_of_city, get_news, news_summarizer, get_forecasted_weather, smart_plan


# Page Configration

# Helper functions
def get_random_quote():
    quotes = [
        "The sun is a daily reminder that we too can rise again from the darkness, that we too can shine our own light.",
        "Write it on your heart that every day is the best day in the year.",
        "I get up every morning and it's going to be a great day. You never know when it's going to be over, so I refuse to have a bad day.",
        "Today's goals: coffee and kindness. Maybe two coffees, and then kindness.",
        "An early-morning walk is a blessing for the whole day.",
        "Morning is an important time of day because how you spend your morning can often tell you what kind of day you are going to have.",
        "Lose an hour in the morning, and you will spend all day looking for it.",
        "When you arise in the morning, think of what a precious privilege it is to be alive - to breathe, to think, to enjoy, to love."

    ]
    return random.choice(quotes)

def get_random_image():
    image_urls = [
        "https://images.unsplash.com/photo-1522075782449-e45a34f1ddfb?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1564485052755-3b56dde409e2?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://plus.unsplash.com/premium_photo-1669802766533-85e0624ff1bd?q=80&w=1940&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1503803548695-c2a7b4a5b875?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://plus.unsplash.com/premium_photo-1669612905191-48c67547f9a0?q=80&w=765&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1615463140607-5933e319f2ba?q=80&w=718&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1707118159195-ee037c02a394?q=80&w=1169&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1689020187528-d0ba5b347ce2?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    ]

    return random.choice(image_urls)

def home_page():
    """Displays the home page with a quote and image."""
    st.title("🌞 Your Morning Buddy")
    st.markdown("---")
    st.subheader("A thought for Your Day")
    st.info(f'"{get_random_quote()}"')
    st.image(get_random_image(), caption = "A beautiful morning to start your day", use_container_width = True)
    st.markdown("---")
    st.write("Use the sidebar on the left to get your daily updates!")

def weather_news_page():
    """Displays the page for getting weather and news by city"""
    st.header("Get weather of the city")
    city = st.text_input("Enter a city name")

    if st.button("Fetch Information"):
        if city:
            temperature_output = temperature_of_city(city)
            st.subheader(f"Weather Info : {temperature_output}")
            st.success("Weather fetched successfully")
        else:
            st.error("Please enter a city name")

def interest_news_page():
    """Displays the page for getting news by interest"""
    st.header("Get news by interest")
    interest = st.text_input("Enter your areas of interests (eg. Technology, Sports, Health)", "Technology")

    if st.button("Fetch News"):
        if interest:
            articles = get_news(interest)
            title = []
            url = []
            image_url = []
            for i in articles:
                title.append(i["title"])
                url.append(i["url"])
                image_url.append(i["urlToImage"])

            if not articles:
                st.error("No news found")

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.subheader(title[0])
                st.markdown("---")
                st.image(image_url[0])
                st.markdown("---")
                st.write("Read full article here", url[0])
                st.markdown("---")
                st.write(news_summarizer(url[0]))

            with col2:
                st.subheader(title[1])
                st.markdown("---")
                st.image(image_url[1])
                st.markdown("---")
                st.write("Read full article here", url[1])
                st.markdown("---")
                st.write(news_summarizer(url[1]))

            with col3:
                st.subheader(title[2])
                st.markdown("---")
                st.image(image_url[2])
                st.markdown("---")
                st.write("Read full article here", url[2])
                st.markdown("---")
                st.write(news_summarizer(url[2]))

            with col4:
                st.subheader(title[3])
                st.markdown("---")
                st.image(image_url[3])
                st.markdown("---")
                st.write("Read full article here", url[3])
                st.markdown("---")
                st.write(news_summarizer(url[3]))

            with col5:
                st.subheader(title[4])
                st.markdown("---")
                st.image(image_url[4])
                st.markdown("---")
                st.write("Read full article here", url[4])
                st.markdown("---")
                st.write(news_summarizer(url[4]))

        else:
            st.error("Please enter an area of interest")



def smart_planner():
    """Displays the page for viewing the days schedule"""
    st.header("Your Smart Planner Day")
    city = st.text_input("Enter a city name")
    if st.button("Let's Plan"):
        if city:
            smart_plans = smart_plan(city)
            st.subheader(smart_plans)
            st.success("Have a nice day")
        else:
            st.error("Please enter a city name")


# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
st.sidebar.markdown("---")
page_option = st.sidebar.radio("Choose a page:", ("Home", "Get Weather of your City", "News by Interest", "Smart Planner"))
st.sidebar.markdown("---")

# --- Page Routing ---
if page_option == "Home":
    home_page()
elif page_option == "Get Weather of your City":
    weather_news_page()
elif page_option == "News by Interest":
    interest_news_page()
elif page_option == "Smart Planner":
    smart_planner()