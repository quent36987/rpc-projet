import fileinput
import math
import argparse
import os
import platform
import subprocess
import sys
import tempfile


class Rgb:
    def __init__(self, r, g, b, a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def lighten(self, factor):
        return Cmyk.from_rgb(self).lighten(factor).to_rgba()

    def darken(self, factor):
        return Cmyk.from_rgb(self).darken(factor).to_rgba()

    def __getitem__(self, item):
        if item == 0:
            return self.r
        elif item == 1:
            return self.g
        elif item == 2:
            return self.b
        elif item == 3:
            return self.a
        else:
            raise IndexError("Rgb index out of range")

    def __str__(self):
        def fmt(channel):
            return int(channel * 255)

        return f"Rgb({fmt(self.r)}, {fmt(self.g)}, {fmt(self.b)}, {fmt(self.a)})"


class Cmyk:
    def __init__(self, c, m, y, k):
        self.c = c
        self.m = m
        self.y = y
        self.k = k

    @staticmethod
    def from_rgb(rgb):
        (r, g, b, _) = rgb

        k = 1.0 - max(r, g, b)
        if k == 1.0:
            return Cmyk(0, 0, 0, 1)

        c = (1.0 - r - k) / (1.0 - k)
        m = (1.0 - g - k) / (1.0 - k)
        y = (1.0 - b - k) / (1.0 - k)

        return Cmyk(c, m, y, k)

    def to_rgba(self):
        r = (1.0 - self.c) * (1.0 - self.k)
        g = (1.0 - self.m) * (1.0 - self.k)
        b = (1.0 - self.y) * (1.0 - self.k)
        return Rgb(r, g, b, 1.0)

    def lighten(self, factor):
        def lighten(u):
            return clamp(u - u * factor, 0.0, 1.0)

        return Cmyk(lighten(self.c), lighten(self.m), lighten(self.y), lighten(self.k))

    def darken(self, factor):
        def darken(u):
            return clamp(u + (1.0 - u) * factor, 0.0, 1.0)

        return Cmyk(darken(self.c), darken(self.m), darken(self.y), darken(self.k))


def rgb(r, g, b):
    return Rgb(r / 255, g / 255, b / 255)


def clamp(x, minv, maxv):
    return max(minv, min(x, maxv))


def path(points, fill="none", fill_opacity="1", stroke="black", stroke_width=".5"):
    return f"""<path d="{' '.join(points)} z" stroke-linejoin="round" stroke="{stroke}" stroke-width="{stroke_width}" fill="{fill}" fill-opacity="{fill_opacity}" />"""


def voxel(x0, y0, z0, x1, y1, z1, color):
    scale = 1
    sin = .5
    cos = math.sqrt(3) / 2

    def p3d(x, y, z):
        return f"{int(200 + (x - y) * cos * scale)} {int(240 + ((x + y - 2 * z) * sin * scale))}"

    def M(point):
        return f"M {point}"

    def L(point):
        return f"L {point}"

    face_a = [
        M(p3d(x0, y0, z1)),
        L(p3d(x1, y0, z1)),
        L(p3d(x1, y1, z1)),
        L(p3d(x0, y1, z1))
    ]

    face_b = [
        M(p3d(x1, y0, z0)),
        L(p3d(x1, y1, z0)),
        L(p3d(x1, y1, z1)),
        L(p3d(x1, y0, z1)),
    ]

    face_c = [
        M(p3d(x0, y1, z0)),
        L(p3d(x1, y1, z0)),
        L(p3d(x1, y1, z1)),
        L(p3d(x0, y1, z1)),
    ]

    return (
            path(face_b, fill=color.darken(20 / 100)) +
            path(face_c, fill=color.lighten(10 / 100)) +
            path(face_a, fill=color.lighten(50 / 100))
    )

def open_file_default(file_path):
    system_platform = platform.system()

    if system_platform == 'Windows':
        os.startfile(file_path)
    elif system_platform == 'Darwin':  # For macOS
        subprocess.Popen(['open', file_path])
    else:  # For Linux or other Unix-based systems
        subprocess.Popen(['xdg-open', file_path])

COLORS = [
    rgb(201, 167, 57),
    rgb(89, 110, 216),
    rgb(156, 185, 52),
    rgb(161, 95, 211),
    rgb(92, 195, 84),
    rgb(201, 78, 177),
    rgb(79, 142, 44),
    rgb(223, 72, 124),
    rgb(106, 194, 130),
    rgb(207, 72, 51),
    rgb(81, 195, 168),
    rgb(163, 74, 118),
    rgb(64, 141, 78),
    rgb(126, 93, 164),
    rgb(224, 136, 48),
    rgb(104, 141, 206),
    rgb(156, 170, 90),
    rgb(216, 141, 199),
    rgb(51, 125, 92),
    rgb(174, 76, 82),
    rgb(74, 184, 210),
    rgb(156, 95, 43),
    rgb(111, 111, 40),
    rgb(229, 133, 116),
    rgb(207, 160, 106)
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser("visualize.py")
    parser.add_argument("input", nargs="?", type=argparse.FileType("r"), default="output.sample", help="Le fichier d'entrée (utilise stdin par défaut)")
    parser.add_argument("--truck-no", type=int, default=0, dest="truck_no", help="Le numéro du véhicule à visualiser")

    args = parser.parse_args()

    svg_content = []
    svg_content.append("""<svg xmlns="http://www.w3.org/2000/svg" width="560" height="560">""")
    blocks = []
    first = True
    i = 0
    for (i, line) in enumerate(args.input):
        if first:
            first = False
            if line == "SAT\n":
                continue
            elif line == "UNSAT\n":
                exit(0)
            else:
                raise ValueError("Invalid input")
        if line == "\n":
            break
        (truck, x0, y0, z0, x1, y1, z1) = map(int, line.split(" "))
        if truck != args.truck_no:
            continue
        blocks.append((i, (x0, y0, z0, x1, y1, z1)))
        i += 1
    blocks.sort(key=lambda x: (x[1][3], x[1][4], x[1][5]))
    for (i, (x0, y0, z0, x1, y1, z1)) in blocks:
        svg_content.append(voxel(x0, y0, z0, x1, y1, z1, COLORS[i % len(COLORS)]))
    svg_content.append("</svg>")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".svg", delete=False) as f:
        f.write("\n".join(svg_content) + "\n")
        output = f.name

    open_file_default(output)
