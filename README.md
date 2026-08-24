# Helpbot

In-site help search widget for ERPNext/Frappe. Employees can search internal
workflow instructions (that you type in) and get links to official ERPNext
docs (docs.erpnext.com), right inside the ERPNext site — via a floating
chat bubble on every page, and a full page at `/helpbot`.

## What this app does
- Adds a new DocType **Help Article** where you (or Nafi/Tamil) paste in:
  - Internal workflow steps (e.g. "How we raise a Sales Invoice at Syvasoft")
  - References to official ERPNext docs pages (title + link to docs.erpnext.com)
- Adds a floating "💬" chat bubble on every ERPNext screen. Employees type a
  question, it searches Help Article records instantly.
- If nothing internal matches, it shows a direct link to search
  docs.erpnext.com for that same query.
- Also available as a full page at `https://yoursite.com/helpbot`.

## Step 1 — Push this to GitHub
1. Create a new empty repository on GitHub, e.g. `helpbot`.
2. On your computer, unzip this folder.
3. On the GitHub repo page, use "Add file → Upload files" and drag in
   everything from the unzipped `helpbot` folder (keep the folder
   structure — GitHub's upload UI preserves subfolders when you drag a
   whole folder in Chrome/Edge).
4. Commit directly to the `main` branch.

   (If drag-and-drop of folders doesn't work in your browser, use
   [GitHub Desktop](https://desktop.github.com/) instead — install it,
   "Add local repository", point it at the unzipped folder, Publish.)

## Step 2 — Connect it in Frappe Cloud
1. Frappe Cloud dashboard → your **Bench** (Private Bench) → **Apps** tab.
2. Click **Add App from GitHub**, paste your repo URL
   (`https://github.com/<you>/helpbot`), branch `main`.
3. Click **Deploy** — Frappe Cloud will build the app. Watch the build log;
   if it fails, copy the error and send it to me, I'll fix the file.
4. Once deployed, go to your **Site** → **Apps** tab → find "Helpbot" →
   **Install**.

## Step 3 — Add your first Help Articles
1. In ERPNext, go to the search bar (Awesomebar) and type `Help Article` →
   **New**.
2. Fill in:
   - Title: the question, e.g. "How do we approve leave requests"
   - Category: Internal Workflow
   - Module: HR
   - Keywords: leave, approval, hr
   - Content: the actual steps
3. For an official ERPNext doc reference instead:
   - Category: ERPNext Official Reference
   - Check "Points to Official ERPNext Docs"
   - Reference URL: paste the exact docs.erpnext.com page link
   - Content: a short 2-3 line summary in your own words (don't copy-paste
     large chunks of the official docs — just enough to help someone decide
     if that's the right page)

That's it — the chat bubble will now search these instantly.

## Notes
- No AI/API key needed — this is fast keyword search, works offline within
  your site, and costs nothing extra to run.
- You (or anyone with edit rights) can keep adding articles over time; the
  more you add, the more useful it gets.
- If later you want it to also answer in full natural language using AI,
  that's a small addition on top of this same app — ask me when you're ready.
