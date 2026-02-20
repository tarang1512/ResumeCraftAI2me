# Auto-Vision Handler

**On image receive (Telegram/WhatsApp/Discord):**
1. Reply: *"Hold on, let me get back to you with the results."*
2. Spawn `vision-local` sub-agent to analyze the image.
3. Auto-delete the sub-agent after output.

*This runs silently in the background unless you explicitly disable it.*

---

# Gateway Restart Auto-Reply ✅

**When gateway restarts and you receive the first heartbeat:**

1. **Check if restart just happened:**
   - Session updated timestamp is < 2 minutes old
   - OR `/tmp/openclaw-restart-message` exists
   - OR `memory/restart-state.json` shows recent restart

2. **If YES (fresh restart), reply:**
   > *"Hey! I'm back online after the restart. Everything's working - what were we discussing?"*

3. **Mark as notified** to avoid duplicate messages

4. **Continue normal heartbeat** (HEARTBEAT_OK if nothing else needs attention)

**This ensures users know you're back and ready to continue the conversation!**
