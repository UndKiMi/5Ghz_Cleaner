"""
Button Components
Reusable button variants following the design system
"""
import flet as ft
from .theme import Colors, Typography, BorderRadius, Spacing, Animation


class PrimaryButton(ft.ElevatedButton):
    """Primary action button"""
    def __init__(
        self,
        text: str,
        on_click=None,
        width: int = None,
        height: int = 45,
        disabled: bool = False,
        icon: str = None,
        **kwargs
    ):
        super().__init__(
            text=text,
            on_click=on_click,
            bgcolor=Colors.ACCENT_PRIMARY,
            color="#ffffff",
            height=height,
            width=width,
            disabled=disabled,
            icon=icon,
            scale=1,
            animate_scale=ft.Animation(Animation.FAST, Animation.CURVE_EASE_OUT),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=BorderRadius.MD),
            ),
            **kwargs
        )


class SecondaryButton(ft.OutlinedButton):
    """Secondary action button"""
    def __init__(
        self,
        text: str,
        on_click=None,
        width: int = None,
        height: int = 45,
        disabled: bool = False,
        icon: str = None,
        **kwargs
    ):
        super().__init__(
            text=text,
            on_click=on_click,
            height=height,
            width=width,
            disabled=disabled,
            icon=icon,
            style=ft.ButtonStyle(
                color=Colors.ACCENT_PRIMARY,
                side=ft.BorderSide(1, Colors.ACCENT_PRIMARY),
                shape=ft.RoundedRectangleBorder(radius=BorderRadius.MD),
            ),
            **kwargs
        )


class IconButton(ft.IconButton):
    """Icon-only button"""
    def __init__(
        self,
        icon: str,
        on_click=None,
        tooltip: str = None,
        icon_size: int = 18,
        icon_color: str = None,
        **kwargs
    ):
        super().__init__(
            icon=icon,
            on_click=on_click,
            tooltip=tooltip,
            icon_size=icon_size,
            icon_color=icon_color or Colors.FG_PRIMARY,
            style=ft.ButtonStyle(
                overlay_color=ft.Colors.with_opacity(0.1, Colors.FG_PRIMARY),
            ),
            **kwargs
        )


class TextButton(ft.TextButton):
    """Text-only button"""
    def __init__(
        self,
        text: str,
        on_click=None,
        color: str = None,
        size: int = None,
        **kwargs
    ):
        super().__init__(
            text=text,
            on_click=on_click,
            style=ft.ButtonStyle(
                color=color or Colors.ACCENT_PRIMARY,
                padding=0,
                text_style=ft.TextStyle(
                    size=size or Typography.SIZE_SM,
                    weight=Typography.WEIGHT_REGULAR
                ),
            ),
            **kwargs
        )
