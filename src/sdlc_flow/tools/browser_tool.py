from crewai_tools import BaseTool
from playwright.sync_api import sync_playwright
from typing import Optional


class BrowserTool(BaseTool):
    name: str = "Browser Tool"
    description: str = "Uses Playwright to interact with web applications for QA verification."

    def _run(self, url: str, action: str, selector: Optional[str] = None, text: Optional[str] = None) -> str:
        """Runs a browser action."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url)
                if action == "click" and selector:
                    page.click(selector)
                elif action == "fill" and selector and text:
                    page.fill(selector, text)
                elif action == "assert_text" and text:
                    content = page.content()
                    if text in content:
                        return f"Success: Text '{text}' found on {url}"
                    else:
                        return f"Failure: Text '{text}' NOT found on {url}"
                
                return f"Action '{action}' executed successfully on {url}"
            except Exception as e:
                return f"Browser action failed: {str(e)}"
            finally:
                browser.close()
