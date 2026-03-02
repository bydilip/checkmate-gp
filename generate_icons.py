#!/usr/bin/env python3
"""Generate Checkmate GP app icons: gold gradient bg, black knight."""

from PIL import Image, ImageDraw

GOLD_LIGHT = (212, 175, 55)   # #D4AF37
GOLD_DARK = (154, 123, 44)    # #9A7B2C
BLACK = (0, 0, 0)


def draw_rounded_rect_mask(size, radius):
    """Create a rounded-rectangle alpha mask."""
    mask = Image.new('L', (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return mask


def gold_gradient(size):
    """Create a 135-degree gold gradient matching the CSS shield."""
    img = Image.new('RGB', (size, size))
    for y in range(size):
        for x in range(size):
            # 135-degree gradient: top-left -> bottom-right
            t = (x + y) / (2 * size - 2)
            r = int(GOLD_LIGHT[0] + (GOLD_DARK[0] - GOLD_LIGHT[0]) * t)
            g = int(GOLD_LIGHT[1] + (GOLD_DARK[1] - GOLD_LIGHT[1]) * t)
            b = int(GOLD_LIGHT[2] + (GOLD_DARK[2] - GOLD_LIGHT[2]) * t)
            img.putpixel((x, y), (r, g, b))
    return img


def get_knight_points(cx, cy, scale):
    """Return a refined chess knight silhouette."""
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
    """Create icon: gold gradient rounded rect, black knight."""
    # Start with black background
    img = Image.new('RGB', (size, size), BLACK)

    # Create gold gradient rounded rect
    margin = int(size * 0.08)
    inner_size = size - 2 * margin
    corner_r = int(inner_size * 0.22)

    grad = gold_gradient(inner_size)
    mask = draw_rounded_rect_mask(inner_size, corner_r)
    img.paste(grad, (margin, margin), mask)

    # Black knight
    center = size / 2
    knight_scale = size * 0.30
    knight_cy = center + size * 0.01
    points = get_knight_points(center, knight_cy, knight_scale)

    draw = ImageDraw.Draw(img)
    draw.polygon(points, fill=BLACK)

    # Eye (gold, since knight is black)
    eye_x = center - knight_scale * 0.10
    eye_y = knight_cy - knight_scale * 0.30
    eye_r = max(2, int(size * 0.014))
    # Midpoint gold for the eye
    mid_gold = (
        (GOLD_LIGHT[0] + GOLD_DARK[0]) // 2,
        (GOLD_LIGHT[1] + GOLD_DARK[1]) // 2,
        (GOLD_LIGHT[2] + GOLD_DARK[2]) // 2,
    )
    draw.ellipse(
        [eye_x - eye_r, eye_y - eye_r, eye_x + eye_r, eye_y + eye_r],
        fill=mid_gold
    )

    img.save(filename, 'PNG')
    print(f"  Created {filename} ({size}x{size})")


def create_maskable_icon(size, filename):
    """Maskable icon — content within inner 80% safe zone."""
    img = Image.new('RGB', (size, size), BLACK)

    # Larger margin for maskable safe zone
    margin = int(size * 0.16)
    inner_size = size - 2 * margin
    corner_r = int(inner_size * 0.22)

    grad = gold_gradient(inner_size)
    mask = draw_rounded_rect_mask(inner_size, corner_r)
    img.paste(grad, (margin, margin), mask)

    center = size / 2
    knight_scale = size * 0.24
    knight_cy = center + size * 0.01
    points = get_knight_points(center, knight_cy, knight_scale)

    draw = ImageDraw.Draw(img)
    draw.polygon(points, fill=BLACK)

    eye_x = center - knight_scale * 0.10
    eye_y = knight_cy - knight_scale * 0.30
    eye_r = max(2, int(size * 0.012))
    mid_gold = (
        (GOLD_LIGHT[0] + GOLD_DARK[0]) // 2,
        (GOLD_LIGHT[1] + GOLD_DARK[1]) // 2,
        (GOLD_LIGHT[2] + GOLD_DARK[2]) // 2,
    )
    draw.ellipse(
        [eye_x - eye_r, eye_y - eye_r, eye_x + eye_r, eye_y + eye_r],
        fill=mid_gold
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
