# DriveEase — Car Rental Management System

A simple, responsive classroom project built with **HTML5, CSS3, JavaScript, Python Flask and SQLite**.

## Pages
1. Home (`/`)
2. Cars (`/cars`)
3. Book a car (`/booking`)
4. About (`/about`)
5. Contact (`/contact`)
6. Booking confirmation (after a successful booking)
7. Demo admin list (`/admin`)

## Run on Windows
1. Install Python 3.10+.
2. Open PowerShell in this project folder.
3. Create and activate a virtual environment:
   ```powershell
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Start the server:
   ```powershell
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.

SQLite database `rental.db` is created automatically on first run. Bookings and contact messages are stored locally.

## Included HTML/CSS requirements
- Semantic HTML5 elements, navigation and at least five pages
- Booking/contact forms with text, email, telephone, date, time, number, select, radio, checkbox, textarea, search, range, color, URL and hidden controls
- Form attributes such as `required`, `placeholder`, `maxlength`, `pattern`, `min`, `max`, `readonly`, `disabled` and `autocomplete`
- Inline CSS (a small booking-form note), internal CSS (home-page hero badge), and external CSS (`static/style.css`)
- Element, class, ID, grouping, universal and pseudo-class selectors
- Flexbox, CSS Grid, box model, typography, colors, backgrounds and responsive media queries

## Important notes
- This is an educational demo, not a production booking platform.
- `/admin` has no login; do not expose it publicly.
- Prices are sample daily rates in INR. The estimate counts calendar rental days; taxes, deposits, availability conflicts and payment processing are not implemented.
- Vehicle photos are loaded from Unsplash, so an internet connection is needed for those photos. Replace image URLs with local files if offline use is required.
