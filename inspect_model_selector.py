# -*- coding: utf-8 -*-
"""
Inspect Gemini's model selector DOM — find the right selectors
to programmatically switch to Gemini Flash/Thinking model.
"""
import asyncio
from playwright.async_api import async_playwright
import os

PROFILE_DIR = os.path.join(os.path.dirname(__file__), "browser_profiles", "gemini")
GEMINI_URL = "https://gemini.google.com/app"

async def inspect():
    pw = await async_playwright().start()
    ctx = await pw.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR, headless=False,
        viewport={"width": 1280, "height": 900},
        args=["--disable-blink-features=AutomationControlled",
              "--start-maximized", "--no-first-run"],
        ignore_default_args=["--enable-automation"],
    )
    page = await ctx.new_page()
    await page.goto(GEMINI_URL)
    await page.wait_for_load_state("domcontentloaded")
    await asyncio.sleep(5)  # Wait for full page render

    # === Inspect model selector area ===
    print("\n🔍 Looking for model selector elements...")

    # Strategy 1: Look for buttons/dropdowns with model names
    model_keywords = ["model", "gemini", "flash", "pro", "thinking", "選擇模型", "模型"]
    
    # Check all buttons
    buttons = await page.query_selector_all("button")
    print(f"\nFound {len(buttons)} buttons total. Checking for model-related ones:")
    for i, btn in enumerate(buttons):
        text = (await btn.inner_text()).strip()
        aria = await btn.get_attribute("aria-label") or ""
        class_name = await btn.get_attribute("class") or ""
        data_attrs = await btn.get_attribute("data-test-id") or ""
        
        if any(kw.lower() in (text + aria + class_name + data_attrs).lower() for kw in model_keywords):
            print(f"  🎯 Button[{i}]: text='{text[:50]}' | aria='{aria[:50]}' | class='{class_name[:80]}'")

    # Strategy 2: Look for dropdown menus / mat-select / custom selectors
    selectors_to_try = [
        "mat-select", "mat-option", ".model-selector", "[data-model]",
        "bard-model-selector", "model-selector", ".dropdown-model",
        "[role='listbox']", "[role='combobox']", ".gmat-menu-trigger",
        "button[data-test-id*='model']", "button.model",
        ".model-picker", "gems-model-switcher",
    ]
    
    print("\n🔍 Trying specific selectors:")
    for sel in selectors_to_try:
        try:
            count = await page.locator(sel).count()
            if count > 0:
                text = await page.locator(sel).first.inner_text()
                print(f"  ✅ '{sel}' → {count} matches, text='{text[:60]}'")
        except Exception:
            pass

    # Strategy 3: Dump the full page HTML near the top header area
    print("\n🔍 Checking header area for model info...")
    header_html = await page.evaluate("""
    () => {
        // Look for elements in the top portion that might contain model info
        const candidates = document.querySelectorAll('header, nav, [role="banner"], .header, .top-bar, .toolbar');
        let result = [];
        for (const el of candidates) {
            result.push(el.outerHTML.substring(0, 500));
        }
        // Also check for any element containing "Gemini" text near the top
        const allEls = document.querySelectorAll('*');
        for (const el of allEls) {
            const rect = el.getBoundingClientRect();
            if (rect.top < 100 && rect.height < 60) {
                const text = el.innerText || '';
                if (text.includes('Gemini') || text.includes('Flash') || text.includes('Pro')) {
                    result.push(`[top-area] tag=${el.tagName} class="${el.className}" text="${text.substring(0, 80)}"`);
                }
            }
        }
        return result.join('\n---\n');
    }
    """)
    print(header_html[:2000] if header_html else "(no header found)")

    # Strategy 4: Look for model picker trigger near the top
    print("\n🔍 Checking for clickable model name elements...")
    top_area = await page.evaluate("""
    () => {
        const elems = document.querySelectorAll('button, [role="button"], a, [tabindex]');
        let found = [];
        for (const el of elems) {
            const text = (el.innerText || '').trim();
            const rect = el.getBoundingClientRect();
            if (rect.top < 150 && text.length > 0 && text.length < 100) {
                found.push({
                    tag: el.tagName,
                    text: text.substring(0, 80),
                    class: (el.className || '').substring(0, 100),
                    ariaLabel: el.getAttribute('aria-label') || '',
                    top: Math.round(rect.top),
                    left: Math.round(rect.left),
                });
            }
        }
        return JSON.stringify(found, null, 2);
    }
    """)
    print(top_area[:3000] if top_area else "(no elements)")

    print("\n⏳ Keeping Chrome open 120 seconds — go look at the model selector manually...")
    print("Check the browser window and tell me what you see!")
    await asyncio.sleep(120)
    
    await ctx.close()
    await pw.stop()

if __name__ == "__main__":
    asyncio.run(inspect())
