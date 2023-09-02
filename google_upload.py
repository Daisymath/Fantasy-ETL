#Upload files to Google Drive

#multiple files
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials

# Load the credentials from the JSON file
credentials = Credentials.from_authorized_user_file('client_id.json')

# Create a Google Drive API client
service = build('drive', 'v3', credentials=credentials)


# delete old files
# file ids are used to identify files in Google Drive
with open('file_ids.txt','r') as file:
    lines = [line.strip() for line in file]


def delete_file(service, file_id):
    try:
        service.files().delete(fileId=file_id).execute()
        print(f"File with ID {file_id} deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

for file_id in lines:
    delete_file(service, file_id)



# List of CSV files to upload
csv_files = [
    'adp_merged.csv',
    'proj_merged.csv',
    'ranking_merged.csv'
]

google_file_ids = []

for csv_file_path in csv_files:
    # Define the file metadata and media (content)
    file_metadata = {
        'name': csv_file_path,  # Extract the file name from the path
        'mimeType': 'application/vnd.ms-excel'  # Adjust the MIME type if needed
    }

    # Load CSV data into a file-like object
    csv_data = open(csv_file_path, 'rb')

    media = MediaIoBaseUpload(csv_data, mimetype='text/csv', resumable=True)

    # Upload the file
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    google_file_ids.append(file.get("id"))

    print(f'Uploaded {csv_file_path}. File ID: {file.get("id")}')


with open('file_ids.txt','w') as file:
    for file_id in google_file_ids:
	    file.write(file_id+"\n")


print('All files uploaded.')