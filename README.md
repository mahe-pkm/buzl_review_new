# 𝐁𝐮𝐳𝐥 𝐃𝐢𝐠𝐢𝐭𝐚𝐥 𝐒𝐨𝐥𝐮𝐭𝐢𝐨𝐧𝐬 — Google Review Assistant

A responsive, premium, and dynamic single-page web application designed to help customers draft honest reviews for businesses and seamlessly publish them on Google. The app dynamically personalizes itself based on URL routing parameters.

---

## 🚀 Key Features

*   **🧬 Dynamic Location-Based Routing**: 
    *   Automatically parses `locationId` from pathnames (e.g. `/locn-dev-397`) and query strings (e.g. `?locationId=...`).
    *   Hides static template options in dynamic mode, keeping the focus entirely on fetched questions.
*   **📋 Dynamic Questionnaire (API 1 Integration)**:
    *   Fetches custom location questions dynamically via `GET /api/locations/{locationId}/reviewquestions` with Basic Auth.
    *   Updates branding headers, subheadings, and instructions dynamically based on the fetched location name.
    *   Updates the destination Google Review redirect link dynamically using the place ID returned by the API.
*   **🔄 AI Review Draft Generation (API 2 Integration)**:
    *   Posts user answers, style choices, and language parameters to the backend AI generation endpoint.
    *   Displays multiple review variants using a premium tabbed interface.
*   **🔌 Local Mock Testing Mode**:
    *   Automatically falls back to local JSON assets (`/API sample json/`) when running on `localhost` or if `?mock=true` is present, facilitating mock testing offline.
*   **🎙️ Real-Time Voice-to-Text Dictation**: 
    *   Transcribes speech word-by-word in real-time as the user speaks.
    *   Uses a synchronous focus trigger to guarantee that mobile virtual keyboards pop up immediately on tap.
    *   Provides high-visibility recording status with red pulsing glows (`.voice-active`) and dynamic instructions.
*   **📊 Review Quality & Length Meter**: Live word counter, reading duration estimator, and visual strength indicator (Too Short ➡️ Good Review ➡️ Superb!) to encourage helpful reviews.
*   **♿ Accessibility First (WCAG 2.1 AA Compliance)**:
    *   All cards and chips are focusable (`tabindex="0"`) and announced correctly (`role="button"`) by screen readers.
    *   Interactive items can be selected using keyboard inputs (**Space** / **Enter**).
    *   Distinct high-contrast focus rings (`:focus-visible`) highlight selections.
*   **📱 Mobile-First Responsive Design**: 
    *   Optimized layout grids for screen sizes down to `320px` (iPhone SE).
    *   Tap targets compliant with Fitts's Law ($>48\text{px}\times48\text{px}$).
    *   Header wraps and layouts adapt dynamically to tablet, viewport, and phone breakpoints.
*   **🛡️ Jitter-Free Validation Warnings**: Copy buttons remain active but prompt interactive validation warnings (flashing red outline and card-styled alerts) if required steps are incomplete, without causing adjacent layout displacement.

---

## 🛠️ Local Development & Testing

Microphone features require secure contexts (HTTPS or `localhost`).

### 1. Start a Local Server
Run the secure local python server in the root of the project to enable HTTPS (required for camera access and speech recognition) and Clean Path-based URLs:

```bash
python "scratch/run_secure_server.py"
```

*   **Welcome Portal**: `https://localhost:7894/`
*   **Direct Path URL**: `https://localhost:7894/locn-dev-397`
*   **Short Numeric Path URL**: `https://localhost:7894/397`
*   *Note*: Since it uses a self-signed certificate, proceed past the browser safety warning when prompted to establish a secure origin context.

Alternatively, you can run a standard HTTP server (note: camera access will be blocked on mobile):

**Using Python:**
```bash
python -m http.server 7894
```

---

## 📂 Project Structure

```
├── index.html                  # Main application entry point (1-step layout & rewriter client)
├── .htaccess                   # Apache rewrite rules enabling SPA path routing on Hostinger
├── .gitignore                  # Git file exclusions (Ver2/ excluded)
├── README.md                   # Project documentation
├── CHANGELOG.md                # Version history
├── API_INTEGRATION_GUIDE.md    # Technical requirements guide for backend API developers
├── scratch/                    # Internal folder for utility scripts
│   └── run_secure_server.py    # HTTPS local server with dynamic self-signed certs & SPA routing
└── API sample json/            # Folder containing local mock json/txt responses
    ├── reviewquestions-locn-dev-269.json
    └── reviewsgeneration.txt
```

---

## 🎨 Design System & Colors
*   **Primary Accent**: `#2563EB` (Cobalt Blue)
*   **Backgrounds**: `#F8FAFC` (Slate Tint) & `#FFFFFF`
*   **Success state**: `#16A34A` (Forest Green)
*   **Warning state**: `#DC2626` (Crimson)
