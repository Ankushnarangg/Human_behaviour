import asyncio
import random
import numpy as np

# Global last mouse position, starting at (100, 100) arbitrarily
_last_pos = (100, 100)

def bezier_quad(t, p0, p1, p2):
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2

def bezier_curve_points(start, control, end, steps=30):
    points = []
    for i in range(steps + 1):
        t = i / steps
        x = bezier_quad(t, start[0], control[0], end[0])
        y = bezier_quad(t, start[1], control[1], end[1])
        points.append((x, y))
    return points

def catmull_rom_spline(P0, P1, P2, P3, steps=20):
    points = []
    for i in range(steps + 1):
        t = i / steps
        t2 = t * t
        t3 = t2 * t
        x = 0.5 * ((2 * P1[0]) + (-P0[0] + P2[0]) * t + 
                   (2*P0[0] - 5*P1[0] + 4*P2[0] - P3[0]) * t2 + 
                   (-P0[0] + 3*P1[0] - 3*P2[0] + P3[0]) * t3)
        y = 0.5 * ((2 * P1[1]) + (-P0[1] + P2[1]) * t + 
                   (2*P0[1] - 5*P1[1] + 4*P2[1] - P3[1]) * t2 + 
                   (-P0[1] + 3*P1[1] - 3*P2[1] + P3[1]) * t3)
        points.append((x, y))
    return points

async def move_mouse_human_like(page, start=None, end=None, steps=30, method="bezier"):
    """
    Move mouse from start to end with smooth human-like motion.
    - start: (x,y) tuple, defaults to last known position.
    - end: (x,y) tuple, required.
    - steps: number of intermediate points.
    - method: "bezier", "spline", or "linear"
    """
    global _last_pos
    if start is None:
        start = _last_pos
    if end is None:
        raise ValueError("End position must be provided.")

    x0, y0 = start
    x1, y1 = end

    if method == "bezier":
        # Control point randomized near midpoint for natural curve
        cx = (x0 + x1) / 2 + random.uniform(-50, 50)
        cy = (y0 + y1) / 2 + random.uniform(-50, 50)
        points = bezier_curve_points((x0, y0), (cx, cy), (x1, y1), steps=steps)
    elif method == "spline":
        # Four points for Catmull-Rom spline
        P0 = (x0 - 50, y0)
        P1 = (x0, y0)
        P2 = (x1, y1)
        P3 = (x1 + 50, y1)
        points = catmull_rom_spline(P0, P1, P2, P3, steps=steps)
    else:
        # Linear fallback
        points = [(x0 + (x1 - x0) * t / steps, y0 + (y1 - y0) * t / steps) for t in range(steps + 1)]

    for (x, y) in points:
        await page.mouse.move(x, y)
        await asyncio.sleep(random.uniform(0.01, 0.03))

    _last_pos = (x1, y1)

async def human_hover(page, element, method="bezier"):
    """
    Move mouse to center of element and hover.
    """
    box = await element.bounding_box()
    if not box:
        print("[Hover] Element not found or invisible.")
        return
    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2
    await move_mouse_human_like(page, end=(x, y), method=method)
    await asyncio.sleep(random.uniform(0.3, 0.7))

async def human_click(page, element, click_type="single", method="bezier"):
    """
    Move mouse to center of element and click.
    click_type: "single", "double", or "right"
    """
    box = await element.bounding_box()
    if not box:
        print("[Click] Element not found or invisible.")
        return
    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2
    await move_mouse_human_like(page, end=(x, y), method=method)
    await asyncio.sleep(random.uniform(0.1, 0.3))

    if click_type == "single":
        await page.mouse.click(x, y, delay=random.randint(50, 150))
    elif click_type == "double":
        await page.mouse.dblclick(x, y, delay=random.randint(50, 150))
    elif click_type == "right":
        await page.mouse.click(x, y, button="right", delay=random.randint(50, 150))
    else:
        await page.mouse.click(x, y, delay=random.randint(50, 150))

    await asyncio.sleep(random.uniform(0.3, 0.7))

async def human_scroll(page, distance, steps=20):
    """
    Scroll vertically by distance in steps.
    Positive distance scrolls down, negative scrolls up.
    """
    step_distance = distance / steps
    for _ in range(steps):
        await page.mouse.wheel(0, step_distance)
        await asyncio.sleep(random.uniform(0.01, 0.05))

async def human_idle(duration_range=(1, 3)):
    """
    Idle for a random time in duration_range (seconds).
    """
    wait_time = random.uniform(*duration_range)
    await asyncio.sleep(wait_time)

async def mouse_wander(page, radius=30, count=4, method='bezier'):
    """
    Move mouse randomly around last position within radius.
    """
    global _last_pos
    x0, y0 = _last_pos
    points = []
    for _ in range(count):
        angle = random.uniform(0, 2 * np.pi)
        r = random.uniform(5, radius)
        x = x0 + r * np.cos(angle)
        y = y0 + r * np.sin(angle)
        points.append((x, y))
    for pt in points:
        await move_mouse_human_like(page, _last_pos, pt, steps=random.randint(15, 35), method=method)
        await asyncio.sleep(random.uniform(0.05, 0.2))

async def idle_behavior(page, idle_time_range=(1, 5)):
    """
    Random small mouse moves and pauses simulating idle behavior.
    """
    total_time = random.uniform(*idle_time_range)
    elapsed = 0
    global _last_pos
    while elapsed < total_time:
        dx = random.uniform(-10, 10)
        dy = random.uniform(-10, 10)
        target = (_last_pos[0] + dx, _last_pos[1] + dy)
        await move_mouse_human_like(page, _last_pos, target, steps=random.randint(10, 20), method='bezier')
        wait = random.uniform(0.5, 1.5)
        await asyncio.sleep(wait)
        elapsed += wait + 0.1
