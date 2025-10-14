"""
Custom Tooltip Component
Tooltip personnalisé avec le design system de l'application
"""
import flet as ft
from .theme import Colors, Spacing, BorderRadius, Typography


class CustomTooltip(ft.Tooltip):
    """Tooltip personnalisé avec le style de l'application"""
    
    def __init__(
        self,
        message: str,
        **kwargs
    ):
        super().__init__(
            message=message,
            padding=Spacing.MD,
            bgcolor=Colors.BG_SECONDARY,
            text_style=ft.TextStyle(
                size=Typography.SIZE_SM,
                color=Colors.FG_PRIMARY,
                weight=Typography.WEIGHT_REGULAR,
            ),
            border=ft.border.all(1, Colors.BORDER_DEFAULT),
            border_radius=BorderRadius.MD,
            wait_duration=500,  # 500ms avant d'afficher
            show_duration=5000,  # 5 secondes d'affichage
            **kwargs
        )


def create_info_icon_with_tooltip(tooltip_text: str, size: int = 16):
    """
    Crée une icône d'information avec tooltip personnalisé
    
    Args:
        tooltip_text: Texte du tooltip
        size: Taille de l'icône
    
    Returns:
        Container avec l'icône et le tooltip
    """
    return ft.Container(
        content=ft.Icon(
            ft.Icons.INFO_OUTLINE_ROUNDED,
            size=size,
            color=Colors.FG_TERTIARY,
        ),
        tooltip=CustomTooltip(tooltip_text),
        on_hover=lambda e: _on_icon_hover(e),
    )


def _on_icon_hover(e):
    """Change la couleur de l'icône au survol"""
    if e.data == "true":
        e.control.content.color = Colors.ACCENT_PRIMARY
    else:
        e.control.content.color = Colors.FG_TERTIARY
    e.control.update()
