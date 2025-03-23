# Uber Receipt Downloader

## Purpose

This tool allows Uber users to bulk download their ride receipts as PDF files for a specified date range, as Uber makes it very cumbersome and difficult to do so on their website. It's particularly useful for expense reporting, accounting, or personal record-keeping purposes.

## Features

- Download Uber ride receipts for a specified date range
- Handles pagination to retrieve all receipts within the date range
- Saves receipts as PDF files with informative filenames
- Gracefully handles cases where receipts are not available (e.g., cancelled rides)

## Prerequisites

- Python 3.7 or higher
- `requests` library

## Setup

1. Clone this repository or download the `uber-receipts.py` script.

2. Install the required Python packages:
   ```
   pip install requests python-dotenv
   ```

   Or with uv:
   ```
   uv add requests python-dotenv
   ```

3. Create a `.env` file in the same directory as the script based on the provided `.env.example`:
   ```
   cookie_sid=your_sid_cookie_value
   cookie_csid=your_csid_cookie_value
   cookie_jwt=your_jwt_session_value
   cookie_geoip=your_geoip_city_id_value
   ```

   Note: These cookies are sensitive information. Do not share them or commit the `.env` file to version control.

## Obtaining Uber Session Cookies

To use this script, you need to provide your Uber session cookies. Here's how to obtain them:

1. Open your web browser (Chrome, Firefox, or Safari recommended).
2. Go to [https://riders.uber.com/](https://riders.uber.com/) and log in to your Uber account.
3. Once logged in, open your browser's Developer Tools:
   - Chrome/Firefox: Right-click anywhere on the page and select "Inspect", then go to the "Network" tab.
   - Safari: Enable the Develop menu in Preferences > Advanced, then select Develop > Show Web Inspector > Network.
4. With the Network tab open, refresh the page.
5. In the Network tab, filter for "graphql" requests to riders.uber.com.
6. Click on any request and look for the "Cookie" header in the request headers.
7. In the Cookie header, find the values for the required cookies:
   - `sid` - The main session ID
   - `csid` - Client session ID
   - `jwt-session` - JSON Web Token session
   - `GEOIP_CITY_ID_COOKIE` - Geographic location ID

8. Copy these values to your `.env` file.

### Important Notes

- These cookies are sensitive information tied to your Uber account. Do not share them with others or expose them publicly.
- Cookies typically expire after some time. If you encounter authentication errors, you may need to repeat this process to obtain fresh cookies.
- Always ensure you're complying with Uber's terms of service when using these cookies and this script.


## Usage

Run the script from the command line with the following arguments:

```
python uber-receipts.py --outdir ./receipts --from YYYYMMDD --to YYYYMMDD
```

- `--outdir`: The directory where the PDF receipts will be saved (default is "receipts")
- `--from`: The start date for the receipt range in YYYYMMDD format
- `--to`: The end date for the receipt range in YYYYMMDD format

Example:
```
python uber-receipts.py --outdir ./my_receipts --from 20230101 --to 20231231
```

This will download all available receipts for rides taken between January 1, 2023, and December 31, 2023, and save them in the `./my_receipts` directory.

## Output

The script will create PDF files in the specified output directory. Each file will be named in the format:

```
MMM DD_trip_uuid.pdf
```

For example: `Jan 30_24f62836-ad8c-42a2-ac94-d964caf180ed.pdf`

## Notes

- The script includes delays between requests to avoid overwhelming Uber's servers. Please use responsibly.
- If a receipt is not available (e.g., for cancelled rides), the script will log a message and continue with the next receipt.
- Ensure your Uber session cookies are up to date. If you encounter authentication errors, try refreshing your cookies.

## Disclaimer

This tool is for personal use only. Please ensure you comply with Uber's terms of service and do not use this script in any way that violates their policies or your agreement with Uber.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/dmahlow/uber-receipt-downloader/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)
