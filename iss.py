import json
import time
import turtle
import urllib.request

import geocoder


def fetch_astronaut_data(api_url):
    """
    Fetches information about astronauts on the ISS from the given API URL.
    Returns the parsed JSON result.
    """
    with urllib.request.urlopen(api_url) as response:
        return json.loads(response.read())


def write_astronaut_info_to_file(file_path, astronaut_data):
    """
    Writes information about astronauts on the ISS to a text file.
    """
    with open(file_path, "w") as file:
        file.write(
            f"There are currently {astronaut_data['number']} astronauts on the ISS:\n\n"
        )
        for person in astronaut_data["people"]:
            file.write(f"{person['name']} - on board\n")

        # Get user's current location and write to file
        user_location = geocoder.ip("me").latlng
        file.write(f"\nYour current lat / long is: {user_location}")


def setup_turtle_world_map():
    """
    Sets up the Turtle graphics world map.
    """
    screen = turtle.Screen()
    screen.title("ISS Loc Tracker..")
    screen.setup(1280, 720)
    screen.setworldcoordinates(-180, -90, 180, 90)

    # Load the world map image
    screen.bgpic("map.gif")
    screen.register_shape("iss.gif")

    iss_turtle = turtle.Turtle()
    iss_turtle.shape("iss.gif")
    iss_turtle.setheading(45)
    iss_turtle.penup()

    return screen, iss_turtle


def update_iss_position(api_url, iss_turtle):
    """
    Updates the ISS position on the Turtle graphics world map.
    """
    while True:
        # Load the current status of the ISS in real-time
        result = fetch_astronaut_data(api_url)

        # Extract the ISS location
        location = result["iss_position"]
        lat, lon = float(location["latitude"]), float(location["longitude"])

        # Output lon and lat to the terminal
        print(f"\nLatitude: {lat}\nLongitude: {lon}")

        # Update the ISS location on the map
        iss_turtle.goto(lon, lat)

        # Refresh every 5 seconds
        time.sleep(5)


if __name__ == "__main__":
    # Free API for astronaut information
    astronaut_api_url = "http://api.open-notify.org/astros.json"

    # File to store astronaut information
    astronaut_info_file = "iss.txt"

    # Fetch and write astronaut information to file
    astronaut_data = fetch_astronaut_data(astronaut_api_url)
    write_astronaut_info_to_file(astronaut_info_file, astronaut_data)

    # Set up Turtle world map
    screen, iss_turtle = setup_turtle_world_map()

    # Update ISS position on the map
    update_iss_position("http://api.open-notify.org/iss-now.json", iss_turtle)
