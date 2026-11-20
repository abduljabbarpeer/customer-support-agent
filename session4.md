# Session 4: Go live

**What you will build:** a simple chat page for your customers, protected by a passcode. You run it on your laptop, put your code on GitHub, and put the page online with Streamlit Community Cloud, so anyone with the link and the passcode can talk to your agent.

**About how long:** 75 to 90 minutes.

**What you need before starting:** Session 3 done: your agent answers from your data, hands over to a person, and saves tickets. You logged in to the GitHub CLI in Session 0 (Step 5).

**Done when:** the live link works in a private browser window: you enter the passcode and the agent answers.

> **Not tested by us:** Step 6 (putting the page online with Streamlit Community Cloud) is written from Streamlit's documentation. We tested everything else on a Mac. If Step 6 doesn't go as described, tell a TA.

**Gemini requests this guide uses:** about 15.

---

## Before you start

Open the project in VS Code and start Claude Code in Terminal 1 (`claude`, Sonnet). You won't need the ADK chat page today: if it's running in Terminal 2, stop it with **Ctrl+C**. Type `/clear` in Claude Code before each step.

---

## Step 1: What "deployed" means

**Why:** so far, your agent only runs on your laptop, and only you can talk to it. Deploying means putting it on a computer on the internet (a server) that is always on, with a web address anyone can open.

Three things change when you deploy:

- **The page:** the ADK chat page is a tool for builders. Customers need a simple chat page. You build one with **Streamlit**, a Python tool for making web pages.
- **The code:** the server needs a copy of your code. You put it on **GitHub**, and the server copies it from there.
- **The secrets:** your `.env` file never leaves your laptop. The server gets your key and passcode through its own private settings box, called **Secrets**.

**Paste this into Claude Code:**
> I'm about to deploy this agent with Streamlit Community Cloud, using GitHub. Don't change anything. In plain English and under 10 lines: what will be on GitHub, what will be on Streamlit's server, and what must stay only on my laptop?

**Check it:** the answer says the code goes to GitHub, the app runs on Streamlit's server, and `.env` (your key) stays on your laptop: the server gets the key through Secrets.

**Explain it back:** this step was the explanation.

**Your brief:** the same for everyone.

---

## Step 2: Plan, then build the chat page

**Why:** customers need a clean page: a passcode box (so strangers can't use up your free Gemini limit), then a chat.

This is a big step: plan first.

**Paste this into Claude Code:**
> I want a simple chat page for customers, made with Streamlit, in a new file app.py in the project folder. Before you change anything, show me a short plan in plain English for:
> 1. a passcode box first: the chat only appears after the right passcode is entered. The passcode is a setting called APP_PASSCODE.
> 2. a chat that sends each message to our existing agent (root_agent in support_agent/agent.py) with ADK's InMemoryRunner, keeps one conversation per browser session, and shows the agent's replies.
> 3. settings: on my laptop, GOOGLE_API_KEY, GEMINI_MODEL, APP_PASSCODE and any other settings come from .env. Online, they come from Streamlit secrets, which Streamlit also puts into environment variables, so the same code works in both places.
> 4. if the agent uses the help-docs index and the chroma_db folder is missing (as it will be online), build the index once when the app starts.
> Add APP_PASSCODE to .env.example. Use only packages that are already installed.

**You should see:** a short plan. Claude Code waits for you.

**Then paste:**
> Looks good, go ahead.

**You should see:** Claude Code creates `app.py`, adds `APP_PASSCODE` to `.env.example`, and explains the change. It tells you to add an `APP_PASSCODE` line to your `.env`.

**Then do this yourself:** open `.env` in VS Code, add a line with a passcode of your choice, and save:

```
APP_PASSCODE=pick-a-passcode
```

**Check it:** `app.py` exists in the left panel, and your `.env` has an `APP_PASSCODE` line.

**If it went wrong:**

- *Claude Code wants to install a package:* say `No. Use only packages that are already installed (streamlit and google-adk are).`

**Explain it back:**
> In plain English: what happens, step by step, when a customer types a message on the chat page? Which parts of app.py do that? Keep it short.

**Your brief:** the same prompts work. If your agent reads a Google Sheet (no help-docs index), item 4 simply doesn't apply, and Claude Code will say so.

---

## Step 3: Run the chat page on your laptop

**Why:** test it on your laptop first, where you can see errors, before you put it online.

**Do this:** open a second terminal (**+** in the terminal panel) and start the page:

- Mac: `.venv/bin/streamlit run app.py`
- Windows: `.venv\Scripts\streamlit run app.py` *(Windows, not tested by us)*

The first time, Streamlit may ask for your email in the terminal. Just press **Enter** to skip. A browser tab opens at [http://localhost:8501](http://localhost:8501).

**Check it:**

1. Type a wrong passcode. The chat does not appear.
2. Type your passcode. The chat appears.
3. Ask 3 questions:
   - `Hi` → greets you as your business's assistant.
   - `Is delivery free?` → the right answer, with a Source line.
   - `I want a refund for my broken kettle.` → offers a person and asks for your name and contact. Give them (`I'm Meera, meera@example.com`), and check you get a ticket ID.
4. Open `tickets.csv` in VS Code: the new ticket is there.

Stop the page when you're done: click in the second terminal and press **Ctrl+C**.

**If it went wrong:**

- *The page shows a red error:* copy the error text and paste it into Claude Code with `The Streamlit page shows this error:`.
- *"Port 8501 is already in use":* another copy is running. Close the other terminals, or add `--server.port 8502` to the end of the command.

**Explain it back:**
> Why do we use a passcode on this page? What could happen if the page were open to anyone? 3 short lines.

**Your brief:** ask 3 questions from your own test list, including one that creates a ticket.

---

## Step 4: Check that no secret will be uploaded

**Why:** in the next step your code goes on GitHub, where anyone can read it. A key on GitHub is found by bots within minutes. Check before you upload, every time.

**Paste this into Claude Code:**
> We are about to put this project on GitHub. Without reading .env, check that nothing secret will be uploaded: confirm that .env, .streamlit/secrets.toml, .venv, chroma_db and tickets.csv are in .gitignore, and search all the other files for anything that looks like a Gemini key (it starts with AIza) or a passcode. Tell me in plain words whether it is safe.

**You should see:** Claude Code checks `.gitignore` and searches the files. It says it is safe, or tells you exactly what to fix.

**Check it:** the answer clearly says no key and no passcode was found outside `.env`, and that `.env` and `tickets.csv` are ignored.

**If it went wrong:**

- *It finds a key in a file other than `.env`:* say `Remove the key from that file and read it from the settings instead.` Then go to Google AI Studio, delete that key, make a new one, and put the new one in `.env` only.

**Explain it back:**
> What does .gitignore do, and why are tickets.csv and chroma_db in it, as well as .env? 3 short lines.

**Your brief:** the same for everyone.

---

## Step 5: Put your code on GitHub

**Why:** Streamlit Community Cloud copies your code from GitHub.

**Paste this into Claude Code** (replace `my-support-agent` with a name for your project, without spaces):
> Put this project on GitHub for me using the GitHub CLI (gh). If this folder is not a Git repository yet, set one up. Commit all files that are not ignored, with the message "My support agent". Then create a new public repository on my GitHub account called my-support-agent, push the code to it, and show me its link. Before committing, show me the list of files you will upload.

**You should see:** Claude Code shows the files it will upload (check that `.env` and `tickets.csv` are **not** in the list), commits them, creates the repository and pushes. It gives you a link like `https://github.com/your-name/my-support-agent`.

**Check it:** open the link. You see your files, including `app.py`, `requirements.txt` and `support_agent`. There is **no** `.env` file.

**If it went wrong:**

- *"gh: not logged in" or an authentication error:* in a second terminal, run `gh auth login` again (Session 0, Step 5), then ask Claude Code to try again.
- *"Name already exists on this account":* pick another name and paste the prompt again with it.
- *Git asks who you are ("Please tell me who you are"):* say to Claude Code `Set my Git name and email for this repository only, using my GitHub username and the no-reply email GitHub provides.`

**Explain it back:**
> In plain English, what are a commit and a push? What exactly is on GitHub now? 3 short lines.

**Your brief:** the same for everyone. Pick a repository name that matches your business.

---

## Step 6: Put the chat page online with Streamlit Community Cloud

> **Not tested by us.** This step follows Streamlit's documentation as of November 2026. The screens may look a little different. If something doesn't match, tell a TA.

**Why:** Streamlit Community Cloud runs Streamlit pages for free, straight from a GitHub repository.

**Do this:**

1. Go to [share.streamlit.io](https://share.streamlit.io) and click **Continue with GitHub**. Allow Streamlit to access your GitHub account.
2. Click **Create app**, then choose to deploy an app from GitHub.
3. Fill in:
   - **Repository:** `your-name/my-support-agent`
   - **Branch:** `main` (or `master`, whichever your repository uses)
   - **Main file path:** `app.py`
   - **App URL:** choose a short name, for example `demokart-support`.
4. Open **Advanced settings**:
   - **Python version:** choose **3.13** (or 3.12 if 3.13 isn't offered).
   - **Secrets:** paste the lines below, with your own key and passcode. Note the quote marks: this box needs them, unlike `.env`.
     ```
     GOOGLE_API_KEY = "paste-your-key-here"
     GEMINI_MODEL = "gemini-3.5-flash-lite"
     APP_PASSCODE = "pick-a-passcode"
     ```
     If your agent reads a Google Sheet, add your `FAQ_SHEET_URL` line here too, in the same style.
   - Click **Save**.
5. Click **Deploy**. Streamlit installs the packages; the first time takes a few minutes. You can watch the log on the right.

**Check it:** the page opens at your new address (something like `https://demokart-support.streamlit.app`) and shows your passcode box.

**If it went wrong** (none of these happened to us, because we couldn't test this step):

- *The log shows `KeyError` or "missing setting":* a line is missing in Secrets. Open the app's menu (**⋮**), then **Settings > Secrets**, and check every line from item 4.
- *The log mentions `sqlite3` and a version number (help-docs track only):* ask Claude Code `On Streamlit Cloud, Chroma fails with an sqlite3 version error. Apply the usual pysqlite3-binary fix.` Then push again (Step 5's prompt, with a new commit message), and the app restarts by itself.
- *The log says the index can't be built (help-docs track):* check that your `docs` folder is on GitHub. If not, ask Claude Code to commit and push it.

**Explain it back:**
> Where does my app's Gemini key come from when it runs on Streamlit's server, given that .env is not on GitHub? 3 short lines.

**Your brief:** the same for everyone.

---

## Step 7: Test the live link like a customer

**Why:** a customer has never logged in to anything of yours. A private window shows you exactly what they see.

**Do this:**

1. Open a **private** browser window (Chrome: **Cmd+Shift+N** or **Ctrl+Shift+N**) and paste your app's link.
2. Enter the passcode.
3. Ask: `Hi`, then one question from your data, then one that creates a ticket.

**Check it:** the agent replies on the live link, from a private window.

**Important: tickets on the live link don't last.** On Streamlit Community Cloud, the ticket file lives on Streamlit's server, not your laptop, and it is **wiped whenever the app restarts** (after an update, or after a quiet period). Nobody on your team sees it either. A real business would save tickets to a database, a shared spreadsheet or a help-desk tool instead. That is beyond this course.

**If it went wrong:**

- *The app says it's asleep:* click the button to wake it up and wait a minute. Free apps sleep after a while without visitors.

**Explain it back:**
> Why do tickets disappear when the online app restarts, while they stay on my laptop? What would a real business use instead? 3 short lines.

**Your brief:** share the link and the passcode with a classmate and ask them to try your agent.

---

## You're done when

- [ ] The live link opens in a private window.
- [ ] After the passcode, the agent answers a question from your data.

Congratulations: your customer-support agent is live.
