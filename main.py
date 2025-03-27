import requests
import gspread
from google.oauth2.service_account import Credentials

# Google Sheet API Setup
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file("SecretClient.json", scopes=scope)
client = gspread.authorize(creds)

# open the google sheet by name. "YTSheet" is my google sheet name
sheet = client.open("YTSheet").sheet1
# youtube api key
YOUTUBE_API_KEY = "enter youtube api key"


# API searches for youtube videos
def search_youtube_videos(query):
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&q={query}&part=snippet&type=video&maxResults=10"

    response = requests.get(url)
    # print("API respones", response.text)

    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
    else:
        print(f"Error fetching data from YouTube: {response.status_code}")
        return []

    videos = []
    for video in items:
        title = video["snippet"]["title"]
        published_at = video["snippet"]["publishedAt"]
        video_id = video["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append([title, published_at, video_id, video_url])

    return videos
    # print(f"{title:<55} {published_at:<25} {video_id:<20}")


def display_videos(videos):
    if not videos:
        print("No videos found.")
        return
    print("=" * 100)

    # for video in videos:
    #     print(f"{video[0]:<55} {video[1]:<25} {video[2]:<15} {video[3]}")


# upload data to Google Sheets
def upload_to_google_sheets(data):
    sheet.append_rows(data)
    print("data successfully uploaded to google sheet")


# update google sheet header manually
def ensure_headers():
    headers = ["Title", "Published At", "VideoId", "Video Link"]
    existing_data = sheet.get_all_values()
    if not existing_data:
        print("adding header row to google sheet")
        # if not sheet.get_all_values():
        sheet.append_row(headers)  # forcefully adding header
    else:
        print("updating header row in google sheets")
        sheet.update(
            range_name="A1:D1", values=[headers]
        )  # updates first row with correct headers


def main():
    query = input("Enter the name of the video to search: ")
    videos = search_youtube_videos(query)
    display_videos(videos)

    # Ensure headers are correct before uploading data
    ensure_headers()

    # upload data to google sheet
    if videos:
        upload_to_google_sheets(videos)


if __name__ == "__main__":
    main()
