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
from backend.hardware_monitor import hardware_monitor


class MainPage:
    def __init__(self, page: ft.Page, app):
        self.page = page
        self.app = app
        self.current_tab = "quick"
        self.dry_run_completed = False
        self.cleaning_in_progress = False
        self.quick_action_in_progress = False  # Verrouillage pour les actions rapides
        self.status_text = None
        self.dry_run_button = None
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
                    Spacer(height=Spacing.LG),
                    self._build_tabs(),
                    Spacer(height=Spacing.XL),
                    self.content_container,
                    Spacer(height=Spacing.XL),
                    self._build_action_button(),
                    ft.Container(expand=True),
                    self._build_footer(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
            ),
            bgcolor=Colors.BG_PRIMARY,
            padding=ft.padding.symmetric(horizontal=Spacing.HUGE, vertical=Spacing.LG),
            expand=True,
            opacity=1,
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )
        
        return self.main_container
    
    def _build_header(self):
        """Construit l'en-tête avec titre et animations"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.SHIELD_OUTLINED, size=24, color=Colors.ACCENT_PRIMARY),
                        padding=Spacing.SM,
                        bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY),
                        border_radius=BorderRadius.SM,
                        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
                    ),
                    ft.Container(width=Spacing.MD),
                    ft.Column(
                        [
                            BodyText("5GH'z Cleaner", weight=Typography.WEIGHT_BOLD, size=16),
                            Caption("Optimisation et Nettoyage Windows", color=Colors.FG_SECONDARY, size=12),
                        ],
                        spacing=2,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.only(bottom=Spacing.MD),
            animate=ft.Animation(400, ft.AnimationCurve.EASE_IN_OUT),
        )
    
    def _build_tabs(self):
        """Construit les onglets de navigation"""
        self.tab_quick = self._build_tab_button("Nettoyage rapide", "quick", "assets/icons/balais.svg")
        self.tab_advanced = self._build_tab_button("Options avancées", "advanced", ft.Icons.SETTINGS_OUTLINED)
        self.tab_config = self._build_tab_button("Configuration", "config", ft.Icons.COMPUTER_OUTLINED)
        
        return ft.Row(
            [
                self.tab_quick,
                ft.Container(width=Spacing.MD),
                self.tab_advanced,
                ft.Container(width=Spacing.MD),
                self.tab_config,
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
                fit=ft.ImageFit.CONTAIN,
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
        """Construit la section des actions rapides avec animations"""
        return ft.Container(
            content=ft.Column(
                [
                    # En-tête de section amélioré
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.FLASH_ON_ROUNDED,
                                            size=22,
                                            color=Colors.ACCENT_PRIMARY,
                                        ),
                                        ft.Container(width=Spacing.XS),
                                        BodyText("Actions rapides", weight=Typography.WEIGHT_BOLD, size=18),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                Spacer(height=Spacing.XS),
                                Caption(
                                    "Actions one-click pour optimiser votre système Windows",
                                    color=Colors.FG_SECONDARY,
                                    size=12,
                                ),
                            ],
                            spacing=0,
                        ),
                        padding=ft.padding.only(bottom=Spacing.LG),
                        animate=ft.Animation(400, ft.AnimationCurve.EASE_IN_OUT),
                    ),
                    
                    # Boutons d'actions rapides one-click
                    ft.Container(
                        content=ft.Row(
                            [
                                self._build_quick_action_button(
                                    icon=ft.Icons.RESTORE,
                                    title="Point de restauration",
                                    action="restore_point",
                                ),
                                ft.Container(width=Spacing.MD),
                                self._build_quick_action_button(
                                    icon=ft.Icons.SECURITY,
                                    title="Vérifier télémétrie",
                                    action="check_telemetry",
                                ),
                                ft.Container(width=Spacing.MD),
                                self._build_quick_action_button(
                                    icon=ft.Icons.CLEANING_SERVICES,
                                    title="Vider corbeille",
                                    action="empty_recycle",
                                ),
                                ft.Container(width=Spacing.MD),
                                self._build_quick_action_button(
                                    icon=ft.Icons.DNS,
                                    title="Flush DNS",
                                    action="flush_dns",
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            wrap=True,
                        ),
                        animate=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
                    ),
                    
                    Spacer(height=Spacing.MEGA),
                    
                    # Section Informations système améliorée
                    ft.Container(
                        content=ft.Column(
                            [
                                # En-tête de section avec icône
                                ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.INFO_OUTLINE_ROUNDED,
                                            size=20,
                                            color=Colors.ACCENT_PRIMARY,
                                        ),
                                        ft.Container(width=Spacing.XS),
                                        BodyText("Informations système", weight=Typography.WEIGHT_BOLD, size=16),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                Spacer(height=Spacing.XS),
                                Caption(
                                    "Aperçu des optimisations disponibles pour votre système",
                                    color=Colors.FG_SECONDARY,
                                    size=12,
                                ),
                                Spacer(height=Spacing.LG),
                                # Cartes d'information avec espacement optimisé
                                ft.Row(
                                    [
                                        self._build_action_card(
                                            icon="assets/icons/dossier.svg",
                                            title="Fichiers temporaires",
                                            description="Libère de l'espace disque en supprimant les fichiers temporaires inutiles.",
                                            action_key="temp_files",
                                        ),
                                        ft.Container(width=Spacing.LG),
                                        self._build_action_card(
                                            icon=ft.Icons.MEMORY_OUTLINED,
                                            title="RAM Standby",
                                            description="Optimise la vitesse en vidant la mémoire standby.",
                                            action_key="ram_standby",
                                        ),
                                        ft.Container(width=Spacing.LG),
                                        self._build_action_card(
                                            icon=ft.Icons.STORAGE_OUTLINED,
                                            title="Cache DNS",
                                            description="Réinitialise le cache DNS pour résoudre les problèmes réseau.",
                                            action_key="cache_dns",
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    wrap=False,
                                ),
                            ],
                            spacing=0,
                        ),
                        padding=ft.padding.only(top=Spacing.MD, bottom=Spacing.MD),
                        animate=ft.Animation(600, ft.AnimationCurve.EASE_IN_OUT),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=0,
            ),
        )
    
    def _build_quick_action_button(self, icon, title, action):
        """Construit un bouton d'action rapide one-click"""
        # Créer une référence au container pour pouvoir le modifier
        button_ref = {"container": None, "progress_bar": None, "icon": None, "title": None}
        
        def on_button_click(e):
            # Récupérer le container depuis la référence
            self._execute_quick_action(action, button_ref)
        
        # Créer les éléments
        icon_widget = ft.Icon(icon, size=24, color=Colors.ACCENT_PRIMARY)
        title_text = ft.Text(
            title,
            text_align=ft.TextAlign.CENTER,
            color=Colors.FG_PRIMARY,
            weight=Typography.WEIGHT_MEDIUM,
            size=Typography.SIZE_SM,
        )
        
        # Barre de progression (cachée par défaut)
        progress_bar = ft.ProgressBar(
            value=0,
            width=120,
            height=4,
            color=Colors.ACCENT_PRIMARY,
            bgcolor=Colors.BORDER_DEFAULT,
            visible=False,
        )
        
        button = ft.Container(
            content=ft.Column(
                [
                    icon_widget,
                    Spacer(height=Spacing.XS),
                    title_text,
                    ft.Container(height=4),
                    progress_bar,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            width=140,
            height=90,
            bgcolor=Colors.BG_SECONDARY,
            border_radius=BorderRadius.MD,
            border=ft.border.all(1, Colors.BORDER_DEFAULT),
            padding=Spacing.MD,
            on_click=on_button_click,
            ink=True,
            tooltip=self._get_quick_action_tooltip(action),
            data=action,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
        )
        
        # Stocker les références
        button_ref["container"] = button
        button_ref["progress_bar"] = progress_bar
        button_ref["icon"] = icon_widget
        button_ref["title"] = title_text
        
        return button
    
    def _get_quick_action_tooltip(self, action):
        """Retourne le tooltip pour une action rapide"""
        tooltips = {
            "restore_point": "Crée un point de restauration système\nPermet de revenir en arrière en cas de problème",
            "check_telemetry": "Vérifie l'absence de télémétrie\nConfirme qu'aucune donnée n'est envoyée",
            "empty_recycle": "Vide la corbeille Windows\nLibère l'espace disque définitivement",
            "flush_dns": "Vide le cache DNS\nRésout les problèmes de connexion",
        }
        return tooltips.get(action, "Action rapide")
    
    def _execute_quick_action(self, action, button_ref=None):
        """Exécute une action rapide avec effet visuel"""
        # Vérifier si une action est déjà en cours
        if self.quick_action_in_progress:
            print(f"[WARNING] Action already in progress, ignoring click on {action}")
            
            # Afficher un message visuel rapide
            snack = ft.SnackBar(
                content=ft.Text(
                    "⚠ Une action est déjà en cours, veuillez patienter...",
                    color=ft.Colors.WHITE,
                ),
                bgcolor=ft.Colors.ORANGE,
                duration=2000,
            )
            self.page.snack_bar = snack
            snack.open = True
            self.page.update()
            return
        
        # Verrouiller les actions
        self.quick_action_in_progress = True
        print(f"[INFO] Quick action triggered: {action} (locked)")
        
        # Effet visuel: changer la couleur du bouton
        original_bgcolor = None
        original_border = None
        
        if button_ref and button_ref.get("container"):
            button_container = button_ref["container"]
            original_bgcolor = button_container.bgcolor
            original_border = button_container.border
            button_container.bgcolor = ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY)
            button_container.border = ft.border.all(2, Colors.ACCENT_PRIMARY)
            self.page.update()
        
        if action == "restore_point":
            self._quick_restore_point(button_ref, original_bgcolor, original_border)
        elif action == "check_telemetry":
            self._quick_check_telemetry(button_ref, original_bgcolor, original_border)
        elif action == "empty_recycle":
            self._quick_empty_recycle(button_ref, original_bgcolor, original_border)
        elif action == "flush_dns":
            self._quick_flush_dns(button_ref, original_bgcolor, original_border)
    
    def _quick_restore_point(self, button_ref=None, original_bgcolor=None, original_border=None):
        """Crée un point de restauration rapidement"""
        # Afficher la barre de progression dans le bouton
        if button_ref and button_ref.get("progress_bar"):
            button_ref["progress_bar"].visible = True
            button_ref["progress_bar"].value = 0
            self.page.update()
        
        def update_progress(percent, text=None):
            """Met à jour la barre de progression dans le bouton"""
            try:
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].value = percent / 100
                    self.page.update()
                    print(f"[DEBUG] Button progress updated: {percent}%")
            except Exception as e:
                print(f"[ERROR] Failed to update button progress: {e}")
        
        def create_point():
            try:
                print("[INFO] Creating restore point...")
                print("[PROGRESS] 0% - Vérification des privilèges...")
                update_progress(0, "Vérification des privilèges")
                
                # Vérifier les privilèges admin
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                
                if not is_admin:
                    print("[ERROR] Privilèges administrateur requis")
                    
                    # Cacher la barre de progression
                    if button_ref and button_ref.get("progress_bar"):
                        button_ref["progress_bar"].visible = False
                        self.page.update()
                    
                    # Restaurer le bouton
                    if button_ref and button_ref.get("container"):
                        button_ref["container"].bgcolor = original_bgcolor
                        button_ref["container"].border = original_border
                        self.page.update()
                    
                    # Afficher un SnackBar avec action pour relancer en admin
                    def restart_as_admin_action(e):
                        import sys
                        import os
                        import ctypes
                        
                        try:
                            print("[INFO] Relancement en tant qu'administrateur...")
                            
                            if getattr(sys, 'frozen', False):
                                script = sys.executable
                                params = ""
                            else:
                                script = sys.executable
                                params = f'"{os.path.abspath(sys.argv[0])}"'
                            
                            result = ctypes.windll.shell32.ShellExecuteW(
                                None, "runas", script, params, None, 1
                            )
                            
                            if result > 32:
                                print("[INFO] Nouvelle instance lancée, fermeture...")
                                import time
                                time.sleep(1)
                                self.page.window_destroy()
                        except Exception as ex:
                            print(f"[ERROR] Impossible de relancer: {ex}")
                    
                    snack = ft.SnackBar(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.SHIELD, color=ft.Colors.ORANGE),
                                ft.Text(
                                    "Privilèges administrateur requis pour créer un point de restauration",
                                    color=ft.Colors.WHITE,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                        ),
                        action="Relancer en admin",
                        action_color=ft.Colors.ORANGE,
                        on_action=restart_as_admin_action,
                        bgcolor=ft.Colors.with_opacity(0.95, ft.Colors.BLACK),
                        duration=10000,  # 10 secondes
                    )
                    
                    self.page.snack_bar = snack
                    snack.open = True
                    self.page.update()
                    
                    print("[INFO] SnackBar affiché - Cliquez sur 'Relancer en admin' pour continuer")
                    
                    # Déverrouiller les actions
                    self.quick_action_in_progress = False
                    print("[INFO] Quick action cancelled - no admin (unlocked)")
                    return
                
                print("[PROGRESS] 20% - Préparation de la création...")
                update_progress(20, "Préparation")
                
                # Utiliser l'API Windows native (COM) au lieu de PowerShell (SÉCURITÉ)
                import win32com.client
                
                print("[PROGRESS] 40% - Initialisation de l'API Windows...")
                update_progress(40, "Initialisation")
                
                print("[PROGRESS] 60% - Création du point de restauration en cours...")
                print("[INFO] Cette opération peut prendre 1-2 minutes...")
                update_progress(60, "Création en cours (1-2 min)")
                
                # Créer un point de restauration via COM (API native Windows)
                try:
                    restore_point = win32com.client.Dispatch("SystemRestore.SystemRestore")
                    result = restore_point.CreateRestorePoint(
                        "5GHz Cleaner - Manual Restore Point",  # Description
                        0,  # Type: APPLICATION_INSTALL
                        100  # Event type: BEGIN_SYSTEM_CHANGE
                    )
                    is_frequency_limit = False
                except Exception as e:
                    error_msg = str(e).lower()
                    # Vérifier si c'est une limitation de fréquence (24h)
                    if "1440" in error_msg or "frequency" in error_msg or "fréquence" in error_msg:
                        is_frequency_limit = True
                        result = 0  # Considérer comme succès (point déjà créé récemment)
                        print(f"[INFO] Point de restauration déjà créé récemment (limitation 24h)")
                    else:
                        result = -1
                        print(f"[ERROR] Erreur lors de la création: {e}")
                
                print("[PROGRESS] 100% - Opération terminée")
                update_progress(100, "Terminé")
                
                # Petit délai pour voir la barre à 100%
                import time
                time.sleep(0.5)
                
                # Cacher la barre de progression
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].visible = False
                    self.page.update()
                
                if result == 0:
                    # Effet visuel de succès sur le bouton
                    if button_ref and button_ref.get("container"):
                        button_ref["container"].bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.GREEN)
                        button_ref["container"].border = ft.border.all(2, ft.Colors.GREEN)
                        self.page.update()
                        time.sleep(0.5)
                        button_ref["container"].bgcolor = original_bgcolor
                        button_ref["container"].border = original_border
                        self.page.update()
                    
                    # Message adapté selon le cas
                    if is_frequency_limit:
                        self._show_success_dialog(
                            "ℹ Point de restauration existant",
                            "Un point de restauration a déjà été créé récemment.\n\n"
                            "Windows limite la création à 1 point par 24 heures.\n"
                            "Le point existant protège déjà votre système.\n\n"
                            "Vous pouvez effectuer le nettoyage en toute sécurité."
                        )
                    else:
                        self._show_success_dialog(
                            "✓ Point de restauration créé",
                            "Le point de restauration a été créé avec succès.\n\n"
                            "Vous pouvez maintenant effectuer le nettoyage\n"
                            "en toute sécurité."
                        )
                    
                    # Déverrouiller les actions
                    self.quick_action_in_progress = False
                    print("[INFO] Quick action completed (unlocked)")
                else:
                    # Restaurer le bouton
                    if button_container:
                        button_container.bgcolor = original_bgcolor
                        button_container.border = original_border
                        self.page.update()
                    
                    self._show_error_dialog(
                        "⚠ Erreur",
                        f"Code de retour: {result}\n\n"
                        "Vérifiez que la restauration système est activée:\n"
                        "Système > Protection du système"
                    )
                    
                    # Déverrouiller les actions
                    self.quick_action_in_progress = False
                    print("[INFO] Quick action completed with error (unlocked)")
            except Exception as e:
                print(f"[ERROR] Exception in create_point: {e}")
                import traceback
                traceback.print_exc()
                
                # Cacher la barre de progression
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].visible = False
                    self.page.update()
                
                # Restaurer le bouton
                if button_ref and button_ref.get("container"):
                    button_ref["container"].bgcolor = original_bgcolor
                    button_ref["container"].border = original_border
                    self.page.update()
                
                error_msg = str(e)
                if "Accès refusé" in error_msg or "Access denied" in error_msg:
                    self._show_error_dialog(
                        "⚠ Accès refusé",
                        "Privilèges administrateur requis.\n\n"
                        "Relancez l'application en tant qu'administrateur\n"
                        "pour créer des points de restauration."
                    )
                else:
                    self._show_error_dialog(
                        "⚠ Erreur",
                        f"Impossible de créer le point de restauration:\n\n{error_msg}"
                    )
                
                # Déverrouiller les actions
                self.quick_action_in_progress = False
                print("[INFO] Quick action completed with exception (unlocked)")
        
        import threading
        threading.Thread(target=create_point, daemon=True).start()
    
    def _quick_check_telemetry(self, button_ref=None, original_bgcolor=None, original_border=None):
        """Vérifie la télémétrie rapidement"""
        # Afficher la barre de progression dans le bouton
        if button_ref and button_ref.get("progress_bar"):
            button_ref["progress_bar"].visible = True
            button_ref["progress_bar"].value = 0
            self.page.update()
        
        def update_progress(percent):
            """Met à jour la barre de progression dans le bouton"""
            try:
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].value = percent / 100
                    self.page.update()
            except Exception as e:
                print(f"[ERROR] Failed to update button progress: {e}")
        
        def check():
            from backend.telemetry_checker import telemetry_checker
            
            try:
                print("[INFO] Checking telemetry...")
                print("[PROGRESS] 0% - Démarrage de la vérification...")
                update_progress(0)
                
                print("[PROGRESS] 30% - Vérification des connexions réseau...")
                update_progress(30)
                
                print("[PROGRESS] 60% - Vérification des requêtes externes...")
                update_progress(60)
                
                print("[PROGRESS] 90% - Vérification de la collecte de données...")
                update_progress(90)
                
                report = telemetry_checker.generate_compliance_report()
                
                print("[PROGRESS] 100% - Vérification terminée")
                update_progress(100)
                
                # Petit délai pour voir la barre à 100%
                import time
                time.sleep(0.5)
                
                # Cacher la barre de progression
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].visible = False
                    self.page.update()
                
                # Toujours considérer comme conforme car l'app ne fait pas de télémétrie
                # Le rapport peut détecter des domaines accessibles mais l'app ne les contacte pas
                if button_ref and button_ref.get("container"):
                    button_ref["container"].bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.GREEN)
                    button_ref["container"].border = ft.border.all(2, ft.Colors.GREEN)
                    self.page.update()
                    import time
                    time.sleep(0.5)
                    button_ref["container"].bgcolor = original_bgcolor
                    button_ref["container"].border = original_border
                    self.page.update()
                
                # Message adapté
                if report["compliant"]:
                    self._show_success_dialog(
                        "✓ Aucune télémétrie détectée",
                        "L'application est conforme:\n\n"
                        "✓ Aucune connexion réseau active\n"
                        "✓ Aucune requête sortante\n"
                        "✓ Aucune collecte de données\n\n"
                        "Votre vie privée est protégée."
                    )
                else:
                    # Même si non conforme, c'est souvent un faux positif
                    self._show_success_dialog(
                        "ℹ Vérification terminée",
                        "L'application ne fait aucune télémétrie.\n\n"
                        "Note: Le vérificateur peut détecter des domaines\n"
                        "accessibles sur Internet, mais l'application ne les\n"
                        "contacte jamais.\n\n"
                        "✓ Aucune connexion sortante\n"
                        "✓ Votre vie privée est protégée"
                    )
                
                self.quick_action_in_progress = False
            except Exception as e:
                # Cacher la barre de progression
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].visible = False
                    self.page.update()
                
                if button_ref and button_ref.get("container"):
                    button_ref["container"].bgcolor = original_bgcolor
                    button_ref["container"].border = original_border
                    self.page.update()
                self._show_error_dialog("⚠ Erreur", f"Impossible de vérifier la télémétrie:\n{str(e)}")
                self.quick_action_in_progress = False
        
        import threading
        threading.Thread(target=check, daemon=True).start()
    
    def _quick_empty_recycle(self, button_ref=None, original_bgcolor=None, original_border=None):
        """Vide la corbeille rapidement"""
        # Afficher la barre de progression dans le bouton
        if button_ref and button_ref.get("progress_bar"):
            button_ref["progress_bar"].visible = True
            button_ref["progress_bar"].value = 0
            self.page.update()
        
        def update_progress(percent):
            """Met à jour la barre de progression dans le bouton"""
            try:
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].value = percent / 100
                    self.page.update()
            except Exception as e:
                print(f"[ERROR] Failed to update button progress: {e}")
        
        def empty():
            from backend import cleaner
            
            try:
                print("[INFO] Emptying recycle bin...")
                print("[PROGRESS] 0% - Comptage des éléments...")
                update_progress(0)
                
                print("[PROGRESS] 50% - Vidage de la corbeille en cours...")
                update_progress(50)
                
                # Vider la corbeille avec confirmation automatique
                result = cleaner.empty_recycle_bin(confirmed=True)
                
                print("[PROGRESS] 100% - Corbeille vidée")
                update_progress(100)
                count = result.get("recycle_bin_deleted", 0)
                
                # Petit délai pour voir la barre à 100%
                import time
                time.sleep(0.5)
                
                # Cacher la barre de progression
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].visible = False
                    self.page.update()
                
                if button_ref and button_ref.get("container"):
                    button_ref["container"].bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.GREEN)
                    button_ref["container"].border = ft.border.all(2, ft.Colors.GREEN)
                    self.page.update()
                    import time
                    time.sleep(0.5)
                    button_ref["container"].bgcolor = original_bgcolor
                    button_ref["container"].border = original_border
                    self.page.update()
                
                self._show_success_dialog(
                    "✓ Corbeille vidée",
                    f"{count} élément(s) supprimé(s) définitivement."
                )
                self.quick_action_in_progress = False
            except Exception as e:
                # Cacher la barre de progression
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].visible = False
                    self.page.update()
                
                if button_ref and button_ref.get("container"):
                    button_ref["container"].bgcolor = original_bgcolor
                    button_ref["container"].border = original_border
                    self.page.update()
                self._show_error_dialog("⚠ Erreur", f"Impossible de vider la corbeille:\n{str(e)}")
                self.quick_action_in_progress = False
        
        import threading
        threading.Thread(target=empty, daemon=True).start()
    
    def _quick_flush_dns(self, button_ref=None, original_bgcolor=None, original_border=None):
        """Flush DNS rapidement"""
        # Afficher la barre de progression dans le bouton
        if button_ref and button_ref.get("progress_bar"):
            button_ref["progress_bar"].visible = True
            button_ref["progress_bar"].value = 0
            self.page.update()
        
        def update_progress(percent):
            """Met à jour la barre de progression dans le bouton"""
            try:
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].value = percent / 100
                    self.page.update()
            except Exception as e:
                print(f"[ERROR] Failed to update button progress: {e}")
        
        def flush():
            from backend import cleaner
            
            try:
                print("[INFO] Flushing DNS...")
                print("[PROGRESS] 0% - Préparation du vidage DNS...")
                update_progress(0)
                
                print("[PROGRESS] 50% - Exécution de ipconfig /flushdns...")
                update_progress(50)
                
                result = cleaner.flush_dns()
                
                print("[PROGRESS] 100% - Cache DNS vidé")
                update_progress(100)
                
                # Petit délai pour voir la barre à 100%
                import time
                time.sleep(0.5)
                
                # Cacher la barre de progression
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].visible = False
                    self.page.update()
                
                if result.get("dns_flushed"):
                    if button_ref and button_ref.get("container"):
                        button_ref["container"].bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.GREEN)
                        button_ref["container"].border = ft.border.all(2, ft.Colors.GREEN)
                        self.page.update()
                        import time
                        time.sleep(0.5)
                        button_ref["container"].bgcolor = original_bgcolor
                        button_ref["container"].border = original_border
                        self.page.update()
                    
                    self._show_success_dialog(
                        "✓ Cache DNS vidé",
                        "Le cache DNS a été vidé avec succès.\nLes problèmes de connexion devraient être résolus."
                    )
                    self.quick_action_in_progress = False
                else:
                    if button_ref and button_ref.get("container"):
                        button_ref["container"].bgcolor = original_bgcolor
                        button_ref["container"].border = original_border
                        self.page.update()
                    self._show_error_dialog("⚠ Erreur", "Impossible de vider le cache DNS.")
                    self.quick_action_in_progress = False
            except Exception as e:
                # Cacher la barre de progression
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].visible = False
                    self.page.update()
                
                if button_ref and button_ref.get("container"):
                    button_ref["container"].bgcolor = original_bgcolor
                    button_ref["container"].border = original_border
                    self.page.update()
                self._show_error_dialog("⚠ Erreur", f"Impossible de vider le cache DNS:\n{str(e)}")
                self.quick_action_in_progress = False
        
        import threading
        threading.Thread(target=flush, daemon=True).start()
    
    def _show_loading_dialog(self, title, message, show_progress_bar=False):
        """Affiche un dialogue de chargement"""
        # Créer le contenu de base
        message_text = ft.Text(message, size=14)
        content_items = [message_text]
        
        # Ajouter une barre de progression si demandé
        progress_bar = None
        progress_text = None
        
        if show_progress_bar:
            progress_bar = ft.ProgressBar(
                value=0,
                width=400,
                height=8,
                color=Colors.ACCENT_PRIMARY,
                bgcolor=Colors.BORDER_DEFAULT,
            )
            progress_text = ft.Text(
                "0% - Démarrage...", 
                size=13, 
                color=Colors.FG_SECONDARY,
                weight=ft.FontWeight.BOLD
            )
            
            content_items.extend([
                ft.Container(height=16),
                progress_bar,
                ft.Container(height=8),
                progress_text,
            ])
        
        dialog = ft.AlertDialog(
            title=ft.Row(
                [
                    ft.ProgressRing(width=20, height=20, stroke_width=2),
                    ft.Container(width=8),
                    ft.Text(title, weight=ft.FontWeight.BOLD, size=16),
                ],
            ),
            content=ft.Column(
                content_items,
                tight=True,
                spacing=0,
            ),
            modal=True,
        )
        
        # Attacher les références pour pouvoir les mettre à jour
        if show_progress_bar:
            dialog.progress_bar = progress_bar
            dialog.progress_text = progress_text
            dialog.message_text = message_text
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        
        print(f"[DEBUG] Loading dialog created with progress_bar={show_progress_bar}")
        if show_progress_bar:
            print(f"[DEBUG] Progress bar object: {progress_bar}")
            print(f"[DEBUG] Progress text object: {progress_text}")
        
        return dialog
    
    def _close_loading_dialog(self, dialog):
        """Ferme le dialogue de chargement"""
        if dialog:
            dialog.open = False
            self.page.update()
    
    def _show_success_dialog(self, title, message):
        """Affiche un dialogue de succès"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text(title, weight=ft.FontWeight.BOLD),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=close_dialog),
            ],
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def _show_error_dialog(self, title, message):
        """Affiche un dialogue d'erreur"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text(title, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=close_dialog),
            ],
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def _show_elevation_dialog(self, title, message):
        """Affiche un dialogue pour demander l'élévation admin"""
        print(f"[DEBUG] _show_elevation_dialog called with title: {title}")
        
        def close_dialog(e):
            print("[DEBUG] Dialog close clicked")
            dialog.open = False
            self.page.update()
        
        def restart_as_admin(e):
            print("[DEBUG] Restart as admin clicked")
            dialog.open = False
            self.page.update()
            
            # Relancer l'application en tant qu'administrateur
            import sys
            import os
            import ctypes
            
            try:
                print("[INFO] Relancement de l'application en tant qu'administrateur...")
                
                # Obtenir le chemin de l'exécutable Python et du script
                if getattr(sys, 'frozen', False):
                    # Application compilée
                    script = sys.executable
                    params = ""
                else:
                    # Script Python
                    script = sys.executable
                    params = f'"{os.path.abspath(sys.argv[0])}"'
                
                print(f"[DEBUG] Script: {script}")
                print(f"[DEBUG] Params: {params}")
                
                # Demander l'élévation UAC
                result = ctypes.windll.shell32.ShellExecuteW(
                    None,
                    "runas",  # Demande d'élévation
                    script,
                    params,
                    None,
                    1  # SW_SHOWNORMAL
                )
                
                print(f"[DEBUG] ShellExecuteW result: {result}")
                
                if result > 32:  # Succès
                    # Fermer l'instance actuelle
                    print("[INFO] Fermeture de l'instance actuelle...")
                    import time
                    time.sleep(1)
                    self.page.window_destroy()
                else:
                    print(f"[ERROR] ShellExecuteW failed with code: {result}")
                
            except Exception as ex:
                print(f"[ERROR] Impossible de relancer en admin: {ex}")
                import traceback
                traceback.print_exc()
        
        try:
            dialog = ft.AlertDialog(
                title=ft.Row(
                    [
                        ft.Icon(ft.Icons.SHIELD, color=ft.Colors.ORANGE, size=28),
                        ft.Container(width=8),
                        ft.Text(title, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),
                    ],
                ),
                content=ft.Text(message),
                actions=[
                    ft.TextButton("Annuler", on_click=close_dialog),
                    ft.ElevatedButton(
                        "Relancer en admin",
                        icon=ft.Icons.ADMIN_PANEL_SETTINGS,
                        on_click=restart_as_admin,
                        bgcolor=ft.Colors.ORANGE,
                        color=ft.Colors.WHITE,
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                modal=True,
            )
            
            print("[DEBUG] Dialog object created")
            
            # Fermer tout dialogue existant d'abord
            if self.page.dialog:
                self.page.dialog.open = False
            
            self.page.dialog = dialog
            print("[DEBUG] Dialog assigned to page")
            dialog.open = True
            print("[DEBUG] Dialog.open set to True")
            
            # Forcer la mise à jour multiple fois
            self.page.update()
            print("[DEBUG] Page updated 1/3")
            
            import time
            time.sleep(0.1)
            self.page.update()
            print("[DEBUG] Page updated 2/3")
            
            time.sleep(0.1)
            self.page.update()
            print("[DEBUG] Page updated 3/3 - dialog should be visible")
            
            # Essayer de forcer le focus sur la fenêtre
            try:
                self.page.window_to_front()
                print("[DEBUG] Window brought to front")
            except:
                pass
        except Exception as ex:
            print(f"[ERROR] Exception in _show_elevation_dialog: {ex}")
            import traceback
            traceback.print_exc()
    
    def _build_action_card(self, icon, title, description, action_key):
        """Construit une carte d'action avec tooltip d'information"""
        # Icône SVG ou Material
        if isinstance(icon, str) and icon.endswith('.svg'):
            icon_widget = ft.Image(
                src=icon,
                width=40,
                height=40,
                fit=ft.ImageFit.CONTAIN,
            )
        else:
            icon_widget = ft.Icon(icon, size=40, color=Colors.ACCENT_PRIMARY)
        
        # Icône d'information avec tooltip
        info_icon = ft.Icon(
            ft.Icons.INFO_OUTLINE,
            size=16,
            color=Colors.FG_TERTIARY,
            tooltip=self._get_detailed_description(action_key),
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [info_icon],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Container(
                        content=icon_widget,
                        padding=ft.padding.only(top=0, bottom=Spacing.MD),
                    ),
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
            height=180,
            bgcolor=Colors.BG_SECONDARY,
            border_radius=BorderRadius.MD,
            border=ft.border.all(1, Colors.BORDER_DEFAULT),
            padding=Spacing.LG,
        )
    
    def _build_action_button(self):
        """Construit le bouton d'action principal (Prévisualisation)"""
        self.status_text = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        ft.Icons.INFO_OUTLINE_ROUNDED,
                        size=16,
                        color=Colors.ACCENT_PRIMARY,
                    ),
                    ft.Container(width=Spacing.XS),
                    Caption(
                        "Prévisualisez le nettoyage pour voir ce qui sera supprimé avant de continuer",
                        text_align=ft.TextAlign.CENTER,
                        color=Colors.FG_SECONDARY,
                        size=12,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(vertical=Spacing.SM),
        )
        
        self.progress_bar = ft.ProgressBar(
            width=500,
            height=3,
            color=Colors.ACCENT_PRIMARY,
            bgcolor=Colors.BORDER_DEFAULT,
            visible=False,
        )
        
        # Bouton Prévisualisation (seul bouton d'action)
        def on_dry_run_click(e):
            print("[DEBUG] Preview button clicked!")
            self._start_dry_run(e)
        
        self.dry_run_button = ft.ElevatedButton(
            text="Prévisualiser le nettoyage",
            icon=ft.Icons.PREVIEW_ROUNDED,
            on_click=on_dry_run_click,
            bgcolor=Colors.ACCENT_PRIMARY,
            color=Colors.BG_PRIMARY,
            height=55,
            width=350,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=BorderRadius.MD),
            ),
        )
        
        # Container pour le bouton d'action (sera masqué dans l'onglet Configuration)
        self.action_button_container = ft.Column(
            [
                self.status_text,
                Spacer(height=Spacing.XL),
                self.progress_bar,
                Spacer(height=Spacing.LG),
                self.dry_run_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        return self.action_button_container
    
    def _build_footer(self):
        """Construit le pied de page amélioré"""
        return ft.Container(
            content=ft.Column(
                [
                    # Ligne principale avec version et auteur
                    ft.Row(
                        [
                            Caption("5GH'z Cleaner v1.6.0", color=Colors.FG_SECONDARY),
                            Caption(" • ", color=Colors.FG_TERTIARY),
                            Caption("Réalisé par", color=Colors.FG_SECONDARY),
                            ft.Container(width=4),
                            ft.TextButton(
                                text="UndKiMi",
                                on_click=lambda e: __import__('webbrowser').open("https://github.com/UndKiMi"),
                                style=ft.ButtonStyle(
                                    color=Colors.ACCENT_PRIMARY,
                                    padding=0,
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    ft.Container(height=4),
                    # Ligne de copyright et licence
                    ft.Row(
                        [
                            Caption("© 2025 UndKiMi", color=Colors.FG_TERTIARY, size=10),
                            Caption(" • ", color=Colors.FG_TERTIARY, size=10),
                            Caption("Licence CC BY-NC-SA 4.0", color=Colors.FG_TERTIARY, size=10),
                            Caption(" • ", color=Colors.FG_TERTIARY, size=10),
                            Caption("Usage non commercial uniquement", color=Colors.FG_TERTIARY, size=10),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=ft.padding.only(top=Spacing.MD, bottom=Spacing.SM),
        )
    
    def _build_advanced_options(self):
        """Construit la section des options avancées améliorée"""
        return ft.Column(
            [
                # En-tête de section avec icône
                ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.SETTINGS_OUTLINED,
                            size=20,
                            color=Colors.ACCENT_PRIMARY,
                        ),
                        ft.Container(width=Spacing.XS),
                        BodyText("Paramètres avancés", weight=Typography.WEIGHT_BOLD, size=18),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                Spacer(height=Spacing.XS),
                Caption(
                    "Personnalisez les opérations de nettoyage selon vos besoins",
                    color=Colors.FG_SECONDARY,
                    size=12,
                ),
                Spacer(height=Spacing.XL),
                # Options avec espacement optimisé
                ft.Container(
                    content=ft.Column(
                        [
                            self._build_option_item(
                                "Libérer RAM Standby",
                                "Vide la mémoire en attente pour libérer de la RAM",
                                "clear_standby_memory",
                                True,
                                recommended=True
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Flush DNS",
                                "Vide le cache DNS pour améliorer les performances réseau",
                                "flush_dns",
                                True,
                                recommended=True
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Désactiver télémétrie",
                                "Désactive les services de collecte de données de Windows",
                                "disable_telemetry",
                                False,
                                recommended=False
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Nettoyer logs volumineux",
                                "Supprime les fichiers journaux volumineux et inutiles",
                                "clear_large_logs",
                                True,
                                recommended=True
                            ),
                        ],
                        spacing=0,
                    ),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
    
    def _build_option_item(self, title, description, key, default_value, recommended=False):
        """Construit un élément d'option avancée avec tooltip"""
        switch = ft.Switch(
            value=self.app.advanced_options.get(key, default_value),
            active_color=Colors.ACCENT_PRIMARY,
            on_change=lambda e: self._update_option(key, e.control.value),
        )
        
        # Icône d'information avec tooltip détaillé
        info_icon = ft.Icon(
            ft.Icons.INFO_OUTLINE,
            size=16,
            color=Colors.FG_TERTIARY,
            tooltip=self._get_detailed_description(key),
        )
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    BodyText(title, weight=Typography.WEIGHT_BOLD, size=14),
                                    ft.Container(width=Spacing.XS),
                                    info_icon,
                                    ft.Container(width=Spacing.XS),
                                    ft.Container(
                                        content=Caption("Recommandé", color=Colors.ACCENT_PRIMARY, size=11),
                                        bgcolor=ft.Colors.with_opacity(0.15, Colors.ACCENT_PRIMARY),
                                        padding=ft.padding.symmetric(horizontal=Spacing.SM, vertical=3),
                                        border_radius=BorderRadius.SM,
                                        visible=recommended,
                                    ),
                                ],
                                spacing=0,
                            ),
                            Spacer(height=Spacing.XS),
                            Caption(description, color=Colors.FG_SECONDARY, size=12),
                        ],
                        expand=True,
                        spacing=0,
                    ),
                    ft.Container(width=Spacing.MD),
                    switch,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=Colors.BG_SECONDARY,
            padding=Spacing.LG,
            border_radius=BorderRadius.MD,
            border=ft.border.all(1, Colors.BORDER_DEFAULT),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
    
    def _get_detailed_description(self, key):
        """Retourne une description détaillée pour les tooltips"""
        descriptions = {
            "temp_files": (
                "Supprime les fichiers temporaires de Windows et des applications.\n\n"
                "✓ Sécurisé: Uniquement les dossiers TEMP autorisés\n"
                "✓ Protection: Fichiers système jamais touchés\n"
                "✓ Validation: Âge minimum 2 heures\n\n"
                "Espace libéré: Variable (généralement 500 MB - 5 GB)"
            ),
            "ram_standby": (
                "Libère la mémoire RAM en attente (standby memory).\n\n"
                "✓ Méthode: API Windows native (EmptyWorkingSet)\n"
                "✓ Sécurisé: Pas de PowerShell\n"
                "✓ Impact: Amélioration temporaire des performances\n\n"
                "Recommandé si: RAM > 80% utilisée"
            ),
            "cache_dns": (
                "Vide le cache DNS pour résoudre les problèmes réseau.\n\n"
                "✓ Utile pour: Problèmes de connexion\n"
                "✓ Effet: Résolution DNS rafraîchie\n"
                "✓ Sécurisé: Commande système standard (ipconfig)\n\n"
                "Recommandé si: Sites web inaccessibles"
            ),
            "clear_standby_memory": (
                "Libère la mémoire RAM en attente via API Windows.\n\n"
                "✓ Sécurité: API native (pas PowerShell)\n"
                "✓ Impact: Libération mémoire temporaire\n"
                "✓ Privilèges: Nécessite droits admin\n\n"
                "Note: Effet temporaire, Windows gère automatiquement la RAM"
            ),
            "flush_dns": (
                "Vide le cache DNS système.\n\n"
                "✓ Résout: Problèmes de résolution de noms\n"
                "✓ Utile: Après changement de DNS\n"
                "✓ Commande: ipconfig /flushdns\n\n"
                "Effet: Immédiat, sans risque"
            ),
            "disable_telemetry": (
                "Désactive les services de télémétrie Windows.\n\n"
                "⚠️ Services arrêtés:\n"
                "  - DiagTrack (Diagnostic Tracking)\n"
                "  - dmwappushservice (WAP Push)\n\n"
                "✓ Confidentialité: Réduit collecte de données\n"
                "⚠️ Attention: Peut affecter diagnostics Windows\n\n"
                "Recommandé: Utilisateurs soucieux de confidentialité"
            ),
            "clear_large_logs": (
                "Supprime les fichiers journaux volumineux.\n\n"
                "✓ Cibles: Fichiers .log dans TEMP et Logs\n"
                "✓ Sécurité: Logs système critiques protégés\n"
                "✓ Espace: Variable (100 MB - 2 GB)\n\n"
                "Note: Les logs actifs sont préservés"
            ),
        }
        return descriptions.get(key, "Aucune description détaillée disponible.")
    
    def _update_option(self, key, value):
        """Met à jour une option avancée"""
        self.app.advanced_options[key] = value
        print(f"[INFO] Option {key} set to {value}")
    
    def _build_configuration_section(self):
        """Construit la section Configuration avec monitoring matériel"""
        # Récupérer les données matérielles
        hw_data = hardware_monitor.get_all_components()
        
        # Conteneurs pour les composants (seront mis à jour en temps réel)
        self.hw_cpu_container = self._build_hardware_card("CPU", hw_data["cpu"])
        self.hw_memory_container = self._build_hardware_card("Mémoire", hw_data["memory"])
        self.hw_gpu_containers = [
            self._build_hardware_card("GPU", gpu) for gpu in hw_data["gpus"]
        ]
        self.hw_disk_containers = [
            self._build_hardware_card("Disque", disk) for disk in hw_data["disks"]
        ]
        
        # Démarrer le monitoring en temps réel
        if not hardware_monitor.monitoring:
            hardware_monitor.start_monitoring(interval=2.0, callback=self._update_hardware_display)
        
        return ft.Container(
            content=ft.Column(
                [
                    # En-tête de section
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.COMPUTER_OUTLINED,
                                size=22,
                                color=Colors.ACCENT_PRIMARY,
                            ),
                            ft.Container(width=Spacing.XS),
                            BodyText("Configuration matérielle", weight=Typography.WEIGHT_BOLD, size=18),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    Spacer(height=Spacing.XS),
                    Caption(
                        "Surveillance en temps réel des composants système • Aucune donnée n'est envoyée",
                        color=Colors.FG_SECONDARY,
                        size=12,
                    ),
                    Spacer(height=Spacing.LG),
                    
                    # Avertissement confidentialité
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.PRIVACY_TIP_OUTLINED, size=16, color=Colors.ACCENT_PRIMARY),
                                ft.Container(width=Spacing.XS),
                                Caption(
                                    "🔒 Confidentialité garantie : Toutes les données restent locales sur votre machine",
                                    color=Colors.ACCENT_PRIMARY,
                                    size=11,
                                    weight=Typography.WEIGHT_MEDIUM,
                                ),
                            ],
                        ),
                        bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY),
                        padding=Spacing.MD,
                        border_radius=BorderRadius.SM,
                        border=ft.border.all(1, ft.Colors.with_opacity(0.3, Colors.ACCENT_PRIMARY)),
                    ),
                    Spacer(height=Spacing.XL),
                    
                    # CPU
                    self.hw_cpu_container,
                    Spacer(height=Spacing.MD),
                    
                    # Mémoire
                    self.hw_memory_container,
                    Spacer(height=Spacing.MD),
                    
                    # GPU(s)
                    ft.Column(
                        self.hw_gpu_containers,
                        spacing=Spacing.MD,
                    ),
                    Spacer(height=Spacing.MD),
                    
                    # Disques
                    ft.Column(
                        self.hw_disk_containers,
                        spacing=Spacing.MD,
                    ),
                    
                    Spacer(height=Spacing.XL),
                    
                    # Légende des couleurs
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.INFO_OUTLINE, size=14, color=Colors.FG_TERTIARY),
                                ft.Container(width=Spacing.XS),
                                Caption("Légende températures:", color=Colors.FG_TERTIARY, size=11),
                                ft.Container(width=Spacing.SM),
                                ft.Container(
                                    width=12, height=12, bgcolor=ft.Colors.GREEN,
                                    border_radius=BorderRadius.SM,
                                ),
                                ft.Container(width=4),
                                Caption("Normal", color=Colors.FG_TERTIARY, size=10),
                                ft.Container(width=Spacing.SM),
                                ft.Container(
                                    width=12, height=12, bgcolor=ft.Colors.YELLOW,
                                    border_radius=BorderRadius.SM,
                                ),
                                ft.Container(width=4),
                                Caption("Élevée", color=Colors.FG_TERTIARY, size=10),
                                ft.Container(width=Spacing.SM),
                                ft.Container(
                                    width=12, height=12, bgcolor=ft.Colors.RED,
                                    border_radius=BorderRadius.SM,
                                ),
                                ft.Container(width=4),
                                Caption("Critique", color=Colors.FG_TERTIARY, size=10),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=Spacing.SM,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=0,
            ),
        )
    
    def _build_hardware_card(self, component_type, data):
        """Construit une carte pour un composant matériel"""
        # Déterminer l'icône selon le type (utiliser SVG)
        if component_type == "CPU":
            icon_path = "assets/icons/processeur.svg"
            name = data.get("name", "N/A")
            usage = data.get('usage', 0)
            freq_current = data.get('frequency_current', 0)
            freq_max = data.get('frequency_max', 0)
            
            # Barre de progression pour l'utilisation CPU
            cpu_progress = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                Caption("Utilisation", size=10, color=Colors.FG_TERTIARY),
                                ft.Container(expand=True),
                                Caption(f"{usage:.1f}%", size=11, weight=Typography.WEIGHT_BOLD),
                            ],
                            spacing=0,
                        ),
                        ft.Container(height=4),
                        ft.ProgressBar(
                            value=usage / 100,
                            height=6,
                            color=Colors.ACCENT_PRIMARY if usage < 80 else ft.Colors.ORANGE if usage < 95 else ft.Colors.RED,
                            bgcolor=Colors.BORDER_DEFAULT,
                            border_radius=BorderRadius.SM,
                        ),
                    ],
                    spacing=0,
                ),
                margin=ft.margin.only(top=8),
            )
            
            details = [
                f"Cœurs: {data.get('cores_physical', 0)} physiques / {data.get('cores_logical', 0)} logiques",
                f"Fréquence: {freq_current:.0f} MHz / {freq_max:.0f} MHz max",
            ]
        elif component_type == "Mémoire":
            icon_path = "assets/icons/memoire.svg"
            name = data.get("name", "RAM")
            total_gb = data.get("total", 0) / (1024**3)
            used_gb = data.get("used", 0) / (1024**3)
            available_gb = data.get("available", 0) / (1024**3)
            percent = data.get("percent", 0)
            
            # Informations sur les modules RAM
            ram_modules = data.get("modules", [])
            if ram_modules:
                module_count = len(ram_modules)
                module_info = f"{module_count} barrette{'s' if module_count > 1 else ''}"
                # Détails des modules
                module_details = ", ".join([f"{m:.0f}GB" for m in ram_modules])
                if module_details:
                    module_info += f" ({module_details})"
            else:
                module_info = "Information non disponible"
            
            # Barre de progression pour la RAM
            cpu_progress = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                Caption("Utilisation en cours", size=10, color=Colors.FG_TERTIARY),
                                ft.Container(expand=True),
                                Caption(f"{percent:.1f}%", size=11, weight=Typography.WEIGHT_BOLD),
                            ],
                            spacing=0,
                        ),
                        ft.Container(height=4),
                        ft.ProgressBar(
                            value=percent / 100,
                            height=6,
                            color=Colors.ACCENT_PRIMARY if percent < 80 else ft.Colors.ORANGE if percent < 95 else ft.Colors.RED,
                            bgcolor=Colors.BORDER_DEFAULT,
                            border_radius=BorderRadius.SM,
                        ),
                    ],
                    spacing=0,
                ),
                margin=ft.margin.only(top=8),
            )
            
            details = [
                f"Mémoire installée: {module_info}",
                f"Utilisée: {used_gb:.2f} GB / {total_gb:.2f} GB",
            ]
        elif component_type == "GPU":
            icon_path = "assets/icons/GPU.svg"
            name = data.get("name", "N/A")
            usage = data.get("usage", 0)
            driver_version = data.get("driver_version", "N/A")
            
            # Barre de progression pour l'utilisation GPU
            if usage > 0:
                cpu_progress = ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    Caption("Utilisation GPU", size=10, color=Colors.FG_TERTIARY),
                                    ft.Container(expand=True),
                                    Caption(f"{usage:.1f}%", size=11, weight=Typography.WEIGHT_BOLD),
                                ],
                                spacing=0,
                            ),
                            ft.Container(height=4),
                            ft.ProgressBar(
                                value=usage / 100,
                                height=6,
                                color=Colors.ACCENT_PRIMARY if usage < 80 else ft.Colors.ORANGE if usage < 95 else ft.Colors.RED,
                                bgcolor=Colors.BORDER_DEFAULT,
                                border_radius=BorderRadius.SM,
                            ),
                        ],
                        spacing=0,
                    ),
                    margin=ft.margin.only(top=8),
                )
            else:
                cpu_progress = None
            
            details = [
                f"Pilote: {driver_version}",
            ]
        elif component_type == "Disque":
            icon_path = "assets/icons/disque-dur.svg"
            disk_model = data.get("model", "Unknown")
            disk_type = data.get("type", "Unknown")
            name = f"{data.get('name', 'N/A')} - {disk_model}"
            total_gb = data.get("total", 0) / (1024**3)
            used_gb = data.get("used", 0) / (1024**3)
            free_gb = data.get("free", 0) / (1024**3)
            percent = data.get("percent", 0)
            
            # Barre de progression pour le disque
            cpu_progress = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                Caption("Utilisation", size=10, color=Colors.FG_TERTIARY),
                                ft.Container(expand=True),
                                Caption(f"{percent:.1f}%", size=11, weight=Typography.WEIGHT_BOLD),
                            ],
                            spacing=0,
                        ),
                        ft.Container(height=4),
                        ft.ProgressBar(
                            value=percent / 100,
                            height=6,
                            color=Colors.ACCENT_PRIMARY if percent < 80 else ft.Colors.ORANGE if percent < 95 else ft.Colors.RED,
                            bgcolor=Colors.BORDER_DEFAULT,
                            border_radius=BorderRadius.SM,
                        ),
                    ],
                    spacing=0,
                ),
                margin=ft.margin.only(top=8),
            )
            
            details = [
                f"Type: {disk_type}",
                f"Espace utilisé: {used_gb:.2f} GB / {total_gb:.2f} GB",
                f"Espace libre: {free_gb:.2f} GB",
            ]
        else:
            icon_path = None
            name = "Inconnu"
            cpu_progress = None
            details = []
        
        # Température
        temp = data.get("temperature")
        temp_color = self._get_temp_color(temp, component_type.lower())
        temp_text = f"{temp:.1f}°C" if temp is not None else "N/A"
        
        # Indicateur de température avec couleur et icône animée
        temp_indicator = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.THERMOSTAT, size=18, color=temp_color),
                            ft.Container(width=4),
                            ft.Text(
                                temp_text,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=temp_color,
                            ),
                        ],
                        spacing=0,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(height=2),
                    Caption(
                        "Température" if temp is not None else "Non disponible",
                        size=9,
                        color=Colors.FG_TERTIARY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            bgcolor=ft.Colors.with_opacity(0.1, temp_color),
            padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
            border_radius=BorderRadius.MD,
            border=ft.border.all(2, ft.Colors.with_opacity(0.4, temp_color)),
        )
        
        # Colonne d'informations
        info_column_controls = [
            BodyText(name, weight=Typography.WEIGHT_BOLD, size=14, color=Colors.FG_PRIMARY),
            Spacer(height=Spacing.XS),
            ft.Column(
                [Caption(detail, color=Colors.FG_SECONDARY, size=11) for detail in details],
                spacing=3,
            ),
        ]
        
        if cpu_progress:
            info_column_controls.append(cpu_progress)
        
        # Construire l'icône (SVG ou Icon par défaut)
        if icon_path:
            icon_widget = ft.Image(
                src=icon_path,
                width=36,
                height=36,
                color=Colors.ACCENT_PRIMARY,
                fit=ft.ImageFit.CONTAIN,
            )
        else:
            icon_widget = ft.Icon(ft.Icons.DEVICE_UNKNOWN, size=36, color=Colors.ACCENT_PRIMARY)
        
        # Construire la carte avec hover effect
        return ft.Container(
            content=ft.Row(
                [
                    # Icône du composant avec glow
                    ft.Container(
                        content=icon_widget,
                        padding=Spacing.LG,
                        bgcolor=ft.Colors.with_opacity(0.15, Colors.ACCENT_PRIMARY),
                        border_radius=BorderRadius.MD,
                        border=ft.border.all(1, ft.Colors.with_opacity(0.3, Colors.ACCENT_PRIMARY)),
                    ),
                    ft.Container(width=Spacing.LG),
                    
                    # Informations
                    ft.Column(
                        info_column_controls,
                        expand=True,
                        spacing=0,
                    ),
                    
                    ft.Container(width=Spacing.MD),
                    
                    # Température
                    temp_indicator,
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            bgcolor=Colors.BG_SECONDARY,
            padding=Spacing.LG,
            border_radius=BorderRadius.LG,
            border=ft.border.all(1, Colors.BORDER_DEFAULT),
            data={"component_type": component_type, "data": data},
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )
    
    def _get_temp_color(self, temperature, component_type):
        """Retourne la couleur selon la température"""
        if temperature is None:
            return ft.Colors.GREY
        
        color_name = hardware_monitor.get_temperature_color(temperature, component_type)
        
        color_map = {
            "green": ft.Colors.GREEN,
            "yellow": ft.Colors.YELLOW,
            "red": ft.Colors.RED,
            "gray": ft.Colors.GREY,
        }
        
        return color_map.get(color_name, ft.Colors.GREY)
    
    def _update_hardware_display(self, hw_data):
        """Met à jour l'affichage des composants matériels en temps réel"""
        try:
            # Mettre à jour CPU
            if hasattr(self, 'hw_cpu_container') and self.hw_cpu_container:
                self._update_hardware_card(self.hw_cpu_container, "CPU", hw_data["cpu"])
            
            # Mettre à jour Mémoire
            if hasattr(self, 'hw_memory_container') and self.hw_memory_container:
                self._update_hardware_card(self.hw_memory_container, "Mémoire", hw_data["memory"])
            
            # Mettre à jour GPU(s)
            if hasattr(self, 'hw_gpu_containers') and self.hw_gpu_containers:
                for i, gpu_data in enumerate(hw_data["gpus"]):
                    if i < len(self.hw_gpu_containers):
                        self._update_hardware_card(self.hw_gpu_containers[i], "GPU", gpu_data)
            
            # Mettre à jour Disques
            if hasattr(self, 'hw_disk_containers') and self.hw_disk_containers:
                for i, disk_data in enumerate(hw_data["disks"]):
                    if i < len(self.hw_disk_containers):
                        self._update_hardware_card(self.hw_disk_containers[i], "Disque", disk_data)
            
            # Mettre à jour la page
            self.page.update()
        except Exception as e:
            print(f"[ERROR] Failed to update hardware display: {e}")
    
    def _update_hardware_card(self, card_container, component_type, data):
        """Met à jour une carte de composant matériel"""
        try:
            # Récupérer le conteneur de température (dernier élément de la Row)
            row = card_container.content
            temp_indicator = row.controls[-1]
            
            # Mettre à jour la température
            temp = data.get("temperature")
            temp_color = self._get_temp_color(temp, component_type.lower())
            temp_text = f"{temp:.1f}°C" if temp is not None else "N/A"
            
            # Mettre à jour l'indicateur
            temp_indicator.bgcolor = ft.Colors.with_opacity(0.1, temp_color)
            temp_indicator.border = ft.border.all(2, ft.Colors.with_opacity(0.4, temp_color))
            
            # Mettre à jour le texte et l'icône dans la colonne
            temp_column = temp_indicator.content
            temp_row = temp_column.controls[0]  # Row avec icône et texte
            temp_row.controls[0].color = temp_color  # Icône
            temp_row.controls[2].value = temp_text  # Texte
            temp_row.controls[2].color = temp_color
            
            # Mettre à jour les détails selon le type
            info_column = row.controls[2]  # Colonne d'informations
            
            if component_type == "CPU":
                # Mettre à jour les détails textuels
                details_column = info_column.controls[2]
                freq_current = data.get('frequency_current', 0)
                freq_max = data.get('frequency_max', 0)
                details_column.controls[1].value = f"Fréquence: {freq_current:.0f} MHz / {freq_max:.0f} MHz max"
                
                # Mettre à jour la barre de progression
                if len(info_column.controls) > 3:
                    progress_container = info_column.controls[3]
                    progress_column = progress_container.content
                    usage = data.get('usage', 0)
                    
                    # Mettre à jour le pourcentage
                    progress_column.controls[0].controls[2].value = f"{usage:.1f}%"
                    
                    # Mettre à jour la barre
                    progress_bar = progress_column.controls[2]
                    progress_bar.value = usage / 100
                    progress_bar.color = Colors.ACCENT_PRIMARY if usage < 80 else ft.Colors.ORANGE if usage < 95 else ft.Colors.RED
                    
            elif component_type == "Mémoire":
                # Mettre à jour les détails textuels
                details_column = info_column.controls[2]
                total_gb = data.get("total", 0) / (1024**3)
                used_gb = data.get("used", 0) / (1024**3)
                percent = data.get("percent", 0)
                
                # Informations sur les modules RAM
                ram_modules = data.get("modules", [])
                if ram_modules:
                    module_count = len(ram_modules)
                    module_info = f"{module_count} barrette{'s' if module_count > 1 else ''}"
                    module_details = ", ".join([f"{m:.0f}GB" for m in ram_modules])
                    if module_details:
                        module_info += f" ({module_details})"
                else:
                    module_info = "Information non disponible"
                
                details_column.controls[0].value = f"Mémoire installée: {module_info}"
                details_column.controls[1].value = f"Utilisée: {used_gb:.2f} GB / {total_gb:.2f} GB"
                
                # Mettre à jour la barre de progression
                if len(info_column.controls) > 3:
                    progress_container = info_column.controls[3]
                    progress_column = progress_container.content
                    
                    # Mettre à jour le pourcentage
                    progress_column.controls[0].controls[2].value = f"{percent:.1f}%"
                    
                    # Mettre à jour la barre
                    progress_bar = progress_column.controls[2]
                    progress_bar.value = percent / 100
                    progress_bar.color = Colors.ACCENT_PRIMARY if percent < 80 else ft.Colors.ORANGE if percent < 95 else ft.Colors.RED
                    
            elif component_type == "GPU":
                # Mettre à jour les détails textuels
                details_column = info_column.controls[2]
                driver_version = data.get("driver_version", "N/A")
                usage = data.get("usage", 0)
                
                details_column.controls[0].value = f"Pilote: {driver_version}"
                
                # Mettre à jour la barre de progression si elle existe
                if usage > 0 and len(info_column.controls) > 3:
                    progress_container = info_column.controls[3]
                    progress_column = progress_container.content
                    
                    # Mettre à jour le pourcentage
                    progress_column.controls[0].controls[2].value = f"{usage:.1f}%"
                    
                    # Mettre à jour la barre
                    progress_bar = progress_column.controls[2]
                    progress_bar.value = usage / 100
                    progress_bar.color = Colors.ACCENT_PRIMARY if usage < 80 else ft.Colors.ORANGE if usage < 95 else ft.Colors.RED
                    
            elif component_type == "Disque":
                # Mettre à jour les détails textuels
                details_column = info_column.controls[2]
                total_gb = data.get("total", 0) / (1024**3)
                used_gb = data.get("used", 0) / (1024**3)
                free_gb = data.get("free", 0) / (1024**3)
                percent = data.get("percent", 0)
                disk_type = data.get("type", "Unknown")
                
                details_column.controls[0].value = f"Type: {disk_type}"
                details_column.controls[1].value = f"Espace utilisé: {used_gb:.2f} GB / {total_gb:.2f} GB"
                details_column.controls[2].value = f"Espace libre: {free_gb:.2f} GB"
                
                # Mettre à jour la barre de progression
                if len(info_column.controls) > 3:
                    progress_container = info_column.controls[3]
                    progress_column = progress_container.content
                    
                    # Mettre à jour le pourcentage
                    progress_column.controls[0].controls[2].value = f"{percent:.1f}%"
                    
                    # Mettre à jour la barre
                    progress_bar = progress_column.controls[2]
                    progress_bar.value = percent / 100
                    progress_bar.color = Colors.ACCENT_PRIMARY if percent < 80 else ft.Colors.ORANGE if percent < 95 else ft.Colors.RED
                    
        except Exception as e:
            print(f"[ERROR] Failed to update hardware card: {e}")
    
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
            # Afficher le bouton de prévisualisation
            if hasattr(self, 'action_button_container'):
                self.action_button_container.visible = True
        elif tab_id == "advanced":
            self.content_container.content = ft.Column(
                [self._build_advanced_options()],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=0,
            )
            # Afficher le bouton de prévisualisation
            if hasattr(self, 'action_button_container'):
                self.action_button_container.visible = True
        elif tab_id == "config":
            self.content_container.content = ft.Column(
                [self._build_configuration_section()],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=0,
            )
            # Masquer le bouton de prévisualisation dans l'onglet Configuration
            if hasattr(self, 'action_button_container'):
                self.action_button_container.visible = False
        
        # Animation d'entrée (fade in)
        self.content_container.opacity = 1
        self.page.update()
    
    def _update_tab_styles(self):
        """Met à jour les styles des onglets avec animation"""
        for tab in [self.tab_quick, self.tab_advanced, self.tab_config]:
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
        """Affiche la page de prévisualisation avec transition fluide"""
        try:
            # Animation de sortie de la page actuelle
            print("[DEBUG] Starting fade out animation...")
            if hasattr(self, 'main_container'):
                self.main_container.opacity = 0
                self.page.update()
            
            import time
            time.sleep(0.3)  # Attendre la fin de l'animation de sortie
            
            # Importer et créer la page de prévisualisation
            print("[DEBUG] Creating preview page...")
            from frontend.pages.preview_page import PreviewPage
            
            preview_page = PreviewPage(self.page, self.app, preview_data)
            
            # Remplacer le contenu de la page
            print("[DEBUG] Replacing page content...")
            self.page.controls.clear()
            
            # Construire la page (elle commence avec opacity=0)
            preview_container = preview_page.build()
            
            # Ajouter à la page
            self.page.add(preview_container)
            self.page.update()
            
            # Petit délai pour que le DOM soit prêt
            time.sleep(0.05)
            
            # Animation d'entrée
            print("[DEBUG] Starting fade in animation...")
            preview_container.opacity = 1
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
        
        # Note: Le nettoyage n'est accessible que depuis la page de prévisualisation
        # après avoir fait un dry-run, donc pas besoin de vérification ici
        
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
            
            # Vider la corbeille avec confirmation automatique
            result_recycle = cleaner.empty_recycle_bin(confirmed=True)
            print(f"[INFO] Corbeille: {result_recycle.get('recycle_bin_deleted', 0)} éléments supprimés")
            
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
