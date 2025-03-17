import os
import requests
import csv

def authenticate_and_fetch_data():
    # Retrieve your EBRAINS API key from environment variables
    # (Ensure you have set EBRAINS_API_KEY in your environment)
    eb_api_key = os.environ.get("EBRAINS_API_KEY")
    if not eb_api_key:
        raise Exception("EBRAINS_API_KEY not set in environment variables.")
    
    # Set up request headers with your API key
    headers = {
        "Authorization": f"Bearer {eb_api_key}",
        "Content-Type": "application/json"
    }
    
    # Define the API endpoint for dementia-related clinical data
    # (Replace this URL with the correct endpoint from MIP)
    api_endpoint = "https://mip.ebrains.eu/api/datasets/dementia"
    
    # Send a GET request to the API
    response = requests.get(api_endpoint, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error fetching data:", response.status_code, response.text)
        return None

def save_data_as_csv(data, filename="dementia_data.csv"):
    # Check if data is valid and non-empty
    if not data:
        print("No data received.")
        return
    
    # Assuming the data is a list of dictionaries
    keys = data[0].keys() if isinstance(data, list) and data else []
    
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        dict_writer = csv.DictWriter(csvfile, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    
    print(f"Data saved successfully to {filename}")

if __name__ == "__main__":
    # Step 1: Authenticate and fetch data
    clinical_data = authenticate_and_fetch_data()
    
    # Step 2: Save the fetched data into a CSV file
    save_data_as_csv(clinical_data)
