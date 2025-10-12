"""
UI Components for 5GH'z Cleaner
Reusable UI building blocks
"""
import flet as ft
from .constants import *


def create_shield_icon():
    """Create shield icon with glow effect"""
    return ft.Container(
        content=ft.Image(
            src="assets/shield_check.svg",
            width=83,
            height=83,
            fit=ft.ImageFit.CONTAIN,
        ),
        shadow=[
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=SHADOW_BLUR_RADIUS,
                color=ft.Colors.with_opacity(SHADOW_OPACITY, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=GLOW_BLUR_MIN,
                color=ft.Colors.with_opacity(GLOW_OPACITY_MIN, BLUE_ACCENT),
                offset=ft.Offset(0, 0),
            ),
        ],
        animate=ft.Animation(SHIELD_GLOW_DURATION, ft.AnimationCurve.EASE_IN_OUT),
    )


def create_warning_box():
    """Create warning information box"""
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=WARNING_COLOR, size=20),
                ft.Container(width=10),
                ft.Text(
                    "Ce logiciel effectue des modifications système importantes. "
                    "Assurez-vous d'avoir sauvegardé vos données importantes avant de continuer.",
                    size=12,
                    color=FG_SECONDARY,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        bgcolor="#2a1810",
        padding=15,
        border_radius=8,
        border=ft.border.all(1, "#2a3342"),
        expand=True,
    )


def create_terms_list():
    """Create terms and conditions list"""
    terms = [
        "Ce logiciel requiert des droits d'administrateur pour fonctionner.",
        "Les modifications effectuées peuvent affecter les performances du système.",
        "Aucune responsabilité ne pourra être engagée en cas de perte de données.",
        "Il est fortement recommandé de créer un point de restauration système avant utilisation.",
    ]
    
    return ft.Container(
        content=ft.Column(
            [ft.Text(f"• {term}", size=13, color=FG_SECONDARY) for term in terms],
            spacing=12,
        ),
        bgcolor="#0f1821",
        padding=20,
        border_radius=8,
        border=ft.border.all(1, "#2a3342"),
        expand=True,
    )


def create_checkbox():
    """Create custom checkbox with label"""
    checkbox = ft.Checkbox(
        value=False,
        fill_color={
            ft.ControlState.DEFAULT: SHADOW_COLOR,
            ft.ControlState.SELECTED: BLUE_ACCENT,
        },
        check_color="#ffffff",
    )
    
    checkbox_row = ft.Row(
        [
            checkbox,
            ft.Column(
                [
                    ft.Text(
                        "J'ai lu et compris les conditions d'utilisation.",
                        size=13,
                        color=FG_SECONDARY,
                        weight=ft.FontWeight.W_400,
                    ),
                    ft.Text(
                        "J'accepte les risques associés à l'utilisation de ce logiciel.",
                        size=13,
                        color=FG_MAIN,
                        weight=ft.FontWeight.W_300,
                    ),
                ],
                spacing=2,
                expand=True,
            ),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
    )
    
    return checkbox, checkbox_row


def create_footer():
    """Create footer with version and credits"""
    return ft.Container(
        content=ft.Row(
            [
                ft.Text(
                    "Version 1.0 Major Update • Réalisé avec",
                    size=11,
                    color="#4a5568",
                ),
                ft.Container(width=4),
                ft.Text("❤️", size=11),
                ft.Container(width=4),
                ft.Text("par", size=11, color="#4a5568"),
                ft.Container(width=4),
                ft.TextButton(
                    "K_iMi",
                    on_click=lambda e: __import__('webbrowser').open("https://github.com/UndKiMi"),
                    style=ft.ButtonStyle(
                        color=BLUE_ACCENT,
                        padding=0,
                        text_style=ft.TextStyle(size=11, weight=ft.FontWeight.NORMAL),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
        ),
        padding=ft.padding.only(bottom=10),
    )
