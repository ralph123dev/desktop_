COLORS = {
    "primary": "#00d9ff",
    "primary_dark": "#0099bb",
    "success": "#00d966",
    "warning": "#ffd700",
    "error": "#ff3333",
    "error_dark": "#cc0000",
    "bg_main": "#0f0f0f",
    "bg_secondary": "#1a1a1a",
    "bg_tertiary": "#2a2a2a",
    "text_primary": "#ffffff",
    "text_secondary": "#888888",
    "text_muted": "#666666",
    "border": "#333333",
}

FONTS = {
    "title": ("Arial", 24, "bold"),
    "header": ("Arial", 18, "bold"),
    "subheader": ("Arial", 14, "bold"),
    "button": ("Arial", 12, "bold"),
    "normal": ("Arial", 11),
    "small": ("Arial", 10),
    "tiny": ("Arial", 9),
}

RAM_COLORS = {
    "low": "#00d9ff",      # 0-30%
    "medium": "#ffd700",   # 31-49%
    "high": "#ff3333",     # 50-80%
    "critical": "#ff0000", # 80%+
}

def get_ram_color(percent):
    if percent <= 30:
        return RAM_COLORS["low"]
    elif percent <= 49:
        return RAM_COLORS["medium"]
    elif percent <= 80:
        return RAM_COLORS["high"]
    else:
        return RAM_COLORS["critical"]
