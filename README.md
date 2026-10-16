# CodeAlpha URL Shortener

A URL shortening application built with Python, Flask and SQLite as part of the CodeAlpha Backend Development Internship.

## Features

- Generate unique short codes for HTTP and HTTPS URLs.
- Store links persistently in SQLite.
- Redirect short links to their original URLs.
- Validate input and handle unknown short codes.
- Simple responsive interface with a copy-to-clipboard button.

## Architecture

The application uses three logical layers:

| Layer | File | Responsibility |
|---|---|---|
| Web | routes.py | HTTP requests, JSON responses and redirects |
| Service | service.py | URL validation and short-code generation |
| Data | repository.py | SQLite queries and persistence |

`app.py` connects the layers and starts the application.
`backend/models.py` defines the ShortLink data model.

## Run locally — Windows PowerShell

Requires Python and Git. Developed using Python 3.14.

```powershell
git clone https://github.com/WajeedAbid/CodeAlpha_URLShortener.git
cd CodeAlpha_URLShortener
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open http://127.0.0.1:5000 in your browser.

The SQLite database, `links.db`, is created automatically.
Stop the server with Ctrl+C.

## API

### POST /api/shorten

Send a JSON body:

```json
{
  "url": "https://www.kth.se/"
}
```

Returns HTTP 201 with `code`, `original_url` and `short_url`.

Invalid input returns HTTP 400.
Requests without a JSON content type return HTTP 415.

### GET /s/<code>

Redirects to the original URL with HTTP 302.
Unknown codes return HTTP 404.

## Manual verification

- Created a short link.
- Copied it to the clipboard.
- Opened it and reached the original website.
- Restarted the server and successfully reused the same short link.

## Local scope

The application currently runs locally. Generated links using
127.0.0.1 work on the computer running the server.
Public sharing requires deployment and a public address.