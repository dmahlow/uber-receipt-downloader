# Uber Receipt Downloader

## Purpose

This tool allows Uber users to bulk download their ride receipts as PDF files for a specified date range. It's particularly useful for expense reporting, accounting, or personal record-keeping purposes.

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

2. Install the required Python package:
   ```
   pip install requests
   ```

3. Set up your Uber session cookies as environment variables. You'll need to extract these from your browser after logging into your Uber account:
   ```
   export cookie_sid=your_sid_cookie_value
   export cookie_csid=your_csid_cookie_value
   ```

   Note: These cookies are sensitive information. Do not share them or commit them to version control.

## Setting Up Uber Session Cookies

To use this script, you need to provide your Uber session cookies. Here's how to obtain and set them:

### Obtaining the Cookies

1. Open your web browser (Chrome, Firefox, or Safari recommended).
2. Go to [https://riders.uber.com/](https://riders.uber.com/) and log in to your Uber account.
3. Once logged in, open your browser's Developer Tools:
   - Chrome/Firefox: Right-click anywhere on the page and select "Inspect", then go to the "Network" tab.
   - Safari: Enable the Develop menu in Preferences > Advanced, then select Develop > Show Web Inspector > Network.
4. With the Network tab open, refresh the page.
5. In the Network tab, filter for "riders.uber.com".
6. Click on any request to riders.uber.com and look for the "Cookie" header in the request headers.
7. In the Cookie header, find the values for `sid` and `csid`. They will look something like this:
   ```
   sid=AbCdEfGhIjKlMnOp1234567890; csid=1234567890-AbCdEfGhIjKlMnOp;
   ```

### Setting the Environment Variables

Once you have the cookie values, you need to set them as environment variables. Here's how to do it:

#### On Unix-based systems (macOS, Linux):

1. Open your terminal.
2. Set the environment variables using the export command:
   ```
   export cookie_sid=AbCdEfGhIjKlMnOp1234567890
   export cookie_csid=1234567890-AbCdEfGhIjKlMnOp
   ```
3. You can add these lines to your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`) to make them persistent across terminal sessions.

#### On Windows:

1. Open Command Prompt or PowerShell as an administrator.
2. Set the environment variables using the setx command:
   ```
   setx cookie_sid AbCdEfGhIjKlMnOp1234567890
   setx cookie_csid 1234567890-AbCdEfGhIjKlMnOp
   ```
3. Note that you'll need to restart your command prompt or PowerShell for the changes to take effect.

### Verifying the Environment Variables

To verify that the environment variables are set correctly:

- On Unix-based systems, use the echo command:
  ```
  echo $cookie_sid
  echo $cookie_csid
  ```
- On Windows, use the echo command in Command Prompt:
  ```
  echo %cookie_sid%
  echo %cookie_csid%
  ```
  Or in PowerShell:
  ```
  echo $env:cookie_sid
  echo $env:cookie_csid
  ```

Make sure these values match the cookies you obtained from your browser.

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

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](link-to-your-issues-page) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)