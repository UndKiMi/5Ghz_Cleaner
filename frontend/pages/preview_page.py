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
        
        # Références aux widgets de statistiques pour mise à jour dynamique
        self.stats_files_text = None
        self.stats_operations_text = None
        self.stats_time_text = None
        self.stats_space_text = None
        self.stats_space_label = None
        self.stats_banner = None
        
        # Par défaut, tout est sélectionné
        for op in preview_data.get('operations', []):
            self.selected_operations[op['name']] = True
    
    def build(self):
        """Construit la page de prévisualisation optimisée avec transition fluide"""
        # Container principal avec animation et scroll auto
        self.main_container = ft.Container(
            content=ft.Column(
                [
                    self._build_header(),
                    ft.Container(height=Spacing.LG),
                    self._build_summary(),
                    ft.Container(height=Spacing.LG),
                    self._build_operations_list(),
                    ft.Container(height=Spacing.LG),
                    self._build_actions(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,  # Scroll uniquement si nécessaire
                spacing=0,
            ),
            padding=Spacing.XL,
            opacity=0,  # Commence invisible pour animation d'entrée
            animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_IN_OUT),
            expand=True,
        )
        
        # L'animation d'entrée sera gérée par la page appelante
        # pour une transition plus fluide
        
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
        """Construit le résumé global amélioré avec mise à jour dynamique"""
        total_files = self.preview_data.get('total_files', 0)
        total_size_mb = self.preview_data.get('total_size_mb', 0)
        total_size_gb = total_size_mb / 1024
        operations_count = len(self.preview_data.get('operations', []))
        
        # Déterminer la couleur selon l'espace
        if total_size_mb > 1000:  # > 1 GB
            space_color = Colors.SUCCESS
            space_emoji = "🚀"
        elif total_size_mb > 100:  # > 100 MB
            space_color = Colors.ACCENT_PRIMARY
            space_emoji = "✅"
        else:
            space_color = Colors.WARNING
            space_emoji = "⚠️"
        
        # Créer les textes avec références
        self.stats_space_text = BodyText(
            f"{total_size_mb:.2f} MB" if total_size_mb < 1024 else f"{total_size_gb:.2f} GB",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=space_color,
        )
        
        self.stats_space_label = Caption(
            "d'espace disque à libérer",
            size=14,
            color=Colors.FG_SECONDARY,
        )
        
        # Bannière avec référence
        self.stats_banner = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                space_emoji,
                                size=48,
                            ),
                            ft.Container(width=Spacing.MD),
                            ft.Column(
                                [
                                    self.stats_space_text,
                                    self.stats_space_label,
                                ],
                                spacing=0,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
            ),
            padding=Spacing.XL,
            bgcolor=ft.Colors.with_opacity(0.05, space_color),
            border_radius=BorderRadius.LG,
            border=ft.border.all(2, space_color),
        )
        
        # Créer les cartes de stats avec références
        self.stats_files_text = ft.Text(f"{total_files:,}", size=20, weight=ft.FontWeight.BOLD, color=Colors.FG_PRIMARY)
        self.stats_operations_text = ft.Text(f"{operations_count}", size=20, weight=ft.FontWeight.BOLD, color=Colors.FG_PRIMARY)
        self.stats_time_text = ft.Text(f"{max(1, operations_count // 2)} min", size=20, weight=ft.FontWeight.BOLD, color=Colors.FG_PRIMARY)
        
        return ft.Container(
            content=ft.Column(
                [
                    # Bannière principale
                    self.stats_banner,
                    ft.Container(height=Spacing.LG),
                    # Statistiques détaillées
                    ft.Row(
                        [
                            self._build_stat_card_with_ref(
                                "Fichiers",
                                self.stats_files_text,
                                ft.Icons.DESCRIPTION_OUTLINED,
                                Colors.ACCENT_PRIMARY,
                            ),
                            ft.Container(width=Spacing.MD),
                            self._build_stat_card_with_ref(
                                "Opérations",
                                self.stats_operations_text,
                                ft.Icons.CHECKLIST_ROUNDED,
                                Colors.ACCENT_PRIMARY,
                            ),
                            ft.Container(width=Spacing.MD),
                            self._build_stat_card_with_ref(
                                "Temps estimé",
                                self.stats_time_text,
                                ft.Icons.TIMER_OUTLINED,
                                Colors.ACCENT_PRIMARY,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
    
    def _build_stat_card(self, label, value, icon, color):
        """Construit une carte de statistique améliorée"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(icon, size=28, color=color),
                        padding=Spacing.SM,
                        bgcolor=ft.Colors.with_opacity(0.1, color),
                        border_radius=BorderRadius.SM,
                    ),
                    ft.Container(height=Spacing.SM),
                    BodyText(value, size=20, weight=ft.FontWeight.BOLD, color=Colors.FG_PRIMARY),
                    Caption(label, color=Colors.FG_SECONDARY, size=12),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=Spacing.XS,
            ),
            width=180,
            padding=Spacing.MD,
            bgcolor=Colors.BG_SECONDARY,
            border_radius=BorderRadius.MD,
            border=ft.border.all(1, Colors.BORDER_DEFAULT),
        )
    
    def _build_stat_card_with_ref(self, label, value_text_widget, icon, color):
        """Construit une carte de statistique avec référence au widget texte"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(icon, size=28, color=color),
                        padding=Spacing.SM,
                        bgcolor=ft.Colors.with_opacity(0.1, color),
                        border_radius=BorderRadius.SM,
                    ),
                    ft.Container(height=Spacing.SM),
                    value_text_widget,
                    Caption(label, color=Colors.FG_SECONDARY, size=12),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=Spacing.XS,
            ),
            width=180,
            padding=Spacing.MD,
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
                            scroll=ft.ScrollMode.AUTO,
                            spacing=0,
                        ),
                        height=350,  # Hauteur optimisée pour éviter le scroll excessif
                    ),
                ],
                spacing=0,
            ),
            width=800,
        )
    
    def _build_operation_card(self, operation):
        """Construit une carte d'opération améliorée avec checkbox"""
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
        if warning:
            border_color = Colors.ERROR
            bg_color = ft.Colors.with_opacity(0.03, Colors.ERROR)
        elif size_mb > 500:
            border_color = Colors.SUCCESS
            bg_color = ft.Colors.with_opacity(0.03, Colors.SUCCESS)
        else:
            border_color = Colors.BORDER_DEFAULT
            bg_color = Colors.BG_SECONDARY
        
        # Barre de progression visuelle de la taille
        max_size = 1000  # MB
        progress_percent = min(size_mb / max_size, 1.0) if size_mb > 0 else 0
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            checkbox,
                            ft.Container(width=Spacing.SM),
                            ft.Container(
                                content=ft.Icon(icon, size=24, color=Colors.ACCENT_PRIMARY),
                                padding=Spacing.XS,
                                bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY),
                                border_radius=BorderRadius.SM,
                            ),
                            ft.Container(width=Spacing.MD),
                            ft.Column(
                                [
                                    BodyText(name, weight=ft.FontWeight.BOLD, size=15),
                                    ft.Container(height=Spacing.XS),
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, size=14, color=Colors.FG_TERTIARY),
                                            ft.Container(width=4),
                                            Caption(f"{files_count:,}", color=Colors.FG_SECONDARY),
                                            ft.Container(width=Spacing.SM),
                                            ft.Icon(ft.Icons.STORAGE_OUTLINED, size=14, color=Colors.FG_TERTIARY),
                                            ft.Container(width=4),
                                            ft.Text(
                                                f"{size_mb:.2f} MB" if size_mb < 1024 else f"{size_mb/1024:.2f} GB",
                                                size=Typography.SIZE_SM,
                                                color=Colors.SUCCESS if size_mb > 100 else Colors.FG_SECONDARY,
                                                weight=ft.FontWeight.BOLD if size_mb > 100 else ft.FontWeight.NORMAL,
                                            ),
                                        ],
                                        spacing=0,
                                    ),
                                ],
                                spacing=Spacing.XS,
                                expand=True,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    # Barre de progression visuelle
                    ft.Container(
                        content=ft.Container(
                            bgcolor=Colors.ACCENT_PRIMARY,
                            border_radius=BorderRadius.SM,
                            height=4,
                        ),
                        width=progress_percent * 700,
                        height=4,
                        border_radius=BorderRadius.SM,
                        bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY),
                        margin=ft.margin.only(top=Spacing.SM, left=40),
                    ) if size_mb > 0 else ft.Container(),
                    # Avertissement si présent
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.WARNING_ROUNDED, size=16, color=Colors.ERROR),
                                ft.Container(width=Spacing.XS),
                                Caption(warning, color=Colors.ERROR, size=12),
                            ],
                        ),
                        margin=ft.margin.only(top=Spacing.XS, left=40),
                        visible=bool(warning),
                    ) if warning else ft.Container(),
                    # Note si présente
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text("ℹ️", size=12),
                                ft.Container(width=Spacing.XS),
                                Caption(note, color=Colors.FG_SECONDARY, size=12),
                            ],
                        ),
                        margin=ft.margin.only(top=Spacing.XS, left=40),
                        visible=bool(note),
                    ) if note else ft.Container(),
                ],
                spacing=0,
            ),
            padding=Spacing.MD,
            bgcolor=bg_color,
            border_radius=BorderRadius.MD,
            border=ft.border.all(1, border_color),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
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
        """Met à jour le résumé selon les sélections en temps réel"""
        # Calculer les totaux des opérations sélectionnées
        total_files = 0
        total_size_mb = 0
        selected_count = 0
        
        for op in self.preview_data.get('operations', []):
            if self.selected_operations.get(op['name'], False):
                total_files += op.get('files_count', 0)
                total_size_mb += op.get('size_mb', 0)
                selected_count += 1
        
        total_size_gb = total_size_mb / 1024
        
        # Déterminer la couleur selon l'espace
        if total_size_mb > 1000:  # > 1 GB
            space_color = Colors.SUCCESS
        elif total_size_mb > 100:  # > 100 MB
            space_color = Colors.ACCENT_PRIMARY
        else:
            space_color = Colors.WARNING
        
        # Mettre à jour les widgets de statistiques
        if self.stats_space_text:
            self.stats_space_text.value = f"{total_size_mb:.2f} MB" if total_size_mb < 1024 else f"{total_size_gb:.2f} GB"
            self.stats_space_text.color = space_color
        
        if self.stats_files_text:
            self.stats_files_text.value = f"{total_files:,}"
        
        if self.stats_operations_text:
            self.stats_operations_text.value = f"{selected_count}"
        
        if self.stats_time_text:
            self.stats_time_text.value = f"{max(1, selected_count // 2)} min"
        
        # Mettre à jour la bannière
        if self.stats_banner:
            self.stats_banner.bgcolor = ft.Colors.with_opacity(0.05, space_color)
            self.stats_banner.border = ft.border.all(2, space_color)
        
        # Mettre à jour la page
        self.page.update()
        
        print(f"[DEBUG] Sélection mise à jour: {total_files} fichiers, {total_size_mb:.2f} MB, {selected_count} opérations")
    
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
