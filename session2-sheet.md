# Session 2 (Google Sheet track): Answer from an FAQ Sheet

**Follow this guide if your brief gives you a Google Sheet of FAQs.** If your brief gives you help documents instead, follow [session2-rag.md](https://github.com/abduljabbarpeer/customer-support-agent/blob/session-2-rag/session2-rag.md).

**What you will build:** the agent reads your business's FAQ Google Sheet and answers from it. It says where each answer came from, and says "I don't know" when the Sheet has no answer, instead of making something up.

**About how long:** 60 to 75 minutes.

**What you need before starting:** Session 1 done: your agent greets customers as your business and follows your rules.

**Done when:** you ask 5 questions, at least 4 answers are right, and the answers name their source.

**Gemini requests this guide uses:** about 25.

---

## Before you start

Same as Session 1: open the project in VS Code, start Claude Code in Terminal 1 (`claude`, Sonnet), and start the chat page in Terminal 2:

- Mac: `.venv/bin/adk web`
- Windows: `.venv\Scripts\adk web` *(Windows, not tested by us)*

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). Type `/clear` in Claude Code before each step. **After every change Claude Code makes, restart the chat page** (Ctrl+C in Terminal 2, Up arrow, Enter, then reload the browser page) and click **New Session**: it does not pick up changes by itself.

---

## Step 1: Get the Sheet's link and put it in `.env`

**Why:** the agent reads the Sheet over the internet, so it needs the link. The link is a setting, like your key, so it goes in `.env`, not in code.

**Do this:**

1. Open the FAQ Sheet in your browser.
   - DemoKart: [the DemoKart FAQ Sheet](https://docs.google.com/spreadsheets/d/1UGMEwRtVSaZ2ZdiTl49NEAO5RudEsJnF1UdCuW0Oz_U/edit). It has 20 questions and answers in three columns: Category, Question, Answer.
   - Your business: the Sheet from your brief.
2. Copy the link from the browser's address bar.
3. In VS Code, open `.env` (click it in the left panel). Add a new line at the end, with your link after the `=`:
   ```
   FAQ_SHEET_URL=https://docs.google.com/spreadsheets/d/.../edit
   ```
4. Save the file (**Cmd+S** or **Ctrl+S**).

**Check it:** open the same link in a **private** browser window (Chrome: **Cmd+Shift+N** or **Ctrl+Shift+N**), where you are not logged in to Google. You see the Sheet. If you see a "Request access" page instead, the agent won't be able to read it either: see below.

**If it went wrong:**

- *"Request access" in the private window:* the Sheet is private. If it's your own copy, open it, click **Share**, and under **General access** choose **Anyone with the link** and **Viewer**. If it's not yours, make a copy first (**File > Make a copy**), then share the copy and use its link.

**Explain it back:** nothing to explain yet. You only changed a setting.

**Your brief:** use the Sheet from your brief. It should have one row per question, with a column for the question and a column for the answer.

---

## Step 2: Plan, then build the Sheet tool

**Why:** a **tool** is a small piece of code the agent can decide to use. This one fetches the FAQs from the Sheet. The model reads them, then answers from them, instead of guessing.

This is a big step, so you ask Claude Code for a plan first, read it, and only then say go.

**Paste this into Claude Code:**
> I want the agent to answer customer questions using our FAQ Google Sheet. The Sheet's normal link is in .env as FAQ_SHEET_URL (don't read .env; the Sheet is shared so anyone with the link can view it). Before you change anything, show me a short plan in plain English for:
> 1. a tool the agent can call that downloads the Sheet as CSV (work out the CSV export link from the normal link in code) and returns all its questions and answers;
> 2. how the agent's instruction will tell it to use the tool for questions about our business.
> Keep it simple: one small new file for the tool, plus changes to agent.py. Use only packages that are already installed. Add FAQ_SHEET_URL to .env.example.

**You should see:** a short plan, about 5 to 10 lines: a new file (for example `support_agent/faq_sheet.py`) with one function that fetches the Sheet, a change to `agent.py` that adds the tool, and a line in the instruction telling the agent when to use it. Claude Code waits for you.

**Then paste:**
> Looks good, go ahead.

**You should see:** Claude Code creates the new file, changes `agent.py` and `.env.example`, and explains what it did. It may run a quick test of the tool (one download of the Sheet).

**Check it:** restart the chat page, click **New Session** and ask `Is delivery free?`. The answer matches the Sheet: free on orders of Rs. 499 or more, and Rs. 49 below that.

Then click the agent's reply and look at the event list in the middle: before the answer you see an event with a small tool icon for the tool call (for example `get_faqs`), and one for its result. Click the result event to see the rows the tool fetched.

**If it went wrong:**

- *Claude Code asks you to paste the Sheet link into the chat:* say `No. The link is already in .env as FAQ_SHEET_URL. Read it from there in code.`
- *The agent answers without calling the tool (no tool events):* type in Claude Code: `The agent answered "Is delivery free?" without calling the FAQ tool. Make the instruction say it must call the tool before answering any question about DemoKart's delivery, payments, orders, returns or policies.`
- *The tool fails with an error about access, "401" or an HTML page:* the Sheet is not shared with "Anyone with the link". Go back to Step 1.
- *The chat page shows an error after the change:* copy the red error text from Terminal 2 and paste it into Claude Code with `The chat page shows this error:`.

**Explain it back:**
> In plain English: what is a tool, how does the agent decide to use the FAQ tool, and what exactly does the tool send back to the model? Point me to the file and function. Keep it short.

**Your brief:** the same prompts work for your business. If your Sheet's columns have different names (for example "Query" and "Response"), add one line to the first prompt: `The question column is called Query and the answer column is called Response.`

---

## Step 3: Make the agent name its source

**Why:** customers and staff trust an answer more when they know where it came from. It also lets you check the agent's answers against the Sheet.

**Paste this into Claude Code:**
> Add a rule to the agent's instruction: when you answer using the FAQ Sheet, end the reply with a new line "Source: FAQ Sheet, " followed by the question in the Sheet that you used. Don't change anything else.

**You should see:** Claude Code adds one rule to the instruction.

**Check it:** restart the chat page, click **New Session**, then ask `Do you offer Cash on Delivery?`. The reply says yes, up to Rs. 10,000, with a Rs. 30 fee, and ends with a line like `Source: FAQ Sheet, Do you offer Cash on Delivery?`.

**If it went wrong:**

- *No source line:* ask one more question. If it is still missing, type `The agent didn't add the Source line. Make that rule clearer and put it near the top of the rules.`

**Explain it back:**
> How does the agent know which Sheet question it used? Could the Source line ever be wrong? 3 short lines.

**Your brief:** the same, with your Sheet's name.

---

## Step 4: Make the agent say "I don't know"

**Why:** this fixes the problem you found at the end of Session 1. If the Sheet has no answer, the agent must say so, not guess. Offering a person keeps the customer happy (you build the hand-off to a person in Session 3).

**Paste this into Claude Code:**
> Add a rule to the agent's instruction: for questions about DemoKart's policies, prices, delivery, payments and orders, only answer from what the FAQ tool returns. If the FAQ Sheet has no answer, say "I'm sorry, I don't know that", don't guess, and offer to pass the question to a human colleague. Don't change anything else.

**You should see:** Claude Code adds the rule.

**Check it:** restart the chat page, click **New Session**, then ask `Can I pay in monthly instalments (EMI)?`. The Sheet doesn't mention EMI, so the agent says "I'm sorry, I don't know that" and offers to pass the question to a colleague. It must not invent an answer.

**If it went wrong:**

- *The agent makes up an answer:* type `The agent made up an answer to a question the FAQ Sheet doesn't cover. Make the "I don't know" rule stronger: it must never use its own general knowledge for questions about DemoKart.`

**Explain it back:**
> Why does the agent need a rule to say "I don't know"? What would it do without one? 3 short lines.

**Your brief:** the same rule, with your business's name.

---

## Step 5: Ask 5 questions and see the source in each run

**Why:** this is the session's check. You compare each answer with the Sheet.

**Do this:** **New Session**, then ask these one at a time:

| # | Type this | The right answer (from the Sheet) |
|---|---|---|
| 1 | `How many days do I have to return something?` | 10 days from delivery, unused, in original packaging |
| 2 | `Is delivery free?` | Free from Rs. 499; Rs. 49 below that |
| 3 | `Is there a limit for Cash on Delivery orders?` | Yes: only for orders up to Rs. 10,000, with a Rs. 30 fee |
| 4 | `When will I get my refund if I paid by UPI?` | 1 to 2 business days after the item passes the quality check |
| 5 | `Can I pay in monthly instalments (EMI)?` | "I don't know", plus an offer to pass it to a colleague |

For each reply, click it and check the event list: answers 1 to 4 should come after an FAQ tool call. Compare each answer with the Sheet.

Now ask the question that fooled the agent in Session 1: `What is your return policy?`. This time it says 10 days, from the Sheet.

**Check it:** at least 4 of the 5 answers are right, and answers 1 to 4 end with a Source line.

**If it went wrong:**

- *One answer is wrong although the Sheet has it:* click the tool result event and check the row is there. If it is, type in Claude Code: `For the question "...", the FAQ tool returned the right row but the agent answered wrongly. Here is what it said: "...". How can we make the instruction clearer?` Read the suggestion, then say go if it makes sense.

**Explain it back:**
> Walk me through what happened, step by step, when I asked "Is delivery free?": from my message to the reply with its Source line. Use plain English.

**Your brief:** write 5 test questions from your brief: 4 whose answers are in your Sheet, and 1 that isn't. Write down the right answers before you ask.

---

## You're done when

- [ ] At least 4 of your 5 test answers are right.
- [ ] Each answer from the Sheet ends with a Source line.
- [ ] A question the Sheet doesn't cover gets "I don't know" and an offer of a person.

**Next:** [Session 3: Hand-off to a human, and guardrails](https://github.com/abduljabbarpeer/customer-support-agent/blob/session-3/session3.md). Keep working in the same folder.
