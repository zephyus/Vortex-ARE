# -*- coding: utf-8 -*-
"""Quick ChatGPT connection test — checks if logged in and project accessible."""
import asyncio
from headless_bridge import HeadlessAIBridge

async def test():
    bridge = HeadlessAIBridge()
    ok = await bridge.initialize()

    if bridge.chatgpt:
        print("\n✅ ChatGPT bridge is connected!")
        # Try a quick prompt
        print("🔴 Sending test prompt to ChatGPT AUTO_LLM_jj project...")
        result = await bridge.ask_chatgpt("Reply with one word: Hello")
        print(f"📦 ChatGPT Response: {result[:200]}")
    else:
        print("\n❌ ChatGPT not connected — likely not logged in.")

    print("\n⏳ Keeping browsers open 30 seconds for observation...")
    await asyncio.sleep(30)
    await bridge.shutdown()

if __name__ == "__main__":
    asyncio.run(test())
