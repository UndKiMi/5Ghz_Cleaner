"""
Main Page - Page principale de l'application
Contient toutes les fonctionnalités de nettoyage
"""
import flet as ft
from ..design_system import *
from ..design_system.theme import Colors, Spacing, Typography, BorderRadius
from backend import cleaner
from backend.logger import CleaningLogger
from backend.security import security_manager


class MainPage:
    def __init__(self, page: ft.Page, app_instance):
        self.page = page
        self.app = app_instance
        self.cleaning_in_progress = False
        self.progress_bar = None
        self.status_text = None
        self.action_button = None
        self.dry_run_button = None
        self.dry_run_completed = False  # Bloque le nettoyage jusqu'au dry-run
        self.current_tab = "quick"  # "quick" or "advanced"
        
    def build(self):
        """Construit la page principale"""
        self.content_container = ft.Container(
            content=ft.Column(
                [
                    self._build_actions_section(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=0,
            ),
            opacity=1,
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )
        
        self.main_container = ft.Container(
            content=ft.Column(
                [
                    self._build_header(),
                    Spacer(height=Spacing.XXL),
                    self._build_tabs(),
                    Spacer(height=Spacing.HUGE),
                    self.content_container,
                    Spacer(height=Spacing.MEGA),
                    self._build_action_button(),
                    ft.Container(expand=True),
                    self._build_footer(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=0,
            ),
            bgcolor=Colors.BG_PRIMARY,
            padding=ft.padding.symmetric(horizontal=Spacing.HUGE, vertical=Spacing.XXL),
            expand=True,
            opacity=1,
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )
        
        return self.main_container
    
    def _build_header(self):
        """Construit l'en-tête avec titre"""
        return ft.Row(
            [
                ft.Icon(ft.Icons.SHIELD_OUTLINED, size=20, color=Colors.ACCENT_PRIMARY),
                ft.Container(width=Spacing.SM),
                ft.Column(
                    [
                        BodyText("5GH'z Cleaner", weight=Typography.WEIGHT_MEDIUM, size=14),
                        Caption("Optimisation et Nettoyage Windows", color=Colors.FG_SECONDARY),
                    ],
                    spacing=0,
                ),
            ],
        )
    
    def _build_tabs(self):
        """Construit les onglets de navigation"""
        self.tab_quick = self._build_tab_button("Nettoyage rapide", "quick", "assets/icons/cleaning.svg")
        self.tab_advanced = self._build_tab_button("Options avancées", "advanced", ft.Icons.SETTINGS_OUTLINED)
        
        return ft.Row(
            [
                self.tab_quick,
                ft.Container(width=Spacing.MD),
                self.tab_advanced,
            ],
        )
    
    def _build_tab_button(self, text, tab_id, icon):
        """Construit un bouton d'onglet"""
        is_active = self.current_tab == tab_id
        
        # Icône SVG ou Material
        if isinstance(icon, str) and icon.endswith('.svg'):
            icon_widget = ft.Image(
                src=icon,
                width=16,
                height=16,
                color=Colors.ACCENT_PRIMARY if is_active else Colors.FG_SECONDARY,
            )
        else:
            icon_widget = ft.Icon(
                icon,
                size=16,
                color=Colors.ACCENT_PRIMARY if is_active else Colors.FG_SECONDARY
            )
        
        return ft.Container(
            content=ft.Row(
                [
                    icon_widget,
                    ft.Container(width=Spacing.XS),
                    BodyText(
                        text,
                        size=13,
                        color=Colors.FG_PRIMARY if is_active else Colors.FG_SECONDARY,
                        weight=Typography.WEIGHT_MEDIUM if is_active else Typography.WEIGHT_REGULAR,
                    ),
                ],
            ),
            padding=ft.padding.symmetric(horizontal=Spacing.LG, vertical=Spacing.SM),
            border=ft.border.only(
                bottom=ft.BorderSide(2, Colors.ACCENT_PRIMARY if is_active else "transparent")
            ),
            on_click=lambda e, tid=tab_id: self._switch_tab(tid),
            ink=True,
            data=tab_id,
        )
    
    def _build_actions_section(self):
        """Construit la section des actions rapides"""
        return ft.Column(
            [
                BodyText("Actions rapides", weight=Typography.WEIGHT_MEDIUM, size=16),
                Spacer(height=4),
                Caption(
                    "Les opérations sont compatibles pour optimiser votre système Windows",
                    color=Colors.FG_SECONDARY,
                ),
                Spacer(height=Spacing.XXXL),
                ft.Row(
                    [
                        self._build_action_card(
                            icon="assets/icons/folder.svg",
                            title="Fichiers temporaires",
                            description="Libère rapidement de l'espace disque en supprimant les fichiers temporaires et le cache système inutiles.",
                            action_key="temp_files",
                        ),
                        ft.Container(width=Spacing.XXXL),
                        self._build_action_card(
                            icon=ft.Icons.MEMORY_OUTLINED,
                            title="RAM Standby",
                            description="Optimisation de la vitesse en vidant la mémoire standby.",
                            action_key="ram_standby",
                        ),
                        ft.Container(width=Spacing.XXXL),
                        self._build_action_card(
                            icon=ft.Icons.STORAGE_OUTLINED,
                            title="Cache DNS",
                            description="Réinitialisation du cache DNS pour résoudre instantanément les problèmes de connexion réseau.",
                            action_key="cache_dns",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
    
    def _build_action_card(self, icon, title, description, action_key):
        """Construit une carte d'action"""
        # Icône SVG ou Material
        if isinstance(icon, str) and icon.endswith('.svg'):
            icon_widget = ft.Image(
                src=icon,
                width=40,
                height=40,
                color=Colors.ACCENT_PRIMARY,
            )
        else:
            icon_widget = ft.Icon(icon, size=40, color=Colors.ACCENT_PRIMARY)
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=icon_widget,
                        padding=Spacing.MD,
                    ),
                    Spacer(height=Spacing.SM),
                    BodyText(
                        title,
                        weight=Typography.WEIGHT_MEDIUM,
                        text_align=ft.TextAlign.CENTER,
                        size=14,
                    ),
                    Spacer(height=Spacing.XS),
                    Caption(
                        description,
                        text_align=ft.TextAlign.CENTER,
                        color=Colors.FG_SECONDARY,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            width=220,
            height=160,
            bgcolor=Colors.BG_SECONDARY,
            border_radius=BorderRadius.MD,
            border=ft.border.all(1, Colors.BORDER_DEFAULT),
            padding=Spacing.LG,
        )
    
    def _build_action_button(self):
        """Construit les boutons d'action (Dry-Run + Nettoyage)"""
        self.status_text = Caption(
            "⚠️ Vous devez d'abord prévisualiser le nettoyage avant de pouvoir l'exécuter.",
            text_align=ft.TextAlign.CENTER,
            color=Colors.FG_SECONDARY,
        )
        
        self.progress_bar = ft.ProgressBar(
            width=500,
            height=3,
            color=Colors.ACCENT_PRIMARY,
            bgcolor=Colors.BORDER_DEFAULT,
            visible=False,
        )
        
        # Bouton Dry-Run (Prévisualisation)
        def on_dry_run_click(e):
            print("[DEBUG] Dry-Run button clicked!")
            self._start_dry_run(e)
        
        self.dry_run_button = ft.ElevatedButton(
            text="Prévisualiser le nettoyage",
            icon=ft.Icons.PREVIEW_ROUNDED,
            on_click=on_dry_run_click,
            bgcolor=Colors.BG_SECONDARY,
            color=Colors.ACCENT_PRIMARY,
            height=50,
            width=300,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=BorderRadius.MD),
                side=ft.BorderSide(2, Colors.ACCENT_PRIMARY),
            ),
        )
        
        # Bouton Nettoyage (Bloqué par défaut)
        def on_button_click(e):
            if not self.dry_run_completed:
                print("[DEBUG] Cleaning blocked - Dry-run required first")
                return
            print("[DEBUG] Cleaning button clicked!")
            self._start_cleaning(e)
        
        self.action_button = ft.ElevatedButton(
            text="Lancer le nettoyage",
            icon=ft.Icons.PLAY_ARROW_ROUNDED,
            on_click=on_button_click,
            bgcolor=Colors.BG_SECONDARY,  # Grisé par défaut
            color=Colors.FG_TERTIARY,     # Texte grisé
            height=50,
            width=300,
            disabled=True,  # Bloqué par défaut
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=BorderRadius.MD),
            ),
        )
        
        return ft.Column(
            [
                self.status_text,
                Spacer(height=Spacing.XXL),
                self.progress_bar,
                Spacer(height=Spacing.MD),
                self.dry_run_button,
                Spacer(height=Spacing.SM),
                self.action_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def _build_footer(self):
        """Construit le pied de page"""
        return ft.Row(
            [
                Caption("5GH'z Cleaner v1.0 • Réalisé par"),
                ft.Container(width=Spacing.XS),
                TextButton(
                    text="K_iMi",
                    on_click=lambda e: __import__('webbrowser').open("https://github.com/UndKiMi"),
                    size=Typography.SIZE_SM,
                ),
                Caption("• Tous droits réservés"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    def _build_advanced_options(self):
        """Construit la section des options avancées"""
        return ft.Column(
            [
                BodyText("Paramètres avancés", weight=Typography.WEIGHT_MEDIUM, size=16),
                Spacer(height=Spacing.XS),
                Caption(
                    "Personnalisez les opérations de nettoyage pour vos besoins",
                    color=Colors.FG_SECONDARY,
                ),
                Spacer(height=Spacing.XXL),
                self._build_option_item(
                    "Libérer RAM Standby",
                    "Vide la mémoire en attente pour libérer de la RAM",
                    "clear_standby_memory",
                    True,
                    recommended=True
                ),
                Spacer(height=Spacing.LG),
                self._build_option_item(
                    "Flush DNS",
                    "Vide le cache DNS pour améliorer les performances réseau",
                    "flush_dns",
                    True,
                    recommended=True
                ),
                Spacer(height=Spacing.LG),
                self._build_option_item(
                    "Désactiver télémétrie",
                    "Désactive les services de collecte de données de Windows",
                    "disable_telemetry",
                    False,
                    recommended=False
                ),
                Spacer(height=Spacing.LG),
                self._build_option_item(
                    "Nettoyer logs volumineux",
                    "Supprime les fichiers journaux volumineux et inutiles",
                    "clear_large_logs",
                    True,
                    recommended=True
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
    
    def _build_option_item(self, title, description, key, default_value, recommended=False):
        """Construit un élément d'option avancée"""
        switch = ft.Switch(
            value=self.app.advanced_options.get(key, default_value),
            active_color=Colors.ACCENT_PRIMARY,
            on_change=lambda e: self._update_option(key, e.control.value),
        )
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    BodyText(title, weight=Typography.WEIGHT_MEDIUM, size=14),
                                    ft.Container(width=Spacing.XS),
                                    ft.Container(
                                        content=Caption("Recommandé", color=Colors.ACCENT_PRIMARY),
                                        bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY),
                                        padding=ft.padding.symmetric(horizontal=Spacing.SM, vertical=2),
                                        border_radius=BorderRadius.SM,
                                        visible=recommended,
                                    ),
                                ],
                            ),
                            Spacer(height=Spacing.XS),
                            Caption(description, color=Colors.FG_SECONDARY),
                        ],
                        expand=True,
                        spacing=0,
                    ),
                    switch,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=Colors.BG_SECONDARY,
            padding=Spacing.LG,
            border_radius=BorderRadius.MD,
            border=ft.border.all(1, Colors.BORDER_DEFAULT),
        )
    
    def _update_option(self, key, value):
        """Met à jour une option avancée"""
        self.app.advanced_options[key] = value
        print(f"[INFO] Option {key} set to {value}")
    
    def _switch_tab(self, tab_id):
        """Change d'onglet avec animation fluide"""
        if self.current_tab == tab_id:
            return
        
        self.current_tab = tab_id
        
        # Animation de sortie (fade out)
        self.content_container.opacity = 0
        self.page.update()
        
        # Attendre la fin de l'animation
        import time
        time.sleep(0.15)
        
        # Mettre à jour l'apparence des onglets
        self._update_tab_styles()
        
        # Mettre à jour le contenu
        if tab_id == "quick":
            self.content_container.content = ft.Column(
                [self._build_actions_section()],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=0,
            )
        else:
            self.content_container.content = ft.Column(
                [self._build_advanced_options()],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=0,
            )
        
        # Animation d'entrée (fade in)
        self.content_container.opacity = 1
        self.page.update()
    
    def _update_tab_styles(self):
        """Met à jour les styles des onglets avec animation"""
        for tab in [self.tab_quick, self.tab_advanced]:
            is_active = tab.data == self.current_tab
            
            # Ajouter l'animation sur le container
            if not hasattr(tab, 'animate_border'):
                tab.animate = ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT)
            
            # Mettre à jour la bordure
            tab.border = ft.border.only(
                bottom=ft.BorderSide(2, Colors.ACCENT_PRIMARY if is_active else "transparent")
            )
            
            # Mettre à jour l'icône et le texte
            icon_widget = tab.content.controls[0]
            text_widget = tab.content.controls[2]
            
            if hasattr(icon_widget, 'color'):
                icon_widget.color = Colors.ACCENT_PRIMARY if is_active else Colors.FG_SECONDARY
            
            text_widget.color = Colors.FG_PRIMARY if is_active else Colors.FG_SECONDARY
            text_widget.weight = Typography.WEIGHT_MEDIUM if is_active else Typography.WEIGHT_REGULAR
    
    def _start_dry_run(self, e):
        """Lance la prévisualisation (Dry-Run)"""
        print("[DEBUG] _start_dry_run called!")
        
        # PROTECTION ANTI-SPAM: Bloquer si une opération est en cours
        if self.cleaning_in_progress:
            print("[DEBUG] Operation already in progress - SPAM BLOCKED")
            return
        
        # PROTECTION ANTI-SPAM: Bloquer si le bouton est désactivé
        if self.dry_run_button and self.dry_run_button.disabled:
            print("[DEBUG] Button disabled - SPAM BLOCKED")
            return
        
        print("[DEBUG] Starting dry-run preview...")
        self.cleaning_in_progress = True
        
        try:
            # Désactiver le bouton dry-run pendant l'analyse
            self.dry_run_button.disabled = True
            self.dry_run_button.text = "Analyse en cours..."
            self.page.update()
            
            # Lancer le dry-run dans un thread
            import threading
            threading.Thread(target=self._run_dry_run, daemon=True).start()
            print("[DEBUG] Dry-run thread started")
        except Exception as ex:
            print(f"[ERROR] Failed to start dry-run: {ex}")
            import traceback
            traceback.print_exc()
            self.cleaning_in_progress = False
            # Réactiver le bouton en cas d'erreur
            if self.dry_run_button:
                self.dry_run_button.disabled = False
                self.dry_run_button.text = "Prévisualiser le nettoyage"
                self.page.update()
    
    def _run_dry_run(self):
        """Exécute le dry-run dans un thread séparé"""
        import time
        from backend.dry_run import dry_run_manager
        
        print("[DEBUG] _run_dry_run started in thread")
        
        try:
            # Mettre à jour le statut
            self.status_text.value = "Analyse en cours... Veuillez patienter."
            self.status_text.color = Colors.ACCENT_PRIMARY
            self.page.update()
            
            # Exécuter le dry-run
            print("[INFO] Running dry-run preview...")
            preview = dry_run_manager.preview_full_cleaning(self.app.advanced_options)
            
            # Dry-run terminé avec succès
            print("[SUCCESS] Dry-run completed successfully")
            
            # Débloquer le bouton de nettoyage
            self.dry_run_completed = True
            
            # Sauvegarder les données de prévisualisation
            self.preview_data = preview
            
            # Afficher la page de prévisualisation avec sélection
            print("[INFO] Affichage de la page de prévisualisation...")
            self._show_preview_page(preview)
            
        except Exception as ex:
            print(f"[ERROR] Dry-run failed: {ex}")
            import traceback
            traceback.print_exc()
            
            # Réactiver le bouton dry-run
            self.dry_run_button.disabled = False
            self.dry_run_button.text = "Prévisualiser le nettoyage"
            
            self.status_text.value = f"❌ Erreur lors de la prévisualisation : {str(ex)}"
            self.status_text.color = Colors.ERROR
            self.page.update()
        
        finally:
            self.cleaning_in_progress = False
    
    def _show_preview_page(self, preview_data):
        """Affiche la page de prévisualisation avec sélection"""
        try:
            # Animation de sortie de la page actuelle
            if hasattr(self, 'main_container'):
                self.main_container.opacity = 0
                self.page.update()
            
            import time
            time.sleep(0.3)
            
            # Importer et créer la page de prévisualisation
            from frontend.pages.preview_page import PreviewPage
            
            preview_page = PreviewPage(self.page, self.app, preview_data)
            
            # Remplacer le contenu de la page
            self.page.controls.clear()
            self.page.add(preview_page.build())
            self.page.update()
            
            print("[SUCCESS] Page de prévisualisation affichée")
            
        except Exception as ex:
            print(f"[ERROR] Failed to show preview page: {ex}")
            import traceback
            traceback.print_exc()
            
            # En cas d'erreur, réactiver les boutons
            self.dry_run_button.disabled = False
            self.dry_run_button.text = "Prévisualiser le nettoyage"
            self.page.update()
    
    def _show_security_warning(self):
        """Affiche un avertissement de sécurité en cas de tentative de contournement"""
        try:
            # Créer une alerte de sécurité
            def close_alert(e):
                alert_dialog.open = False
                self.page.update()
            
            alert_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Row(
                    [
                        ft.Icon(ft.Icons.SECURITY, color=Colors.ERROR, size=32),
                        ft.Container(width=Spacing.SM),
                        ft.Text("Avertissement de Sécurité", size=20, weight=ft.FontWeight.BOLD, color=Colors.ERROR),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "⚠️ TENTATIVE DE CONTOURNEMENT DÉTECTÉE",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=Colors.ERROR,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(height=Spacing.MD),
                            ft.Text(
                                "Pour des raisons de sécurité, vous DEVEZ prévisualiser le nettoyage avant de pouvoir l'exécuter.",
                                size=14,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(height=Spacing.SM),
                            ft.Text(
                                "Cette mesure vous protège contre les suppressions accidentelles.",
                                size=13,
                                color=Colors.FG_SECONDARY,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(height=Spacing.MD),
                            ft.Container(
                                content=ft.Text(
                                    "Veuillez cliquer sur 'Prévisualiser le nettoyage' d'abord.",
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color=Colors.ACCENT_PRIMARY,
                                ),
                                bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY),
                                padding=Spacing.MD,
                                border_radius=BorderRadius.SM,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    width=400,
                ),
                actions=[
                    ft.TextButton(
                        "J'ai compris",
                        on_click=close_alert,
                        style=ft.ButtonStyle(
                            color=Colors.ACCENT_PRIMARY,
                        ),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
                bgcolor=Colors.BG_SECONDARY,
            )
            
            self.page.dialog = alert_dialog
            alert_dialog.open = True
            self.page.update()
            
            print("[SECURITY] Security warning displayed to user")
            
        except Exception as ex:
            print(f"[ERROR] Failed to show security warning: {ex}")
    
    def _start_cleaning(self, e):
        """Lance le processus de nettoyage"""
        print("[DEBUG] _start_cleaning called!")
        
        # ========================================================================
        # SÉCURITÉ CRITIQUE: ANTI-CONTOURNEMENT
        # ========================================================================
        # Cette vérification DOIT être la première chose exécutée
        # Elle empêche tout contournement de la sécurité
        
        if not self.dry_run_completed:
            print("[SECURITY] TENTATIVE DE CONTOURNEMENT DÉTECTÉE!")
            print("[SECURITY] Le nettoyage est BLOQUÉ - Dry-run obligatoire")
            
            # Afficher un avertissement de sécurité à l'utilisateur
            self._show_security_warning()
            return
        
        # Vérification supplémentaire: le bouton doit être débloqué
        if self.action_button and self.action_button.disabled:
            print("[SECURITY] TENTATIVE DE CONTOURNEMENT DÉTECTÉE!")
            print("[SECURITY] Le bouton est désactivé - Accès refusé")
            self._show_security_warning()
            return
        
        # ========================================================================
        
        if self.cleaning_in_progress:
            print("[DEBUG] Cleaning already in progress, returning")
            return
        
        print("[DEBUG] Starting cleaning process...")
        print("[SECURITY] Dry-run completed - Cleaning authorized")
        self.cleaning_in_progress = True
        
        try:
            # Animation de sortie
            print("[DEBUG] Fading out main page...")
            self.main_container.opacity = 0
            self.page.update()
            
            import time
            time.sleep(0.3)
            
            # Remplacer le contenu de la page
            print("[DEBUG] Showing cleaning page...")
            self._show_cleaning_page()
            
            print("[DEBUG] Starting cleaning thread...")
            import threading
            threading.Thread(target=self._run_cleaning, daemon=True).start()
            print("[DEBUG] Thread started successfully")
        except Exception as ex:
            print(f"[ERROR] Failed to start cleaning: {ex}")
            import traceback
            traceback.print_exc()
    
    def _show_cleaning_page(self):
        """Affiche la page de nettoyage"""
        # Progress ring
        self.progress_ring = ft.ProgressRing(
            width=50,
            height=50,
            stroke_width=3,
            color=Colors.ACCENT_PRIMARY,
        )
        
        # Titre et statut
        self.cleaning_title = Heading("Nettoyage en cours...", level=4, text_align=ft.TextAlign.CENTER)
        self.cleaning_status = Caption("Préparation du nettoyage...", text_align=ft.TextAlign.CENTER, color=Colors.FG_SECONDARY)
        
        # Barre de progression avec animation fluide
        self.dialog_progress = ft.ProgressBar(
            width=350,
            height=3,
            color=Colors.ACCENT_PRIMARY,
            bgcolor=Colors.BORDER_DEFAULT,
            value=0,
            bar_height=3,
            border_radius=2,
        )
        
        # Pourcentage
        self.percentage_text = Caption("0%", color=Colors.ACCENT_PRIMARY, size=11)
        
        # Créer les éléments de la liste des tâches
        self.task_items = {}
        self.task_list = ft.Column(
            spacing=Spacing.XS,
            scroll=ft.ScrollMode.AUTO,
            height=200,
        )
        
        # Ajouter les tâches
        tasks = [
            ("analyze", "Analyse du système"),
            ("temp", "Nettoyage des fichiers temporaires"),
            ("prefetch", "Nettoyage du cache temporaire"),
            ("ram", "Libération de la RAM Standby"),
            ("dns", "Vidage du cache DNS"),
            ("recycle", "Nettoyage de la corbeille"),
            ("telemetry", "Désactivation de la télémétrie"),
            ("logs", "Nettoyage des logs système"),
            ("finalize", "Finalisation"),
        ]
        
        for task_id, task_title in tasks:
            task_item = self._create_task_item(task_title, "pending")
            self.task_items[task_id] = task_item
            self.task_list.controls.append(task_item)
        
        # Countdown text (caché au début)
        self.countdown_text = Caption(
            "",
            text_align=ft.TextAlign.CENTER,
            color=Colors.FG_SECONDARY,
            size=12,
        )
        self.countdown_text.visible = False
        
        # Container principal de la page de nettoyage
        self.cleaning_container = ft.Container(
            content=ft.Column(
                [
                    ft.Container(expand=True),
                    self.progress_ring,
                    Spacer(height=Spacing.MD),
                    self.cleaning_title,
                    Spacer(height=Spacing.XS),
                    self.cleaning_status,
                    Spacer(height=Spacing.XL),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        Caption("Tâches en cours", color=Colors.FG_PRIMARY, size=12),
                                        ft.Container(expand=True),
                                        self.percentage_text,
                                    ],
                                ),
                                Spacer(height=Spacing.SM),
                                self.dialog_progress,
                                Spacer(height=Spacing.MD),
                                self.task_list,
                            ],
                        ),
                        bgcolor=Colors.BG_SECONDARY,
                        padding=Spacing.MD,
                        border_radius=BorderRadius.MD,
                        border=ft.border.all(1, Colors.BORDER_DEFAULT),
                        width=450,
                    ),
                    Spacer(height=Spacing.LG),
                    Caption(
                        "L'optimisation de votre système peut prendre quelques instants. Merci de patienter.",
                        text_align=ft.TextAlign.CENTER,
                        color=Colors.FG_SECONDARY,
                        size=11,
                    ),
                    Spacer(height=Spacing.MD),
                    self.countdown_text,
                    ft.Container(expand=True),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            bgcolor=Colors.BG_PRIMARY,
            padding=Spacing.XXL,
            expand=True,
            opacity=0,
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )
        
        # Remplacer le contenu de la page
        print("[DEBUG] Replacing page content...")
        self.page.controls.clear()
        self.page.add(self.cleaning_container)
        self.page.update()
        
        # Animation d'entrée
        import time
        time.sleep(0.1)
        self.cleaning_container.opacity = 1
        self.page.update()
        print("[DEBUG] Page content replaced with fade in")
    
    def _create_task_item(self, title, status="pending"):
        """Crée un élément de tâche"""
        # Icône selon le statut
        if status == "pending":
            icon = ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, size=14, color=Colors.FG_SECONDARY)
        elif status == "in_progress":
            icon = ft.ProgressRing(width=14, height=14, stroke_width=2, color=Colors.ACCENT_PRIMARY)
        elif status == "completed":
            icon = ft.Icon(ft.Icons.CHECK_CIRCLE, size=14, color=Colors.SUCCESS)
        else:
            icon = ft.Icon(ft.Icons.ERROR, size=14, color=Colors.ERROR)
        
        return ft.Container(
            content=ft.Row(
                [
                    icon,
                    ft.Container(width=Spacing.SM),
                    Caption(
                        title, 
                        color=Colors.FG_PRIMARY if status == "in_progress" else Colors.FG_SECONDARY,
                        size=11
                    ),
                ],
            ),
            padding=ft.padding.symmetric(vertical=4),
        )
    
    def _update_task_status(self, task_key, status, title=None):
        """Met à jour le statut d'une tâche"""
        if task_key in self.task_items:
            # Récupérer le titre actuel si non fourni
            if title is None:
                try:
                    title = self.task_items[task_key].content.controls[2].value
                except:
                    title = "Tâche"
            
            # Trouver l'index de la tâche dans la liste
            task_index = list(self.task_items.keys()).index(task_key)
            
            # Créer le nouvel élément
            new_task_item = self._create_task_item(title, status)
            
            # Remplacer dans le dictionnaire et la liste
            self.task_items[task_key] = new_task_item
            self.task_list.controls[task_index] = new_task_item
            
            self.page.update()
    
    def _run_cleaning(self):
        """Exécute le nettoyage dans un thread séparé"""
        import time
        
        print("[DEBUG] _run_cleaning started in thread")
        
        # SÉCURITÉ: Vérifier l'intégrité du système avant de commencer
        print("[SECURITY] Verifying system integrity...")
        if not security_manager.verify_system_integrity():
            print("[SECURITY] System integrity check failed")
            self.cleaning_status.value = "Vérification de sécurité échouée"
            self.progress_ring.visible = False
            self.page.update()
            time.sleep(3)
            self._return_to_main_page()
            return
        
        if not security_manager.is_safe_to_proceed():
            print("[SECURITY] Not safe to proceed with cleaning")
            self.cleaning_status.value = "Nettoyage annulé pour des raisons de sécurité"
            self.progress_ring.visible = False
            self.page.update()
            time.sleep(3)
            self._return_to_main_page()
            return
        
        print("[SECURITY] System integrity verified - Safe to proceed")
        
        # Initialiser le logger
        logger = CleaningLogger()
        
        try:
            total_tasks = 9
            current_task = 0
            
            # Petite pause pour s'assurer que le dialog est affiché
            time.sleep(0.3)
            
            # Analyse
            current_task += 1
            print(f"[DEBUG] Task {current_task}/{total_tasks}: Analyze")
            self._update_task_status("analyze", "in_progress")
            self._update_cleaning_progress("Analyse du système...", current_task / total_tasks)
            time.sleep(0.3)
            self._update_task_status("analyze", "completed")
            
            # Fichiers temporaires
            current_task += 1
            self._update_task_status("temp", "in_progress")
            self._update_cleaning_progress("Nettoyage des fichiers temporaires...", current_task / total_tasks)
            
            op_index = logger.log_operation_start("Nettoyage fichiers temporaires", "Suppression des fichiers temporaires système et utilisateur")
            logger.current_op = op_index
            result_temp = cleaner.clean_temp_files(logger=logger)
            logger.log_operation_end(op_index, result_temp.get('files_deleted', 0), result_temp.get('space_freed', 0), True)
            
            time.sleep(0.3)
            self._update_task_status("temp", "completed")
            
            # Prefetch
            current_task += 1
            self._update_task_status("prefetch", "in_progress")
            self._update_cleaning_progress("Nettoyage du cache temporaire...", current_task / total_tasks)
            time.sleep(0.3)
            self._update_task_status("prefetch", "completed")
            
            # RAM Standby
            if self.app.advanced_options.get("clear_standby_memory", True):
                current_task += 1
                self._update_task_status("ram", "in_progress")
                self._update_cleaning_progress("Libération de la RAM Standby...", current_task / total_tasks)
                cleaner.clear_standby_memory()
                time.sleep(0.3)
                self._update_task_status("ram", "completed")
            else:
                self._update_task_status("ram", "completed")
                current_task += 1
            
            # Cache DNS
            if self.app.advanced_options.get("flush_dns", True):
                current_task += 1
                self._update_task_status("dns", "in_progress")
                self._update_cleaning_progress("Vidage du cache DNS...", current_task / total_tasks)
                cleaner.flush_dns()
                time.sleep(0.3)
                self._update_task_status("dns", "completed")
            else:
                self._update_task_status("dns", "completed")
                current_task += 1
            
            # Corbeille
            current_task += 1
            self._update_task_status("recycle", "in_progress")
            self._update_cleaning_progress("Nettoyage de la corbeille...", current_task / total_tasks)
            time.sleep(0.3)
            self._update_task_status("recycle", "completed")
            
            # Télémétrie
            if self.app.advanced_options.get("disable_telemetry", False):
                current_task += 1
                self._update_task_status("telemetry", "in_progress")
                self._update_cleaning_progress("Désactivation de la télémétrie...", current_task / total_tasks)
                cleaner.disable_telemetry()
                time.sleep(0.3)
                self._update_task_status("telemetry", "completed")
            else:
                self._update_task_status("telemetry", "completed")
                current_task += 1
            
            # Logs
            if self.app.advanced_options.get("clear_large_logs", True):
                current_task += 1
                self._update_task_status("logs", "in_progress")
                self._update_cleaning_progress("Nettoyage des logs système...", current_task / total_tasks)
                cleaner.clear_large_logs()
                time.sleep(0.3)
                self._update_task_status("logs", "completed")
            else:
                self._update_task_status("logs", "completed")
                current_task += 1
            
            # Finalisation
            current_task += 1
            self._update_task_status("finalize", "in_progress")
            self._update_cleaning_progress("Finalisation...", current_task / total_tasks)
            time.sleep(0.3)
            self._update_task_status("finalize", "completed")
            
            # Finaliser les logs
            log_info = logger.finalize()
            
            # Terminé
            self._update_cleaning_progress("Nettoyage terminé avec succès !", 1.0)
            self.cleaning_title.value = "Nettoyage terminé !"
            self.progress_ring.visible = False
            self.page.update()
            
            # Afficher le résumé rapide
            total_files = logger.session_data["summary"]["total_files_deleted"]
            total_space = logger.session_data["summary"]["total_space_freed_mb"]
            self.cleaning_status.value = f"Espace libéré: {total_space:.2f} MB • Fichiers supprimés: {total_files:,}"
            self.page.update()
            
            # Stocker les infos de log pour affichage
            self.last_log_info = log_info
            
            # Décompte de 6 secondes
            self.countdown_text.visible = True
            for i in range(6, 0, -1):
                self.countdown_text.value = f"Retour à la page principale dans {i} seconde{'s' if i > 1 else ''}..."
                self.page.update()
                time.sleep(1)
            
            # Retour à la page principale
            self._return_to_main_page()
            
        except Exception as ex:
            print(f"[ERROR] Cleaning failed: {ex}")
            self._update_cleaning_progress(f"Erreur: {str(ex)}", 0)
            self.cleaning_title.value = "Erreur"
            self.cleaning_status.value = "Une erreur est survenue lors du nettoyage"
            self.progress_ring.visible = False
            self.page.update()
            
            # Attendre 3 secondes puis retourner
            time.sleep(3)
            self._return_to_main_page()
        
        finally:
            self.cleaning_in_progress = False
    
    def _return_to_main_page(self):
        """Retourne à la page principale avec animation"""
        import time
        
        print("[DEBUG] Fading out cleaning page...")
        self.cleaning_container.opacity = 0
        self.page.update()
        time.sleep(0.3)
        
        print("[DEBUG] Returning to main page...")
        self.page.controls.clear()
        new_main = self.build()
        new_main.opacity = 0
        self.page.add(new_main)
        self.page.update()
        
        # Animation d'entrée
        time.sleep(0.1)
        new_main.opacity = 1
        self.page.update()
        print("[DEBUG] Main page restored with fade in")
    
    def _update_cleaning_progress(self, message, value):
        """Met à jour la progression avec animation fluide"""
        import time
        
        # Mettre à jour le message
        self.cleaning_status.value = message
        
        # Animation fluide de la barre de progression
        current_value = self.dialog_progress.value or 0
        steps = 20  # Nombre d'étapes pour l'animation
        increment = (value - current_value) / steps
        
        for i in range(steps):
            self.dialog_progress.value = current_value + (increment * (i + 1))
            percentage = int(self.dialog_progress.value * 100)
            self.percentage_text.value = f"{percentage}%"
            self.page.update()
            time.sleep(0.01)  # 10ms entre chaque étape = 200ms total
        
        # S'assurer que la valeur finale est exacte
        self.dialog_progress.value = value
        percentage = int(value * 100)
        self.percentage_text.value = f"{percentage}%"
        self.page.update()
    
    def _update_progress(self, message, value):
        """Met à jour la barre de progression"""
        self.status_text.value = message
        self.progress_bar.value = value
        self.page.update()
    
    def _show_summary(self, result):
        """Affiche le résumé du nettoyage"""
        def close_dlg(e):
            dlg.open = False
            self.page.update()
        
        dlg = ft.AlertDialog(
            title=ft.Row(
                [
                    SuccessIcon(size=28),
                    ft.Container(width=Spacing.SM),
                    Heading("Nettoyage terminé", level=4),
                ],
            ),
            content=ft.Column(
                [
                    BodyText(f"Espace libéré: {result.get('space_freed', 0)} MB"),
                    BodyText(f"Fichiers supprimés: {result.get('files_deleted', 0)}"),
                ],
                tight=True,
            ),
            actions=[
                PrimaryButton("OK", on_click=close_dlg, width=100),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
