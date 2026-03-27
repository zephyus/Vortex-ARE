# -*- coding: utf-8 -*-
"""
ChatGPT Login Helper — Opens Playwright Chrome for manual ChatGPT login.
After you log in, the session is saved to browser_profiles/chatgpt/.
Future launches will stay logged in automatically.
"""
import asyncio
import os
from playwright.async_api import async_playwright

PROFILE_DIR = os.path.join(os.path.dirname(__file__), "browser_profiles", "chatgpt")
CHATGPT_PROJECT_URL = "https://chatgpt.com/g/g-p-69c5e41e06048191b338ce99fe37395f-auto-llm-jj/project"

async def login():
    os.makedirs(PROFILE_DIR, exist_ok=True)
    pw = await async_playwright().start()

    ctx = await pw.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR, headless=False,
        viewport={"width": 1280, "height": 900},
        args=["--disable-blink-features=AutomationControlled",
              "--start-maximized", "--no-first-run"],
        ignore_default_args=["--enable-automation"],
    )

    page = await ctx.new_page()
    await page.goto(CHATGPT_PROJECT_URL)

    print("=" * 60)
    print("🔐 請在 Chrome 中登入 ChatGPT")
    print("   登入完成後，回到這裡按 Enter")
    print("   登入資訊會自動儲存到 browser_profiles/chatgpt/")
    print("=" * 60)

    input("\n按 Enter 結束並儲存登入狀態...")

    await ctx.close()
    await pw.stop()
    print("✅ 登入狀態已儲存！")

if __name__ == "__main__":
    asyncio.run(login())
