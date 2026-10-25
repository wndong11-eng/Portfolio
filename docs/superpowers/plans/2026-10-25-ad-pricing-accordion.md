# Same-page advertising article implementation plan

Goal: Add the approved black-and-gold expandable article between services and contact on a feature branch only.
Architecture: Native details/summary with complete static HTML article; scoped responsive styles; in-page contents and contact anchors; bottom close button restores focus and scroll position.
Tech stack: Existing static HTML, CSS and JavaScript; Python stdlib Markdown conversion; Playwright browser verification.

Constraints: Preserve supplied article copy verbatim. No main updates, no deployment settings changes, no second generated image. Existing site sections remain unchanged. Backup main before edits.

- [x] Clone current GitHub main into isolated local checkout, create backup branch and local ZIP.
- [x] Add browser tests for collapsed initial state, keyboard expand, complete article visibility, same-page anchors, bottom close, mobile width, and no-JavaScript reading; run before implementation to see missing feature failure.
- [x] Copy original article into articles/ad-agency-pricing.md; convert trusted Markdown to escaped semantic static HTML; insert native details article and scoped CSS before contact.
- [x] Run desktop/mobile/JavaScript-disabled tests, capture screenshots and review; verify original content and unrelated sections preserved.
- [x] Commit feature branch, independently review diff, push and open draft PR. Confirm main still matches backup. User approved merging on 2026-10-26.
