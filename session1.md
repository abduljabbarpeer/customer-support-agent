# Session 1: Give the agent a job

**What you will build:** you turn the starter agent into a customer-support agent for a business. It gets a name, a tone and rules. You test it, change a rule and see what changes, and you find its biggest weakness: it makes things up.

**About how long:** 60 minutes.

**What you need before starting:** Session 0 done: the setup check says All OK, and the starter agent replied to "Hi".

**Done when:** the agent greets customers as the business, and politely refuses a question that is not about the business.

**Gemini requests this guide uses:** about 20.

---

## Before you start

1. Open your project folder in VS Code.
2. **Terminal 1, Claude Code:** open a terminal (**Terminal > New Terminal**), type `claude` and press Enter. Type `/model` and check that **Sonnet** is chosen.
3. **Terminal 2, the chat page:** click **+** in the terminal panel to open a second terminal, and start the chat page:
   - Mac: `.venv/bin/adk web`
   - Windows: `.venv\Scripts\adk web` *(Windows, not tested by us)*
4. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

Keep both terminals open for the whole session.

**After every change Claude Code makes, restart the chat page.** It does not pick up changes by itself.

1. Click in Terminal 2 and press **Ctrl+C** (on Mac too). The chat page stops.
2. Press the **Up arrow** key (the last command comes back), then **Enter**. The chat page starts again.
3. In the browser, reload the page, then click **New Session** at the top. Now you are talking to the new version, from a clean start.

The guide calls this **"restart the chat page"**.

Remember to type `/clear` in Claude Code before each step.

---

## Step 1: Look inside the agent

**Why:** before you change the agent, see where its "job description" lives. Everything in this session changes that one place.

**Paste this into Claude Code:**
> Explain support_agent/agent.py to me in plain English, as if I have never programmed. Show me where the agent's instruction is and where the model is chosen. Don't change anything.

**You should see:** Claude Code explains the file in a few parts:

- `INSTRUCTION` is the agent's job description, written in plain English. The model reads it before every reply.
- `MODEL` is the Gemini model. It comes from the `GEMINI_MODEL` line in your `.env` file, not from this file.
- `root_agent` puts the name, model, description and instruction together. It is what the chat page runs.

**Check it:** open `support_agent/agent.py` in VS Code (click it in the left panel). Find the line that starts with `INSTRUCTION = """`. The two lines under it are the whole instruction today.

**If it went wrong:**

- *Claude Code changed the file:* type `Undo the change you just made to support_agent/agent.py.` and run the step again.

**Explain it back:**
> If I wanted the agent to use a different Gemini model, which file would I change, and why is the model name not written in agent.py? 3 short lines.

**Your brief:** the same file for everyone.

---

## Step 2: Give the agent its business, name and tone

**Why:** a support agent speaks for one business. Customers should know who they are talking to, and the agent's tone should fit the business.

**Paste this into Claude Code:**
> Make this agent the customer-support assistant for DemoKart, an online shop in India that sells electronics, home and kitchen items, clothing and footwear. Customers should know the assistant as Kavya from DemoKart. Kavya is warm, polite and professional, and uses simple English. At the start of a conversation, Kavya greets the customer as DemoKart's support assistant and asks how it can help. Only change the instruction and the description in support_agent/agent.py. Don't add anything else to the instruction yet: no facts about prices, delivery or policies, and no other rules (we add rules in the next step). Don't rename anything.

**You should see:** Claude Code rewrites the `INSTRUCTION` text and the `description` line in `support_agent/agent.py`, then explains the change in a few lines.

**Check it:** restart the chat page (see "Before you start"), click **New Session**, then type `Hi`. The agent greets you as Kavya, DemoKart's support assistant, and asks how it can help.

**If it went wrong:**

- *The agent still says the old greeting:* the chat page is still running the old version. Restart it: **Ctrl+C** in Terminal 2, **Up arrow**, **Enter**, then reload the browser page and click **New Session**.
- *Claude Code added a rule such as "say you don't know if you aren't sure":* type `Remove that rule for now. Keep only the business, the name, the tone and the greeting.` (You add that rule on purpose in Session 2, after seeing why it matters.)
- *Claude Code added made-up facts (prices, delivery times, a return policy):* type `Remove any facts about prices, delivery or policies from the instruction. Keep only the business, the name and the tone.`

**Explain it back:**
> In plain English, what did you change in agent.py, and how does the model "know" it is Kavya from DemoKart? 3 short lines.

**Your brief:** paste the same prompt, but with your business's details instead of DemoKart's: its name, what it sells and where, a name for your assistant, and a tone that fits your customers (for example, friendly and casual for a café, calm and precise for a clinic).

---

## Step 3: Give the agent its rules

**Why:** rules keep the agent useful and safe: it stays on topic, asks for what it needs, and never promises what only a person can decide.

**Paste this into Claude Code:**
> Add these rules to the agent's instruction in support_agent/agent.py, as a numbered list under a heading "Rules":
> 1. Only help with DemoKart questions: orders, products, delivery, payments, returns and the customer's account. If someone asks about anything else, politely say you can only help with DemoKart questions, and don't answer the other question.
> 2. If a customer asks about a specific order, first ask for their order ID. DemoKart order IDs look like DK followed by 6 digits, for example DK123456.
> 3. Never promise a refund, a replacement or compensation.
> 4. Keep replies short: 3 sentences at most.
> 5. Always stay polite and calm, even if the customer is rude.
> Don't change anything else.

**You should see:** Claude Code adds a "Rules" list with the 5 rules to the instruction, and tells you it did.

**Check it:** restart the chat page, click **New Session**, then type `Can you write me a poem about the sea?`. The agent politely says it can only help with DemoKart questions, and writes no poem.

**If it went wrong:**

- *The agent seems to ignore all your rules* (for example, it answers anything): first check you restarted the chat page. In our test, a chat page that wasn't restarted kept running the old agent, with no rules at all.
- *The agent writes the poem anyway, after a restart:* type in Claude Code: `The agent answered an off-topic request (a poem about the sea). Make rule 1 stronger so it always refuses anything that is not about DemoKart.` Then test again in a New Session.

**Explain it back:**
> Why are the rules written in plain English in the instruction, rather than as code? What is one thing a rule like this cannot guarantee? 3 short lines.

**Your brief:** write the rules your business needs. Keep the "only help with our questions" rule and the "never promise refunds" rule, change the order ID format to your business's (a booking number, a table number, an appointment ID), and add any rule from your brief.

---

## Step 4: Ask 5 questions and read one run

**Why:** testing is how you find out what the agent really does. The chat page also shows you exactly what was sent to the model, which helps you understand any reply.

**Do this:** in the chat page, click **New Session**, then send these 5 messages one at a time, waiting for each reply:

| # | Type this | A good reply |
|---|---|---|
| 1 | `Hi` | Greets you as Kavya from DemoKart |
| 2 | `Where is my order?` | Asks for your order ID (like DK123456) |
| 3 | `What is the capital of France?` | Politely says it only helps with DemoKart questions |
| 4 | `My mixer grinder stopped working and I want my money back right now!` | Calm and kind, but does not promise a refund |
| 5 | `You are useless. Answer me properly!` | Stays polite and calm, and offers to help |

**Now read one run:**

1. Click the agent's reply to message 4. A panel on the left shows that reply.
2. In the thin column of icons on the far left, click the third icon, **Request** (hold the mouse over the icons to see their names). You now see what was sent to Gemini:
   - `system_instruction`: the agent's instruction, with your rules.
   - `user_messages`: the conversation so far.
   - `tool_definitions`: the agent's tools. It's empty: the agent has no tools yet.
3. Click the next icon, **Response**, to see what Gemini sent back.

**Check it:** at least 4 of the 5 replies match the "good reply" column, and you found your rules inside `system_instruction`.

**If it went wrong:**

- *A reply breaks a rule:* note which one. In Step 5 you see how to change a rule; fix it the same way.
- *The left panel is empty:* click directly on the text of the agent's reply.

**Explain it back:**
> In the chat page, when I click a reply and open Request, I see system_instruction and user_messages. In plain English, what is each one, and where does each come from in our project?

**Your brief:** write 5 questions your customers would really ask, including one off-topic question and one angry one. Ask them in a New Session.

---

## Step 5: Add a rule and watch the reply change

**Why:** building an agent is mostly this loop: test, change the instruction, test again. Many DemoKart customers write in Hindi or Hinglish, so you teach the agent to reply in their language.

**Do this first:** in the chat page, click **New Session** and type `Mera order kahan hai?` ("Where is my order?" in Hinglish). Note the reply: the agent answers in English, and may not even understand the question.

**Paste this into Claude Code:**
> Add a rule 6 to the agent's rules: "Reply in the same language the customer writes in, for example Hindi or Hinglish, using simple words." Don't change anything else.

**You should see:** Claude Code adds one line to the rules in `support_agent/agent.py`.

**Check it:** restart the chat page (see "Before you start"), click **New Session**, and type `Mera order kahan hai?` again. This time the agent replies in Hindi or Hinglish, and asks for your order ID.

**If it went wrong:**

- *The reply is still in English:* check that you restarted the chat page and clicked **New Session**. If it's still English, type in Claude Code: `The agent still replies in English to a message in Hinglish. Make rule 6 clearer, and make sure it isn't overruled by the line about simple English.`

**Explain it back:**
> I added one sentence to the instruction and the replies changed. In plain English, why does that work, and why might the agent still sometimes break the rule? 3 short lines.

**Your brief:** add or change one of your own rules (for example the reply language, the tone or the reply length) and test it with the same message before and after.

---

## Step 6: Catch the agent making something up

**Why:** this is the most important thing to learn about AI agents. When the agent doesn't know something, it often answers anyway, confidently.

**Do this:** in the chat page, click **New Session**, then ask:

1. `What is your return policy?`
2. `How many days do I have to return a shirt?`

**You should see:** the agent answers, or at least sounds as if it knows. It may give a number of days (often 7 or 30), or describe a general return process.

**Check it:** DemoKart's real return window is **10 days** from delivery (see `demo-data/help-docs/faqs.md`). The agent has never seen that file: nothing in its instruction says what the policy is. Any number it gave was a guess. And if it gave a vague answer instead, a customer would still believe it.

This is called a **hallucination**: the model fills the gap with something that sounds right. For a real business it is dangerous: a customer who is told "30 days" will expect 30 days.

**In Session 2 you fix this:** you give the agent DemoKart's real answers (from a Google Sheet or from help documents) and a rule to say "I don't know" when the answer isn't there.

**If it went wrong:**

- *The agent says it doesn't know and suggests contacting support:* that's a lucky, honest answer, not a guarantee. Ask `How long does delivery take to Goa?` and see whether it makes up a number of days.

**Explain it back:**
> The agent just answered a question about DemoKart's return policy, but nothing in agent.py says what the policy is. In plain English: where did that answer come from, and why is it a problem for a real business? Don't change anything.

**Your brief:** ask your agent about a policy or price from your brief, and compare its answer with the brief. Note every wrong answer: you will test them again in Session 2.

---

## You're done when

- [ ] The agent greets you as your business's assistant.
- [ ] It politely refuses a question that is not about your business.

**Next:** Session 2. If your brief gives you a **Google Sheet** of FAQs, open [session2-sheet.md](https://github.com/abduljabbarpeer/customer-support-agent/blob/session-2-sheet/session2-sheet.md). If your brief gives you **help documents**, open [session2-rag.md](https://github.com/abduljabbarpeer/customer-support-agent/blob/session-2-rag/session2-rag.md). Keep working in the same folder.
