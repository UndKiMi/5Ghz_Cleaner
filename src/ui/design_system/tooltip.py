"""
Custom Tooltip Component - Version thématisée avec niveaux de risque
Tooltips cohérents avec le design system de l'application
"""
import flet as ft
from .theme import Colors, Spacing, BorderRadius, Typography


def create_tooltip(text: str):
    """
    Crée un tooltip avec le style de l'application
    
    Args:
        text: Texte du tooltip
        
    Returns:
        String de tooltip formaté
    """
    return text


def create_info_icon_with_tooltip(tooltip_text: str, size: int = 16, risk_level: str = "info"):
    """
    Crée une icône d'information avec tooltip et couleur selon le niveau de risque
    
    Args:
        tooltip_text: Texte du tooltip
        size: Taille de l'icône
        risk_level: Niveau de risque ("info", "warning", "danger")
            - "info": Bleu/Gris - Information normale
            - "warning": Orange - Action avec précautions
            - "danger": Rouge - Action risquée pour le système
    
    Returns:
        Icône avec tooltip intégré et couleur appropriée
    """
    # Déterminer la couleur selon le niveau de risque
    if risk_level == "danger":
        icon_color = Colors.ERROR  # Rouge pour actions à risque
    elif risk_level == "warning":
        icon_color = Colors.WARNING  # Orange pour précautions
    else:
        icon_color = Colors.SUCCESS  # Vert pour actions sûres
    
    return ft.Icon(
        ft.Icons.INFO_OUTLINE_ROUNDED,
        size=size,
        color=icon_color,
        tooltip=tooltip_text,
    )
