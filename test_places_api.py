import google.auth
from google.auth.transport.requests import Request
import requests

def test_places_api():
    # Get Application Default Credentials (assuming browser auth via gcloud auth application-default login)
    try:
        credentials, project_id = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
    except google.auth.exceptions.DefaultCredentialsError as e:
        print("Failed to load Application Default Credentials.")
        print(f"Error: {e}")
        print("Have you run `gcloud auth application-default login`?")
        return

    # Refresh credentials to get a valid access token
    credentials.refresh(Request())
    
    if not project_id:
        print("Warning: Project ID could not be determined automatically.")
        # You can manually set your project ID here if needed
        # project_id = "your-project-id"
        
    print(f"Using Project ID: {project_id}")

    # Prepare the request to the Places API (New)
    url = "https://places.googleapis.com/v1/places:searchText"
    
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json",
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress"
    }
    
    if project_id:
        headers["X-Goog-User-Project"] = project_id
    
    data = {
        "textQuery": "Googleplex, Mountain View, CA"
    }
    
    print("Sending request to Google Places API (New)...")
    try:
        response = requests.post(url, headers=headers, json=data)
    except requests.exceptions.RequestException as e:
        print("Request failed to send.")
        print(f"Error: {e}")
        return
        
    if response.status_code == 200:
        print("Success!")
        print("Response data:")
        print(response.json())
    else:
        print(f"Failed with status code: {response.status_code}")
        print(f"Error response: {response.text}")

if __name__ == "__main__":
    test_places_api()
