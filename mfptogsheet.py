import myfitnesspal
import browser_cookie3
import csv
import pandas as pd
import os.path
from datetime import date,timedelta, datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def mfp_to_csv():
    client = myfitnesspal.Client(browser_cookie3.chrome())
    end_date = date(date.today().year, 12, 31)
    end_date2 = date.today()
    start_date = date(date.today().year, 12, 10)
    delta = timedelta(days=1)
    mfp_date = []
    mfp_calories = []
    mfp_fats = []
    mfp_carbs = []
    mfp_protein = []
    mfp_weight = []

    current_date = start_date

    while current_date <= end_date2: #in the timespan of ten days ago until now
        mfp_time = client.get_date(current_date) #assigns variable for the command that gets all user macros for the specified timespan
        mfp_time_str = mfp_time.date.strftime("%m-%d-%Y")
        mfp_measurement = client.get_measurements(measurement= "Weight", lower_bound= current_date, upper_bound = current_date) #assigns variable for the command that gets all user weights for the specified timespan
        if current_date in mfp_measurement: #if the date is in the dict for weight
            mfp_weight.append(mfp_measurement.get(current_date,0)) #the 
        else:
            mfp_weight.append("NaN")
            
        mfp_date.append(mfp_time_str)
        mfp_calories.append(mfp_time.totals.get('calories',0))
        mfp_fats.append(mfp_time.totals.get('fat',0))   
        mfp_carbs.append(mfp_time.totals.get('carbohydrates',0))
        mfp_protein.append(mfp_time.totals.get('protein',0))
    
        current_date += delta
    
    data = {
        "Date": mfp_date,
        "Weight": mfp_weight,
        "Fats": mfp_fats,
        "Carbs": mfp_carbs,
        "Protein": mfp_protein,
        "Calories": mfp_calories,
        
    }
    
    with open('/Users/shreyasnatesan/Documents/python/mfp_csv.csv', 'r+', newline = '') as f:
        writer = csv.writer(f)
        reader = csv.reader(f)
        headers = ["Date", 'Calories', 'Carbohydrates', 'Fat', 'Protein']
        df = pd.DataFrame(data)
        df.to_csv("/Users/shreyasnatesan/Documents/python/mfp_csv.csv", index = False)

# Modify these scopes for read/write access
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    # The ID and range of the spreadsheet
    SPREADSHEET_ID = "1YcpbP-R90caUwBJyyj6ACdYR7p8bmep5tYu7sYSPcJs"
    RANGE_NAME = "Current Overall Protocol 2024!B276"  # Change this to the range where you want to write data

    def main():
        """Shows basic usage of the Sheets API.
        Writes values to a sample spreadsheet.
        """
        creds = None
        # Check for token.json file to store credentials
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If no valid credentials, initiate login flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "/Users/shreyasnatesan/Documents/python/credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for future runs
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            service = build("sheets", "v4", credentials=creds)

            values = df.values.tolist()
            # Prepare the values to be written (update with your values)

            # Create the body of the request
            body = {
                'values': values
            }

            # Use the spreadsheets.values.update method to write data
            result = service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption="USER_ENTERED",  # Use "RAW" for unparsed data
                body=body
            ).execute()

            print(f"{result.get('updatedCells')} cells updated.")

        except HttpError as err:
            print(err)

    if __name__ == "__main__":
        main()

        
mfp_to_csv()






