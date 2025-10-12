"""
Text Components
Typography components following the design system
"""
import flet as ft
from .theme import Colors, Typography


class Heading(ft.Text):
    """Heading text component"""
    def __init__(
        self,
        text: str,
        level: int = 1,  # 1-6
        color: str = None,
        text_align=None,
        **kwargs
    ):
        size_map = {
            1: Typography.SIZE_XXXL,
            2: Typography.SIZE_XXL,
            3: Typography.SIZE_XL,
            4: Typography.SIZE_LG,
            5: Typography.SIZE_MD,
            6: Typography.SIZE_BASE,
        }
        
        super().__init__(
            text,
            size=size_map.get(level, Typography.SIZE_XXL),
            weight=Typography.WEIGHT_BOLD,
            color=color or Colors.FG_PRIMARY,
            text_align=text_align,
            **kwargs
        )


class BodyText(ft.Text):
    """Body text component"""
    def __init__(
        self,
        text: str,
        size: int = None,
        color: str = None,
        weight=None,
        **kwargs
    ):
        super().__init__(
            text,
            size=size or Typography.SIZE_BASE,
            color=color or Colors.FG_PRIMARY,
            weight=weight or Typography.WEIGHT_REGULAR,
            **kwargs
        )


class Caption(ft.Text):
    """Caption/small text component"""
    def __init__(
        self,
        text: str,
        color: str = None,
        size: int = None,
        weight=None,
        **kwargs
    ):
        super().__init__(
            text,
            size=size or Typography.SIZE_SM,
            color=color or Colors.FG_SECONDARY,
            weight=weight or Typography.WEIGHT_REGULAR,
            **kwargs
        )


class Link(ft.Text):
    """Link text component"""
    def __init__(
        self,
        text: str,
        url: str = None,
        on_click=None,
        color: str = None,
        underline: bool = False,
        **kwargs
    ):
        def handle_click(e):
            if url:
                import webbrowser
                webbrowser.open(url)
            if on_click:
                on_click(e)
        
        style = None
        if underline:
            style = ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
        
        super().__init__(
            text,
            size=Typography.SIZE_BASE,
            color=color or Colors.ACCENT_PRIMARY,
            weight=Typography.WEIGHT_REGULAR,
            style=style,
            **kwargs
        )
        
        if url or on_click:
            self.on_click = handle_click
