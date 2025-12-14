# ==========================================
# 1. MODERN ELEGANT COLOR PALETTE & CONFIG
# ==========================================
# ==========================================
# 1. DESIGN: BATSTATEU 'CYBER-NEON' PALETTE
# ==========================================

APP_NAME = "Gear Grab"

# Backgrounds: Added a tiny hint of blue to the darks to make them "richer"
COLOR_BG = "#0B0C15"           # Deepest Midnight (Better than flat charcoal)
COLOR_CARD = "#151625"         # Rich Dark Blue-Gray (Soft separation from BG)

# Accents: Kept your core identity but harmonized them
COLOR_ACCENT_PRIMARY = "#4CC9F0"   # Soft Cyan (Your Brand Color)
COLOR_ACCENT_SECONDARY = "#7209B7" # Elegant Purple (Depth)

# Text: Cooled down the white/gray to match the dark blue background
COLOR_TEXT_WHITE = "#F0F0F5"   # Cool White (Easier on eyes than #F8F9FA)
COLOR_TEXT_GRAY = "#9494A8"    # Cool Muted Blue-Gray

# Status Colors (The Major Fix):
# - Success: Changed from 'Grass Green' to 'Neon Mint' to match the Cyan.
# - Warning: Changed from 'Safety Orange' to 'Goldenrod' for less eye strain.
# - Danger: Kept your Red, it was perfect.
COLOR_SUCCESS = "#06D6A0"      # Neon Mint (Available) -> Matches the Cyberpunk vibe
COLOR_WARNING = "#FFB703"      # Goldenrod (Maintenance) -> Warm but not harsh
COLOR_DANGER = "#F72585"       # Neon Rose (Borrowed/Lost) -> Replaced Red with this vibrant Pink-Red
COLOR_NEUTRAL = "#4895EF"      # Soft Blue (Internal Use)

# Status colors mapping
STATUS_COLORS = {
    'Available': COLOR_SUCCESS,
    'Borrowed': COLOR_DANGER,
    'Internal': COLOR_WARNING,
    'Maintenance': COLOR_WARNING,
    'Lost': COLOR_DANGER
}

# Category icons mapping
CATEGORY_ICONS = {
    "Camera Body": "📷",
    "Camera Lens": "🔘",
    "Lighting": "💡",
    "Tripods & Support": "◬",
    "Audio & Microphones": "🎤",
    "Drones": "🚁",
    "Stabilizers & Gimbals": "🦾",
    "Studio Accessories": "📦",
    "Default": "⚙️"  # Fallback icon
}
