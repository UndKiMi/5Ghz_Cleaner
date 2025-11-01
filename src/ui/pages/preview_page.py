"""
Page de Prévisualisation - Interface Premium et Accessible
Design moderne avec header sticky, animations, tooltips et accessibilité complète

Author: UndKiMi
Version: 5.1.0 - OPTIMIZED
"""
import flet as ft
from datetime import datetime
from src.ui.design_system.theme import Colors, Spacing, BorderRadius


class PreviewPage:
    """Page de prévisualisation avec expérience utilisateur premium"""
    
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
        
        # Références pour mise à jour dynamique
        self.status_message_ref = ft.Ref[ft.Text]()
        self.clean_button_ref = ft.Ref[ft.Container]()
        self.stats_refs = {
            'operations': ft.Ref[ft.Text]()
        }
    
    def build(self):
        """Construit la page avec design premium"""
        return ft.Column(
            [
                # Header sticky avec stats et bouton action
                self._build_sticky_header(),
                
                # Contenu scrollable
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(height=Spacing.LG),
                            
                            # Message de statut dynamique
                            self._build_status_message(),
                            
                            ft.Container(height=Spacing.LG),
                            
                            # Barre d'outils de sélection
                            self._build_action_bar(),
                            
                            ft.Container(height=Spacing.XL),
                            
                            # Liste des opérations
                            self._build_operation_list(),
                            
                            ft.Container(height=Spacing.XL),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                        scroll=ft.ScrollMode.ALWAYS,
                    ),
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )
    
    # ==================== HEADER STICKY ====================
    
    def _build_sticky_header(self):
        """
        Header sticky avec titre, date, stats et bouton action
        Reste visible au scroll avec séparation visuelle
        """
        return ft.Container(
            content=ft.Column(
                [
                    # Titre et date
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.PREVIEW_ROUNDED,
                                    size=24,
                                    color=Colors.ACCENT_PRIMARY,
                                ),
                                width=40,
                                height=40,
                                border_radius=20,
                                bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY),
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(width=Spacing.SM),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Rapport de Prévisualisation",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=Colors.FG_PRIMARY,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, size=11, color=Colors.FG_SECONDARY),
                                            ft.Container(width=4),
                                            ft.Text(
                                                f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
                                                size=11,
                                                color=Colors.FG_SECONDARY,
                                            ),
                                        ],
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                    ),
                    
                    ft.Container(height=Spacing.MD),
                    
                    # Stats tabs + Bouton action
                    self._build_stats_tabs(),
                ],
                spacing=0,
            ),
            padding=ft.padding.all(Spacing.LG),
            bgcolor=Colors.BG_PRIMARY,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )
    
    def _build_stats_tabs(self):
        """
        Tabs visuels avec stats + Bouton action à droite
        Effet hover sur tabs, animation sur bouton
        """
        total_files = self.preview_data.get('total_files', 0)
        total_size_mb = self.preview_data.get('total_size_mb', 0)
        total_size_gb = total_size_mb / 1024
        operations_count = len(self.preview_data.get('operations', []))
        selected_count = sum(1 for v in self.selected_operations.values() if v)
        
        # Vérifier si seules les options safe sont cochées
        only_safe_selected = self._check_only_safe_selected()
        
        # Bouton Retour (discret)
        back_button = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, size=16, color=Colors.FG_SECONDARY),
                    ft.Container(width=6),
                    ft.Text(
                        "Retour",
                        size=13,
                        weight=ft.FontWeight.W_500,
                        color=Colors.FG_SECONDARY,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.MD),
            border_radius=BorderRadius.MD,
            bgcolor=ft.Colors.with_opacity(0.03, Colors.FG_SECONDARY),
            border=ft.border.all(1, ft.Colors.with_opacity(0.15, Colors.FG_SECONDARY)),
            on_click=lambda e: self.app.show_main_page(),
            ink=True,
            tooltip="Retour à la page principale",
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
        
        # Bouton de nettoyage avec désactivation intelligente
        clean_button = ft.Container(
            ref=self.clean_button_ref,
            content=ft.Row(
                [
                    ft.Icon(
                        ft.Icons.CLEANING_SERVICES_ROUNDED if not only_safe_selected else ft.Icons.VERIFIED_USER_ROUNDED,
                        size=18,
                        color=ft.Colors.WHITE if selected_count > 0 else Colors.FG_TERTIARY
                    ),
                    ft.Container(width=8),
                    ft.Text(
                        "Lancer le nettoyage",
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.WHITE if selected_count > 0 else Colors.FG_TERTIARY,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=Spacing.LG, vertical=Spacing.MD),
            border_radius=BorderRadius.MD,
            bgcolor=Colors.SUCCESS if only_safe_selected and selected_count > 0 else Colors.ACCENT_PRIMARY if selected_count > 0 else Colors.BG_SECONDARY,
            on_click=self._start_cleaning if selected_count > 0 else None,
            ink=True if selected_count > 0 else False,
            tooltip="Lance un nettoyage avec les options sélectionnées" if selected_count > 0 else "Veuillez sélectionner au moins une opération à nettoyer",
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.3, Colors.SUCCESS if only_safe_selected else Colors.ACCENT_PRIMARY),
                offset=ft.Offset(0, 4),
            ) if selected_count > 0 else None,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            disabled=selected_count == 0,
        )
        
        return ft.Row(
            [
                # Container des tabs
                ft.Container(
                    content=ft.Row(
                        [
                            self._build_stat_tab(
                                ft.Icons.DESCRIPTION_ROUNDED,
                                "Fichiers détectés",
                                f"{total_files:,}",
                                True,
                                "Nombre total de fichiers qui seront traités"
                            ),
                            self._build_stat_tab(
                                ft.Icons.STORAGE_ROUNDED,
                                "Espace à libérer",
                                f"{total_size_gb:.2f} GB" if total_size_gb >= 1 else f"{total_size_mb:.0f} MB",
                                False,
                                "Espace disque qui sera récupéré"
                            ),
                            self._build_stat_tab(
                                ft.Icons.CHECKLIST_ROUNDED,
                                "Opérations",
                                f"{selected_count}/{operations_count}",
                                False,
                                "Nombre d'opérations sélectionnées",
                                ref=self.stats_refs['operations']
                            ),
                        ],
                        spacing=0,
                    ),
                    bgcolor=Colors.BG_SECONDARY,
                    border_radius=BorderRadius.MD,
                    padding=ft.padding.all(4),
                ),
                
                # Espacement minimal entre tabs et boutons
                ft.Container(width=Spacing.MD),
                
                # Bouton Retour (discret)
                back_button,
                
                # Espacement entre les deux boutons
                ft.Container(width=Spacing.SM),
                
                # Bouton Lancer le nettoyage
                clean_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    def _build_stat_tab(self, icon, label, value, is_active=False, tooltip_text="", ref=None):
        """Tab visuel individuel avec effet hover"""
        icon_color = Colors.ACCENT_PRIMARY if is_active else Colors.FG_SECONDARY
        text_color = Colors.FG_PRIMARY if is_active else Colors.FG_SECONDARY
        text_weight = ft.FontWeight.W_500 if is_active else ft.FontWeight.NORMAL
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=16, color=icon_color),
                    ft.Container(width=Spacing.XS),
                    ft.Column(
                        [
                            ft.Text(label, size=10, color=text_color, weight=text_weight),
                            ft.Text(
                                value,
                                size=13,
                                weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.W_500,
                                color=Colors.ACCENT_PRIMARY if is_active else Colors.FG_SECONDARY,
                                ref=ref,
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
            tooltip=tooltip_text,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            on_hover=self._on_tab_hover,
        )
    
    def _on_tab_hover(self, e):
        """Effet hover sur tab"""
        e.control.scale = 1.02 if e.data == "true" else 1.0
        e.control.update()
    
    # ==================== MESSAGE DE STATUT ====================
    
    def _build_status_message(self):
        """Message dynamique selon le contexte"""
        selected_count = sum(1 for v in self.selected_operations.values() if v)
        only_safe = self._check_only_safe_selected()
        
        total_size_mb = self.preview_data.get('total_size_mb', 0)
        total_size_gb = total_size_mb / 1024
        size_text = f"{total_size_gb:.2f} GB" if total_size_gb >= 1 else f"{total_size_mb:.0f} MB"
        
        # Déterminer le message et l'icône
        if selected_count == 0:
            icon, color = ft.Icons.INFO_OUTLINE_ROUNDED, Colors.FG_SECONDARY
            message = "Sélectionnez les opérations que vous souhaitez effectuer"
        elif only_safe:
            icon, color = ft.Icons.VERIFIED_USER_ROUNDED, Colors.SUCCESS
            message = f"🎉 Nettoyage 100% sécurisé sélectionné • Vous allez gagner {size_text}"
        else:
            icon, color = ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED, Colors.ACCENT_PRIMARY
            message = f"✓ Vous allez libérer {size_text} d'espace disque"
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=18, color=color),
                    ft.Container(width=Spacing.SM),
                    ft.Text(
                        message,
                        size=13,
                        color=color,
                        weight=ft.FontWeight.W_500,
                        ref=self.status_message_ref,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=Spacing.LG, vertical=Spacing.MD),
            border_radius=BorderRadius.MD,
            bgcolor=ft.Colors.with_opacity(0.05, color),
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, color)),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )
    
    # ==================== BARRE D'OUTILS ====================
    
    def _build_action_bar(self):
        """
        Barre d'outils avec boutons de sélection rapide
        Tooltips explicatifs sur chaque bouton
        """
        has_safe_operations = len(self.safe_operations) > 0
        
        return ft.Row(
            [
                # Tout cocher
                self._build_action_button(
                    ft.Icons.CHECK_BOX,
                    "Tout cocher",
                    Colors.ACCENT_PRIMARY,
                    self._select_all,
                    "Sélectionne toutes les opérations disponibles"
                ),
                
                ft.Container(width=Spacing.SM),
                
                # Tout décocher
                self._build_action_button(
                    ft.Icons.CHECK_BOX_OUTLINE_BLANK,
                    "Tout décocher",
                    Colors.FG_SECONDARY,
                    self._deselect_all,
                    "Désélectionne toutes les opérations"
                ),
                
                ft.Container(width=Spacing.SM),
                
                # Sélection safe uniquement
                self._build_action_button(
                    ft.Icons.VERIFIED_USER_ROUNDED,
                    "Sélectionner uniquement les options sécurisées",
                    Colors.SUCCESS,
                    self._select_safe_only if has_safe_operations else None,
                    "Sélectionne uniquement les opérations sans risque pour votre système" if has_safe_operations else "Aucune opération sécurisée disponible",
                    disabled=not has_safe_operations
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    def _build_action_button(self, icon, text, color, on_click, tooltip_text, disabled=False):
        """
        Bouton d'action avec tooltip
        Args:
            icon: Icône du bouton
            text: Texte du bouton
            color: Couleur du bouton
            on_click: Callback au clic
            tooltip_text: Texte du tooltip
            disabled: Si le bouton est désactivé
        """
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=16, color=color if not disabled else Colors.FG_TERTIARY),
                    ft.Container(width=6),
                    ft.Text(
                        text,
                        size=13,
                        color=color if not disabled else Colors.FG_TERTIARY,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
            ),
            padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
            border_radius=BorderRadius.SM,
            bgcolor=ft.Colors.with_opacity(0.05, color) if not disabled else Colors.BG_SECONDARY,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, color) if not disabled else Colors.BORDER_DEFAULT),
            on_click=on_click if not disabled else None,
            ink=True if not disabled else False,
            tooltip=tooltip_text,
            disabled=disabled,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
    
    # ==================== LISTE DES OPÉRATIONS ====================
    
    def _build_operation_list(self):
        """
        Liste verticale des opérations avec tri
        Limite de largeur 700px, centrée
        """
        operations = self.preview_data.get('operations', [])
        
        # Trier : safe d'abord, puis par espace libéré
        sorted_operations = sorted(
            operations,
            key=lambda op: (
                op['name'] not in self.safe_operations,  # Safe en premier
                -op.get('size_mb', 0)  # Puis par taille décroissante
            )
        )
        
        items = []
        for operation in sorted_operations:
            items.append(self._build_operation_item(operation))
            items.append(ft.Container(height=Spacing.SM))
        
        return ft.Column(
            items,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def _build_operation_item(self, operation):
        """
        Item d'opération avec checkbox, icône, badge safe, stats et warning
        Fond accentué quand coché, focus clavier visible
        Args:
            operation: Dictionnaire contenant les infos de l'opération
        """
        name = operation['name']
        files_count = operation.get('files_count', 0)
        size_mb = operation.get('size_mb', 0)
        size_gb = size_mb / 1024
        result = operation.get('result', {})
        warning = result.get('warning', '')
        
        # État de sélection
        is_selected = self.selected_operations.get(name, True)
        is_safe = name in self.safe_operations
        
        # Checkbox avec accessibilité
        def on_change(e):
            self.selected_operations[name] = e.control.value
            self._update_ui()
        
        checkbox = ft.Checkbox(
            value=is_selected,
            on_change=on_change,
            fill_color=Colors.ACCENT_PRIMARY,
            check_color=ft.Colors.WHITE,
            autofocus=False,
        )
        self.operation_checkboxes[name] = checkbox
        
        # Icône selon l'opération
        icon = self._get_operation_icon(name)
        
        return ft.Container(
            content=ft.Row(
                [
                    # Checkbox
                    checkbox,
                    ft.Container(width=Spacing.SM),
                    
                    # Icône
                    ft.Icon(icon, size=20, color=Colors.ACCENT_PRIMARY),
                    ft.Container(width=Spacing.SM),
                    
                    # Nom de l'opération (gras si safe)
                    ft.Text(
                        name,
                        color=Colors.FG_PRIMARY,
                        weight=ft.FontWeight.BOLD if is_safe else ft.FontWeight.W_500,
                        size=14,
                        expand=True,
                    ),
                    
                    # Badge Safe
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.VERIFIED_USER, size=12, color=Colors.SUCCESS),
                                ft.Container(width=4),
                                ft.Text("Sécurisé", size=11, color=Colors.SUCCESS, weight=ft.FontWeight.W_600),
                            ],
                        ),
                        padding=ft.padding.symmetric(horizontal=6, vertical=2),
                        border_radius=BorderRadius.SM,
                        bgcolor=ft.Colors.with_opacity(0.1, Colors.SUCCESS),
                        tooltip="Cette opération est sans risque pour votre système",
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
                    
                    # Warning avec dialog explicatif
                    ft.Container(width=Spacing.SM) if warning and not is_safe else ft.Container(),
                    ft.IconButton(
                        icon=ft.Icons.WARNING_ROUNDED,
                        icon_size=18,
                        icon_color=Colors.ERROR,
                        tooltip="Attention : pour utilisateur avancé - Cliquez pour plus d'infos",
                        on_click=lambda e, w=warning, n=name: self._show_warning_dialog(n, w),
                    ) if warning and not is_safe else ft.Container(),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            width=700,
            padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.MD),
            border_radius=BorderRadius.MD,
            bgcolor=ft.Colors.with_opacity(0.05, Colors.ACCENT_PRIMARY) if is_selected else Colors.BG_SECONDARY,
            border=ft.border.all(2, ft.Colors.with_opacity(0.3, Colors.ACCENT_PRIMARY) if is_selected else Colors.BORDER_DEFAULT),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
    
    # ==================== DIALOGS ====================
    
    def _show_warning_dialog(self, operation_name, warning_text):
        """
        Affiche un dialog explicatif pour les warnings
        Args:
            operation_name: Nom de l'opération
            warning_text: Texte du warning
        """
        dialog = ft.AlertDialog(
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.WARNING_ROUNDED, size=24, color=Colors.ERROR),
                    ft.Container(width=Spacing.SM),
                    ft.Text(
                        "Attention : Opération avancée",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=Colors.FG_PRIMARY,
                    ),
                ],
            ),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            f"Opération : {operation_name}",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=Colors.FG_PRIMARY,
                        ),
                        ft.Container(height=Spacing.SM),
                        ft.Text(
                            warning_text,
                            size=13,
                            color=Colors.FG_SECONDARY,
                        ),
                        ft.Container(height=Spacing.MD),
                        ft.Container(
                            content=ft.Text(
                                "⚠️ Cette opération est réservée aux utilisateurs expérimentés. "
                                "Assurez-vous de comprendre les implications avant de continuer.",
                                size=12,
                                color=Colors.WARNING,
                                weight=ft.FontWeight.W_500,
                            ),
                            padding=Spacing.SM,
                            border_radius=BorderRadius.SM,
                            bgcolor=ft.Colors.with_opacity(0.1, Colors.WARNING),
                        ),
                    ],
                    tight=True,
                ),
                width=400,
            ),
            actions=[
                ft.TextButton(
                    "J'ai compris",
                    on_click=lambda e: self._close_dialog(),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def _close_dialog(self):
        """Ferme le dialog actif"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
    
    # ==================== UTILITAIRES ====================
    
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
    
    def _check_only_safe_selected(self):
        """Vérifie si seules les options safe sont cochées"""
        selected = [name for name, checked in self.selected_operations.items() if checked]
        if not selected:
            return False
        return all(name in self.safe_operations for name in selected)
    
    def _update_ui(self):
        """Met à jour l'interface après un changement"""
        # Mettre à jour le compteur d'opérations
        selected_count = sum(1 for v in self.selected_operations.values() if v)
        operations_count = len(self.preview_data.get('operations', []))
        only_safe_selected = self._check_only_safe_selected()
        
        # Mettre à jour le compteur dans les stats
        if self.stats_refs['operations'].current:
            self.stats_refs['operations'].current.value = f"{selected_count}/{operations_count}"
        
        # Mettre à jour le bouton de nettoyage
        if self.clean_button_ref.current:
            button = self.clean_button_ref.current
            
            # Mettre à jour les couleurs
            if selected_count > 0:
                button.bgcolor = Colors.SUCCESS if only_safe_selected else Colors.ACCENT_PRIMARY
                button.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=12,
                    color=ft.Colors.with_opacity(0.3, Colors.SUCCESS if only_safe_selected else Colors.ACCENT_PRIMARY),
                    offset=ft.Offset(0, 4),
                )
                button.ink = True
                button.disabled = False
                button.tooltip = "Lance un nettoyage avec les options sélectionnées"
            else:
                button.bgcolor = Colors.BG_SECONDARY
                button.shadow = None
                button.ink = False
                button.disabled = True
                button.tooltip = "Veuillez sélectionner au moins une opération à nettoyer"
            
            # Mettre à jour l'icône et le texte
            button.content.controls[0].color = ft.Colors.WHITE if selected_count > 0 else Colors.FG_TERTIARY
            button.content.controls[0].name = ft.Icons.CLEANING_SERVICES_ROUNDED if not only_safe_selected else ft.Icons.VERIFIED_USER_ROUNDED
            button.content.controls[2].color = ft.Colors.WHITE if selected_count > 0 else Colors.FG_TERTIARY
            
            button.on_click = self._start_cleaning if selected_count > 0 else None
        
        self.page.update()
    
    # ==================== ACTIONS ====================
    
    def _select_all(self, e):
        """Sélectionne toutes les opérations"""
        for name in self.selected_operations:
            self.selected_operations[name] = True
            if name in self.operation_checkboxes:
                self.operation_checkboxes[name].value = True
        self._update_ui()
    
    def _deselect_all(self, e):
        """Désélectionne toutes les opérations"""
        for name in self.selected_operations:
            self.selected_operations[name] = False
            if name in self.operation_checkboxes:
                self.operation_checkboxes[name].value = False
        self._update_ui()
    
    def _select_safe_only(self, e):
        """Sélectionne uniquement les opérations sécurisées"""
        for name in self.selected_operations:
            is_safe = name in self.safe_operations
            self.selected_operations[name] = is_safe
            if name in self.operation_checkboxes:
                self.operation_checkboxes[name].value = is_safe
        self._update_ui()
    
    def _start_cleaning(self, e):
        """Lance le nettoyage avec les opérations sélectionnées"""
        selected_ops = [name for name, checked in self.selected_operations.items() if checked]
        if selected_ops:
            # TODO: Implémenter la barre de progression
            self.app.start_real_cleaning(selected_ops)
