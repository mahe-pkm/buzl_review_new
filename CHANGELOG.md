# Changelog

All notable changes to the **Buzl Digital Solutions — Google Review Assistant** will be documented in this file.

---

## [2.0.0] - 2026-06-30

### Added
*   **🎙️ Real-Time Voice Typing (Speech-to-Text)**: Added Web Speech API dictation support that transcribes speech word-by-word in real-time. Added support for Tamil (`ta-IN`) and English (`en-US`) speech engines.
*   **📊 Review Quality Meter (Gamified UX)**: Added a dynamic dashboard reporting word count, estimated reading speed (seconds), and a color-changing progress bar (Too Short 🔴 ➡️ Good Review 🟡 ➡️ Superb! 🟢).
*   **⭐ Star Rating Preview Simulator**: Added a dynamic star preview widget on the final draft card. The stars fill dynamically (e.g. 5 stars for Excellent, 3 stars for Average) with fluid staggered transition animations.
*   **♿ WCAG 2.1 AA Keyboard Accessibility**: 
    *   Programmatically added `tabindex="0"` and `role="button"` on page load (`DOMContentLoaded`) for option cards and quality chips.
    *   Injected keydown event handlers mapping **Enter** and **Spacebar** keys to select options.
    *   Designed high-contrast, focus-visible outline indicators (`outline: 3px solid var(--primary)`).
*   **🛡️ Jitter-Free Interactive Warnings**: Pre-allocated transparent borders on `.confirm-wrap` to prevent visual elements from shifting when validation animations trigger.
*   **📱 Sticky Header Autoscroll Margin Fix**: Integrated native CSS `scroll-margin-top: 88px` on form-containers and inputs to provide breathing room and prevent sticky headers from covering titles during auto-scroll navigations.

### Changed
*   **⚡ Wizard Consolidation (3 Steps to 2)**: Reorganized the form structure. Step 1 now focuses on Service & Experience. Step 2 consolidates qualities, styles, languages, and drafting.
*   **⚙️ Default Selections**: Set default pre-selected states for Writing Style ("Simple") and Language ("English") in both Javascript state and HTML classes. Overhauled `restartAssistant()` to restore these defaults cleanly.
*   **💬 Responsive Writing Style Tooltips**: Styled premium bubble tooltips above info SVG icons, using flexible typography wrapping for narrow mobile devices.
*   **📱 Mobile Action Layouts**: Configured copy buttons and navigation buttons to stretch to full width (`100%`) under `768px` for comfortable finger-touch tapping.

---

## [1.0.0] - 2026-06-04

### Added
*   **✨ Initial Release**: Launch of the basic Google Review Assistant wizard. Includes support for service selection, experience rating, quality selection, copy buttons, and standard text generation templates.
