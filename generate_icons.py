#!/usr/bin/env python3
"""Generate Checkmate GP app icons: checkered flag + chess knight."""

from PIL import Image, ImageDraw

GOLD = (212, 175, 55)
DARK_GOLD = (154, 123, 44)
BLACK = (0, 0, 0)
NEAR_BLACK = (20, 20, 20)
WHITE_GOLD = (245, 208, 96)

def draw_checkered_bg(draw, size, rows=8, cols=8):
    """Draw a checkered flag pattern."""
    sq_w = size / cols
    sq_h = size / rows
    for r in range(rows):
        for c in range(cols):
            color = GOLD if (r + c) % 2 == 0 else BLACK
            x0, y0 = c * sq_w, r * sq_h
            draw.rectangle([x0, y0, x0 + sq_w, y0 + sq_h], fill=color)


def draw_knight(draw, cx, cy, scale):
    """Draw a chess knight silhouette centered at (cx, cy) with given scale.

    The knight is drawn as a polygon path, designed to be bold and recognizable.
    Coordinates are relative, scaled and translated to center.
    """
    # Knight silhouette points (designed on a 0-100 canvas, facing left)
    raw_points = [
        # Base
        (25, 90), (75, 90),
        # Right side going up
        (75, 82), (70, 75),
        # Back of neck / mane
        (72, 65), (73, 55), (72, 45), (68, 35),
        # Top of head / ears
        (62, 25), (58, 15), (54, 18), (55, 25),
        (52, 22), (48, 12), (44, 16), (46, 25),
        # Forehead
        (42, 28), (35, 32),
        # Nose bridge
        (28, 38), (22, 45),
        # Nose/mouth
        (18, 50), (20, 55), (25, 56),
        # Jaw/chin
        (28, 58), (30, 62),
        # Throat
        (28, 68), (25, 75), (25, 82),
    ]

    # Scale and translate
    points = []
    for x, y in raw_points:
        px = cx + (x - 50) * scale / 50
        py = cy + (y - 52) * scale / 50
        points.append((px, py))

    return points


def create_icon(size, filename):
    """Create a single icon at the given size."""
    img = Image.new('RGBA', (size, size), BLACK)
    draw = ImageDraw.Draw(img)

    # -- Checkered background --
    grid = 8
    draw_checkered_bg(draw, size, grid, grid)

    # -- Dark overlay circle behind the knight for contrast --
    center = size / 2
    radius = size * 0.38
    # Draw filled dark circle with semi-transparent overlay
    overlay = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        fill=(0, 0, 0, 210)
    )
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # -- Gold ring around the circle --
    ring_width = max(2, int(size * 0.012))
    for i in range(ring_width):
        draw.ellipse(
            [center - radius - i, center - radius - i,
             center + radius + i, center + radius + i],
            outline=GOLD
        )

    # -- Draw the knight --
    knight_scale = size * 0.32
    knight_cy = center + size * 0.02  # shift down slightly
    points = draw_knight(draw, center, knight_cy, knight_scale)

    # Outline (thick, dark)
    outline_width = max(2, int(size * 0.015))
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx * dx + dy * dy <= outline_width * outline_width:
                shifted = [(x + dx, y + dy) for x, y in points]
                draw.polygon(shifted, fill=DARK_GOLD)

    # Main knight body in gold
    draw.polygon(points, fill=GOLD)

    # Highlight edge (lighter gold on top portion)
    highlight_points = points[:len(points) // 2]
    if len(highlight_points) > 2:
        # Just add a subtle line along the top
        for i in range(len(highlight_points) - 1):
            draw.line(
                [highlight_points[i], highlight_points[i + 1]],
                fill=WHITE_GOLD, width=max(1, int(size * 0.006))
            )

    # Eye
    eye_x = center - knight_scale * 0.08
    eye_y = knight_cy - knight_scale * 0.38
    eye_r = max(2, int(size * 0.018))
    draw.ellipse(
        [eye_x - eye_r, eye_y - eye_r, eye_x + eye_r, eye_y + eye_r],
        fill=BLACK
    )

    # Convert to RGB for PNG (no alpha needed for app icons)
    final = Image.new('RGB', (size, size), BLACK)
    final.paste(img, mask=img.split()[3])
    final.save(filename, 'PNG')
    print(f"  Created {filename} ({size}x{size})")


def create_maskable_icon(size, filename):
    """Create a maskable icon with safe zone padding."""
    # Maskable icons need content within the inner 80% (safe zone)
    img = Image.new('RGBA', (size, size), BLACK)
    draw = ImageDraw.Draw(img)

    # Full checkered background
    draw_checkered_bg(draw, size, 8, 8)

    # Larger dark overlay for maskable (content is smaller)
    center = size / 2
    radius = size * 0.33  # slightly smaller for safe zone

    overlay = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        fill=(0, 0, 0, 210)
    )
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Gold ring
    ring_width = max(2, int(size * 0.012))
    for i in range(ring_width):
        draw.ellipse(
            [center - radius - i, center - radius - i,
             center + radius + i, center + radius + i],
            outline=GOLD
        )

    # Knight (smaller for safe zone)
    knight_scale = size * 0.27
    knight_cy = center + size * 0.02
    points = draw_knight(draw, center, knight_cy, knight_scale)

    outline_width = max(2, int(size * 0.015))
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx * dx + dy * dy <= outline_width * outline_width:
                shifted = [(x + dx, y + dy) for x, y in points]
                draw.polygon(shifted, fill=DARK_GOLD)

    draw.polygon(points, fill=GOLD)

    # Eye
    eye_x = center - knight_scale * 0.08
    eye_y = knight_cy - knight_scale * 0.38
    eye_r = max(2, int(size * 0.016))
    draw.ellipse(
        [eye_x - eye_r, eye_y - eye_r, eye_x + eye_r, eye_y + eye_r],
        fill=BLACK
    )

    final = Image.new('RGB', (size, size), BLACK)
    final.paste(img, mask=img.split()[3])
    final.save(filename, 'PNG')
    print(f"  Created {filename} ({size}x{size}) [maskable]")


if __name__ == '__main__':
    print("Generating Checkmate GP icons...")
    create_icon(512, 'icons/icon-512.png')
    create_icon(192, 'icons/icon-192.png')
    create_icon(180, 'icons/apple-touch-icon.png')
    create_icon(32, 'icons/favicon-32.png')
    create_maskable_icon(512, 'icons/icon-maskable-512.png')
    print("Done!")
