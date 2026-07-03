import google.auth
from google.auth.transport.requests import Request
import requests

def search_cervecerias():
    # Get Application Default Credentials
    try:
        credentials, project_id = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
    except google.auth.exceptions.DefaultCredentialsError as e:
        print("Failed to load Application Default Credentials.")
        print(f"Error: {e}")
        return

    # Refresh credentials to get a valid access token
    credentials.refresh(Request())
    
    # Prepare the request to the Places API (New)
    url = "https://places.googleapis.com/v1/places:searchText"
    
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json",
        # Requesting display name, address, location, and rating details
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.rating,places.userRatingCount"
    }
    
    if project_id:
        headers["X-Goog-User-Project"] = project_id
    
    data = {
        "textQuery": "cervecerias en CDMX",
        "languageCode": "es", # Get results in Spanish
        "pageSize": 20 # Maximum number of results per page (max is 20)
    }
    
    print("Searching for cervecerias in CDMX...")
    try:
        response = requests.post(url, headers=headers, json=data)
    except requests.exceptions.RequestException as e:
        print("Request failed to send.")
        print(f"Error: {e}")
        return
        
    if response.status_code == 200:
        results = response.json()
        places = results.get('places', [])
        print(f"Found {len(places)} cervecerias:")
        
        for idx, place in enumerate(places, 1):
            name = place.get('displayName', {}).get('text', 'N/A')
            address = place.get('formattedAddress', 'N/A')
            location = place.get('location', {})
            lat = location.get('latitude', 'N/A')
            lng = location.get('longitude', 'N/A')
            rating = place.get('rating', 'N/A')
            ratings_count = place.get('userRatingCount', 'N/A')
            
            print(f"{idx}. {name}")
            print(f"   Address: {address}")
            print(f"   Location: {lat}, {lng}")
            print(f"   Rating: {rating} ({ratings_count} reviews)")
            print()
    else:
        print(f"Failed with status code: {response.status_code}")
        print(f"Error response: {response.text}")

if __name__ == "__main__":
    search_cervecerias()
