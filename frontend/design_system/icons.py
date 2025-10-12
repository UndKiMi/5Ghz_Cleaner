"""
Icon Components
Icon components with consistent styling
"""
import flet as ft
from .theme import Colors, Shadows


class ShieldIcon(ft.Container):
    """Shield icon with glow effect"""
    def __init__(
        self,
        size: int = 83,
        with_glow: bool = True,
        **kwargs
    ):
        shadows = []
        if with_glow:
            shadows = [
                ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                    offset=ft.Offset(0, 2),
                ),
                Shadows.glow(Colors.ACCENT_PRIMARY, 0.15),
            ]
        
        super().__init__(
            content=ft.Image(
                src="assets/shield_check.svg",
                width=size,
                height=size,
                fit=ft.ImageFit.CONTAIN,
            ),
            shadow=shadows if shadows else None,
            animate=ft.Animation(1500, ft.AnimationCurve.EASE_IN_OUT) if with_glow else None,
            **kwargs
        )


class WarningIcon(ft.Icon):
    """Warning icon"""
    def __init__(self, size: int = 20, **kwargs):
        super().__init__(
            ft.Icons.WARNING_AMBER_ROUNDED,
            color=Colors.WARNING,
            size=size,
            **kwargs
        )


class InfoIcon(ft.Icon):
    """Info icon"""
    def __init__(self, size: int = 20, **kwargs):
        super().__init__(
            ft.Icons.INFO_OUTLINED,
            color=Colors.INFO,
            size=size,
            **kwargs
        )


class SuccessIcon(ft.Icon):
    """Success/check icon"""
    def __init__(self, size: int = 20, **kwargs):
        super().__init__(
            ft.Icons.CHECK_CIRCLE_OUTLINED,
            color=Colors.SUCCESS,
            size=size,
            **kwargs
        )


class ErrorIcon(ft.Icon):
    """Error icon"""
    def __init__(self, size: int = 20, **kwargs):
        super().__init__(
            ft.Icons.ERROR_OUTLINED,
            color=Colors.ERROR,
            size=size,
            **kwargs
        )
