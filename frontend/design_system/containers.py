"""
Container Components
Layout and container components following the design system
"""
import flet as ft
from .theme import Colors, BorderRadius, Spacing, Shadows


class Card(ft.Container):
    """Card container with shadow and border"""
    def __init__(
        self,
        content=None,
        width: int = None,
        padding: int = None,
        bgcolor: str = None,
        border_color: str = None,
        shadow_level: str = "md",  # sm, md, lg
        **kwargs
    ):
        shadow_map = {
            "sm": Shadows.sm(),
            "md": Shadows.md(),
            "lg": Shadows.lg(),
        }
        
        super().__init__(
            content=content,
            width=width,
            padding=padding or Spacing.XL,
            bgcolor=bgcolor or Colors.BG_PRIMARY,
            border_radius=BorderRadius.LG,
            border=ft.border.all(1, border_color or Colors.BORDER_DEFAULT),
            shadow=shadow_map.get(shadow_level, Shadows.md()),
            **kwargs
        )


class Panel(ft.Container):
    """Panel container for grouping content"""
    def __init__(
        self,
        content=None,
        bgcolor: str = None,
        padding: int = None,
        **kwargs
    ):
        super().__init__(
            content=content,
            bgcolor=bgcolor or Colors.BG_TERTIARY,
            padding=padding or Spacing.LG,
            border_radius=BorderRadius.MD,
            border=ft.border.all(1, Colors.BORDER_DEFAULT),
            **kwargs
        )


class WarningBox(ft.Container):
    """Warning/alert container"""
    def __init__(
        self,
        message: str,
        icon: str = None,
        **kwargs
    ):
        super().__init__(
            content=ft.Row(
                [
                    ft.Icon(
                        icon or ft.Icons.WARNING_AMBER_ROUNDED,
                        color=Colors.WARNING,
                        size=20
                    ),
                    ft.Container(width=Spacing.SM),
                    ft.Text(
                        message,
                        size=12,
                        color=Colors.FG_PRIMARY,
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            bgcolor=Colors.BG_WARNING,
            padding=Spacing.LG,
            border_radius=BorderRadius.MD,
            border=ft.border.all(1, Colors.BORDER_DEFAULT),
            **kwargs
        )


class Divider(ft.Container):
    """Horizontal divider"""
    def __init__(self, height: int = 1, color: str = None, **kwargs):
        super().__init__(
            height=height,
            bgcolor=color or Colors.BORDER_DEFAULT,
            **kwargs
        )


class Spacer(ft.Container):
    """Vertical spacer"""
    def __init__(self, height: int = Spacing.MD, **kwargs):
        super().__init__(height=height, **kwargs)
