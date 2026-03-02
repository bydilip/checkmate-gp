#!/usr/bin/env python3
"""Generate Checkmate GP app icons: gold gradient bg, premium black knight."""

from PIL import Image, ImageDraw
import math

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
            t = (x + y) / (2 * size - 2)
            r = int(GOLD_LIGHT[0] + (GOLD_DARK[0] - GOLD_LIGHT[0]) * t)
            g = int(GOLD_LIGHT[1] + (GOLD_DARK[1] - GOLD_LIGHT[1]) * t)
            b = int(GOLD_LIGHT[2] + (GOLD_DARK[2] - GOLD_LIGHT[2]) * t)
            img.putpixel((x, y), (r, g, b))
    return img


def bezier(p0, p1, p2, p3, steps=20):
    """Cubic bezier curve returning list of (x,y) points."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = u**3*p0[0] + 3*u**2*t*p1[0] + 3*u*t**2*p2[0] + t**3*p3[0]
        y = u**3*p0[1] + 3*u**2*t*p1[1] + 3*u*t**2*p2[1] + t**3*p3[1]
        pts.append((x, y))
    return pts


def get_premium_knight(cx, cy, scale):
    """Premium chess knight — classic Staunton style with smooth curves."""
    def p(x, y):
        return (cx + (x - 50) * scale / 50, cy + (y - 50) * scale / 50)

    pts = []

    # Wide stable base
    pts += [p(24, 90), p(76, 90)]

    # Right base rising into body
    pts += bezier(p(76, 90), p(76, 86), p(74, 82), p(72, 78), 8)

    # Back body — thick, solid rising curve
    pts += bezier(p(72, 78), p(70, 70), p(70, 62), p(68, 54), 12)

    # Back of neck — smooth powerful curve
    pts += bezier(p(68, 54), p(66, 46), p(63, 38), p(58, 32), 14)

    # Crown of head — rounded
    pts += bezier(p(58, 32), p(56, 29), p(54, 26), p(52, 24), 8)

    # Right ear — small, elegant
    pts += bezier(p(52, 24), p(52, 19), p(50, 16), p(48, 18), 6)

    # Left ear — small, elegant
    pts += bezier(p(48, 18), p(46, 15), p(44, 18), p(44, 22), 6)

    # Forehead — smooth dome
    pts += bezier(p(44, 22), p(42, 25), p(40, 28), p(38, 31), 8)

    # Face — elegant long nose
    pts += bezier(p(38, 31), p(34, 36), p(30, 42), p(26, 47), 12)

    # Muzzle — squared-off classic horse nose
    pts += bezier(p(26, 47), p(23, 51), p(21, 54), p(20, 57), 8)

    # Bottom of muzzle / lip
    pts += bezier(p(20, 57), p(21, 59), p(24, 60), p(27, 59), 6)

    # Chin notch
    pts += [p(27, 59), p(29, 57)]

    # Lower jaw
    pts += bezier(p(29, 57), p(31, 58), p(33, 60), p(34, 63), 6)

    # Jaw line sweeping down
    pts += bezier(p(34, 63), p(35, 67), p(34, 72), p(32, 76), 10)

    # Throat to chest
    pts += bezier(p(32, 76), p(30, 80), p(28, 84), p(26, 86), 8)

    # Close to base
    pts += bezier(p(26, 86), p(25, 88), p(24, 89), p(24, 90), 4)

    return pts


def get_mane_points(cx, cy, scale):
    """Mane detail — elegant curve along back of neck."""
    def p(x, y):
        return (cx + (x - 50) * scale / 50, cy + (y - 50) * scale / 50)

    pts = []
    # From behind the ear down the neck
    pts += bezier(p(50, 24), p(54, 30), p(58, 38), p(60, 46), 12)
    pts += bezier(p(60, 46), p(62, 52), p(63, 58), p(64, 64), 10)
    return pts


def create_icon(size, filename):
    """Create icon: gold gradient rounded rect, premium black knight."""
    img = Image.new('RGB', (size, size), BLACK)

    # Gold gradient rounded rect
    margin = int(size * 0.08)
    inner_size = size - 2 * margin
    corner_r = int(inner_size * 0.22)

    grad = gold_gradient(inner_size)
    mask = draw_rounded_rect_mask(inner_size, corner_r)
    img.paste(grad, (margin, margin), mask)

    # Premium knight silhouette
    center = size / 2
    knight_scale = size * 0.32
    knight_cy = center + size * 0.01
    points = get_premium_knight(center, knight_cy, knight_scale)

    draw = ImageDraw.Draw(img)
    draw.polygon(points, fill=BLACK)

    # Eye
    eye_x = center - knight_scale * 0.14
    eye_y = knight_cy - knight_scale * 0.32
    eye_r = max(2, int(size * 0.016))
    mid_gold = (
        (GOLD_LIGHT[0] + GOLD_DARK[0]) // 2,
        (GOLD_LIGHT[1] + GOLD_DARK[1]) // 2,
        (GOLD_LIGHT[2] + GOLD_DARK[2]) // 2,
    )
    draw.ellipse(
        [eye_x - eye_r, eye_y - eye_r, eye_x + eye_r, eye_y + eye_r],
        fill=mid_gold
    )

    # Mane detail line
    mane = get_mane_points(center, knight_cy, knight_scale)
    mane_width = max(2, int(size * 0.006))
    for i in range(len(mane) - 1):
        draw.line([mane[i], mane[i+1]], fill=mid_gold, width=mane_width)

    img.save(filename, 'PNG')
    print(f"  Created {filename} ({size}x{size})")


def create_maskable_icon(size, filename):
    """Maskable icon — content within inner 80% safe zone."""
    img = Image.new('RGB', (size, size), BLACK)

    margin = int(size * 0.16)
    inner_size = size - 2 * margin
    corner_r = int(inner_size * 0.22)

    grad = gold_gradient(inner_size)
    mask = draw_rounded_rect_mask(inner_size, corner_r)
    img.paste(grad, (margin, margin), mask)

    center = size / 2
    knight_scale = size * 0.26
    knight_cy = center + size * 0.01
    points = get_premium_knight(center, knight_cy, knight_scale)

    draw = ImageDraw.Draw(img)
    draw.polygon(points, fill=BLACK)

    eye_x = center - knight_scale * 0.14
    eye_y = knight_cy - knight_scale * 0.32
    eye_r = max(2, int(size * 0.014))
    mid_gold = (
        (GOLD_LIGHT[0] + GOLD_DARK[0]) // 2,
        (GOLD_LIGHT[1] + GOLD_DARK[1]) // 2,
        (GOLD_LIGHT[2] + GOLD_DARK[2]) // 2,
    )
    draw.ellipse(
        [eye_x - eye_r, eye_y - eye_r, eye_x + eye_r, eye_y + eye_r],
        fill=mid_gold
    )

    mane = get_mane_points(center, knight_cy, knight_scale)
    mane_width = max(2, int(size * 0.005))
    for i in range(len(mane) - 1):
        draw.line([mane[i], mane[i+1]], fill=mid_gold, width=mane_width)

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
