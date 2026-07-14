# 📝 Buzl Review Assistant

A static site generator and desktop management tool that creates branded, location-specific Google Review landing pages for Buzl partner clients.

---

## 📁 Project Structure

```
.
├── index.html                    # Generic root landing page (QR scanner + code entry)
├── site-generator/
│   ├── template.html             # Master client page template
│   ├── vendors.json              # Client configuration registry
│   ├── generate.py               # Static site compiler
│   ├── gui_manager.py            # Tkinter desktop GUI manager
│   ├── server.py                 # Local SPA testing server
│   └── dist/                     # Compiled output (ready to deploy)
│       ├── index.html
│       ├── .htaccess
│       ├── 269/
│       ├── locn-dev-269/
│       ├── 409/
│       ├── locn-dev-409/
│       └── 67ac841e7afd41ccec826b52/
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.x** — No additional packages required. All scripts use standard library only.

---

## 🖥️ Desktop GUI Manager

Launch the graphical client manager to add, edit, enable/disable clients and trigger builds:

```bash
cd site-generator
python gui_manager.py
```

### Features:
| Feature | Description |
|---------|-------------|
| ➕ Add Client | Register a new partner client with all required details |
| ✏️ Edit Client | Update name, Place ID, GA ID, OG metadata for an existing client |
| 🔘 Enable / Disable | Toggle the `active` status to include or exclude from builds |
| 🖼️ Upload OG Image | Browse and upload a custom Open Graph share thumbnail per client |
| 🔨 Compile | Trigger `generate.py` to rebuild all active client pages into `dist/` |

---

## ⚙️ Compile Sites (Command Line)

Build all active client pages from `vendors.json` into the `dist/` folder:

```bash
cd site-generator
python generate.py
```

- Inactive clients (`"active": false`) are **skipped** automatically.
- The compiled `dist/` folder is deployment-ready for Apache/Nginx hosting.
- The `.htaccess` routing file is automatically copied into `dist/`.

---

## 🌐 Local Testing Server

Run a custom SPA-aware local server on **port 8546** that serves compiled pages and gracefully handles unknown paths:

```bash
cd site-generator
python server.py
```

Open in your browser:
- Root landing page: [http://localhost:8546/](http://localhost:8546/)
- Client page (e.g.): [http://localhost:8546/269/](http://localhost:8546/269/)

> Any unknown path (e.g. `/nonexistent-client/`) is automatically routed to `index.html` instead of showing a raw 404 error. The client-side JS then redirects the user back to the landing page.

---

## 📋 Adding a New Client

### Option A — GUI (Recommended)
1. Run `python gui_manager.py`
2. Click **"New Client"**
3. Fill in the form fields
4. Click **"Save"** then **"Compile"**

### Option B — Manually edit `vendors.json`

```json
{
  "locationId": "locn-dev-XXX",
  "shortId": "XXX",
  "locationName": "Your Business Name",
  "placeId": "ChIJ...",
  "googleAnalyticsId": "G-XXXXXXXXXX",
  "ogTitle": "Review Your Business on Google",
  "ogDescription": "Draft an honest Google review using our interactive assistant.",
  "ogImage": "https://yourdomain.com/assets/og-image-XXX.png",
  "active": true
}
```

Then run:
```bash
python generate.py
```

---

## 🔑 API Credentials

The API authorization header is stored as a Base64-encoded Basic Auth constant inside each HTML file:

```javascript
const BASIC_AUTH_HEADER = 'Basic <base64(username:password)>';
```

### ⚠️ Security Warning for Production
Never expose raw API credentials in client-side JavaScript on a public site.

**Recommended approach:** Use a **server-side proxy** (PHP, Nginx, or Cloudflare Worker) to inject the `Authorization` header before forwarding requests to the backend. See the [API Integration Guide](./API_INTEGRATION_GUIDE.md) for details.

---

## 🚢 Deployment

1. Compile the sites: `python generate.py`
2. Upload the contents of `site-generator/dist/` to your web server root.
3. Ensure the `.htaccess` file is present (Apache `mod_rewrite` must be enabled).
4. All client paths (e.g. `/269/`, `/locn-dev-269/`) will resolve correctly.

---

## 🧪 Automated Verification

A Selenium-based test script is available to verify all compiled client pages load correctly:

```bash
pip install selenium
python verify_star_rating.py
```

Tests cover:
- ✅ Brand name rendering per client
- ✅ Dynamic question options loading from the API
- ✅ 404 routing fallback (invalid paths return `200` via SPA routing)

---

## 📄 License

Internal use only — Buzl Technologies.
