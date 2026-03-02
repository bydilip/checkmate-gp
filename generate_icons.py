#!/usr/bin/env python3
"""Generate Checkmate GP app icons: plain carbon background + gold knight."""

from PIL import Image, ImageDraw

GOLD = (212, 175, 55)        # #D4AF37
DARK_GOLD = (154, 123, 44)   # darker gold for outline
WHITE_GOLD = (245, 208, 96)  # highlight
CARBON_LIGHT = (34, 34, 34)  # #222222 --carbon-light
CARBON_EYE = (34, 34, 34)    # same as bg for eye cutout


def draw_knight(cx, cy, scale):
    """Return chess knight silhouette points centered at (cx, cy)."""
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
    points = []
    for x, y in raw_points:
        px = cx + (x - 50) * scale / 50
        py = cy + (y - 52) * scale / 50
        points.append((px, py))
    return points


def create_icon(size, filename):
    """Create a plain icon: carbon-light bg + gold knight."""
    img = Image.new('RGB', (size, size), CARBON_LIGHT)
    draw = ImageDraw.Draw(img)

    center = size / 2
    knight_scale = size * 0.40  # big and bold
    knight_cy = center + size * 0.02

    points = draw_knight(center, knight_cy, knight_scale)

    # Dark gold outline for depth
    outline_w = max(2, int(size * 0.018))
    for dx in range(-outline_w, outline_w + 1):
        for dy in range(-outline_w, outline_w + 1):
            if dx * dx + dy * dy <= outline_w * outline_w:
                shifted = [(x + dx, y + dy) for x, y in points]
                draw.polygon(shifted, fill=DARK_GOLD)

    # Main gold knight
    draw.polygon(points, fill=GOLD)

    # Subtle highlight along top edge
    highlight_pts = points[:len(points) // 2]
    if len(highlight_pts) > 2:
        for i in range(len(highlight_pts) - 1):
            draw.line(
                [highlight_pts[i], highlight_pts[i + 1]],
                fill=WHITE_GOLD, width=max(1, int(size * 0.008))
            )

    # Eye (cut out in background color)
    eye_x = center - knight_scale * 0.08
    eye_y = knight_cy - knight_scale * 0.38
    eye_r = max(2, int(size * 0.02))
    draw.ellipse(
        [eye_x - eye_r, eye_y - eye_r, eye_x + eye_r, eye_y + eye_r],
        fill=CARBON_LIGHT
    )

    img.save(filename, 'PNG')
    print(f"  Created {filename} ({size}x{size})")


def create_maskable_icon(size, filename):
    """Create maskable icon with safe-zone padding."""
    img = Image.new('RGB', (size, size), CARBON_LIGHT)
    draw = ImageDraw.Draw(img)

    center = size / 2
    knight_scale = size * 0.33  # smaller for safe zone
    knight_cy = center + size * 0.02

    points = draw_knight(center, knight_cy, knight_scale)

    outline_w = max(2, int(size * 0.018))
    for dx in range(-outline_w, outline_w + 1):
        for dy in range(-outline_w, outline_w + 1):
            if dx * dx + dy * dy <= outline_w * outline_w:
                shifted = [(x + dx, y + dy) for x, y in points]
                draw.polygon(shifted, fill=DARK_GOLD)

    draw.polygon(points, fill=GOLD)

    eye_x = center - knight_scale * 0.08
    eye_y = knight_cy - knight_scale * 0.38
    eye_r = max(2, int(size * 0.018))
    draw.ellipse(
        [eye_x - eye_r, eye_y - eye_r, eye_x + eye_r, eye_y + eye_r],
        fill=CARBON_LIGHT
    )

    img.save(filename, 'PNG')
    print(f"  Created {filename} ({size}x{size}) [maskable]")


if __name__ == '__main__':
    print("Generating Checkmate GP icons...")
    create_icon(512, 'icons/icon-512.png')
    create_icon(192, 'icons/icon-192.png')
    create_icon(180, 'icons/apple-touch-icon.png')
    create_icon(32, 'icons/favicon-32.png')
    create_maskable_icon(512, 'icons/icon-maskable-512.png')
    print("Done!")
