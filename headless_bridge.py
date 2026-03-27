# -*- coding: utf-8 -*-
"""
Headless AI Bridge — Dual-LLM Production Controller
=====================================================
Supports BOTH Gemini and ChatGPT via proven multi_llm_orchestrator patterns.
Runs background threads for each LLM, sends prompts via DOM,
waits for generation, and extracts responses.
"""

import asyncio
import os
import threading
import queue

from playwright.async_api import async_playwright


# ==============================================================================
# Configuration
# ==============================================================================

GEMINI_URL = "https://gemini.google.com/app"
CHATGPT_PROJECT_URL = "https://chatgpt.com/g/g-p-69c5e41e06048191b338ce99fe37395f-auto-llm-jj/project"

PROFILE_DIR_GEMINI = os.path.join(os.path.dirname(__file__), "browser_profiles", "gemini")
PROFILE_DIR_CHATGPT = os.path.join(os.path.dirname(__file__), "browser_profiles", "chatgpt")

# Timing
BETWEEN_MESSAGES_WAIT = 2
MAX_RESPONSE_WAIT = 600
COMPLETION_GRACE_WAIT = 3
RESPONSE_STABLE_WAIT = 5


# ==============================================================================
# CompletionDetector (from multi_llm_orchestrator/browser/detector.py)
# ==============================================================================

class CompletionDetector:
    def __init__(self, page):
        self.page = page

    async def text_stable(self, js_expr: str, stable_seconds: int = 5) -> bool:
        last_text = None
        stable = 0
        while stable < stable_seconds:
            try:
                text = await self.page.evaluate(js_expr)
                text = (text or "").strip()
            except Exception:
                text = ""
            if text and text == last_text:
                stable += 1
            else:
                stable = 0
                last_text = text
            await asyncio.sleep(1)
        return True

    async def count_chatgpt_copy_buttons(self) -> int:
        return await self.page.evaluate("""
        () => {
            const buttons = document.querySelectorAll(
              'button[data-testid="copy-turn-action-button"], button[aria-label="Copy"]'
            );
            let assistantCount = 0;
            for (const btn of buttons) {
                let el = btn;
                let isAssistant = false;
                for (let i = 0; i < 15; i++) {
                    if (!el.parentElement) break;
                    el = el.parentElement;
                    if (el.querySelector('[data-message-author-role="assistant"]')) {
                        isAssistant = true;
                        break;
                    }
                    if (el.tagName === 'ARTICLE') break;
                }
                if (isAssistant) assistantCount++;
            }
            return assistantCount;
        }
        """)

    async def count_chatgpt_turns(self) -> int:
        return await self.page.evaluate("""
        () => {
            const textMsgs = document.querySelectorAll('[data-message-author-role="assistant"]');
            const agentTurns = document.querySelectorAll('.agent-turn');
            const articles = new Set();
            for (const el of [...textMsgs, ...agentTurns]) {
                let cur = el;
                for (let i = 0; i < 15; i++) {
                    if (!cur.parentElement) break;
                    cur = cur.parentElement;
                    if (cur.tagName === 'ARTICLE') {
                        articles.add(cur);
                        break;
                    }
                }
            }
            return articles.size;
        }
        """)

    async def latest_chatgpt_turn_has_image(self) -> bool:
        return await self.page.evaluate("""
        () => {
            const articles = document.querySelectorAll('article');
            if (!articles.length) return false;
            const last = articles[articles.length - 1];
            if (last.querySelector('img[alt="Generated image"]')) return true;
            if (last.querySelector('div[id^="image-"] img')) return true;
            return false;
        }
        """)


# ==============================================================================
# Gemini Browser Controller
# ==============================================================================

GEMINI_TEXTAREA = "rich-textarea .ql-editor"
GEMINI_RESPONSE_SELECTORS = ["model-response-text", ".model-response-text", "message-content model-response-text"]
GEMINI_SEND_CANDIDATES = ['button[aria-label*="Send" i]', 'button[mattooltip*="Send" i]', 'button.send-button', '.send-button button', 'button[type="submit"]']
GEMINI_STOP_CANDIDATES = ['button[aria-label*="Stop" i]', 'button[mattooltip*="Stop" i]', 'button:has-text("Stop")']
GEMINI_FEEDBACK_CANDIDATES = ['button[aria-label*="Good response" i]', 'button[aria-label*="Bad response" i]', 'button[aria-label*="Thumbs up" i]', 'button[aria-label*="Thumbs down" i]']


class GeminiBridge:
    """Gemini DOM controller — ported from GeminiBrowser."""

    def __init__(self, page):
        self.page = page

    async def select_model(self, model_name: str = "思考型"):
        """Select a Gemini model via the mode picker dropdown.
        Options: '快捷' (Flash), '思考型' (Thinking), 'Pro'
        """
        print(f"[Gemini] Selecting model: {model_name}...")
        try:
            # Click the mode picker button
            picker_selectors = [
                'button[aria-label*="模式挑選器"]',
                'button[aria-label*="mode picker"]',
                'button[aria-label*="model"]',
                '.input-area-switch',
            ]
            clicked = False
            for sel in picker_selectors:
                try:
                    loc = self.page.locator(sel).first
                    if await loc.is_visible():
                        await loc.click()
                        clicked = True
                        break
                except Exception:
                    pass

            if not clicked:
                print("[Gemini] ⚠️ Could not find model picker button.")
                return False

            # Wait for dropdown menu to appear
            await asyncio.sleep(1)

            # Click the target model option
            model_btn = self.page.locator(f'button:has-text("{model_name}")').first
            try:
                await model_btn.wait_for(state="visible", timeout=5000)
                await model_btn.click()
                print(f"[Gemini] ✅ Model switched to: {model_name}")
                await asyncio.sleep(1)
                return True
            except Exception:
                print(f"[Gemini] ⚠️ Model '{model_name}' not found in dropdown.")
                # Click elsewhere to close dropdown
                await self.page.keyboard.press("Escape")
                return False

        except Exception as e:
            print(f"[Gemini] ⚠️ Model selection error: {e}")
            return False

    async def count_response_nodes(self) -> int:
        total = 0
        for sel in GEMINI_RESPONSE_SELECTORS:
            try:
                count = await self.page.locator(sel).count()
                if count > total:
                    total = count
            except Exception:
                pass
        return total

    async def send_and_wait(self, prompt: str) -> str:
        pre_count = await self.count_response_nodes()

        editor = self.page.locator(GEMINI_TEXTAREA).first
        await editor.wait_for(state="visible", timeout=30000)
        await editor.click()
        await editor.press("ControlOrMeta+A")
        await editor.press("Delete")
        await editor.fill(prompt)
        await asyncio.sleep(0.5)

        clicked = False
        for sel in GEMINI_SEND_CANDIDATES:
            locator = self.page.locator(sel)
            try:
                count = await locator.count()
            except Exception:
                count = 0
            for i in range(count):
                try:
                    btn = locator.nth(i)
                    if await btn.is_visible() and await btn.is_enabled():
                        await btn.click()
                        clicked = True
                        break
                except Exception:
                    pass
                if clicked:
                    break
        if not clicked:
            await editor.press("Enter")

        print("[Gemini] ✉️ Prompt sent...")
        await self._wait_for_completion(pre_count)
        return await self._get_latest_response()

    async def _wait_for_completion(self, pre_count=0):
        await asyncio.sleep(BETWEEN_MESSAGES_WAIT)
        timeout_ms = MAX_RESPONSE_WAIT * 1000
        new_response_seen = False
        stop_seen = False
        elapsed = 0

        while elapsed < timeout_ms:
            if not new_response_seen:
                if await self.count_response_nodes() > pre_count:
                    new_response_seen = True

            for sel in GEMINI_STOP_CANDIDATES:
                try:
                    if await self.page.locator(sel).first.is_visible():
                        stop_seen = True
                        break
                except Exception:
                    pass

            stop_hidden = True
            for sel in GEMINI_STOP_CANDIDATES:
                try:
                    if await self.page.locator(sel).first.is_visible():
                        stop_hidden = False
                        break
                except Exception:
                    pass

            if new_response_seen:
                if (stop_seen and stop_hidden and (feedback_seen or send_ready)) or \
                   (not stop_seen and (feedback_seen or send_ready)):
                    await asyncio.sleep(COMPLETION_GRACE_WAIT)
                    response_css = ", ".join(GEMINI_RESPONSE_SELECTORS)
                    ok = await CompletionDetector(self.page).text_stable(f"""
                    () => {{
                        const nodes = document.querySelectorAll('{response_css}');
                        if (!nodes.length) return '';
                        return nodes[nodes.length - 1].innerText || '';
                    }}
                    """, stable_seconds=RESPONSE_STABLE_WAIT)
                    if ok:
                        print("[Gemini] ✅ Generation complete.")
                        return

            await asyncio.sleep(1)
            elapsed += 1000
        print("[Gemini] ⚠️ Timeout.")

    async def _get_latest_response(self) -> str:
        for sel in GEMINI_RESPONSE_SELECTORS:
            try:
                elements = await self.page.query_selector_all(sel)
                if elements:
                    return (await elements[-1].inner_text()).strip()
            except Exception:
                pass
        return "[No response]"


# ==============================================================================
# ChatGPT Browser Controller
# ==============================================================================

CHATGPT_TEXTAREA = "#prompt-textarea"
CHATGPT_STOP_SELECTORS = ['button[data-testid="stop-button"]', 'button[aria-label="Stop generating"]', 'button[aria-label="Stop streaming"]', 'button:has-text("Stop")']
CHATGPT_RESPONSE_SELECTORS = ['div[data-message-author-role="assistant"] .markdown', 'div[data-message-author-role="assistant"] .prose', '.agent-turn .markdown', '.markdown.prose']


class ChatGPTBridge:
    """ChatGPT DOM controller — sends prompts inside AUTO_LLM_jj project."""

    def __init__(self, page):
        self.page = page

    async def navigate_to_project(self):
        """Navigate to the project page and wait for the chat input to be ready."""
        await self.page.goto(CHATGPT_PROJECT_URL)
        await self.page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(3)
        print("[ChatGPT] ✅ Navigated to AUTO_LLM_jj project.")

    async def _find_textarea(self):
        """Find the input textarea — project page may use different selectors."""
        selectors = [
            CHATGPT_TEXTAREA,                             # #prompt-textarea
            'div[contenteditable="true"]',                # contenteditable fallback
            'textarea',                                   # generic textarea
            'div[data-placeholder]',                      # placeholder-based
        ]
        for sel in selectors:
            try:
                el = await self.page.wait_for_selector(sel, timeout=5000)
                if el:
                    return el
            except Exception:
                pass
        return None

    async def send_and_wait(self, prompt: str) -> str:
        detector = CompletionDetector(self.page)
        pre_turns = await detector.count_chatgpt_turns()
        pre_copy = await detector.count_chatgpt_copy_buttons()

        textarea = await self._find_textarea()
        if not textarea:
            return "Error: Could not find ChatGPT input field."
        await textarea.click()
        await textarea.fill("")
        await textarea.fill(prompt)
        await asyncio.sleep(0.5)

        try:
            send_btn = self.page.locator('button[data-testid="send-button"]').first
            if await send_btn.is_visible() and await send_btn.is_enabled():
                await send_btn.click()
            else:
                await textarea.press("Enter")
        except Exception:
            await textarea.press("Enter")

        print("[ChatGPT] ✉️ Prompt sent...")
        await self._wait_for_completion(pre_turns, pre_copy)
        response = await self._get_latest_response()
        
        # Navigate back to project root so the next prompt creates a NEW conversation
        # instead of infinitely extending this one.
        await self.navigate_to_project()
        return response

    async def _wait_for_completion(self, pre_turns=0, pre_copy=0):
        await asyncio.sleep(BETWEEN_MESSAGES_WAIT)
        detector = CompletionDetector(self.page)
        timeout_ms = MAX_RESPONSE_WAIT * 1000
        stop_seen = False
        stop_disappeared = False
        elapsed = 0

        while elapsed < timeout_ms:
            stop_visible_now = False
            for sel in CHATGPT_STOP_SELECTORS:
                try:
                    if await self.page.locator(sel).first.is_visible():
                        stop_visible_now = True
                        stop_seen = True
                        break
                except Exception:
                    pass

            if stop_seen and not stop_visible_now:
                stop_disappeared = True

            if stop_visible_now:
                await asyncio.sleep(1)
                elapsed += 1000
                continue

            # Primary signal: new copy button
            if await detector.count_chatgpt_copy_buttons() > pre_copy:
                await asyncio.sleep(2)
                print("[ChatGPT] ✅ Generation complete (copy button).")
                return

            # Image turn
            if await detector.latest_chatgpt_turn_has_image():
                await asyncio.sleep(2)
                print("[ChatGPT] ✅ Generation complete (image).")
                return

            # Turn count + stop disappeared
            current_turns = await detector.count_chatgpt_turns()
            if current_turns > pre_turns and stop_disappeared:
                await asyncio.sleep(COMPLETION_GRACE_WAIT)

                if await detector.count_chatgpt_copy_buttons() > pre_copy:
                    print("[ChatGPT] ✅ Generation complete.")
                    return

                # Verify stop hasn't come back (thinking → generating two-phase)
                stop_back = False
                for sel in CHATGPT_STOP_SELECTORS:
                    try:
                        if await self.page.locator(sel).first.is_visible():
                            stop_back = True
                            break
                    except Exception:
                        pass

                if stop_back:
                    stop_disappeared = False
                    await asyncio.sleep(1)
                    elapsed += 1000
                    continue

                # Final fallback: text stability
                ok = await detector.text_stable("""
                () => {
                    const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
                    if (msgs.length) return msgs[msgs.length - 1].innerText || '';
                    const agents = document.querySelectorAll('.agent-turn');
                    if (agents.length) return agents[agents.length - 1].innerText || '';
                    return '';
                }
                """, stable_seconds=RESPONSE_STABLE_WAIT)
                if ok:
                    print("[ChatGPT] ✅ Generation complete (text stable).")
                    return

            await asyncio.sleep(1)
            elapsed += 1000

        print("[ChatGPT] ⚠️ Timeout.")

    async def _get_latest_response(self) -> str:
        for sel in CHATGPT_RESPONSE_SELECTORS:
            try:
                elements = await self.page.query_selector_all(sel)
                if elements:
                    return (await elements[-1].inner_text()).strip()
            except Exception:
                pass
        return "[No response]"


# ==============================================================================
# HeadlessAIBridge — Manages Both LLMs
# ==============================================================================

class HeadlessAIBridge:
    def __init__(self):
        self.playwright = None
        self.gemini_ctx = None
        self.chatgpt_ctx = None
        self.gemini = None
        self.chatgpt = None

    async def _launch_context(self, profile_dir: str):
        return await self.playwright.chromium.launch_persistent_context(
            user_data_dir=profile_dir, headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled",
                   # "--window-position=-32000,-32000",  # Testing mode: visible
                   "--start-maximized", "--no-first-run", "--no-default-browser-check"],
            ignore_default_args=["--enable-automation"],
        )

    async def initialize(self):
        self.playwright = await async_playwright().start()
        print("[Headless Bridge] Launching dual-LLM contexts...")

        for profile_dir in [PROFILE_DIR_GEMINI, PROFILE_DIR_CHATGPT]:
            os.makedirs(profile_dir, exist_ok=True)

        # Launch Gemini
        try:
            self.gemini_ctx = await self._launch_context(PROFILE_DIR_GEMINI)
            gemini_page = await self.gemini_ctx.new_page()
            await gemini_page.goto(GEMINI_URL)
            await gemini_page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(3)  # Wait for full render
            self.gemini = GeminiBridge(gemini_page)
            # Auto-select 思考型 (Thinking) to save Pro quota
            await self.gemini.select_model("思考型")
            print("[Headless Bridge] ✅ Gemini connected (思考型).")
        except Exception as e:
            print(f"[Headless Bridge] ❌ Gemini failed: {e}")

        # Launch ChatGPT — navigate to AUTO_LLM_jj project
        try:
            self.chatgpt_ctx = await self._launch_context(PROFILE_DIR_CHATGPT)
            chatgpt_page = await self.chatgpt_ctx.new_page()
            self.chatgpt = ChatGPTBridge(chatgpt_page)
            await self.chatgpt.navigate_to_project()
            print("[Headless Bridge] ✅ ChatGPT connected (AUTO_LLM_jj).")
        except Exception as e:
            print(f"[Headless Bridge] ⚠️ ChatGPT failed: {e}")
            print("[Headless Bridge] ℹ️ Run 'python login_chatgpt.py' to log in.")

        return self.gemini is not None or self.chatgpt is not None

    async def ask_gemini(self, prompt: str) -> str:
        if not self.gemini:
            return "Error: Gemini not initialized."
        try:
            return await self.gemini.send_and_wait(prompt)
        except Exception as e:
            return f"Gemini error: {e}"

    async def ask_chatgpt(self, prompt: str) -> str:
        if not self.chatgpt:
            return "Error: ChatGPT not initialized."
        try:
            return await self.chatgpt.send_and_wait(prompt)
        except Exception as e:
            return f"ChatGPT error: {e}"

    async def ask_ai(self, prompt: str, prefer: str = "gemini") -> str:
        """Smart routing: try preferred LLM first, fall back to the other."""
        if prefer == "chatgpt" and self.chatgpt:
            result = await self.ask_chatgpt(prompt)
            if not result.startswith("Error") and not result.startswith("ChatGPT error"):
                return result
            if self.gemini:
                return await self.ask_gemini(prompt)
            return result
        else:
            if self.gemini:
                result = await self.ask_gemini(prompt)
                if not result.startswith("Error") and not result.startswith("Gemini error"):
                    return result
            if self.chatgpt:
                return await self.ask_chatgpt(prompt)
            return "Error: No LLM available."

    async def shutdown(self):
        if self.gemini_ctx:
            await self.gemini_ctx.close()
        if self.chatgpt_ctx:
            await self.chatgpt_ctx.close()
        if self.playwright:
            await self.playwright.stop()


# ==============================================================================
# HeadlessWorker — Background Thread (API for SystemEngine)
# ==============================================================================

class HeadlessWorker(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.task_queue = queue.Queue()
        self.bridge = HeadlessAIBridge()
        self.is_ready = False

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._async_loop())

    async def _async_loop(self):
        self.is_ready = await self.bridge.initialize()
        if not self.is_ready:
            print("[Headless Worker] ❌ Failed to start bridge.")
            return

        while True:
            try:
                if not self.task_queue.empty():
                    prompt, callback, prefer = self.task_queue.get_nowait()
                    print(f"[Headless Worker] 🔧 Processing prompt ({len(prompt)} chars) via {prefer}...")
                    result = await self.bridge.ask_ai(prompt, prefer=prefer)
                    if callback:
                        try:
                            callback(result)
                        except Exception as cb_err:
                            print(f"[Headless Worker] Callback error: {cb_err}")
                    self.task_queue.task_done()
                else:
                    await asyncio.sleep(0.5)
            except Exception as e:
                print(f"[Headless Worker] Event loop error: {e}")
                await asyncio.sleep(1)

    def submit_prompt(self, prompt: str, callback=None, prefer="gemini"):
        if not self.is_ready:
            print("[Headless Worker] Warning: Bridge not ready. Queuing anyway.")
        self.task_queue.put((prompt, callback, prefer))

    def ask_sync(self, prompt: str, prefer="gemini", timeout=MAX_RESPONSE_WAIT + 60) -> str:
        if not self.is_ready:
            return "Error: Worker starting up or failed."
        res_queue = queue.Queue()
        self.submit_prompt(prompt, lambda res: res_queue.put(res), prefer=prefer)
        try:
            return res_queue.get(timeout=timeout)
        except queue.Empty:
            return "Error: Queue timeout waiting for LLM response."
