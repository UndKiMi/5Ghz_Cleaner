"""
Page de Prévisualisation - Interface Épurée et Cohérente
Design unifié avec thème global, sélection avancée et ergonomie optimisée

Author: UndKiMi
Version: 4.0.0 - UNIFIED THEME
"""
import flet as ft
from datetime import datetime
from frontend.design_system.theme import Colors, Spacing, BorderRadius, Typography, Shadows
from frontend.design_system.text import Heading, BodyText, Caption
from frontend.design_system.buttons import PrimaryButton, SecondaryButton


class PreviewPage:
    """Page de prévisualisation avec design unifié"""
    
    def __init__(self, page: ft.Page, app_instance, preview_data):
        self.page = page
        self.app = app_instance
        self.preview_data = preview_data
        self.selected_operations = {}
        self.operation_checkboxes = {}
        
        # Par défaut tout sélectionné
        for op in preview_data.get('operations', []):
            self.selected_operations[op['name']] = True
        
        # Définir les opérations sécurisées (safe)
        self.safe_operations = {
            "Fichiers temporaires",
            "Cache Windows Update",
            "Prefetch",
            "Historique récent",
            "Cache miniatures",
            "Vider cache navigateurs",
        }
    
    def build(self):
        """Construit la page avec design unifié"""
        return ft.Container(
            content=ft.Column(
                [
                    # Header avec titre et date
                    self._build_header(),
                    
                    ft.Container(height=Spacing.LG),
                    
                    # Barre de stats (tabs visuels) + Bouton nettoyage
                    self._build_stats_bar_with_action(),
                    
                    ft.Container(height=Spacing.XL),
                    
                    # Boutons de sélection rapide
                    self._build_selection_toolbar(),
                    
                    ft.Container(height=Spacing.LG),
                    
                    # Liste des opérations
                    self._build_operations_list(),
                    
                    ft.Container(height=Spacing.XL),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            expand=True,
            padding=ft.padding.symmetric(vertical=Spacing.MD, horizontal=Spacing.LG),
        )
    
    def _build_header(self):
        """Header simple avec titre et date"""
        return ft.Column(
            [
                # Titre avec logo
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.PREVIEW_ROUNDED,
                                size=28,
                                color=Colors.ACCENT_PRIMARY,
                            ),
                            width=48,
                            height=48,
                            border_radius=24,
                            bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(width=Spacing.MD),
                        ft.Text(
                            "Rapport de Prévisualisation",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=Colors.FG_PRIMARY,
                        ),
                    ],
                ),
                ft.Container(height=Spacing.XS),
                # Date
                ft.Row(
                    [
                        ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, size=13, color=Colors.FG_SECONDARY),
                        ft.Container(width=6),
                        ft.Text(
                            f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
                            size=12,
                            color=Colors.FG_SECONDARY,
                        ),
                    ],
                ),
            ],
            spacing=0,
        )
    
    def _build_stats_bar_with_action(self):
        """Barre de stats (tabs style interface) + Bouton nettoyage à droite"""
        total_files = self.preview_data.get('total_files', 0)
        total_size_mb = self.preview_data.get('total_size_mb', 0)
        total_size_gb = total_size_mb / 1024
        operations_count = len(self.preview_data.get('operations', []))
        selected_count = sum(1 for v in self.selected_operations.values() if v)
        
        return ft.Container(
            content=ft.Row(
                [
                    # Tabs style interface principale
                    ft.Container(
                        content=ft.Row(
                            [
                                self._build_stat_tab(
                                    ft.Icons.DESCRIPTION_ROUNDED,
                                    "Fichiers détectés",
                                    f"{total_files:,}",
                                    True  # Premier tab actif
                                ),
                                self._build_stat_tab(
                                    ft.Icons.STORAGE_ROUNDED,
                                    "Espace à libérer",
                                    f"{total_size_gb:.2f} GB" if total_size_gb >= 1 else f"{total_size_mb:.0f} MB",
                                    False
                                ),
                                self._build_stat_tab(
                                    ft.Icons.CHECKLIST_ROUNDED,
                                    "Opérations",
                                    f"{selected_count}/{operations_count}",
                                    False
                                ),
                            ],
                            spacing=0,
                        ),
                        bgcolor=Colors.BG_SECONDARY,
                        border_radius=BorderRadius.MD,
                        padding=ft.padding.all(4),
                    ),
                    
                    # Spacer
                    ft.Container(expand=True),
                    
                    # Bouton Prévisualiser (style de l'image)
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, size=18, color=ft.Colors.WHITE),
                                ft.Container(width=8),
                                ft.Text(
                                    "Lancer le nettoyage",
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.Colors.WHITE,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(horizontal=Spacing.LG, vertical=Spacing.SM),
                        border_radius=BorderRadius.MD,
                        bgcolor=Colors.ACCENT_PRIMARY if selected_count > 0 else Colors.BG_SECONDARY,
                        on_click=self._start_cleaning if selected_count > 0 else None,
                        ink=True,
                        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                        disabled=selected_count == 0,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.symmetric(vertical=Spacing.SM),
        )
    
    def _build_stat_tab(self, icon, label, value, is_active=False):
        """Tab style interface principale"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=16, color=Colors.ACCENT_PRIMARY if is_active else Colors.FG_SECONDARY),
                    ft.Container(width=Spacing.XS),
                    ft.Column(
                        [
                            ft.Text(
                                label,
                                size=11,
                                color=Colors.FG_PRIMARY if is_active else Colors.FG_SECONDARY,
                                weight=ft.FontWeight.W_500 if is_active else ft.FontWeight.NORMAL,
                            ),
                            ft.Text(
                                value,
                                size=13,
                                weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.W_500,
                                color=Colors.ACCENT_PRIMARY if is_active else Colors.FG_SECONDARY,
                            ),
                        ],
                        spacing=2,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
            border_radius=BorderRadius.SM,
            bgcolor=Colors.BG_PRIMARY if is_active else ft.Colors.TRANSPARENT,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY)) if is_active else None,
        )
    
    def _build_selection_toolbar(self):
        """Barre d'outils de sélection rapide"""
        return ft.Row(
            [
                # Tout cocher
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.CHECK_BOX, size=16, color=Colors.ACCENT_PRIMARY),
                            ft.Container(width=6),
                            ft.Text("Tout cocher", size=13, color=Colors.ACCENT_PRIMARY),
                        ],
                    ),
                    padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
                    border_radius=BorderRadius.SM,
                    bgcolor=ft.Colors.with_opacity(0.05, Colors.ACCENT_PRIMARY),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, Colors.ACCENT_PRIMARY)),
                    on_click=self._select_all,
                    ink=True,
                ),
                ft.Container(width=Spacing.SM),
                
                # Tout décocher
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.CHECK_BOX_OUTLINE_BLANK, size=16, color=Colors.FG_SECONDARY),
                            ft.Container(width=6),
                            ft.Text("Tout décocher", size=13, color=Colors.FG_SECONDARY),
                        ],
                    ),
                    padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
                    border_radius=BorderRadius.SM,
                    bgcolor=Colors.BG_SECONDARY,
                    border=ft.border.all(1, Colors.BORDER_DEFAULT),
                    on_click=self._deselect_all,
                    ink=True,
                ),
                ft.Container(width=Spacing.SM),
                
                # Cocher uniquement safe
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.VERIFIED_USER_ROUNDED, size=16, color=Colors.SUCCESS),
                            ft.Container(width=6),
                            ft.Text("Sélectionner uniquement les options sécurisées", size=13, color=Colors.SUCCESS),
                        ],
                    ),
                    padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
                    border_radius=BorderRadius.SM,
                    bgcolor=ft.Colors.with_opacity(0.05, Colors.SUCCESS),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, Colors.SUCCESS)),
                    on_click=self._select_safe_only,
                    ink=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    def _build_operations_header(self):
        """En-tête de la section opérations"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.PLAYLIST_ADD_CHECK_ROUNDED, size=24, color=Colors.ACCENT_PRIMARY),
                    ft.Container(width=Spacing.SM),
                    ft.Text(
                        "Opérations à effectuer",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=Colors.FG_PRIMARY,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )
    
    def _build_operations_list(self):
        """Liste simple des opérations avec checkboxes"""
        operations = self.preview_data.get('operations', [])
        
        items = []
        for operation in operations:
            items.append(self._build_operation_item(operation))
            items.append(ft.Container(height=Spacing.SM))
        
        return ft.Column(
            items,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def _build_operation_item(self, operation):
        """Item simple d'opération avec checkbox"""
        name = operation['name']
        files_count = operation.get('files_count', 0)
        size_mb = operation.get('size_mb', 0)
        size_gb = size_mb / 1024
        result = operation.get('result', {})
        warning = result.get('warning', '')
        
        # État de sélection
        is_selected = self.selected_operations.get(name, True)
        
        # Checkbox
        def on_change(e):
            self.selected_operations[name] = e.control.value
            self.page.update()
        
        checkbox = ft.Checkbox(
            value=is_selected,
            on_change=on_change,
            fill_color=Colors.ACCENT_PRIMARY,
            check_color=ft.Colors.WHITE,
        )
        self.operation_checkboxes[name] = checkbox
        
        # Icône selon l'opération
        icon = self._get_operation_icon(name)
        
        # Vérifier si l'opération est safe
        is_safe = name in self.safe_operations
        
        # Ligne simple
        return ft.Container(
            content=ft.Row(
                [
                    # Checkbox
                    checkbox,
                    ft.Container(width=Spacing.SM),
                    
                    # Icône (couleur du thème uniquement)
                    ft.Icon(icon, size=20, color=Colors.ACCENT_PRIMARY),
                    ft.Container(width=Spacing.SM),
                    
                    # Nom de l'opération
                    ft.Text(
                        name,
                        color=Colors.FG_PRIMARY,
                        weight=ft.FontWeight.W_500,
                        size=14,
                        expand=True,
                    ),
                    
                    # Badge Safe
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.VERIFIED_USER, size=12, color=Colors.SUCCESS),
                                ft.Container(width=4),
                                ft.Text("Sécurisé", size=11, color=Colors.SUCCESS, weight=ft.FontWeight.W_500),
                            ],
                        ),
                        padding=ft.padding.symmetric(horizontal=6, vertical=2),
                        border_radius=BorderRadius.SM,
                        bgcolor=ft.Colors.with_opacity(0.1, Colors.SUCCESS),
                    ) if is_safe else ft.Container(),
                    
                    ft.Container(width=Spacing.SM) if is_safe else ft.Container(),
                    
                    # Statistiques
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, size=14, color=Colors.FG_SECONDARY),
                            ft.Container(width=4),
                            ft.Text(
                                f"{files_count:,}",
                                color=Colors.FG_SECONDARY,
                                size=13,
                            ),
                            ft.Container(width=Spacing.SM),
                            ft.Icon(ft.Icons.STORAGE_OUTLINED, size=14, color=Colors.FG_SECONDARY),
                            ft.Container(width=4),
                            ft.Text(
                                f"{size_gb:.2f} GB" if size_gb >= 1 else f"{size_mb:.0f} MB",
                                color=Colors.FG_SECONDARY,
                                size=13,
                            ),
                        ],
                    ),
                    
                    # Warning si présent
                    ft.Container(width=Spacing.SM) if warning else ft.Container(),
                    ft.Icon(ft.Icons.WARNING_ROUNDED, size=16, color=Colors.ERROR, tooltip=warning) if warning else ft.Container(),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            width=700,
            padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
            border_radius=BorderRadius.MD,
            bgcolor=ft.Colors.with_opacity(0.03, Colors.ACCENT_PRIMARY) if is_selected else Colors.BG_SECONDARY,
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, Colors.ACCENT_PRIMARY) if is_selected else Colors.BORDER_DEFAULT),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
    
    def _select_safe_only(self, e):
        """Sélectionne uniquement les opérations sécurisées"""
        for name in self.selected_operations:
            # Cocher uniquement si l'opération est dans la liste safe
            self.selected_operations[name] = name in self.safe_operations
            if name in self.operation_checkboxes:
                self.operation_checkboxes[name].value = name in self.safe_operations
        self.page.update()
    
    def _get_operation_icon(self, name):
        """Retourne l'icône selon l'opération"""
        icons = {
            "Fichiers temporaires": ft.Icons.DELETE_SWEEP_ROUNDED,
            "Cache Windows Update": ft.Icons.SYSTEM_UPDATE_ROUNDED,
            "Prefetch": ft.Icons.SPEED_ROUNDED,
            "Historique récent": ft.Icons.HISTORY_ROUNDED,
            "Cache miniatures": ft.Icons.IMAGE_ROUNDED,
            "Dumps de crash": ft.Icons.BUG_REPORT_ROUNDED,
            "Windows.old": ft.Icons.FOLDER_DELETE_ROUNDED,
            "Corbeille": ft.Icons.DELETE_ROUNDED,
            "Nettoyer logs volumineux": ft.Icons.DESCRIPTION_ROUNDED,
            "Vider cache navigateurs": ft.Icons.WEB_ROUNDED,
            "Nettoyer journaux événements": ft.Icons.EVENT_NOTE_ROUNDED,
            "Libérer RAM Standby": ft.Icons.MEMORY_ROUNDED,
            "Flush DNS": ft.Icons.DNS_ROUNDED,
        }
        return icons.get(name, ft.Icons.CLEANING_SERVICES_ROUNDED)
    
    
    def _select_all(self, e):
        """Sélectionne tout"""
        for name in self.selected_operations:
            self.selected_operations[name] = True
            if name in self.operation_checkboxes:
                self.operation_checkboxes[name].value = True
        self.page.update()
    
    def _deselect_all(self, e):
        """Désélectionne tout"""
        for name in self.selected_operations:
            self.selected_operations[name] = False
            if name in self.operation_checkboxes:
                self.operation_checkboxes[name].value = False
        self.page.update()
    
    def _start_cleaning(self, e):
        """Lance le nettoyage"""
        selected_ops = [name for name, selected in self.selected_operations.items() if selected]
        if not selected_ops:
            return
        print(f"[INFO] Lancement du nettoyage: {len(selected_ops)} opérations")
        self.app.start_real_cleaning(selected_ops)
