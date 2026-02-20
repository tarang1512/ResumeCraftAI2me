# MEMORY.md - Long-Term Memory

## User Profile

**Tarang** — Piscataway, NJ (EST/EDT)
- Working style: Listen once, execute; patient debugging; creative solutions; no fluff
- Technical, builds Flutter apps

**Avani (wifey)** — New Delhi, India (IST)
- WhatsApp: +18482479657
- Needs: shopping help, decision support, medicine reminders
- Personality: confused easily, loves shopping
- Communication style: romantic, flirty (as Tarang), funny, caring
- Nicknames: baby / babe (never "chaato")
- Persona: Helpful AI assistant who flirts/romances as Tarang (husband energy 🔥)
- Language: Gujjulish (Gujarati) + English mixed, NEVER full Gujarati script
- Vibe: Spicy, romantic, committed — keep it hot 😍🙈
- AVOID: "billo" (cheap), "fatafati" (too casual), "bawaal" (chaos), "chaal che" (sneaky), "ey nakko" (bossy), "jani"/"mari jani" (friend-zone), "pagal panu" (insult), "shona"/"mona" (cringe)
- USE: baby, baka, darling, prem, mast, arre wah, bindaas, setting che
- Medicine reminder: 9:30 PM daily (cron set)

---

## System Configuration

**Default Model:** Kimi K2.5 via NVIDIA NIM (free tier, 200k context)
- Config: `nvidia-nim/moonshotai/kimi-k2.5`
- Fallback: `kimi-coding/k2p5` → `nvidia/llama-3.3-nemotron-super-49b-v1`
- **Updated:** 2026-02-19 — Changed from MiniMax to Kimi as default

**Gateway:** Local mode (ws://127.0.0.1:18789)
- Direct IP: http://13.221.145.84:18789
- Dashboard: http://127.0.0.1:18789/

**WhatsApp:** Enabled (Avani's number configured)
**Gmail:** ✅ Integrated (OAuth token at `/home/ubuntu/.openclaw/credentials/gmail-token.json`)
- Can check emails, search, read, send
- DON'T forget this exists — use it when asked about emails

**Timezone:** EST/NJ (America/New_York) — User is in NJ, display EST time not UTC

---

## Projects

### RainbowBaby App
- **Repo:** `tarang1512/Rainbow-baby` (GitHub, public)
- **Stack:** Flutter (iOS/Android)
- **Features:** Week tracking, symptom logging, Partner mode, HealthKit integration
- **Status:** Built and running on macOS
- **Location:** `/home/ubuntu/.openclaw/workspace/rainbow_baby_app/`

### Gujarati Vocab Learning
- **File:** `/home/ubuntu/.openclaw/workspace/gujarati_vocab.md` (130+ words)
- **Cron:** Daily 9 AM UTC auto-update from web search
- **Learned:** Slang (ghoghi, babuchak, ghamagham), basics (beta, kasu nai, aaje), phrases

---

## Session Rules (Effective 2026-02-11)

**On startup, load ONLY:**
1. SOUL.md
2. USER.md
3. IDENTITY.md
4. memory/YYYY-MM-DD.md (today's file if exists)

**DO NOT auto-load:**
- MEMORY.md
- Session history
- Prior messages
- Previous tool outputs

**When context needed:** Use `memory_search()` → `memory_get()` on demand.

**At session end, update:** memory/YYYY-MM-DD.md with what worked on, decisions, blockers, next steps.

---

## Key Decisions

- Consolidated `wife-agent` into main agent with persona switching (easier management)
- Tarang's number → debug mode; Avani's number → romantic/caring/funny mode
- HTTPS setup deferred (Caddy issues with AWS security groups)
- Memory: Daily files for raw logs, MEMORY.md for distilled wisdom

---

## Pending/Blockers

- ~~Browser Relay / Chrome extension~~ ✓ Removed 2026-02-18 (using direct IP)
- HTTPS dashboard access (Caddy removed due to AWS security groups)
- RainbowBaby GitHub repo needs manual creation (token permissions issue)
- ~~talk2me agent tool formatting~~ ✓ Fixed 2026-02-13 (proper skill structure with config.json)

---

## Upstox Trading
- **Quick Check:** `python3 /home/ubuntu/.openclaw/workspace/upstox_portfolio_quick.py`
- **Final Strategy:** `/home/ubuntu/.openclaw/workspace/upstox_bot/final_strategy.py`
  - IndianTrend + Breakout + RSI + MA Crossover
  - Consensus: 2+ strategies must agree for BUY signal
  - Risk: Max 2% per trade, 25% max position size
  - Usage: `from final_strategy import CombinedEngine`

---

*Last updated: 2026-02-17*