import asyncio
from backend.utils.gemini_client import call_gemini_text
from backend.main import LIVE_CHAT_BASE_INSTRUCTIONS, config
import json

history_text = '''Client: Hi
Aria: Hi there! Let's map your AP process. What is the process called?
Client: It is called Invoice Processing.
Aria: Got it. What triggers the start of the invoice processing?
Client: We receive an email from the vendor with the invoice PDF.
Aria: Oh, that's super helpful. What's the very next step after an email...'''

director_prompt = f"""You are an expert AI orchestrator.
A voice agent named Aria was interviewing a client about their Accounts Payable process. The call disconnected.
Here is the transcript of their conversation so far:
<transcript>
{history_text}
</transcript>

Aria's goal is to collect 8 domains:
1. PROCESS IDENTITY (Name, trigger, start/end)
2. STEP-BY-STEP WORKFLOW (Actions, who does it, inputs/outputs)
3. SYSTEMS & TOOLS (ERP, CRM, spreadsheets used)
4. PEOPLE & ROLES (Job titles, headcount, approvers)
5. VOLUME & TIME (Frequency, duration)
6. PAIN POINTS & ERRORS (Bottlenecks, rework)
7. COST & BUSINESS IMPACT (Hourly rates, error costs)
8. EXISTING AUTOMATION & CONSTRAINTS (Current bots, IT policies)

Analyze the transcript and generate a STRICT two-part markdown block for Aria's new system prompt.

FORMAT EXACTLY LIKE THIS (preserve the separator lines):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FACTS ALREADY GATHERED (DO NOT ASK ABOUT THESE AGAIN)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[List exactly what the client has already stated. Be specific with names/numbers. E.g. 'Systems: They use SAP and Excel.']

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INFORMATION YOU STILL MUST COLLECT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[List ONLY the domains that are missing or severely incomplete. DO NOT repeat any domain listed above.]"""

print("--- Calling Director Agent ---")
res = call_gemini_text(
    prompt=director_prompt,
    system_prompt='You are an AI Orchestrator. Output ONLY the two-part markdown checklist block, nothing else.',
    model=config.GEMINI_MODEL_FAST
)

print('\n--- DIRECTOR OUTPUT ---')
print(res)

print('\n--- TESTING GEMINI LIVE API SYSTEM PROMPT ---')
effective_prompt = LIVE_CHAT_BASE_INSTRUCTIONS + '\n\n' + res

print('Testing effective prompt with text API just to see first question...')
test_q = call_gemini_text(
    prompt='I am back. Let\'s resume.',
    system_prompt=effective_prompt,
    model='gemini-2.5-flash',
    use_live_key=False
)
print('\nARIA REPLIES:', test_q)
