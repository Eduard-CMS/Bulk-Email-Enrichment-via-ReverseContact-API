import asyncio
import aiohttp
import pandas as pd
import json
from tempfile import NamedTemporaryFile
from tqdm import tqdm
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# API details
API_KEY = 'YOUR_API_KEY' #Grab it from https://app.reversecontact.com/api
API_URL = 'https://api.reversecontact.com/enrichment?email={}&apikey=' + API_KEY

# Function to call the ReverseContact API and get enriched data
async def enrich_reversecontact_email(email, session):
    try:
        async with session.get(API_URL.format(email)) as response:
            if response.status == 200:
                return email, await response.json()
            else:
                print(f"Error for {email}: {response.status}")
                return email, None
    except Exception as e:
        print(f"Exception for {email}: {e}")
        return email, None

# Function to process the CSV and save as a temporary JSON
async def process_csv_to_temp_json(input_csv):
    df = pd.read_csv(input_csv)
    tasks = []

    with tqdm(total=len(df), desc="Enriching Emails", unit="email") as pbar:
        async with aiohttp.ClientSession() as session:
            for email in df['email']:
                tasks.append(enrich_reversecontact_email(email, session))

            enriched_data = []
            for future in asyncio.as_completed(tasks):
                email, result = await future
                if result is not None:
                    enriched_data.append({
                        'email': email,
                        'api_data': result  # Store the entire API response for each email
                    })
                else:
                    enriched_data.append({
                        'email': email,
                        'api_data': None  # If the API call fails, store None
                    })
                pbar.update(1)  # Update progress bar after each email is processed

    # Save enriched data to a temporary JSON file
    temp_file = NamedTemporaryFile(delete=False, suffix=".json")
    with open(temp_file.name, 'w') as f:
        json.dump(enriched_data, f, indent=4)
    
    return temp_file.name  # Return the path of the temporary file

# Function to convert JSON to CSV with additional logging and 'Website' headers
def json_to_csv(json_file, original_file_name, input_csv):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Convert the nested API data to a flat structure
    flattened_data = []
    for entry in data:
        email = entry['email']
        api_data = entry['api_data'] or {}
        flattened_row = {'email': email}

        # Flattening the API data into a structured format, respecting the 'Website' headers

        # Person-related fields (with 'person.' prefix)
        person_data = api_data.get('person', {})
        if person_data is not None:
            flattened_row.update({
                'person.publicIdentifier': person_data.get('publicIdentifier'),
                'person.linkedInIdentifier': person_data.get('linkedInIdentifier'),
                'person.memberIdentifier': person_data.get('memberIdentifier'),
                'person.linkedInUrl': person_data.get('linkedInUrl'),
                'person.firstName': person_data.get('firstName'),
                'person.lastName': person_data.get('lastName'),
                'person.headline': person_data.get('headline'),
                'person.location': person_data.get('location'),
                'person.summary': person_data.get('summary'),
                'person.photoUrl': person_data.get('photoUrl'),
                'person.backgroundUrl': person_data.get('backgroundUrl'),
                'person.openToWork': person_data.get('openToWork'),
                'person.premium': person_data.get('premium'),
                'person.pronoun': person_data.get('pronoun'),
                'person.showVerificationBadge': person_data.get('showVerificationBadge'),
                'person.creationDate': person_data.get('creationDate'),
                'person.followerCount': person_data.get('followerCount'),
                'person.positions': person_data.get('positions'),
                'person.schools': person_data.get('schools'),
                'person.skills': person_data.get('skills'),
                'person.languages': person_data.get('languages'),
                'person.recommendations': person_data.get('recommendations'),
                'person.certifications': person_data.get('certifications'),
            })

        # Company-related fields (with 'company.' prefix)
        company_data = api_data.get('company', {})
        if company_data is not None:
            flattened_row.update({
                'company.linkedInId': company_data.get('linkedInId'),
                'company.name': company_data.get('name'),
                'company.universalName': company_data.get('universalName'),
                'company.linkedInUrl': company_data.get('linkedInUrl'),
                'company.employeeCount': company_data.get('employeeCount'),
                'company.followerCount': company_data.get('followerCount'),
                'company.employeeCountRange': company_data.get('employeeCountRange'),
                'company.websiteUrl': company_data.get('websiteUrl'),
                'company.tagline': company_data.get('tagline'),
                'company.description': company_data.get('description'),
                'company.industry': company_data.get('industry'),
                'company.phone': company_data.get('phone'),
                'company.specialities': company_data.get('specialities'),
                'company.headquarter': company_data.get('headquarter'),
                'company.logo': company_data.get('logo'),
                'company.fundingData': company_data.get('fundingData'),
            })

        flattened_data.append(flattened_row)

    # Convert flattened data into a DataFrame and write to CSV
    df = pd.DataFrame(flattened_data)

    # Debugging: Check the DataFrame before saving
    print(f"DataFrame:\n{df.head()}")  # Log the first few rows of the DataFrame to check

    # Output the CSV file with the name based on the original file name
    output_csv = f"{original_file_name}_results.csv"
    df.to_csv(output_csv, index=False)

# Main function to run the process
async def main():
    # Prompt user to upload the CSV file
    Tk().withdraw()
    input_csv = askopenfilename(title="Select your CSV file", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))

    # Extract the original file name for later use
    original_file_name = input_csv.split("/")[-1].split(".")[0]

    # Process the CSV to get enriched data in a temporary JSON file
    temp_json = await process_csv_to_temp_json(input_csv)

    # Convert the enriched data from JSON to CSV with the correct file naming
    json_to_csv(temp_json, original_file_name, input_csv)

    print(f"Enriched data saved to {original_file_name}_results.csv")

# Run the asynchronous main function
asyncio.run(main())
