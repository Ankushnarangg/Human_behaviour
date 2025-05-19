human_mouse
A Python module to simulate natural, human-like mouse movements and interactions using Playwright.

Overview
human_mouse provides smooth, realistic mouse movements including hovering, clicking, scrolling, and idle wandering. It mimics human behavior with curved paths and randomized delays to help automation look more natural and less robotic.

Features
Smooth mouse movement with Bézier curves or spline paths.

Hover over elements naturally.

Click elements with single, double, or right clicks.

Scroll the page with gradual steps.

Idle behavior to simulate user inactivity with small random movements.

Mouse wandering for subtle cursor shifts.

Easy to customize start/end points and movement methods.

Installation
Install Playwright (if not installed):

bash
Copy
Edit
pip install playwright
playwright install
Save the human_mouse.py file in your project directory.

Import human_mouse in your script.

Usage
Here is a minimal example showing how to move the mouse smoothly and interact with a page element:

python
Copy
Edit
import asyncio
from playwright.async_api import async_playwright
import human_mouse

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://example.com")

        # Move mouse from (100, 100) to (400, 300) using spline curve
        await human_mouse.move_mouse_human_like(page, start=(100, 100), end=(400, 300), method="spline")

        # Hover over the first <h1> element
        element = await page.query_selector("h1")
        await human_mouse.human_hover(page, element)

        # Click the element with a single left click
        await human_mouse.human_click(page, element, click_type="single")

        await browser.close()

asyncio.run(run())
API Reference
move_mouse_human_like(page, start=None, end, steps=30, method="bezier")
Move mouse cursor smoothly from start to end.

page: Playwright page object.

start: Starting coordinates (x, y) (default: last mouse position).

end: Ending coordinates (x, y) (required).

steps: Number of intermediate movement steps.

method: Movement method; "bezier", "spline", or "linear".

human_hover(page, element, method="bezier")
Move mouse cursor to center of an element and hover.

page: Playwright page object.

element: Playwright element handle.

method: Movement method (default "bezier").

human_click(page, element, click_type="single", method="bezier")
Move mouse to element and perform a click.

page: Playwright page object.

element: Playwright element handle.

click_type: "single" (default), "double", or "right".

method: Movement method.

human_scroll(page, distance, steps=20)
Scroll vertically with gradual steps.

page: Playwright page object.

distance: Pixels to scroll (positive = down, negative = up).

steps: Number of scroll increments.

human_idle(duration_range=(1, 3))
Idle for a random duration to simulate user inactivity.

duration_range: Tuple specifying min and max idle time in seconds.

mouse_wander(page, radius=30, count=4, method='bezier')
Move mouse cursor randomly within a radius around last position.

page: Playwright page object.

radius: Max radius for wandering.

count: Number of wandering points.

method: Movement method.

idle_behavior(page, idle_time_range=(1, 5))
Simulate natural idle with random micro-movements and pauses.

page: Playwright page object.

idle_time_range: Tuple (min, max) seconds to idle.

Customization Tips
Adjust movement method between "bezier" (curved), "spline" (smooth), or "linear" (straight) to fit your desired behavior.

Use custom start and end coordinates for direct control over mouse movement.

Change steps to make movements faster or slower and more or less smooth.

Combine hover, click, and scroll calls to mimic complex human browsing patterns.

Use idle_behavior and mouse_wander to keep your automation session alive and natural-looking.

Notes
The module maintains the last mouse position internally for smooth chaining between movements.

Always provide a valid end coordinate or element for mouse movements.

Make sure your Playwright page is fully loaded and elements are visible before interacting.

License
MIT License © [Ankush Narang]