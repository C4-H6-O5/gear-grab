# ==========================================
# 1. MODERN ELEGANT COLOR PALETTE & CONFIG
# ==========================================
COLOR_BG = "#0A0A0F"           # Deep Charcoal (Professional Dark)
COLOR_CARD = "#1A1A24"         # Slightly lighter charcoal for cards
COLOR_ACCENT_PRIMARY = "#4CC9F0"  # Soft Cyan (BatStateU Blue-inspired)
COLOR_ACCENT_SECONDARY = "#7209B7" # Elegant Purple
COLOR_TEXT_WHITE = "#F8F9FA"   # Off-white for better readability
COLOR_TEXT_GRAY = "#ADB5BD"    # Muted gray for secondary text
COLOR_SUCCESS = "#38B000"      # Elegant Green (Available)
COLOR_WARNING = "#FF9E00"      # Amber (Maintenance/Internal)
COLOR_DANGER = "#FF0054"       # Modern Red (Borrowed/Lost)
COLOR_NEUTRAL = "#4361EE"      # Blue for other statuses

# Status colors mapping
STATUS_COLORS = {
    'Available': COLOR_SUCCESS,
    'Borrowed': COLOR_DANGER,
    'Internal': COLOR_WARNING,
    'Maintenance': COLOR_WARNING,
    'Lost': COLOR_DANGER
}
