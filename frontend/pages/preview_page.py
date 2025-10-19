"""
Page de Prévisualisation - Style Cohérent avec les Onglets
Inspiré du design des onglets Nettoyage et Configuration

Author: UndKiMi
Version: 2.1.0 - COHÉRENT
"""
import flet as ft
from datetime import datetime
from frontend.design_system.theme import Colors, Spacing, BorderRadius, Typography, Shadows
from frontend.design_system.text import Heading, BodyText, Caption
from frontend.design_system.buttons import PrimaryButton, SecondaryButton


class PreviewPage:
    """Page de prévisualisation avec design cohérent"""
    
    def __init__(self, page: ft.Page, app_instance, preview_data):
        self.page = page
        self.app = app_instance
        self.preview_data = preview_data
        self.selected_operations = {}
        self.operation_checkboxes = {}
        
        # Par défaut tout sélectionné
        for op in preview_data.get('operations', []):
            self.selected_operations[op['name']] = True
    
    def build(self):
        """Construit la page avec le style des autres onglets"""
        return ft.Container(
            content=ft.Column(
                [
                    # Message info (comme dans Nettoyage)
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.INFO_OUTLINE_ROUNDED,
                                    size=16,
                                    color=Colors.ACCENT_PRIMARY,
                                ),
                                ft.Container(width=Spacing.XS),
                                Caption(
                                    "Vérifiez les opérations ci-dessous avant de lancer le nettoyage",
                                    text_align=ft.TextAlign.CENTER,
                                    color=Colors.FG_SECONDARY,
                                    size=12,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(vertical=Spacing.SM),
                    ),
                    
                    # En-tête centré (comme dans Nettoyage)
                    ft.Container(
                        content=ft.Column(
                            [
                                BodyText(
                                    "Rapport de Prévisualisation",
                                    weight=ft.FontWeight.W_600,
                                    size=22,
                                    color=Colors.FG_PRIMARY,
                                ),
                                ft.Container(height=Spacing.XS),
                                Caption(
                                    f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
                                    color=Colors.FG_SECONDARY,
                                    size=13,
                                ),
                            ],
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.only(bottom=Spacing.MD),
                    ),
                    
                    # Résumé rapide (style Configuration)
                    self._build_summary_row(),
                    
                    ft.Container(height=Spacing.XL),
                    
                    # Boutons de sélection rapide
                    self._build_selection_buttons(),
                    
                    ft.Container(height=Spacing.LG),
                    
                    # Liste des opérations (style cartes d'actions rapides)
                    self._build_operations_grid(),
                    
                    ft.Container(height=Spacing.XL),
                    
                    # Boutons d'action
                    self._build_action_buttons(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
            ),
        )
    
    def _build_summary_row(self):
        """Résumé en ligne (style Configuration)"""
        total_files = self.preview_data.get('total_files', 0)
        total_size_mb = self.preview_data.get('total_size_mb', 0)
        total_size_gb = total_size_mb / 1024
        operations_count = len(self.preview_data.get('operations', []))
        
        return ft.Row(
            [
                # Fichiers
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, size=18, color=Colors.INFO),
                                    ft.Container(width=Spacing.XS),
                                    BodyText("Fichiers", weight=ft.FontWeight.W_600, size=14),
                                ],
                            ),
                            ft.Container(height=Spacing.XS),
                            BodyText(f"{total_files:,}", size=20, weight=ft.FontWeight.W_600, color=Colors.INFO),
                        ],
                        spacing=0,
                    ),
                    padding=Spacing.MD,
                    bgcolor=Colors.BG_SECONDARY,
                    border_radius=BorderRadius.MD,
                    border=ft.border.all(1, Colors.BORDER_DEFAULT),
                    width=160,
                ),
                
                ft.Container(width=Spacing.LG),
                
                # Espace
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.STORAGE_OUTLINED, size=18, color=Colors.SUCCESS),
                                    ft.Container(width=Spacing.XS),
                                    BodyText("Espace", weight=ft.FontWeight.W_600, size=14),
                                ],
                            ),
                            ft.Container(height=Spacing.XS),
                            BodyText(
                                f"{total_size_gb:.2f} GB" if total_size_gb >= 1 else f"{total_size_mb:.0f} MB",
                                size=20,
                                weight=ft.FontWeight.W_600,
                                color=Colors.SUCCESS
                            ),
                        ],
                        spacing=0,
                    ),
                    padding=Spacing.MD,
                    bgcolor=Colors.BG_SECONDARY,
                    border_radius=BorderRadius.MD,
                    border=ft.border.all(1, Colors.BORDER_DEFAULT),
                    width=160,
                ),
                
                ft.Container(width=Spacing.LG),
                
                # Opérations
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.CHECKLIST_ROUNDED, size=18, color=Colors.ACCENT_PRIMARY),
                                    ft.Container(width=Spacing.XS),
                                    BodyText("Opérations", weight=ft.FontWeight.W_600, size=14),
                                ],
                            ),
                            ft.Container(height=Spacing.XS),
                            BodyText(str(operations_count), size=20, weight=ft.FontWeight.W_600, color=Colors.ACCENT_PRIMARY),
                        ],
                        spacing=0,
                    ),
                    padding=Spacing.MD,
                    bgcolor=Colors.BG_SECONDARY,
                    border_radius=BorderRadius.MD,
                    border=ft.border.all(1, Colors.BORDER_DEFAULT),
                    width=160,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    def _build_selection_buttons(self):
        """Boutons de sélection rapide"""
        return ft.Row(
            [
                ft.TextButton(
                    "Tout sélectionner",
                    icon=ft.Icons.CHECK_BOX,
                    on_click=self._select_all,
                    style=ft.ButtonStyle(color=Colors.SUCCESS),
                ),
                ft.TextButton(
                    "Tout désélectionner",
                    icon=ft.Icons.CHECK_BOX_OUTLINE_BLANK,
                    on_click=self._deselect_all,
                    style=ft.ButtonStyle(color=Colors.ERROR),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=Spacing.MD,
        )
    
    def _build_operations_grid(self):
        """Grille d'opérations (style actions rapides 2x2)"""
        operations = self.preview_data.get('operations', [])
        
        # Créer des lignes de 2 cartes
        rows = []
        for i in range(0, len(operations), 2):
            row_ops = operations[i:i+2]
            row = ft.Row(
                [
                    self._build_operation_card(row_ops[0]),
                    ft.Container(width=Spacing.LG) if len(row_ops) > 1 else ft.Container(),
                    self._build_operation_card(row_ops[1]) if len(row_ops) > 1 else ft.Container(),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            rows.append(row)
            if i + 2 < len(operations):
                rows.append(ft.Container(height=Spacing.LG))
        
        return ft.Column(
            rows,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def _build_operation_card(self, operation):
        """Carte d'opération (style bouton d'action rapide)"""
        name = operation['name']
        files_count = operation.get('files_count', 0)
        size_mb = operation.get('size_mb', 0)
        size_gb = size_mb / 1024
        result = operation.get('result', {})
        warning = result.get('warning', '')
        
        # Checkbox
        def on_change(e):
            self.selected_operations[name] = e.control.value
            self.page.update()
        
        checkbox = ft.Checkbox(
            value=self.selected_operations.get(name, True),
            on_change=on_change,
            fill_color=Colors.ACCENT_PRIMARY,
        )
        self.operation_checkboxes[name] = checkbox
        
        # Icône
        icon = self._get_operation_icon(name)
        
        # Badge warning si présent
        warning_badge = None
        if warning:
            warning_badge = ft.Container(
                content=ft.Icon(ft.Icons.WARNING_ROUNDED, size=16, color=Colors.ERROR),
                tooltip=warning,
            )
        
        return ft.Container(
            content=ft.Row(
                [
                    # Checkbox à gauche
                    checkbox,
                    ft.Container(width=Spacing.XS),
                    
                    # Icône
                    ft.Container(
                        content=ft.Icon(icon, size=32, color=Colors.ACCENT_PRIMARY),
                        width=56,
                        height=56,
                        border_radius=BorderRadius.SM,
                        bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(width=Spacing.MD),
                    
                    # Texte
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        name,
                                        color=Colors.FG_PRIMARY,
                                        weight=ft.FontWeight.W_600,
                                        size=15,
                                    ),
                                    ft.Container(width=Spacing.XS) if warning_badge else ft.Container(),
                                    warning_badge if warning_badge else ft.Container(),
                                ],
                            ),
                            ft.Container(height=Spacing.XS),
                            ft.Text(
                                f"{files_count:,} fichiers • {size_gb:.2f} GB" if size_gb >= 1 else f"{files_count:,} fichiers • {size_mb:.0f} MB",
                                color=Colors.FG_SECONDARY,
                                size=12,
                            ),
                        ],
                        spacing=0,
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            width=320,
            height=80,
            bgcolor=Colors.BG_SECONDARY,
            border_radius=BorderRadius.MD,
            border=ft.border.all(1, Colors.BORDER_DEFAULT),
            padding=Spacing.MD,
        )
    
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
    
    def _build_action_buttons(self):
        """Boutons d'action en bas"""
        return ft.Row(
            [
                SecondaryButton(
                    text="← Annuler",
                    on_click=lambda e: self.app.show_main_page(),
                    width=140,
                ),
                ft.Container(width=Spacing.XL),
                PrimaryButton(
                    text="Lancer le nettoyage",
                    icon=ft.Icons.PLAY_ARROW_ROUNDED,
                    on_click=self._start_cleaning,
                    width=220,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
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
