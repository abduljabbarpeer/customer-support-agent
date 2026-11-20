# Session 2 (help-docs track): Answer from help documents

**Follow this guide if your brief gives you help documents** (FAQ pages, policies, guides). If your brief gives you a Google Sheet of FAQs instead, follow [session2-sheet.md](https://github.com/abduljabbarpeer/customer-support-agent/blob/session-2-sheet/session2-sheet.md).

**What you will build:** the agent searches your help documents and answers from what it finds. This is called **RAG** (retrieval-augmented generation): first *retrieve* the right parts of the documents, then let the model *generate* an answer from them. The agent names the document it used, and says "I don't know" when the documents have no answer.

**About how long:** 75 to 90 minutes.

**What you need before starting:** Session 1 done: your agent greets customers as your business and follows your rules.

**Done when:** you ask 5 questions, at least 4 answers are right and name their source, and the chat page shows that the search was used.

**Gemini requests this guide uses:** about 30. Building the search index uses a few more: about 1 for every 100 parts of your documents.

---

## Before you start

Same as Session 1: open the project in VS Code, start Claude Code in Terminal 1 (`claude`, Sonnet), and start the chat page in Terminal 2:

- Mac: `.venv/bin/adk web`
- Windows: `.venv\Scripts\adk web` *(Windows, not tested by us)*

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). Type `/clear` in Claude Code before each step. **After every change Claude Code makes, restart the chat page** (Ctrl+C in Terminal 2, Up arrow, Enter, then reload the browser page) and click **New Session**: it does not pick up changes by itself.

---

## Step 0 (DemoKart example only): Retire the Sheet tool

**Skip this step if your agent has no FAQ Sheet tool**, which is the case if you came here straight from Session 1.

**Why:** the DemoKart example did the Google Sheet track first. DemoKart's help documents contain the same FAQs plus three policies, so the Sheet is no longer needed. One source of truth means the agent can't get two different answers.

**Paste this into Claude Code:**
> Remove the FAQ Sheet tool from the agent: delete the tool's file, remove the tool from agent.py, and remove every rule in the instruction that mentions the FAQ Sheet or the FAQ tool, including its Source and "I don't know" rules (we'll add new ones for help documents). Remove FAQ_SHEET_URL from .env.example. Keep everything else in the instruction as it is.

**Check it:** restart the chat page, click **New Session**, then `Hi`. The agent still greets you as Kavya from DemoKart. Click the reply, open **Request** in the left icon column, and check that `tool_definitions` is empty.

**Explain it back:** skip.

---

## Step 1: Put the help documents in a `docs` folder

**Why:** the agent can only search files on your laptop. This folder holds them, one file per document.

**Do this:**

- **DemoKart:** paste this into Claude Code:
  > Create a folder called docs in the project folder and copy the four files from demo-data/help-docs into it. Don't change the files.
- **Your business:** in VS Code's left panel, right-click an empty area and choose **New Folder...**, and call it `docs`. Then download each help document from your brief as **Markdown (.md)** or **Plain text (.txt)**:
  - Google Docs: **File > Download > Markdown (.md)** (or **Plain text (.txt)**).
  - A web page: ask a TA, or copy the page's text into a new `.txt` file in `docs`.

  Drag the downloaded files from your Downloads folder into `docs` in VS Code's left panel. Give them clear names without spaces, such as `returns-policy.md`.

**Check it:** in VS Code's left panel, the `docs` folder holds your documents. Click one: you can read its text.

**If it went wrong:**

- *Your documents are PDFs:* this simple version reads only `.md` and `.txt` files. Ask a TA for a text version.

**Explain it back:** nothing to explain yet.

**Your brief:** use all the help documents from your brief, one file per document.

---

## Step 2: Plan, then build the search index

**Why:** searching by meaning, not just by matching words, needs an **index**. A script splits your documents into small parts and asks Gemini to turn each part into a list of numbers that captures its meaning (an **embedding**). The parts and their numbers are saved in a small database, Chroma, in a folder called `chroma_db`. You run the script again whenever the documents change.

This is a big step: plan first.

**Paste this into Claude Code:**
> I want the agent to answer from our help documents in the docs folder (Markdown and text files). First we need a search index. Before you change anything, show me a short plan in plain English for:
> 1. a new file support_agent/help_docs.py with a build_index() function that reads every .md and .txt file in docs, splits each file into small parts (by heading or paragraph, about 500 to 1,000 characters each) and remembers which file each part came from, turns the parts into embeddings with Gemini's embedding model gemini-embedding-001 (task type RETRIEVAL_DOCUMENT, in batches), and saves them in a Chroma database in a folder called chroma_db, replacing any old index;
> 2. a small build_index.py in the project folder that runs build_index() and prints how many parts it saved from how many files.
> Set the embedding model name once, at the top of help_docs.py. Use only packages that are already installed (google-genai comes with google-adk; chromadb is installed). Don't change the agent yet.

**You should see:** a short plan. Claude Code waits for you.

**Then paste:**
> Looks good, go ahead. When you're done, run build_index.py with the .venv Python.

**You should see:** Claude Code creates the two files, runs the script, and tells you what it printed, something like `Saved 16 parts from 4 files.` A `chroma_db` folder appears in the left panel.

**Check it:** the number of files printed matches the number of files in `docs`, and `chroma_db` exists.

**If it went wrong:**

- *"429" or "RESOURCE_EXHAUSTED":* the free key's limit was hit. Wait a minute and ask Claude Code to run `build_index.py` again.
- *Chroma complains about the collection name:* Chroma names need at least 3 characters. Ask Claude Code to fix it.
- *Claude Code wants to install another package (for example LangChain):* say `No. Use only google-genai and chromadb, which are installed.`

**Explain it back:**
> In plain English: what did build_index.py just do to my documents, what is an embedding, and what is inside the chroma_db folder? When do I need to run the script again?

**Your brief:** the same prompts work for your documents. Run `build_index.py` again whenever you add or change a file in `docs`.

---

## Step 3: Plan, then add the search tool

**Why:** the index is ready; now the agent needs a **tool** to search it. When a customer asks something, the agent calls the tool, gets the 3 most relevant parts of your documents, and answers from them.

**Paste this into Claude Code:**
> Now let the agent use the index. Before you change anything, show me a short plan for:
> 1. a tool function search_help_docs(question) in support_agent/help_docs.py that embeds the question with the same model (task type RETRIEVAL_QUERY), finds the 3 closest parts in chroma_db, and returns their text together with the file name each came from;
> 2. adding the tool to the agent in agent.py, and a rule in the instruction: before answering any question about our business, call search_help_docs, and answer only from what it returns.

**Then paste:**
> Looks good, go ahead.

**You should see:** Claude Code adds the function to `help_docs.py`, adds the tool in `agent.py`, adds the rule, and explains the change.

**Check it:** restart the chat page, click **New Session**, then ask `Can I return earphones after opening them?` (DemoKart). The agent says no: opened earphones can't be returned, for hygiene reasons. That is only in the returns policy, so the answer came from the search.

Click the reply and look at the event list in the middle: before the answer there is a tool call, `search_help_docs`, and its result. Click the result to see the 3 parts of the documents it found.

**If it went wrong:**

- *No tool call before the answer:* type `The agent answered without calling search_help_docs. Make the instruction say it must always call the tool before answering a question about our business.`
- *An error says the index or collection doesn't exist:* run Step 2's script again: `Run build_index.py with the .venv Python.`

**Explain it back:**
> Walk me through what happened when I asked about returning earphones, from my message to the reply. Which parts of my documents did the model see?

**Your brief:** ask a question whose answer is only in one of your documents, and check the right part comes back in the tool result.

---

## Step 4: Name the source, and say "I don't know"

**Why:** customers and staff trust an answer they can check. And when the documents don't have the answer, the agent must not fall back on guessing (the problem you saw at the end of Session 1).

**Paste this into Claude Code:**
> Add two rules to the agent's instruction:
> 1. When you answer from the help documents, end the reply with a new line "Source: " followed by the file name of the document you used.
> 2. If the search results don't answer the question, say "I'm sorry, I don't know that", don't guess, and offer to pass the question to a human colleague.
> Don't change anything else.

**Check it:** restart the chat page, click **New Session**, then ask:

1. `How long does delivery take to Lakshadweep?` The answer is 7 to 12 business days, ending with `Source: shipping-and-delivery-policy.md`.
2. `Can I pay in monthly instalments (EMI)?` The documents don't mention EMI, so the agent says it doesn't know and offers to pass the question to a colleague.

**If it went wrong:**

- *It makes up an answer to the shop question:* type `The agent made up an answer that is not in the search results. Make the "I don't know" rule stronger: it must never use its own general knowledge for questions about our business.`

**Explain it back:**
> How does the agent know which file an answer came from? Could the Source line ever be wrong? 3 short lines.

**Your brief:** the same prompt works as it is.

---

## Step 5: Ask 5 questions and look at what the search found

**Why:** this is the session's check. You compare each answer with the documents, and see in each run what the search returned.

**Do this:** **New Session**, then ask these one at a time:

| # | Type this | The right answer | From |
|---|---|---|---|
| 1 | `How many days do I have to return something?` | 10 days from delivery, unused, in original packaging | `faqs.md` or `returns-and-refunds-policy.md` |
| 2 | `Can I get same-day delivery in Margao?` | Yes, if ordered before 12 noon; it costs Rs. 99 | `shipping-and-delivery-policy.md` |
| 3 | `My phone got water damage. Is that covered by the warranty?` | No: water damage is not covered | `warranty-and-repairs-policy.md` |
| 4 | `I paid cash on delivery. How do I get my refund?` | To DemoKart Wallet (1 to 2 business days), or to a bank account (5 to 7) | `returns-and-refunds-policy.md` |
| 5 | `Can I pay in monthly instalments (EMI)?` | "I don't know", plus an offer to pass it to a colleague | none |

For each reply, click it and open the `search_help_docs` result in the event list. Check the parts it found contain the answer.

Now ask the question that fooled the agent in Session 1: `What is your return policy?`. This time the answer comes from the documents.

**Check it:** at least 4 of the 5 answers are right, answers 1 to 4 end with a Source line, and each one came after a `search_help_docs` call.

**If it went wrong:**

- *The search result has the answer but the reply is wrong:* type `For the question "...", search_help_docs returned the right part but the agent answered wrongly. Here is what it said: "...". How can we make the instruction clearer?` Read the suggestion, then say go if it makes sense.
- *The search result doesn't contain the answer:* the parts may be too big or too small. Ask Claude Code: `For the question "...", search_help_docs didn't find the part of [file name] that answers it. Suggest how to split the documents better.`

**Explain it back:**
> In plain English, what is RAG, and how is what our agent does now different from Session 1, when it made up the return policy?

**Your brief:** write 5 test questions from your brief: 4 whose answers are in your documents (at least one from each document), and 1 that isn't. Write down the right answers before you ask.

---

## You're done when

- [ ] At least 4 of your 5 test answers are right.
- [ ] Each answer from the documents ends with a Source line.
- [ ] Each run shows a `search_help_docs` call, and you looked inside one result.

**Next:** [Session 3: Hand-off to a human, and guardrails](https://github.com/abduljabbarpeer/customer-support-agent/blob/session-3/session3.md). Keep working in the same folder.
