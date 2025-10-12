"""
Page de prévisualisation des résultats du dry-run
Permet à l'utilisateur de sélectionner les opérations à effectuer
"""
import flet as ft
from frontend.design_system.theme import Colors, Spacing, BorderRadius, Typography
from frontend.design_system.text import Heading, BodyText, Caption
from frontend.design_system.buttons import PrimaryButton, SecondaryButton


class PreviewPage:
    """Page de prévisualisation avec sélection des opérations"""
    
    def __init__(self, page: ft.Page, app_instance, preview_data):
        self.page = page
        self.app = app_instance
        self.preview_data = preview_data
        self.selected_operations = {}  # Dict pour stocker les sélections
        self.operation_checkboxes = {}  # Référence aux checkboxes
        
        # Par défaut, tout est sélectionné
        for op in preview_data.get('operations', []):
            self.selected_operations[op['name']] = True
    
    def build(self):
        """Construit la page de prévisualisation"""
        # Container principal avec animation et scroll
        self.main_container = ft.Container(
            content=ft.Column(
                [
                    self._build_header(),
                    ft.Container(height=Spacing.XL),
                    self._build_summary(),
                    ft.Container(height=Spacing.XL),
                    self._build_operations_list(),
                    ft.Container(height=Spacing.XL),
                    self._build_actions(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.ALWAYS,  # Toujours afficher la scrollbar
                spacing=0,
            ),
            padding=Spacing.XXL,
            opacity=0,  # Pour animation d'entrée
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            expand=True,  # Prend toute la hauteur disponible
        )
        
        # Animation d'entrée
        self.page.update()
        self.main_container.opacity = 1
        self.page.update()
        
        return self.main_container
    
    def _build_header(self):
        """Construit l'en-tête de la page"""
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.PREVIEW_ROUNDED,
                            size=48,
                            color=Colors.ACCENT_PRIMARY,
                        ),
                        ft.Container(width=Spacing.MD),
                        ft.Column(
                            [
                                Heading("Rapport de Prévisualisation"),
                                Caption(
                                    "Sélectionnez les opérations que vous souhaitez effectuer",
                                    color=Colors.FG_SECONDARY,
                                ),
                            ],
                            spacing=Spacing.XS,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def _build_summary(self):
        """Construit le résumé global"""
        total_files = self.preview_data.get('total_files', 0)
        total_size_mb = self.preview_data.get('total_size_mb', 0)
        total_size_gb = total_size_mb / 1024
        
        return ft.Container(
            content=ft.Row(
                [
                    self._build_stat_card(
                        "Fichiers/Éléments",
                        f"{total_files:,}",
                        ft.Icons.DESCRIPTION_OUTLINED,
                        Colors.ACCENT_PRIMARY,
                    ),
                    ft.Container(width=Spacing.LG),
                    self._build_stat_card(
                        "Espace à libérer",
                        f"{total_size_mb:.2f} MB" if total_size_mb < 1024 else f"{total_size_gb:.2f} GB",
                        ft.Icons.STORAGE_ROUNDED,
                        Colors.SUCCESS if total_size_mb > 100 else Colors.WARNING,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )
    
    def _build_stat_card(self, label, value, icon, color):
        """Construit une carte de statistique"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=32, color=color),
                    ft.Container(height=Spacing.SM),
                    BodyText(value, size=24, weight=ft.FontWeight.BOLD, color=color),
                    Caption(label, color=Colors.FG_SECONDARY),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=Spacing.XS,
            ),
            width=200,
            padding=Spacing.LG,
            bgcolor=Colors.BG_SECONDARY,
            border_radius=BorderRadius.MD,
            border=ft.border.all(1, Colors.BORDER_DEFAULT),
        )
    
    def _build_operations_list(self):
        """Construit la liste des opérations avec checkboxes"""
        operations = self.preview_data.get('operations', [])
        
        operation_cards = []
        for op in operations:
            card = self._build_operation_card(op)
            operation_cards.append(card)
            operation_cards.append(ft.Container(height=Spacing.MD))
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            BodyText("Opérations à effectuer", weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            ft.TextButton(
                                "Tout sélectionner",
                                on_click=self._select_all,
                                style=ft.ButtonStyle(color=Colors.ACCENT_PRIMARY),
                            ),
                            ft.TextButton(
                                "Tout désélectionner",
                                on_click=self._deselect_all,
                                style=ft.ButtonStyle(color=Colors.FG_SECONDARY),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=Spacing.MD),
                    ft.Container(
                        content=ft.Column(
                            operation_cards,
                            scroll=ft.ScrollMode.ALWAYS,
                            spacing=0,
                        ),
                        height=400,  # Hauteur maximale pour la liste
                    ),
                ],
                spacing=0,
            ),
            width=800,
        )
    
    def _build_operation_card(self, operation):
        """Construit une carte d'opération avec checkbox"""
        name = operation['name']
        files_count = operation.get('files_count', 0)
        size_mb = operation.get('size_mb', 0)
        result = operation.get('result', {})
        warning = result.get('warning', '')
        note = result.get('note', '')
        
        # Créer la checkbox
        def on_checkbox_change(e):
            self.selected_operations[name] = e.control.value
            self._update_summary()
        
        checkbox = ft.Checkbox(
            value=self.selected_operations.get(name, True),
            on_change=on_checkbox_change,
            fill_color=Colors.ACCENT_PRIMARY,
        )
        
        self.operation_checkboxes[name] = checkbox
        
        # Icône selon le type d'opération
        icon = self._get_operation_icon(name)
        
        # Couleur selon l'importance
        border_color = Colors.ERROR if warning else Colors.BORDER_DEFAULT
        
        return ft.Container(
            content=ft.Row(
                [
                    checkbox,
                    ft.Container(width=Spacing.SM),
                    ft.Icon(icon, size=24, color=Colors.ACCENT_PRIMARY),
                    ft.Container(width=Spacing.MD),
                    ft.Column(
                        [
                            BodyText(name, weight=ft.FontWeight.BOLD),
                            ft.Container(height=Spacing.XS),
                            ft.Row(
                                [
                                    Caption(f"{files_count:,} éléments", color=Colors.FG_SECONDARY),
                                    Caption(" • ", color=Colors.FG_TERTIARY),
                                    Caption(
                                        f"{size_mb:.2f} MB" if size_mb < 1024 else f"{size_mb/1024:.2f} GB",
                                        color=Colors.SUCCESS if size_mb > 0 else Colors.FG_TERTIARY,
                                    ),
                                ],
                                spacing=0,
                            ),
                            # Avertissement si présent
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.WARNING_ROUNDED, size=16, color=Colors.ERROR),
                                        ft.Container(width=Spacing.XS),
                                        Caption(warning, color=Colors.ERROR),
                                    ],
                                ),
                                visible=bool(warning),
                            ) if warning else ft.Container(),
                            # Note si présente
                            ft.Container(
                                content=Caption(f"ℹ️ {note}", color=Colors.FG_SECONDARY),
                                visible=bool(note),
                            ) if note else ft.Container(),
                        ],
                        spacing=Spacing.XS,
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=Spacing.MD,
            bgcolor=Colors.BG_SECONDARY,
            border_radius=BorderRadius.SM,
            border=ft.border.all(1, border_color),
        )
    
    def _get_operation_icon(self, operation_name):
        """Retourne l'icône appropriée selon l'opération"""
        icons_map = {
            "Fichiers temporaires": ft.Icons.DELETE_SWEEP_ROUNDED,
            "Cache Windows Update": ft.Icons.SYSTEM_UPDATE_ROUNDED,
            "Prefetch": ft.Icons.SPEED_ROUNDED,
            "Historique récent": ft.Icons.HISTORY_ROUNDED,
            "Cache miniatures": ft.Icons.IMAGE_ROUNDED,
            "Dumps de crash": ft.Icons.BUG_REPORT_ROUNDED,
            "Windows.old": ft.Icons.FOLDER_DELETE_ROUNDED,
            "Corbeille": ft.Icons.DELETE_ROUNDED,
        }
        return icons_map.get(operation_name, ft.Icons.CLEANING_SERVICES_ROUNDED)
    
    def _select_all(self, e):
        """Sélectionne toutes les opérations"""
        for name in self.selected_operations:
            self.selected_operations[name] = True
            if name in self.operation_checkboxes:
                self.operation_checkboxes[name].value = True
        self._update_summary()
        self.page.update()
    
    def _deselect_all(self, e):
        """Désélectionne toutes les opérations"""
        for name in self.selected_operations:
            self.selected_operations[name] = False
            if name in self.operation_checkboxes:
                self.operation_checkboxes[name].value = False
        self._update_summary()
        self.page.update()
    
    def _update_summary(self):
        """Met à jour le résumé selon les sélections"""
        # Calculer les totaux des opérations sélectionnées
        total_files = 0
        total_size_mb = 0
        
        for op in self.preview_data.get('operations', []):
            if self.selected_operations.get(op['name'], False):
                total_files += op.get('files_count', 0)
                total_size_mb += op.get('size_mb', 0)
        
        # Mettre à jour l'affichage (à implémenter si nécessaire)
        print(f"[DEBUG] Sélection mise à jour: {total_files} fichiers, {total_size_mb:.2f} MB")
    
    def _build_actions(self):
        """Construit les boutons d'action"""
        selected_count = sum(1 for v in self.selected_operations.values() if v)
        
        return ft.Row(
            [
                SecondaryButton(
                    "Annuler",
                    icon=ft.Icons.ARROW_BACK_ROUNDED,
                    on_click=self._go_back,
                    width=200,
                ),
                ft.Container(width=Spacing.LG),
                PrimaryButton(
                    f"Lancer le nettoyage ({selected_count} opérations)",
                    icon=ft.Icons.PLAY_ARROW_ROUNDED,
                    on_click=self._start_cleaning,
                    width=300,
                    disabled=selected_count == 0,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    def _go_back(self, e):
        """Retour à la page principale"""
        print("[DEBUG] Retour à la page principale")
        # Animation de sortie
        self.main_container.opacity = 0
        self.page.update()
        
        import time
        time.sleep(0.3)
        
        # Retour à la page principale
        self.app.show_main_page()
    
    def _start_cleaning(self, e):
        """Lance le nettoyage avec les opérations sélectionnées"""
        print("[DEBUG] Lancement du nettoyage avec sélections")
        
        # Récupérer les opérations sélectionnées
        selected_ops = [name for name, selected in self.selected_operations.items() if selected]
        
        print(f"[INFO] Opérations sélectionnées: {selected_ops}")
        
        # Animation de sortie
        self.main_container.opacity = 0
        self.page.update()
        
        import time
        time.sleep(0.3)
        
        # Lancer le nettoyage réel avec les opérations sélectionnées
        self.app.start_real_cleaning(selected_ops)
