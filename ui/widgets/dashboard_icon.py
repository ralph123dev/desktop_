import math

from PIL import Image, ImageDraw
import customtkinter as ctk


def create_navigation_icon(
    icon_name, size=16, light_color="#000000", dark_color="#ffffff"
):
    image_size = size * 4
    scale = image_size / 16

    def render(color):
        image = Image.new("RGBA", (image_size, image_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        def point(x, y):
            return (round(x * scale), round(y * scale))

        def line(points, width=1.5):
            draw.line(
                [point(x, y) for x, y in points],
                fill=color,
                width=max(1, round(width * scale)),
                joint="curve",
            )

        def ellipse(bounds, fill=None, outline=None, width=1):
            draw.ellipse(
                tuple(round(value * scale) for value in bounds),
                fill=fill,
                outline=outline,
                width=max(1, round(width * scale)),
            )

        def polygon(points, fill=color):
            draw.polygon([point(x, y) for x, y in points], fill=fill)

        if icon_name == "bar-chart":
            for bounds in ((1, 10, 5, 15), (6, 6, 10, 15), (11, 1, 15, 15)):
                draw.rectangle(
                    tuple(round(value * scale) for value in bounds),
                    fill=color,
                )
                inner = (bounds[0] + 1, bounds[1] + 1, bounds[2] - 1, bounds[3] - 1)
                draw.rectangle(
                    tuple(round(value * scale) for value in inner),
                    fill=(0, 0, 0, 0),
                )
        elif icon_name == "wifi":
            for bounds in ((0.4, 2.5, 15.6, 10.1), (2.4, 5.3, 13.6, 11.6), (5, 8.2, 11, 13)):
                draw.arc(
                    tuple(round(value * scale) for value in bounds),
                    start=215,
                    end=325,
                    fill=color,
                    width=max(1, round(1.3 * scale)),
                )
            ellipse((7.2, 11.3, 8.8, 12.9), fill=color)
        elif icon_name == "router":
            draw.arc(
                tuple(round(value * scale) for value in (4.4, 0.1, 11.6, 6.7)),
                start=220,
                end=320,
                fill=color,
                width=max(1, round(scale)),
            )
            draw.arc(
                tuple(round(value * scale) for value in (6.2, 2.3, 9.8, 6.3)),
                start=220,
                end=320,
                fill=color,
                width=max(1, round(scale)),
            )
            ellipse((7.35, 4.9, 8.65, 6.2), fill=color)
            line(((3.1, 8.1), (1.8, 4.2)), 1.1)
            line(((12.9, 8.1), (14.2, 4.2)), 1.1)
            draw.rounded_rectangle(
                tuple(round(value * scale) for value in (0.8, 8, 15.2, 13.2)),
                radius=round(scale),
                outline=color,
                width=max(1, round(scale)),
            )
            for x in (2.5, 7.5, 10, 12.5, 14):
                ellipse((x - 0.45, 10, x + 0.45, 10.9), fill=color)
        elif icon_name == "sd-card":
            polygon(((5.9, 0.5), (12.5, 0.5), (14.5, 2.5), (14.5, 14.5), (2.5, 14.5), (2.5, 4)))
            line(((5.9, 0.5), (12.5, 0.5), (14.5, 2.5), (14.5, 14.5), (2.5, 14.5), (2.5, 4), (5.9, 0.5)), 1)
            for x in (5, 7, 9, 11):
                line(((x, 1.3), (x, 5.1)), 0.8)
        elif icon_name == "gear":
            points = []
            for index in range(48):
                angle = -math.pi / 2 + index * 2 * math.pi / 48
                phase = index % 6
                radius = (7.4, 7.4, 6.1, 6.1, 7.4, 7.4)[phase]
                points.append((8 + radius * math.cos(angle), 8 + radius * math.sin(angle)))
            polygon(points)
            ellipse((5.2, 5.2, 10.8, 10.8), fill=(0, 0, 0, 0), outline=color, width=1.3)
            line(((8, 1.3), (8, 3.2)), 0.8)
            line(((8, 12.8), (8, 14.7)), 0.8)
            line(((1.3, 8), (3.2, 8)), 0.8)
            line(((12.8, 8), (14.7, 8)), 0.8)
        elif icon_name == "virus":
            for index in range(8):
                angle = index * math.pi / 4
                inner = (8 + 5.4 * math.cos(angle), 8 + 5.4 * math.sin(angle))
                outer = (8 + 7.2 * math.cos(angle), 8 + 7.2 * math.sin(angle))
                line((inner, outer), 1.5)
                dot = (8 + 7.2 * math.cos(angle), 8 + 7.2 * math.sin(angle))
                ellipse((dot[0] - 0.8, dot[1] - 0.8, dot[0] + 0.8, dot[1] + 0.8), fill=color)
            ellipse((3, 3, 13, 13), outline=color, width=1)
            for x, y in ((6, 5.3), (10, 7.2), (7.2, 10)):
                ellipse((x - 0.75, y - 0.75, x + 0.75, y + 0.75), fill=color)
        elif icon_name == "x-circle":
            ellipse((0.7, 0.7, 15.3, 15.3), outline=color, width=1)
            line(((4.6, 4.6), (11.4, 11.4)), 1)
            line(((11.4, 4.6), (4.6, 11.4)), 1)
        else:
            raise ValueError(f"Unknown navigation icon: {icon_name}")

        return image.resize((size, size), Image.Resampling.LANCZOS)

    return ctk.CTkImage(
        light_image=render(light_color),
        dark_image=render(dark_color),
        size=(size, size),
    )


def create_dashboard_icon(size=16, light_color="#000000", dark_color="#ffffff"):
    return create_navigation_icon("bar-chart", size, light_color, dark_color)
