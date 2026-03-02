#!/usr/bin/env python3
"""Generate Checkmate GP app icons: dark bg, gold rounded rect, gold knight."""

from PIL import Image, ImageDraw

GOLD = (212, 175, 55)        # #D4AF37
DARK_GOLD = (154, 123, 44)
WHITE_GOLD = (245, 208, 96)
BLACK = (0, 0, 0)
CARBON = (10, 10, 10)        # inner fill of rounded rect


def draw_rounded_rect(draw, x0, y0, x1, y1, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    if fill:
        # Fill the main body
        draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
        draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
        # Fill the four corners
        draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)
        draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)
        draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)
        draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)
    if outline:
        # Draw the outline arcs and lines
        draw.arc([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([x0 + radius, y0, x1 - radius, y0], fill=outline, width=width)
        draw.line([x0 + radius, y1, x1 - radius, y1], fill=outline, width=width)
        draw.line([x0, y0 + radius, x0, y1 - radius], fill=outline, width=width)
        draw.line([x1, y0 + radius, x1, y1 - radius], fill=outline, width=width)


def get_knight_points(cx, cy, scale):
    """Return a refined chess knight silhouette."""
    # More refined knight shape on 0-100 canvas
    raw = [
        # Base (flat bottom)
        (28, 88), (72, 88),
        # Right base up
        (72, 82),
        # Back of body curving up into neck
        (68, 74), (70, 65), (72, 55),
        # Back of neck (elegant curve)
        (71, 48), (68, 40), (64, 33),
        # Top of head
        (60, 27),
        # Right ear
        (58, 18), (55, 14), (52, 18),
        # Between ears
        (51, 22),
        # Left ear
        (49, 14), (45, 12), (44, 18),
        # Forehead
        (44, 24), (40, 28),
        # Face / nose bridge
        (36, 33), (32, 38),
        # Snout
        (28, 43), (24, 48),
        # Nose tip / nostril area
        (22, 52), (24, 56),
        # Mouth / lip
        (28, 57), (30, 55),
        # Chin
        (32, 58),
        # Jaw line
        (34, 62), (32, 66),
        # Throat going down
        (30, 72), (28, 78), (28, 82),
    ]
    points = []
    for x, y in raw:
        px = cx + (x - 50) * scale / 50
        py = cy + (y - 50) * scale / 50
        points.append((px, py))
    return points


def create_icon(size, filename):
    """Create icon: black bg, gold rounded rect border, gold knight."""
    img = Image.new('RGB', (size, size), BLACK)
    draw = ImageDraw.Draw(img)

    # Rounded rectangle
    margin = int(size * 0.12)
    border_w = max(2, int(size * 0.014))
    corner_r = int(size * 0.14)

    # Fill the rounded rect with dark carbon
    draw_rounded_rect(draw,
                      margin, margin, size - margin, size - margin,
                      corner_r, fill=CARBON)

    # Gold border
    for i in range(border_w):
        draw_rounded_rect(draw,
                          margin - i, margin - i,
                          size - margin + i, size - margin + i,
                          corner_r + i, outline=GOLD, width=1)

    # Knight
    center = size / 2
    knight_scale = size * 0.30
    knight_cy = center + size * 0.01
    points = get_knight_points(center, knight_cy, knight_scale)

    # Dark outline for depth
    outline_w = max(2, int(size * 0.012))
    for dx in range(-outline_w, outline_w + 1):
        for dy in range(-outline_w, outline_w + 1):
            if dx * dx + dy * dy <= outline_w * outline_w:
                shifted = [(x + dx, y + dy) for x, y in points]
                draw.polygon(shifted, fill=DARK_GOLD)

    # Main gold body
    draw.polygon(points, fill=GOLD)

    # Eye
    eye_x = center - knight_scale * 0.10
    eye_y = knight_cy - knight_scale * 0.30
    eye_r = max(2, int(size * 0.016))
    draw.ellipse(
        [eye_x - eye_r, eye_y - eye_r, eye_x + eye_r, eye_y + eye_r],
        fill=CARBON
    )

    img.save(filename, 'PNG')
    print(f"  Created {filename} ({size}x{size})")


def create_maskable_icon(size, filename):
    """Maskable icon — content within inner 80% safe zone."""
    img = Image.new('RGB', (size, size), BLACK)
    draw = ImageDraw.Draw(img)

    # Larger margin for maskable safe zone
    margin = int(size * 0.18)
    border_w = max(2, int(size * 0.014))
    corner_r = int(size * 0.12)

    draw_rounded_rect(draw,
                      margin, margin, size - margin, size - margin,
                      corner_r, fill=CARBON)
    for i in range(border_w):
        draw_rounded_rect(draw,
                          margin - i, margin - i,
                          size - margin + i, size - margin + i,
                          corner_r + i, outline=GOLD, width=1)

    center = size / 2
    knight_scale = size * 0.24
    knight_cy = center + size * 0.01
    points = get_knight_points(center, knight_cy, knight_scale)

    outline_w = max(2, int(size * 0.012))
    for dx in range(-outline_w, outline_w + 1):
        for dy in range(-outline_w, outline_w + 1):
            if dx * dx + dy * dy <= outline_w * outline_w:
                shifted = [(x + dx, y + dy) for x, y in points]
                draw.polygon(shifted, fill=DARK_GOLD)

    draw.polygon(points, fill=GOLD)

    eye_x = center - knight_scale * 0.10
    eye_y = knight_cy - knight_scale * 0.30
    eye_r = max(2, int(size * 0.014))
    draw.ellipse(
        [eye_x - eye_r, eye_y - eye_r, eye_x + eye_r, eye_y + eye_r],
        fill=CARBON
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
