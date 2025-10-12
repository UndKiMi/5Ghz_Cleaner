"""
Input Components
Form input components following the design system
"""
import flet as ft
from .theme import Colors, Typography, BorderRadius, Spacing


class Checkbox(ft.Checkbox):
    """Styled checkbox"""
    def __init__(
        self,
        label: str = None,
        value: bool = False,
        on_change=None,
        **kwargs
    ):
        super().__init__(
            label=label,
            value=value,
            on_change=on_change,
            fill_color={
                ft.ControlState.DEFAULT: Colors.SHADOW_DEFAULT,
                ft.ControlState.SELECTED: Colors.ACCENT_PRIMARY,
            },
            check_color="#ffffff",
            **kwargs
        )


class CustomCheckbox:
    """Custom checkbox with multi-line label"""
    @staticmethod
    def create(primary_text: str, secondary_text: str = None):
        checkbox = ft.Checkbox(
            value=False,
            fill_color={
                ft.ControlState.DEFAULT: Colors.SHADOW_DEFAULT,
                ft.ControlState.SELECTED: Colors.ACCENT_PRIMARY,
            },
            check_color="#ffffff",
        )
        
        texts = [
            ft.Text(
                primary_text,
                size=Typography.SIZE_BASE,
                color=Colors.FG_PRIMARY,
                weight=Typography.WEIGHT_REGULAR,
            )
        ]
        
        if secondary_text:
            texts.append(
                ft.Text(
                    secondary_text,
                    size=Typography.SIZE_BASE,
                    color=Colors.FG_SECONDARY,
                    weight=Typography.WEIGHT_LIGHT,
                )
            )
        
        return checkbox, ft.Row(
            [
                checkbox,
                ft.Column(
                    texts,
                    spacing=2,
                    expand=True,
                ),
            ],
            spacing=Spacing.SM,
            alignment=ft.MainAxisAlignment.START,
        )


class Slider(ft.Slider):
    """Styled slider"""
    def __init__(
        self,
        min: float = 0,
        max: float = 100,
        value: float = 50,
        divisions: int = None,
        label: str = None,
        on_change=None,
        **kwargs
    ):
        super().__init__(
            min=min,
            max=max,
            value=value,
            divisions=divisions,
            label=label,
            on_change=on_change,
            active_color=Colors.ACCENT_PRIMARY,
            inactive_color=Colors.BORDER_DEFAULT,
            thumb_color=Colors.ACCENT_PRIMARY,
            **kwargs
        )


class Switch(ft.Switch):
    """Styled switch"""
    def __init__(
        self,
        label: str = None,
        value: bool = False,
        on_change=None,
        **kwargs
    ):
        super().__init__(
            label=label,
            value=value,
            on_change=on_change,
            active_color=Colors.ACCENT_PRIMARY,
            active_track_color=ft.Colors.with_opacity(0.5, Colors.ACCENT_PRIMARY),
            inactive_thumb_color=Colors.FG_SECONDARY,
            inactive_track_color=Colors.BORDER_DEFAULT,
            **kwargs
        )


class TextField(ft.TextField):
    """Styled text field"""
    def __init__(
        self,
        label: str = None,
        hint_text: str = None,
        value: str = "",
        password: bool = False,
        multiline: bool = False,
        on_change=None,
        **kwargs
    ):
        super().__init__(
            label=label,
            hint_text=hint_text,
            value=value,
            password=password,
            multiline=multiline,
            on_change=on_change,
            border_color=Colors.BORDER_DEFAULT,
            focused_border_color=Colors.ACCENT_PRIMARY,
            cursor_color=Colors.ACCENT_PRIMARY,
            text_size=Typography.SIZE_BASE,
            **kwargs
        )
