"""
Design System Theme Configuration
Centralized design tokens and theme values
"""
import flet as ft


class Colors:
    """Color palette"""
    # Background
    BG_PRIMARY = "#0d1b2a"
    BG_SECONDARY = "#1b263b"
    BG_TERTIARY = "#0f1821"
    BG_WARNING = "#2a1810"
    
    # Foreground
    FG_PRIMARY = "#e0e1dd"
    FG_SECONDARY = "#778da9"
    FG_TERTIARY = "#4a5568"
    
    # Accent
    ACCENT_PRIMARY = "#4a9eff"
    ACCENT_SECONDARY = "#e0e1dd"
    
    # Semantic
    SUCCESS = "#10b981"
    WARNING = "#ff9500"
    ERROR = "#ef4444"
    INFO = "#3b82f6"
    
    # Borders & Shadows
    BORDER_DEFAULT = "#2a3342"
    BORDER_LIGHT = "#1a2332"
    SHADOW_DEFAULT = "#2a3342"


class Spacing:
    """Spacing scale (in pixels)"""
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 20
    XXL = 24
    XXXL = 32
    HUGE = 40
    MEGA = 50


class Typography:
    """Typography scale"""
    # Font sizes
    SIZE_XS = 10
    SIZE_SM = 11
    SIZE_BASE = 13
    SIZE_MD = 14
    SIZE_LG = 16
    SIZE_XL = 20
    SIZE_XXL = 28
    SIZE_XXXL = 32
    
    # Font weights
    WEIGHT_LIGHT = ft.FontWeight.W_300
    WEIGHT_REGULAR = ft.FontWeight.W_400
    WEIGHT_MEDIUM = ft.FontWeight.W_500
    WEIGHT_BOLD = ft.FontWeight.BOLD


class BorderRadius:
    """Border radius scale"""
    SM = 4
    MD = 8
    LG = 12
    XL = 16
    FULL = 9999


class Shadows:
    """Shadow definitions"""
    @staticmethod
    def sm():
        return ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 1),
        )
    
    @staticmethod
    def md():
        return ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        )
    
    @staticmethod
    def lg():
        return ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        )
    
    @staticmethod
    def glow(color: str, intensity: float = 0.3):
        return ft.BoxShadow(
            spread_radius=0,
            blur_radius=12,
            color=ft.Colors.with_opacity(intensity, color),
            offset=ft.Offset(0, 0),
        )


class Animation:
    """Animation timing"""
    FAST = 100
    NORMAL = 300
    SLOW = 500
    VERY_SLOW = 1500
    
    CURVE_EASE = ft.AnimationCurve.EASE
    CURVE_EASE_IN = ft.AnimationCurve.EASE_IN
    CURVE_EASE_OUT = ft.AnimationCurve.EASE_OUT
    CURVE_EASE_IN_OUT = ft.AnimationCurve.EASE_IN_OUT


class Layout:
    """Layout constants"""
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 1019
    WINDOW_MIN_WIDTH = 876
    WINDOW_MIN_HEIGHT = 1019
    
    CARD_MAX_WIDTH = 700
    CONTENT_PADDING = 40
