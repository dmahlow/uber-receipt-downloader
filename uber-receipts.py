import argparse
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timedelta

import requests

UBER_API = "https://riders.uber.com"

QUERY_ACTIVITIES = """
query Activities($endTimeMs: Float, $limit: Int = 10, $nextPageToken: String, $startTimeMs: Float) {
  activities {
    past(
      endTimeMs: $endTimeMs
      limit: $limit
      nextPageToken: $nextPageToken
      orderTypes: [RIDES, TRAVEL]
      profileType: PERSONAL
      startTimeMs: $startTimeMs
    ) {
      activities {
        uuid
        subtitle
      }
      nextPageToken
    }
  }
}
"""

def uber_request(data: dict) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept": "*/*",
        "content-type": "application/json",
        "x-csrf-token": "x",
        "Origin": "https://riders.uber.com",
        "Cookie": f'sid={os.environ["cookie_sid"]}; csid={os.environ["cookie_csid"]}',
    }
    response = requests.post(f"{UBER_API}/graphql", headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def get_activities(next_page_token: str, start_time_ms: int, end_time_ms: int) -> dict:
    data = {
        "operationName": "Activities",
        "variables": {
            "limit": 10,
            "nextPageToken": next_page_token,
            "startTimeMs": start_time_ms,
            "endTimeMs": end_time_ms
        },
        "query": QUERY_ACTIVITIES,
    }
    return uber_request(data)

def download_receipt(trip_uuid: str, trip_date: str, outdir: Path) -> None:
    filename = outdir / f"{trip_date}_{trip_uuid}.pdf"
    try:
        response = requests.get(
            f"{UBER_API}/trips/{trip_uuid}/receipt?contentType=PDF",
            headers={"Cookie": f'sid={os.environ["cookie_sid"]}; csid={os.environ["cookie_csid"]}'}
        )
        response.raise_for_status()
        filename.write_bytes(response.content)
        print(f"Downloaded receipt: {filename}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"No receipt available for trip {trip_uuid} (possibly cancelled)")
        else:
            print(f"Error downloading receipt for trip {trip_uuid}: {e}")

def main(outdir: str, from_date: str, to_date: str) -> None:
    outdir_path = Path(outdir)
    outdir_path.mkdir(parents=True, exist_ok=True)

    start_date = datetime.strptime(from_date, "%Y%m%d")
    end_date = datetime.strptime(to_date, "%Y%m%d")
    print(f"Date range: {start_date.date()} to {end_date.date()}")

    current_month = start_date.replace(day=1)
    while current_month <= end_date:
        next_month = (current_month + timedelta(days=32)).replace(day=1)
        month_end = min(next_month - timedelta(days=1), end_date)

        start_time_ms = int(current_month.timestamp() * 1000)
        end_time_ms = int(month_end.timestamp() * 1000)
        print(f"Processing: {current_month.strftime('%B %Y')}")

        next_page_token = ""
        while True:
            activities_data = get_activities(next_page_token, start_time_ms, end_time_ms)
            past_activities = activities_data["data"]["activities"]["past"]["activities"]

            for activity in past_activities:
                trip_uuid = activity["uuid"]
                trip_date = activity["subtitle"].split(" • ")[0]
                download_receipt(trip_uuid, trip_date, outdir_path)
                time.sleep(1)

            next_page_token = activities_data["data"]["activities"]["past"]["nextPageToken"]
            if not next_page_token:
                break
            time.sleep(5)

        current_month = next_month

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Uber Receipt Downloader")
    parser.add_argument("--outdir", default="receipts", help="Output directory for receipts")
    parser.add_argument("--from", dest="from_date", required=True, help="Start date (YYYYMMDD)")
    parser.add_argument("--to", dest="to_date", required=True, help="End date (YYYYMMDD)")
    args = parser.parse_args()

    if not os.environ.get("cookie_sid") or not os.environ.get("cookie_csid"):
        print("Please set cookie_sid and cookie_csid environment variables.")
        sys.exit(1)

    main(args.outdir, args.from_date, args.to_date)