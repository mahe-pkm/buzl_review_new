# Backend API Integration Requirements Guide

This document outlines the technical requirements, hosting models, and JSON payload specifications for backend developers to implement so that the Google Review Assistant frontend can transition from Mock Mode to your live APIs.

---

## 🔒 1. Hosting Models & Cross-Origin (CORS) Considerations

To accommodate both testing environments and production deployment, the frontend includes a dynamic base URL resolver:
```javascript
const API_CONFIG = {
  baseUrl: window.location.hostname.includes('gobuzl.com') ? '/api' : 'https://dev.web.gobuzl.com/api',
  ...
};
```

This supports two distinct hosting models:

### Model A: Same-Origin Deployment (Production — Recommended)
When you deploy the static HTML frontend files directly onto your main server (on any `gobuzl.com` domain/subdomain):
*   **API Path**: The frontend will automatically resolve requests to relative paths (e.g. `/api/locations/...`).
*   **CORS Gaps**: Since both the page and the API share the same domain name, the browser treats it as **Same-Origin**.
*   **Backend Requirement**: **No CORS headers are required on the backend API server in this model.**

### Model B: Cross-Origin Deployment (Temporary Testing)
When you host the frontend on an external domain (like the temporary testing server `buzl.rclk.in`) while keeping the API on `dev.web.gobuzl.com`:
*   **CORS Requirement**: The API server at `dev.web.gobuzl.com` **MUST** return CORS headers to prevent the browser from blocking requests:
    *   `Access-Control-Allow-Origin: https://buzl.rclk.in` (or `*` during development)
    *   `Access-Control-Allow-Headers: Content-Type, Authorization`
    *   `Access-Control-Allow-Methods: GET, POST, OPTIONS`
    *   *Note: Preflight `OPTIONS` requests must return a `200 OK` or `204 No Content` containing these headers.*

---

## 📋 2. API 1: Fetch Questions (`reviewquestions`)

*   **Method**: `GET`
*   **Endpoint (Production)**: `/api/locations/{locationId}/reviewquestions`
*   **Endpoint (Testing)**: `https://dev.web.gobuzl.com/api/locations/{locationId}/reviewquestions`
*   **Headers**:
    *   `Authorization: Basic <base64(locationId + ":")>`

### Expected JSON Response Structure
```json
{
    "resp": {
        "locId": "locn-dev-397",
        "placeId": "ChIJbfT9ntf1qjsRCjeaPBrgenM", 
        "scope": "location",
        "count": 1,
        "questions": [
            {
                "_id": "6a43e328e6de60db9817b7b7",
                "qid": "rvq-9b66a6d5-cd45-4598-a351-c0d486124176",
                "scope": "location",
                "locId": "locn-dev-397",
                "question": "How were the faculty?",
                "responseGuidance": {
                    "location": "Santhiya Chandran IAS Academy",
                    "keyword": "",
                    "aspect": "staff"
                },
                "suggestedResponses": [
                    "Excellent",
                    "Knowledgeable",
                    "Average",
                    "Disappointing"
                ]
            }
        ]
    }
}
```

### Critical Keys for Frontend:
1.  **`resp.placeId`** (or `googlePlaceId` / `reviewUrl`): The Google Place ID of the business. The frontend uses this to generate the Google Review redirect link dynamically. If missing, it defaults to Buzl.
2.  **`questions[0].responseGuidance.location`**: The business name. The frontend extracts this to update header logo text and instruction subheadings dynamically.

---

## 🔄 3. API 2: Review Generation (`reviewsgeneration`)

*   **Method**: `POST`
*   **Endpoint (Production)**: `/api/locations/{locationId}/reviewsgeneration`
*   **Endpoint (Testing)**: `https://dev.web.gobuzl.com/api/locations/{locationId}/reviewsgeneration`
*   **Headers**:
    *   `Content-Type: application/json`
    *   `Authorization: Basic <base64(locationId + ":")>`

### Expected JSON Request Payload
```json
{
    "language": "en", 
    "writingStyle": "Simple",
    "answers": [
        {
            "qid": "rvq-9b66a6d5-cd45-4598-a351-c0d486124176",
            "response": "Excellent"
        }
    ],
    "customDetail": "The teaching method was superb. Very helpful."
}
```
*Note on `language` mapping*:
*   "English" ➡️ `"en"`
*   "Tamil" ➡️ `"ta"`
*   "Tamil-English Mix" ➡️ `"ta-en"`

### Expected JSON Response Structure
```json
{
    "resp": {
        "status": "complete",
        "sessId": "rv_272889dfaa7e4c23",
        "language": "en",
        "variants": [
            {
                "index": 0,
                "text": "First AI-generated review draft based on the dynamic answers."
            },
            {
                "index": 1,
                "text": "Second alternative review draft based on the dynamic answers."
            }
        ]
    }
}
```

---

## 🛠️ 4. Local Testing & Mock Mode Toggle

The frontend contains a configuration toggle:
```javascript
const host = window.location.hostname;
if (host === 'localhost' || host === '127.0.0.1' || urlParams.get('mock') === 'true') {
  API_CONFIG.isLocalMock = true;
}
```
*   When `isLocalMock` is `true`, it bypasses network CORS and live basic auth entirely by reading local mock JSON files from the `/API sample json/` directory.
*   Once backend Basic Authentication and CORS are fixed on your dev servers, access the site normally (without `?mock=true`) to fetch from the live endpoints.

### 🔀 Path-Based Routing Implementation
To support clean path-based URLs (like `/locn-dev-397`) instead of traditional query parameters, we have implemented path-based routing:
1.  **Frontend Extraction**: The frontend automatically parses the `locationId` from the URL path segment using `window.location.pathname`.
2.  **Server Rewrites (.htaccess)**: We have added a `.htaccess` file in the root directory to handle internal rewrites on Apache/Hostinger. This forwards URLs like `/locn-dev-397` internally to `index.html` without triggering 404 errors.
    *   *Note: If your production backend uses Nginx or a Node.js server, make sure to configure a corresponding rewrite rule (SPA routing) so that all dynamic paths fall back to `index.html`.*

### 🧪 Example Testing URLs:
*   **Path-Based Route (Mock)**: `https://buzl.rclk.in/locn-dev-397?mock=true` (Extracts `locn-dev-397` from path, runs in Mock Mode)
*   **Query-Based Route (Mock)**: `https://buzl.rclk.in/?locationId=locn-dev-269&mock=true` (Extracts `locn-dev-269` from query param, runs in Mock Mode)
*   **Live Route (Production)**: `https://buzl.rclk.in/locn-dev-397` (Extracts `locn-dev-397` from path, runs live network call)
