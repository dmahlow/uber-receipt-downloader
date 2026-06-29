# Setup - Uber Receipt Downloader

Download Uber ride receipts by authenticating via browser and pulling cookies automatically.

## Steps

1. **Install dependencies** - Run `uv sync` to install Python dependencies.

2. **Open Uber login page** - Launch `~/go/bin/bdg` (browser automation) and navigate to `https://riders.uber.com/trips`. If a bdg session is already active, navigate the existing session with `~/go/bin/bdg dom eval "window.location.href = 'https://riders.uber.com/trips'"`.

3. **Wait for user to log in** - Take a screenshot with `~/go/bin/bdg dom screenshot` to check the page state. If it shows a login form, tell the user to log in and wait for them to confirm. Keep checking via screenshots until the trips page is visible.

4. **Extract cookies via CDP** - Once logged in, grab all cookies (including HttpOnly) using:
   ```
   ~/go/bin/bdg cdp Network.getCookies --params '{"urls": ["https://riders.uber.com"]}'
   ```
   Build a semicolon-separated cookie string from all returned cookies in the format `name=value; name2=value2`.

5. **Write .env file** - Write the cookie string to `.env` as `cookie_full=<cookie_string>`. If `.env` already exists, update only the `cookie_full` line.

6. **Ask user for date range** - Ask the user what date range they want to download receipts for. Suggest the current calendar year (Jan 1 to today) as default. Accept dates in any format and convert to YYYYMMDD for the script.

7. **Download receipts** - Run the download script:
   ```
   uv run python uber-receipts.py --from <YYYYMMDD> --to <YYYYMMDD> --outdir receipts_<YYYY>
   ```
   Run this in the background so it doesn't block. Monitor progress and report when done.

8. **Zip and open** - After download completes, zip the output folder:
   ```
   zip -j receipts_<YYYY>_<timestamp>.zip receipts_<YYYY>/*.pdf
   ```
   Then open the enclosing folder with `open .`.

## Notes

- The script at `uber-receipts.py` uses Uber's internal GraphQL API with browser session cookies for auth.
- Cookies expire periodically, so this setup flow needs to be repeated each time.
- Some trips (cancelled ones) will show "No receipt available" - this is normal.
- The `cookie_full` env var takes precedence over individual cookie vars (`cookie_sid`, `cookie_csid`, etc.).
