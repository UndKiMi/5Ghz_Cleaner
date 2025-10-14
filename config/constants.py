"""
UI Constants and Design System Values
Centralized to avoid magic numbers and improve maintainability
"""

# ============================================================================
# DESIGN SYSTEM - COLORS
# ============================================================================

# Background colors
BG_MAIN = "#0a1929"
BG_PRIMARY = "#0a1929"
BG_SECONDARY = "#132f4c"

# Foreground colors
FG_MAIN = "#ffffff"
FG_PRIMARY = "#ffffff"
FG_SECONDARY = "#b2bac2"
FG_TERTIARY = "#6b7a90"

# Accent colors
ACCENT_COLOR = "#3b82f6"
ACCENT_PRIMARY = "#3b82f6"
BLUE_ACCENT = "#3b82f6"

# Status colors
SUCCESS_COLOR = "#10b981"
WARNING_COLOR = "#f59e0b"
ERROR_COLOR = "#ef4444"

# Border colors
BORDER_DEFAULT = "#1e3a5f"

# ============================================================================
# DESIGN SYSTEM - SHADOWS AND EFFECTS
# ============================================================================

SHADOW_BLUR_RADIUS = 12
SHADOW_OPACITY = 0.2
GLOW_BLUR_MIN = 8
GLOW_BLUR_MAX = 15
GLOW_OPACITY_MIN = 0.15
GLOW_OPACITY_MAX = 0.25

# ============================================================================
# DESIGN SYSTEM - ANIMATION
# ============================================================================

SHIELD_PULSE_INTERVAL = 2.0  # seconds
FADE_IN_DURATION = 300  # milliseconds
FADE_OUT_DURATION = 300  # milliseconds

# ============================================================================
# EXPORT ALL CONSTANTS
# ============================================================================

__all__ = [
    # Colors
    'BG_MAIN', 'BG_PRIMARY', 'BG_SECONDARY',
    'FG_MAIN', 'FG_PRIMARY', 'FG_SECONDARY', 'FG_TERTIARY',
    'ACCENT_COLOR', 'ACCENT_PRIMARY', 'BLUE_ACCENT',
    'SUCCESS_COLOR', 'WARNING_COLOR', 'ERROR_COLOR',
    'BORDER_DEFAULT',
    # Effects
    'SHADOW_BLUR_RADIUS', 'SHADOW_OPACITY',
    'GLOW_BLUR_MIN', 'GLOW_BLUR_MAX',
    'GLOW_OPACITY_MIN', 'GLOW_OPACITY_MAX',
    # Animation
    'SHIELD_PULSE_INTERVAL', 'FADE_IN_DURATION', 'FADE_OUT_DURATION',
]
