import requests


def get_route_distance(latitude1, longitude1, latitude2, longitude2):
    openrouteservicekey = "5b3ce3597851110001cf62484db44eb190ef411dbb198d3f503b379a"
    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={openrouteservicekey}&start={longitude1},{latitude1}&end={longitude2},{latitude2}"

    data = requests.get(url).json()

    distance = data["features"][0]["properties"]["summary"]["distance"]

    # print("La distanza su strada tra i due punti è", distance, "metri.")

    return distance
