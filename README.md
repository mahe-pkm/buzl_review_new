# 𝐁𝐮𝐳𝐥 𝐃𝐢𝐠𝐢𝐭𝐚𝐥 𝐒𝐨𝐥𝐮𝐭𝐢𝐨𝐧𝐬 — Google Review Assistant

A responsive, premium, and offline-first single-page web application designed to help customers draft review text for **𝐁𝐮𝐳𝐥 𝐃𝐢𝐠𝐢𝐭𝐚𝐥 𝐒𝐨𝐥𝐮𝐭𝐢𝐨𝐧𝐬** and seamlessly publish them on Google.

---

## 🚀 Key Features

*   **⚡ 2-Step Simplified Wizard**: Consolidated form that flows naturally from choosing a service and rating the experience (Step 1) to selecting qualities, writing styles, languages, and drafting comments (Step 2).
*   **🎙️ Real-Time Voice-to-Text Dictation**: 
    *   Transcribes speech word-by-word in real-time as the user speaks.
    *   Uses a synchronous focus trigger to guarantee that mobile virtual keyboards pop up immediately on tap.
    *   Provides high-visibility recording status with red pulsing glows (`.voice-active`) and dynamic instructions.
*   **📊 Review Quality & Length Meter**: Live word counter, reading duration estimator, and visual color-changing strength indicator (Too Short ➡️ Good Review ➡️ Superb!) to encourage helpful reviews.
*   **⭐ Staggered Star Rating Simulator**: Dynamic visual feedback box displaying vector stars with staggered animation delays, colored based on the rating selected.
*   **♿ Accessibility First (WCAG 2.1 AA Compliance)**:
    *   All cards and chips are focusable (`tabindex="0"`) and announced correctly (`role="button"`) by screen readers.
    *   Interactive items can be selected using keyboard inputs (**Space** / **Enter**).
    *   Distinct high-contrast focus rings (`:focus-visible`) highlight selections.
*   **📱 Mobile-First Responsive Design**: 
    *   Optimized layout grids for screen sizes down to `320px` (iPhone SE).
    *   Tap targets compliant with Fitts's Law ($>48\text{px}\times48\text{px}$).
    *   Header wraps and layouts adapt dynamically to tablet, viewport, and phone breakpoints.
*   **🛡️ Jitter-Free Validation Warnings**: Copy buttons remain active but prompt interactive validation warnings (flashing red outline and card-styled alerts) if required steps are incomplete, without causing adjacent layout displacement.
*   **🔌 Zero Dependencies & 100% Offline Capable**: Built entirely on client-side vanilla CSS and JavaScript for lightning-fast speeds and private, secure browser processing.

---

## 🛠️ Local Development & Setup

Since the app relies on the native **Web Speech API** for dictation, the browser restricts microphone access to secure contexts (HTTPS or `localhost`). 

### 1. Start a Local Server
Run a local HTTP server in the root of the directory.

**Using Python:**
```bash
python -m http.server 7894
```

**Using Node.js (via live-server or serve):**
```bash
npx serve -l 7894
```

### 2. Access the Application
Open your browser and navigate to:
*   [http://localhost:7894](http://localhost:7894)

---

## 📂 Project Structure

```
├── index.html       # Primary application entry point (v2.0 optimized code)
├── .gitignore       # Git file exclusions
├── README.md        # Project documentation
├── CHANGELOG.md     # Version history
└── Ver2/
    └── Google_review_v2.0.html # Backup archive code
```

---

## 🎨 Design System & Colors
*   **Primary Accent**: `#2563EB` (Cobalt Blue)
*   **Backgrounds**: `#F8FAFC` (Slate Tint) & `#FFFFFF`
*   **Success state**: `#16A34A` (Forest Green)
*   **Warning state**: `#DC2626` (Crimson)
