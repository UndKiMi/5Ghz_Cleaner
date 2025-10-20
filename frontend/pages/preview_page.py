"""
Page de Prévisualisation - Design Moderne et User-Friendly
Interface élégante avec animations et interactions fluides

Author: UndKiMi
Version: 3.0.0 - MODERN UI
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
        """Construit la page avec un design moderne et élégant"""
        return ft.Container(
            content=ft.Column(
                [
                    # Header moderne avec gradient
                    self._build_modern_header(),
                    
                    ft.Container(height=Spacing.LG),
                    
                    # Cartes statistiques avec animations
                    self._build_stats_cards(),
                    
                    ft.Container(height=Spacing.XL),
                    
                    # Divider élégant
                    ft.Container(
                        height=1,
                        bgcolor=ft.Colors.with_opacity(0.1, Colors.FG_PRIMARY),
                        margin=ft.margin.symmetric(horizontal=40),
                    ),
                    
                    ft.Container(height=Spacing.XL),
                    
                    # Section titre opérations
                    self._build_operations_header(),
                    
                    ft.Container(height=Spacing.MD),
                    
                    # Boutons de sélection rapide modernisés
                    self._build_selection_buttons(),
                    
                    ft.Container(height=Spacing.LG),
                    
                    # Liste des opérations avec design amélioré
                    self._build_operations_grid(),
                    
                    ft.Container(height=Spacing.XL),
                    
                    # Boutons d'action avec design moderne
                    self._build_action_buttons(),
                    
                    ft.Container(height=Spacing.LG),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            expand=True,
            padding=ft.padding.symmetric(vertical=Spacing.MD),
        )
    
    def _build_modern_header(self):
        """Header moderne avec gradient et icône"""
        return ft.Container(
            content=ft.Column(
                [
                    # Icône principale avec cercle
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.PREVIEW_ROUNDED,
                            size=48,
                            color=Colors.ACCENT_PRIMARY,
                        ),
                        width=96,
                        height=96,
                        border_radius=48,
                        bgcolor=ft.Colors.with_opacity(0.15, Colors.ACCENT_PRIMARY),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=Spacing.MD),
                    
                    # Titre principal
                    ft.Text(
                        "Rapport de Prévisualisation",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=Colors.FG_PRIMARY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=Spacing.XS),
                    
                    # Sous-titre avec icône
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, size=14, color=Colors.FG_SECONDARY),
                            ft.Container(width=6),
                            ft.Text(
                                f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
                                size=13,
                                color=Colors.FG_SECONDARY,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(height=Spacing.SM),
                    
                    # Message info élégant
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.INFO_OUTLINE_ROUNDED,
                                    size=16,
                                    color=Colors.ACCENT_PRIMARY,
                                ),
                                ft.Container(width=8),
                                ft.Text(
                                    "Sélectionnez les opérations à effectuer",
                                    size=13,
                                    color=Colors.FG_SECONDARY,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
                        border_radius=BorderRadius.MD,
                        bgcolor=ft.Colors.with_opacity(0.05, Colors.ACCENT_PRIMARY),
                        border=ft.border.all(1, ft.Colors.with_opacity(0.2, Colors.ACCENT_PRIMARY)),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=ft.padding.only(top=Spacing.MD, bottom=Spacing.LG),
        )
    
    def _build_stats_cards(self):
        """Cartes statistiques modernes avec animations"""
        total_files = self.preview_data.get('total_files', 0)
        total_size_mb = self.preview_data.get('total_size_mb', 0)
        total_size_gb = total_size_mb / 1024
        operations_count = len(self.preview_data.get('operations', []))
        
        # Calculer le nombre d'opérations sélectionnées
        selected_count = sum(1 for v in self.selected_operations.values() if v)
        
        stats = [
            {
                "icon": ft.Icons.DESCRIPTION_ROUNDED,
                "label": "Fichiers détectés",
                "value": f"{total_files:,}",
                "color": Colors.INFO,
                "bg_color": ft.Colors.with_opacity(0.15, Colors.INFO),
            },
            {
                "icon": ft.Icons.STORAGE_ROUNDED,
                "label": "Espace à libérer",
                "value": f"{total_size_gb:.2f} GB" if total_size_gb >= 1 else f"{total_size_mb:.0f} MB",
                "color": Colors.SUCCESS,
                "bg_color": ft.Colors.with_opacity(0.15, Colors.SUCCESS),
            },
            {
                "icon": ft.Icons.CHECKLIST_ROUNDED,
                "label": "Opérations",
                "value": f"{selected_count}/{operations_count}",
                "color": Colors.ACCENT_PRIMARY,
                "bg_color": ft.Colors.with_opacity(0.15, Colors.ACCENT_PRIMARY),
            },
        ]
        
        cards = []
        for stat in stats:
            card = ft.Container(
                content=ft.Column(
                    [
                        # Icône avec cercle
                        ft.Container(
                            content=ft.Icon(stat["icon"], size=28, color=stat["color"]),
                            width=64,
                            height=64,
                            border_radius=32,
                            bgcolor=stat["bg_color"],
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(height=Spacing.MD),
                        
                        # Label
                        ft.Text(
                            stat["label"],
                            size=13,
                            color=Colors.FG_SECONDARY,
                            weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=Spacing.XS),
                        
                        # Valeur
                        ft.Text(
                            stat["value"],
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=stat["color"],
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
                width=180,
                padding=Spacing.LG,
                border_radius=BorderRadius.LG,
                bgcolor=Colors.BG_SECONDARY,
                border=ft.border.all(1, Colors.BORDER_DEFAULT),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=10,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4),
                ),
                animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            )
            cards.append(card)
        
        return ft.Row(
            cards,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=Spacing.XL,
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
        """Boutons de sélection rapide modernisés"""
        return ft.Row(
            [
                # Bouton Tout sélectionner
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=18, color=Colors.SUCCESS),
                            ft.Container(width=8),
                            ft.Text("Tout sélectionner", size=13, weight=ft.FontWeight.W_500, color=Colors.SUCCESS),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
                    border_radius=BorderRadius.MD,
                    bgcolor=ft.Colors.with_opacity(0.1, Colors.SUCCESS),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.3, Colors.SUCCESS)),
                    on_click=self._select_all,
                    ink=True,
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                ),
                ft.Container(width=Spacing.MD),
                
                # Bouton Tout désélectionner
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.CANCEL_ROUNDED, size=18, color=Colors.ERROR),
                            ft.Container(width=8),
                            ft.Text("Tout désélectionner", size=13, weight=ft.FontWeight.W_500, color=Colors.ERROR),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
                    border_radius=BorderRadius.MD,
                    bgcolor=ft.Colors.with_opacity(0.1, Colors.ERROR),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.3, Colors.ERROR)),
                    on_click=self._deselect_all,
                    ink=True,
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
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
        """Carte d'opération moderne avec hover effect"""
        name = operation['name']
        files_count = operation.get('files_count', 0)
        size_mb = operation.get('size_mb', 0)
        size_gb = size_mb / 1024
        result = operation.get('result', {})
        warning = result.get('warning', '')
        
        # État de sélection
        is_selected = self.selected_operations.get(name, True)
        
        # Checkbox personnalisée
        def on_change(e):
            self.selected_operations[name] = e.control.value
            # Mettre à jour le compteur dans les stats
            self.page.update()
        
        checkbox = ft.Checkbox(
            value=is_selected,
            on_change=on_change,
            fill_color=Colors.ACCENT_PRIMARY,
            check_color=ft.Colors.WHITE,
        )
        self.operation_checkboxes[name] = checkbox
        
        # Icône et couleur selon l'opération
        icon = self._get_operation_icon(name)
        icon_color = self._get_operation_color(name)
        
        # Badge warning si présent
        warning_badge = None
        if warning:
            warning_badge = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.WARNING_ROUNDED, size=14, color=Colors.ERROR),
                        ft.Container(width=4),
                        ft.Text("Attention", size=11, color=Colors.ERROR, weight=ft.FontWeight.W_500),
                    ],
                ),
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                border_radius=BorderRadius.SM,
                bgcolor=ft.Colors.with_opacity(0.1, Colors.ERROR),
                tooltip=warning,
            )
        
        # Conteneur de la carte avec effet hover
        card = ft.Container(
            content=ft.Row(
                [
                    # Checkbox
                    checkbox,
                    ft.Container(width=Spacing.SM),
                    
                    # Icône avec cercle coloré
                    ft.Container(
                        content=ft.Icon(icon, size=28, color=icon_color),
                        width=60,
                        height=60,
                        border_radius=30,
                        bgcolor=ft.Colors.with_opacity(0.15, icon_color),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(width=Spacing.MD),
                    
                    # Contenu texte
                    ft.Column(
                        [
                            # Nom de l'opération
                            ft.Text(
                                name,
                                color=Colors.FG_PRIMARY,
                                weight=ft.FontWeight.W_600,
                                size=14,
                            ),
                            ft.Container(height=6),
                            
                            # Statistiques
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, size=12, color=Colors.FG_SECONDARY),
                                    ft.Container(width=4),
                                    ft.Text(
                                        f"{files_count:,} fichiers",
                                        color=Colors.FG_SECONDARY,
                                        size=12,
                                    ),
                                    ft.Container(width=Spacing.SM),
                                    ft.Icon(ft.Icons.STORAGE_OUTLINED, size=12, color=Colors.FG_SECONDARY),
                                    ft.Container(width=4),
                                    ft.Text(
                                        f"{size_gb:.2f} GB" if size_gb >= 1 else f"{size_mb:.0f} MB",
                                        color=Colors.FG_SECONDARY,
                                        size=12,
                                    ),
                                ],
                            ),
                            
                            # Badge warning si présent
                            ft.Container(height=6) if warning_badge else ft.Container(),
                            warning_badge if warning_badge else ft.Container(),
                        ],
                        spacing=0,
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            width=340,
            padding=Spacing.MD,
            border_radius=BorderRadius.LG,
            bgcolor=Colors.BG_SECONDARY,
            border=ft.border.all(
                1.5 if is_selected else 1,
                icon_color if is_selected else Colors.BORDER_DEFAULT
            ),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8 if is_selected else 4,
                color=ft.Colors.with_opacity(0.15 if is_selected else 0.08, icon_color if is_selected else ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        
        return card
    
    def _get_operation_color(self, name):
        """Retourne la couleur selon l'opération"""
        colors = {
            "Fichiers temporaires": "#FF6B6B",
            "Cache Windows Update": "#4ECDC4",
            "Prefetch": "#45B7D1",
            "Historique récent": "#FFA07A",
            "Cache miniatures": "#98D8C8",
            "Dumps de crash": "#F7B731",
            "Windows.old": "#FF7979",
            "Corbeille": "#FF6348",
            "Nettoyer logs volumineux": "#A29BFE",
            "Vider cache navigateurs": "#74B9FF",
            "Nettoyer journaux événements": "#FD79A8",
            "Libérer RAM Standby": "#FDCB6E",
            "Flush DNS": "#6C5CE7",
        }
        return colors.get(name, Colors.ACCENT_PRIMARY)
    
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
        """Boutons d'action modernes avec animations"""
        selected_count = sum(1 for v in self.selected_operations.values() if v)
        
        return ft.Column(
            [
                # Message de confirmation
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                                size=16,
                                color=Colors.SUCCESS if selected_count > 0 else Colors.FG_SECONDARY,
                            ),
                            ft.Container(width=8),
                            ft.Text(
                                f"{selected_count} opération(s) sélectionnée(s)" if selected_count > 0 else "Aucune opération sélectionnée",
                                size=13,
                                color=Colors.SUCCESS if selected_count > 0 else Colors.FG_SECONDARY,
                                weight=ft.FontWeight.W_500,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.symmetric(vertical=Spacing.SM),
                ),
                
                ft.Container(height=Spacing.MD),
                
                # Boutons
                ft.Row(
                    [
                        # Bouton Annuler
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, size=18, color=Colors.FG_SECONDARY),
                                    ft.Container(width=8),
                                    ft.Text("Retour", size=14, weight=ft.FontWeight.W_600, color=Colors.FG_SECONDARY),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            width=140,
                            height=48,
                            border_radius=BorderRadius.MD,
                            bgcolor=Colors.BG_SECONDARY,
                            border=ft.border.all(1, Colors.BORDER_DEFAULT),
                            on_click=lambda e: self.app.show_main_page(),
                            ink=True,
                            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                        ),
                        
                        ft.Container(width=Spacing.LG),
                        
                        # Bouton Lancer le nettoyage
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, size=20, color=ft.Colors.WHITE),
                                    ft.Container(width=8),
                                    ft.Text(
                                        "Lancer le nettoyage",
                                        size=15,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            width=240,
                            height=52,
                            border_radius=BorderRadius.MD,
                            bgcolor=Colors.SUCCESS if selected_count > 0 else Colors.BG_SECONDARY,
                            on_click=self._start_cleaning if selected_count > 0 else None,
                            ink=True,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=12,
                                color=ft.Colors.with_opacity(0.3, Colors.SUCCESS) if selected_count > 0 else ft.Colors.TRANSPARENT,
                                offset=ft.Offset(0, 4),
                            ) if selected_count > 0 else None,
                            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                            disabled=selected_count == 0,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
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
