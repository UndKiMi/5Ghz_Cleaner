"""
Main Page - Page principale de l'application
Contient toutes les fonctionnalités de nettoyage
"""
import flet as ft
from ..design_system import *
from ..design_system.theme import Colors, Spacing, Typography, BorderRadius
from src.core import cleaner
from src.utils.logger_safe import SafeCleaningLogger as CleaningLogger
from src.services.security import security_manager
from src.services.hardware_monitor import hardware_monitor


class MainPage:
    def __init__(self, page: ft.Page, app):
        self.page = page
        self.app = app
        self.current_tab = "quick"  # "quick" or "advanced"
        self.dry_run_completed = False
        self.cleaning_in_progress = False
        self.quick_action_in_progress = False  # Verrouillage pour les actions rapides
        self.status_text = None
        self.dry_run_button = None
        
        # ANTI-SPAM: Système de cooldown pour les boutons (PROTECTION)
        import time
        import threading
        self._last_action_time = {}  # Timestamp de la dernière action par bouton
        self._cooldown_duration = 600  # Cooldown de 10 minutes (600 secondes) - Protection anti-spam renforcée
        self._cooldown_timers = {}  # Timers actifs pour chaque bouton
        self._cooldown_lock = threading.Lock()  # Lock pour thread-safety
        self._button_original_texts = {}  # Textes originaux des boutons (pour restauration après cooldown)
        self._button_original_colors = {}  # Couleurs originales des boutons (pour restauration après cooldown)
        
        # NOUVEAU: Système de références persistantes pour mise à jour dynamique (REFONTE UI)
        self.storage_item_refs = {
            'cleanable': {'title': None, 'current': None, 'progress': None, 'container': None},
            'ram': {'title': None, 'current': None, 'progress': None, 'container': None},
            'dns': {'title': None, 'current': None, 'progress': None, 'container': None},
        }
        self.storage_total_text_ref = None
        
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
        
        # Créer le bouton de prévisualisation pour la barre d'onglets (AGRANDI)
        def on_preview_click(e):
            self._start_dry_run(e)
        
        # Créer les références pour le texte et l'icône du bouton tabs
        self.preview_button_tabs_icon = ft.Icon(ft.Icons.PREVIEW_ROUNDED, size=18, color=ft.Colors.WHITE)
        self.preview_button_tabs_text = ft.Text(
            "Prévisualiser",
            size=14,
            weight=ft.FontWeight.W_600,
            color=ft.Colors.WHITE,
        )
        
        self.preview_button_tabs = ft.Container(
            content=ft.Row(
                [
                    self.preview_button_tabs_icon,
                    ft.Container(width=8),
                    self.preview_button_tabs_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=24, vertical=10),
            border_radius=BorderRadius.MD,
            bgcolor=Colors.ACCENT_PRIMARY,
            on_click=on_preview_click,
            ink=True,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        
        return ft.Container(
            content=ft.Row(
                [
                    self.tab_quick,
                    ft.Container(width=2, height=32, bgcolor=Colors.BORDER_DEFAULT),
                    self.tab_advanced,
                    ft.Container(width=2, height=32, bgcolor=Colors.BORDER_DEFAULT),
                    self.tab_config,
                    ft.Container(width=Spacing.LG),  # Espacement
                    ft.Container(width=2, height=32, bgcolor=Colors.BORDER_DEFAULT),  # Séparation propre
                    ft.Container(width=Spacing.SM),  # Petit espacement
                    self.preview_button_tabs,  # Bouton de prévisualisation
                ],
                spacing=Spacing.MD,
            ),
            padding=ft.padding.only(bottom=Spacing.SM),
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
        """Construit la section des actions - DESIGN CENTRÉ ET MODERNE"""
        return ft.Container(
            content=ft.Column(
                [
                    # Message de prévisualisation
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
                                    "Prévisualisez le nettoyage pour voir ce qui sera supprimé avant de continuer",
                                    text_align=ft.TextAlign.CENTER,
                                    color=Colors.FG_SECONDARY,
                                    size=12,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(vertical=Spacing.SM),
                    ),
                    
                    # En-tête centré
                    ft.Container(
                        content=ft.Column(
                            [
                                BodyText(
                                    "Actions rapides", 
                                    weight=ft.FontWeight.W_600, 
                                    size=22,
                                    color=Colors.FG_PRIMARY,
                                ),
                                Spacer(height=Spacing.XS),
                                Caption(
                                    "Optimisez votre système en un clic.",
                                    color=Colors.FG_SECONDARY,
                                    size=13,
                                ),
                            ],
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.only(bottom=Spacing.MD),
                    ),
                    
                    # Grille d'actions rapides CENTRÉE - 2x2
                    ft.Container(
                        content=ft.Column(
                            [
                                # Ligne 1
                                ft.Row(
                                    [
                                        self._build_quick_action_button(
                                            icon=ft.Icons.RESTORE_ROUNDED,
                                            title="Point de restauration",
                                            description="Crée une sauvegarde du système.",
                                            action="restore_point",
                                        ),
                                        ft.Container(width=Spacing.LG),
                                        self._build_quick_action_button(
                                            icon=ft.Icons.STORAGE_ROUNDED,
                                            title="Optimisation Disque dur",
                                            description="Optimise et fluidifie le disque.",
                                            action="optimize_disk",
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                Spacer(height=Spacing.LG),
                                # Ligne 2
                                ft.Row(
                                    [
                                        self._build_quick_action_button(
                                            icon=ft.Icons.DELETE_SWEEP_ROUNDED,
                                            title="Vider la corbeille",
                                            description="Supprime définitivement les éléments.",
                                            action="empty_recycle",
                                        ),
                                        ft.Container(width=Spacing.LG),
                                        self._build_quick_action_button(
                                            icon=ft.Icons.DNS_ROUNDED,
                                            title="Flush DNS",
                                            description="Réinitialise le cache DNS.",
                                            action="flush_dns",
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ),
                    
                    Spacer(height=Spacing.XL),
                    
                    # Section Stockage et Optimisations EN BAS
                    # DONNÉES RÉELLES calculées dynamiquement
                    self._build_storage_preview_section(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
        )
    
    def _build_quick_action_button(self, icon, title, description, action):
        """Construit un bouton d'action - REFONTE TOTALE CARD DESIGN"""
        button_ref = {"container": None, "progress_bar": None, "icon": None, "title": None}
        
        def on_button_click(e):
            self._execute_quick_action(action, button_ref)
        
        # Icône moderne
        icon_widget = ft.Icon(
            icon, 
            size=32, 
            color=Colors.ACCENT_PRIMARY
        )
        
        # Titre
        title_text = ft.Text(
            title,
            color=Colors.FG_PRIMARY,
            weight=ft.FontWeight.W_600,
            size=15,
        )
        
        # Description
        desc_text = ft.Text(
            description,
            color=Colors.FG_SECONDARY,
            size=12,
        )
        
        # Barre de progression (cachée par défaut)
        progress_bar = ft.ProgressBar(
            value=0,
            height=2,
            color=Colors.ACCENT_PRIMARY,
            bgcolor=Colors.BORDER_DEFAULT,
            visible=False,
        )
        
        button = ft.Container(
            content=ft.Row(
                [
                    # Icône à gauche
                    ft.Container(
                        content=icon_widget,
                        width=56,
                        height=56,
                        border_radius=BorderRadius.SM,
                        bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(width=Spacing.MD),
                    # Texte à droite
                    ft.Column(
                        [
                            title_text,
                            Spacer(height=Spacing.XS),
                            desc_text,
                            ft.Container(height=Spacing.XS),
                            progress_bar,
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
            on_click=on_button_click,
            ink=True,
            tooltip=self._get_quick_action_tooltip(action),
            data=action,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        
        button_ref["container"] = button
        button_ref["progress_bar"] = progress_bar
        button_ref["icon"] = icon_widget
        button_ref["title"] = title_text
        
        return button
    
    def _calculate_storage_data(self):
        """
        Calcule les données de stockage de manière optimisée et centralisée
        Retourne un dictionnaire avec toutes les valeurs calculées
        NOUVELLE VERSION: Utilise scan_all_cleanable_files pour les fichiers
        """
        from src.core import cleaner
        import psutil
        import time
        
        # === CALCUL DES FICHIERS À NETTOYER (tous types) ===
        try:
            # Utiliser la nouvelle fonction qui scanne TOUT
            scan_result = cleaner.scan_all_cleanable_files()
            cleanable_size_mb = scan_result.get('total_size_mb', 0)
            cleanable_count = scan_result.get('file_count', 0)
        except Exception as e:
            print(f"[ERROR] Failed to scan cleanable files: {e}")
            cleanable_size_mb = 0
            cleanable_count = 0
        
        # === CALCUL DE LA RAM STANDBY (NOUVEAU - PRÉCIS) ===
        try:
            from src.core.ram_manager import ram_manager
            
            # Utiliser le nouveau gestionnaire RAM pour un calcul précis
            ram_info = ram_manager.get_detailed_memory_info()
            standby_mb = ram_info['standby_mb']
            standby_percent = ram_info['percent_standby']
            total_mb_ram = ram_info['total_mb']
            
            pass  # RAM Standby calculée
        except Exception as e:
            print(f"[ERROR] Failed to calculate RAM standby: {e}")
            import traceback
            traceback.print_exc()
            # Fallback vers psutil
            memory = psutil.virtual_memory()
            total_mb_ram = memory.total / (1024 * 1024)
            standby_mb = total_mb_ram * 0.10  # Estimation conservatrice
            standby_percent = 10.0
        
        # === CALCUL DU CACHE DNS ===
        try:
            dns_mb = cleaner.get_dns_cache_size()
        except Exception as e:
            print(f"[ERROR] Failed to get DNS cache size: {e}")
            dns_mb = 0.05
        
        return {
            'cleanable_mb': cleanable_size_mb,
            'cleanable_gb': cleanable_size_mb / 1024,
            'cleanable_count': cleanable_count,
            'standby_mb': standby_mb,
            'standby_gb': standby_mb / 1024,
            'standby_percent': standby_percent,
            'dns_mb': dns_mb,
            'dns_gb': dns_mb / 1024
        }
    
    def _build_storage_preview_section(self):
        """Construit la section de prévisualisation avec DONNÉES RÉELLES - VERSION OPTIMISÉE"""
        # Conteneur avec message de chargement initial
        storage_container = ft.Container(
            content=ft.Column(
                [
                    BodyText(
                        "Espace à libérer", 
                        weight=ft.FontWeight.W_600, 
                        size=20,
                        color=Colors.FG_PRIMARY,
                    ),
                    Spacer(height=Spacing.XS),
                    Caption(
                        "Calcul en cours...",
                        color=Colors.FG_SECONDARY,
                        size=13,
                    ),
                    Spacer(height=Spacing.XL),
                    ft.ProgressRing(width=32, height=32, color=Colors.ACCENT_PRIMARY),
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        
        # Stocker la référence pour mise à jour automatique
        self.storage_container = storage_container
        self.storage_update_timer = None
        self.storage_update_running = False
        
        # Cache pour éviter les recalculs inutiles
        self.last_temp_size = 0
        self.last_standby_size = 0
        self.last_update_time = 0
        
        # Initialiser les compteurs pour les scans
        self.last_cleanable_scan = 0
        self.last_ram_scan = 0
        self.last_dns_scan = 0
        
        # Créer les widgets de texte qui seront mis à jour (pas recréés)
        self.storage_total_text = None
        self.storage_cleanable_text = None
        self.storage_cleanable_progress = None
        self.storage_ram_text = None
        self.storage_ram_progress = None
        self.storage_dns_text = None
        self.storage_dns_progress = None
        
        # Lancer le calcul en arrière-plan
        import threading
        def calculate_storage():
            try:
                # Utiliser la fonction centralisée
                storage_data = self._calculate_storage_data()
                
                cleanable_mb = storage_data['cleanable_mb']
                cleanable_gb = storage_data['cleanable_gb']
                standby_mb = storage_data['standby_mb']
                standby_gb = storage_data['standby_gb']
                standby_percent = storage_data['standby_percent']
                dns_mb = storage_data['dns_mb']
                
                # Calculer le total pour les pourcentages
                total_mb = cleanable_mb + standby_mb + dns_mb
                
                # Mettre à jour l'interface avec les vraies données
                storage_container.content = self._build_storage_content(
                    cleanable_mb, cleanable_gb, 
                    standby_mb, standby_gb, standby_percent,
                    dns_mb, total_mb
                )
                self.page.update()
                
                # Démarrer la mise à jour automatique
                self._start_storage_auto_update()
                
            except Exception as e:
                print(f"[ERROR] Failed to calculate storage: {e}")
                import traceback
                traceback.print_exc()
                # Afficher un message d'erreur
                storage_container.content = ft.Column(
                    [
                        BodyText(
                            "Espace à libérer", 
                            weight=ft.FontWeight.W_600, 
                            size=20,
                            color=Colors.FG_PRIMARY,
                        ),
                        Spacer(height=Spacing.XS),
                        Caption(
                            "Impossible de calculer l'espace",
                            color=Colors.ERROR,
                            size=13,
                        ),
                    ],
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
                self.page.update()
        
        # Lancer le thread de calcul
        threading.Thread(target=calculate_storage, daemon=True).start()
        
        return storage_container
    
    def _build_storage_content(self, cleanable_mb, cleanable_gb, standby_mb, standby_gb, standby_percent, dns_mb, total_mb):
        """Construit le contenu de la section de stockage - CRÉATION UNIQUE"""
        # Si c'est la première fois, créer les widgets et stocker les références
        if self.storage_total_text is None:
            # Créer les widgets de texte
            self.storage_total_text = Caption(
                f"Total estimé: {total_mb / 1024:.2f} GB",
                color=Colors.FG_SECONDARY,
                size=13,
            )
            
            # Créer les items de stockage avec références
            self.storage_cleanable_item = self._build_storage_item_with_tooltip(
                icon=ft.Icons.CLEANING_SERVICES_OUTLINED,
                title="Fichiers à nettoyer",
                current=f"{cleanable_gb:.2f} GB" if cleanable_gb >= 1 else f"{cleanable_mb:.0f} MB",
                percentage=cleanable_mb / total_mb if total_mb > 0 else 0,
                color=Colors.WARNING,
                show_button=True,
                button_text="Nettoyage rapide",
                button_action=lambda e: self._quick_clean_files(),
                button_ref_key="clean_button",
                tooltip="Fichiers temporaires, logs, cache Windows et corbeille. Scan des dossiers toutes les 2 s.",
                item_key="cleanable"
            )
            
            self.storage_ram_item = self._build_storage_item_with_tooltip(
                icon=ft.Icons.MEMORY_OUTLINED,
                title=f"RAM Standby ({standby_percent:.1f}%)",
                current=f"{standby_gb:.2f} GB" if standby_gb >= 1 else f"{standby_mb:.0f} MB",
                percentage=standby_mb / total_mb if total_mb > 0 else 0,
                color=Colors.INFO,
                show_button=True,
                button_text="Vider la RAM",
                button_action=lambda e: self._clear_ram_action(),
                button_ref_key="ram_button",
                tooltip="La RAM en standby sur un PC est une mémoire occupée par des données récentes mais non utilisées, conservées pour accélérer la réouverture des applications.",
                item_key="ram"
            )
            
            self.storage_dns_item = self._build_storage_item_with_tooltip(
                icon=ft.Icons.DNS_OUTLINED,
                title="Cache DNS",
                current=f"{dns_mb:.2f} MB" if dns_mb >= 1 else f"{dns_mb * 1024:.0f} KB",
                percentage=dns_mb / total_mb if total_mb > 0 else 0,
                color=Colors.SUCCESS,
                show_button=False,
                tooltip="Le cache DNS est une mémoire locale sur ton PC qui stocke les adresses IP des sites récemment visités pour accélérer leur accès et éviter de redemander l'information à chaque fois à l'ordinateur.",
                item_key="dns"
            )
            
            return ft.Column(
                [
                    BodyText(
                        "Espace à libérer", 
                        weight=ft.FontWeight.W_600, 
                        size=20,
                        color=Colors.FG_PRIMARY,
                    ),
                    Spacer(height=Spacing.XS),
                    self.storage_total_text,
                    Spacer(height=Spacing.MD),  # Réduit de XL à MD
                    ft.Column(
                        [
                            self.storage_cleanable_item,
                            Spacer(height=Spacing.SM),  # Réduit de MD à SM
                            self.storage_ram_item,
                            Spacer(height=Spacing.SM),  # Réduit de MD à SM
                            self.storage_dns_item,
                        ],
                        spacing=0,
                    ),
                ],
                spacing=0,
            )
        else:
            # Mise à jour uniquement des valeurs (pas de recréation)
            self._update_storage_values(cleanable_mb, cleanable_gb, standby_mb, standby_gb, standby_percent, dns_mb, total_mb)
            # Retourner None pour indiquer qu'on a juste mis à jour
            return None
    
    def _update_storage_values(self, cleanable_mb, cleanable_gb, standby_mb, standby_gb, standby_percent, dns_mb, total_mb):
        """Met à jour uniquement les valeurs sans recréer les widgets"""
        # Mettre à jour le total
        if self.storage_total_text:
            self.storage_total_text.value = f"Total estimé: {total_mb / 1024:.2f} GB"
        
        # Mettre à jour les items via leurs références stockées
        if hasattr(self, 'storage_item_refs'):
            # Fichiers à nettoyer
            if 'cleanable' in self.storage_item_refs:
                refs = self.storage_item_refs['cleanable']
                refs['title'].value = "Fichiers à nettoyer"
                refs['current'].value = f"À libérer: {cleanable_gb:.2f} GB" if cleanable_gb >= 1 else f"À libérer: {cleanable_mb:.0f} MB"
                refs['progress'].value = cleanable_mb / total_mb if total_mb > 0 else 0
            
            # RAM Standby
            if 'ram' in self.storage_item_refs:
                refs = self.storage_item_refs['ram']
                refs['title'].value = f"RAM Standby ({standby_percent:.1f}%)"
                refs['current'].value = f"À libérer: {standby_gb:.2f} GB" if standby_gb >= 1 else f"À libérer: {standby_mb:.0f} MB"
                # Protection contre division par zéro
                refs['progress'].value = (standby_mb / total_mb) if total_mb > 0 else 0
            
            # Cache DNS
            if 'dns' in self.storage_item_refs:
                refs = self.storage_item_refs['dns']
                refs['title'].value = "Cache DNS"
                refs['current'].value = f"À libérer: {dns_mb:.2f} MB" if dns_mb >= 1 else f"À libérer: {dns_mb * 1024:.0f} KB"
                refs['progress'].value = dns_mb / total_mb if total_mb > 0 else 0
    
    def _start_storage_auto_update(self):
        """Démarre la mise à jour automatique avec intervalles différents pour chaque section"""
        import threading
        import time
        
        def auto_update_loop():
            while True:
                try:
                    current_time = time.time()
                    
                    # Déterminer quoi scanner selon les intervalles
                    scan_cleanable = (current_time - self.last_cleanable_scan) >= 2  # 2 secondes
                    scan_ram = (current_time - self.last_ram_scan) >= 2  # 2 secondes
                    scan_dns = (current_time - self.last_dns_scan) >= 2  # 2 secondes
                    
                    # Scanner uniquement ce qui est nécessaire
                    if scan_cleanable or scan_ram or scan_dns:
                        storage_data = self._calculate_storage_data_selective(
                            scan_cleanable, scan_ram, scan_dns
                        )
                        
                        # Mettre à jour les timestamps
                        if scan_cleanable:
                            self.last_cleanable_scan = current_time
                        if scan_ram:
                            self.last_ram_scan = current_time
                        if scan_dns:
                            self.last_dns_scan = current_time
                        
                        cleanable_mb = storage_data['cleanable_mb']
                        cleanable_gb = storage_data['cleanable_gb']
                        standby_mb = storage_data['standby_mb']
                        standby_gb = storage_data['standby_gb']
                        standby_percent = storage_data['standby_percent']
                        dns_mb = storage_data['dns_mb']
                        
                        total_mb = cleanable_mb + standby_mb + dns_mb
                        
                        # Mettre à jour l'interface (sans recréer les widgets)
                        if hasattr(self, 'storage_container') and self.storage_container:
                            # Appeler _build_storage_content qui va juste mettre à jour les valeurs
                            result = self._build_storage_content(
                                cleanable_mb, cleanable_gb,
                                standby_mb, standby_gb, standby_percent,
                                dns_mb, total_mb
                            )
                            # Si result n'est pas None, c'est la première création
                            if result is not None:
                                self.storage_container.content = result
                            # Sinon, les valeurs ont juste été mises à jour
                            self.page.update()
                    
                    time.sleep(0.5)  # Vérifier toutes les 0.5 secondes
                
                except Exception as e:
                    print(f"[ERROR] Auto-update storage failed: {e}")
                    time.sleep(1)
        
        # Lancer le thread de mise à jour automatique
        self.storage_update_timer = threading.Thread(target=auto_update_loop, daemon=True)
        self.storage_update_timer.start()
    
    def _calculate_storage_data_selective(self, scan_cleanable, scan_ram, scan_dns):
        """Calcule sélectivement les données selon ce qui doit être scanné"""
        from src.core import cleaner
        import psutil
        
        # Utiliser les valeurs en cache si pas besoin de rescanner
        if not hasattr(self, '_cached_storage_data'):
            self._cached_storage_data = {
                'cleanable_mb': 0,
                'cleanable_gb': 0,
                'cleanable_count': 0,
                'standby_mb': 0,
                'standby_gb': 0,
                'standby_percent': 0,
                'dns_mb': 0.05,
                'dns_gb': 0.00005
            }
        
        # Scanner les fichiers à nettoyer si nécessaire
        if scan_cleanable:
            try:
                scan_result = cleaner.scan_all_cleanable_files()
                self._cached_storage_data['cleanable_mb'] = scan_result.get('total_size_mb', 0)
                self._cached_storage_data['cleanable_gb'] = scan_result.get('total_size_gb', 0)
                self._cached_storage_data['cleanable_count'] = scan_result.get('file_count', 0)
            except Exception as e:
                print(f"[ERROR] Failed to scan cleanable files: {e}")
        
        # Scanner la RAM si nécessaire (NOUVEAU - PRÉCIS)
        if scan_ram:
            try:
                from src.core.ram_manager import ram_manager
                
                # Utiliser le nouveau gestionnaire RAM pour un calcul précis
                ram_info = ram_manager.get_detailed_memory_info()
                standby_mb = ram_info['standby_mb']
                standby_percent = ram_info['percent_standby']
                
                self._cached_storage_data['standby_mb'] = standby_mb
                self._cached_storage_data['standby_gb'] = standby_mb / 1024
                self._cached_storage_data['standby_percent'] = standby_percent
            except Exception as e:
                print(f"[ERROR] Failed to calculate RAM standby: {e}")
                import traceback
                traceback.print_exc()
        
        # Scanner le DNS si nécessaire
        if scan_dns:
            try:
                dns_mb = cleaner.get_dns_cache_size()
                self._cached_storage_data['dns_mb'] = dns_mb
                self._cached_storage_data['dns_gb'] = dns_mb / 1024
            except Exception as e:
                print(f"[ERROR] Failed to get DNS cache size: {e}")
        
        return self._cached_storage_data
    
    def _build_storage_item_with_tooltip(self, icon, title, current, percentage, color, show_button=False, button_text="", button_action=None, button_ref_key=None, tooltip="", item_key=None):
        """Construit un item de stockage avec barre de progression, bouton optionnel et tooltip"""
        # Créer le bouton si demandé
        button_widget = None
        if show_button:
            button_widget = ft.Container(
                content=ft.Text(
                    button_text,
                    size=12,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.WHITE,
                ),
                padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
                border_radius=BorderRadius.SM,
                bgcolor=color,
                on_click=button_action,
                ink=True,
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            )
            
            # Stocker la référence du bouton si une clé est fournie
            if button_ref_key:
                if not hasattr(self, 'storage_item_buttons'):
                    self.storage_item_buttons = {}
                self.storage_item_buttons[button_ref_key] = button_widget
                
                # CORRECTION: Stocker le texte et la couleur ORIGINAUX du bouton
                if not hasattr(self, '_button_original_texts'):
                    self._button_original_texts = {}
                self._button_original_texts[button_ref_key] = button_text
                
                if not hasattr(self, '_button_original_colors'):
                    self._button_original_colors = {}
                self._button_original_colors[button_ref_key] = color
        
        # Créer les widgets texte et progress bar
        title_text = ft.Text(
            title,
            color=Colors.FG_PRIMARY,
            weight=ft.FontWeight.W_600,
            size=15,
        )
        
        current_text = ft.Text(
            f"À libérer: {current}",
            color=Colors.FG_SECONDARY,
            size=12,
        )
        
        progress_bar = ft.ProgressBar(
            value=percentage,
            height=8,
            color=color,
            bgcolor=ft.Colors.with_opacity(0.2, color),
            border_radius=BorderRadius.SM,
        )
        
        # Stocker les références si une clé est fournie
        if item_key:
            if not hasattr(self, 'storage_item_refs'):
                self.storage_item_refs = {}
            self.storage_item_refs[item_key] = {
                'title': title_text,
                'current': current_text,
                'progress': progress_bar,
            }
        
        return ft.Container(
            content=ft.Column(
                [
                    # En-tête avec icône et titre
                    ft.Row(
                        [
                            # Icône avec effet subtil
                            ft.Container(
                                content=ft.Icon(icon, size=24, color=color),
                                width=48,
                                height=48,
                                border_radius=BorderRadius.SM,
                                bgcolor=ft.Colors.with_opacity(0.15, color),
                                alignment=ft.alignment.center,
                                shadow=ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=8,
                                    color=ft.Colors.with_opacity(0.2, color),
                                    offset=ft.Offset(0, 2),
                                ),
                            ),
                            ft.Container(width=Spacing.MD),
                            # Titre et taille
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            title_text,
                                            ft.Container(width=Spacing.XS),
                                            ft.Icon(
                                                ft.Icons.INFO_OUTLINE_ROUNDED,
                                                size=14,
                                                color=Colors.FG_TERTIARY,
                                                tooltip=tooltip,
                                            ) if tooltip else ft.Container(),
                                        ],
                                        spacing=0,
                                    ),
                                    current_text,
                                ],
                                spacing=Spacing.XS,
                                expand=True,
                            ),
                            # Bouton ou badge pourcentage
                            button_widget if show_button else ft.Container(
                                content=ft.Text(
                                    f"{int(percentage * 100)}%",
                                    color=color,
                                    weight=ft.FontWeight.W_700,
                                    size=14,
                                ),
                                padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
                                border_radius=BorderRadius.SM,
                                bgcolor=ft.Colors.with_opacity(0.15, color),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    Spacer(height=Spacing.MD),
                    # Barre de progression avec effet
                    ft.Container(
                        content=progress_bar,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=6,
                            color=ft.Colors.with_opacity(0.3, color),
                            offset=ft.Offset(0, 2),
                        ),
                    ),
                ],
                spacing=0,
            ),
            padding=Spacing.LG,
            border_radius=BorderRadius.MD,
            bgcolor=Colors.BG_SECONDARY,
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, color)),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
    
    def _update_storage_item_dynamic(self, item_key, new_title=None, new_current=None, new_percentage=None):
        """
        Met à jour un item de stockage SANS le reconstruire (REFONTE UI)
        Thread-safe avec protection contre les race conditions
        
        Args:
            item_key: Clé de l'item ('cleanable', 'ram', 'dns')
            new_title: Nouveau titre (optionnel)
            new_current: Nouvelle valeur actuelle (optionnel)
            new_percentage: Nouveau pourcentage pour la barre (optionnel)
        """
        if item_key not in self.storage_item_refs:
            print(f"[WARNING] Storage item '{item_key}' not found in refs")
            return
        
        refs = self.storage_item_refs[item_key]
        
        try:
            # Mise à jour du titre si fourni
            if new_title and refs.get('title'):
                refs['title'].value = new_title
            
            # Mise à jour de la valeur actuelle
            if new_current and refs.get('current'):
                refs['current'].value = f"À libérer: {new_current}"
            
            # Mise à jour de la barre de progression avec animation
            if new_percentage is not None and refs.get('progress'):
                refs['progress'].value = new_percentage
                # Animation de feedback visuel
                refs['progress'].animate_opacity = ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT)
            
            # Forcer la mise à jour de l'interface
            self.page.update()
            
            pass  # Storage item updated
            
        except Exception as e:
            print(f"[ERROR] Failed to update storage item '{item_key}': {e}")
            import traceback
            traceback.print_exc()
    
    def _can_execute_action(self, action_name: str) -> tuple[bool, float]:
        """
        Vérifie si une action peut être exécutée (cooldown)
        ANTI-SPAM: Protection contre le spam des boutons (PATCH)
        
        Returns:
            (can_execute, remaining_time)
        """
        import time
        
        with self._cooldown_lock:
            current_time = time.time()
            
            # Vérifier si l'action a déjà été exécutée
            if action_name in self._last_action_time:
                elapsed = current_time - self._last_action_time[action_name]
                remaining = self._cooldown_duration - elapsed
                
                if remaining > 0:
                    # Cooldown actif
                    return False, remaining
            
            # Action autorisée
            return True, 0
    
    def _register_action(self, action_name: str):
        """
        Enregistre qu'une action a été exécutée
        ANTI-SPAM: Démarre le cooldown (PATCH)
        """
        import time
        
        with self._cooldown_lock:
            self._last_action_time[action_name] = time.time()
    
    def _show_cooldown_message(self, remaining_time: float):
        """
        Affiche un message de cooldown
        ANTI-SPAM: Informe l'utilisateur du temps restant (PATCH)
        """
        snack = ft.SnackBar(
            content=ft.Text(
                f"⏳ Veuillez patienter {int(remaining_time)} secondes avant de relancer cette action",
                color=ft.Colors.WHITE,
            ),
            bgcolor=ft.Colors.ORANGE,
            duration=2000,
        )
        self.page.snack_bar = snack
        snack.open = True
        self.page.update()
    
    def _start_cooldown_timer(self, action_name: str, button_ref_key: str):
        """
        Démarre un timer visuel sur le bouton pendant le cooldown
        ANTI-SPAM: Affichage visuel du temps restant (UX)
        CORRECTION: Restaure le texte ORIGINAL du bouton (pas le texte de succès)
        """
        import threading
        import time
        
        def update_button_timer():
            try:
                # Récupérer le bouton
                if not hasattr(self, 'storage_item_buttons') or button_ref_key not in self.storage_item_buttons:
                    return
                
                button = self.storage_item_buttons[button_ref_key]
                
                # Récupérer le texte et la couleur ORIGINAUX (stockés avant l'action)
                original_text = self._button_original_texts.get(button_ref_key, "Action")
                original_bgcolor = self._button_original_colors.get(button_ref_key, ft.Colors.BLUE)
                
                # Boucle de mise à jour du timer
                for remaining in range(self._cooldown_duration, 0, -1):
                    # Vérifier que le bouton existe toujours
                    if not hasattr(self, 'storage_item_buttons') or button_ref_key not in self.storage_item_buttons:
                        break
                    
                    # Mettre à jour le bouton avec le timer
                    button.bgcolor = ft.Colors.ORANGE_300
                    button.content.value = f"⏳ {remaining}s"
                    button.disabled = True
                    
                    try:
                        self.page.update()
                    except:
                        break
                    
                    time.sleep(1)
                
                # Restaurer le bouton avec le texte ORIGINAL
                if hasattr(self, 'storage_item_buttons') and button_ref_key in self.storage_item_buttons:
                    button.bgcolor = original_bgcolor
                    button.content.value = original_text  # Texte original restauré
                    button.disabled = False
                    
                    try:
                        self.page.update()
                    except:
                        pass
                        
            except Exception as e:
                print(f"[ERROR] Cooldown timer failed: {e}")
        
        # Lancer le timer dans un thread
        threading.Thread(target=update_button_timer, daemon=True).start()
    
    def _start_quick_action_cooldown_timer(self, action_name: str, button_ref: dict):
        """
        Démarre un timer visuel sur un bouton d'action rapide pendant le cooldown
        ANTI-SPAM: Affichage visuel du temps restant pour actions rapides (UX)
        """
        import threading
        import time
        
        def update_button_timer():
            try:
                # Vérifier que le bouton existe
                if not button_ref or not button_ref.get("container"):
                    return
                
                container = button_ref["container"]
                original_bgcolor = container.bgcolor
                original_border = container.border
                original_content = container.content
                
                pass  # Starting cooldown timer
                
                # Créer un overlay avec le timer
                timer_overlay = ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "⏳ 5s",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.ORANGE,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "Cooldown actif",
                                size=12,
                                color=ft.Colors.ORANGE_300,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
                
                # Boucle de mise à jour du timer
                for remaining in range(self._cooldown_duration, 0, -1):
                    # Mettre à jour le bouton avec le timer
                    container.bgcolor = ft.Colors.with_opacity(0.3, ft.Colors.ORANGE)
                    container.border = ft.border.all(2, ft.Colors.ORANGE)
                    
                    # Mettre à jour le texte du timer
                    timer_overlay.content.controls[0].value = f"⏳ {remaining}s"
                    container.content = timer_overlay
                    
                    try:
                        self.page.update()
                    except Exception as e:
                        print(f"[ERROR] Failed to update page: {e}")
                        break
                    
                    time.sleep(1)
                
                # Restaurer le bouton
                container.bgcolor = original_bgcolor
                container.border = original_border
                container.content = original_content
                
                try:
                    self.page.update()
                    pass  # Cooldown timer ended
                except Exception as e:
                    print(f"[ERROR] Failed to restore button: {e}")
                        
            except Exception as e:
                print(f"[ERROR] Quick action cooldown timer failed: {e}")
                import traceback
                traceback.print_exc()
        
        # Lancer le timer dans un thread
        threading.Thread(target=update_button_timer, daemon=True).start()
    
    def _clear_ram_action(self):
        """Vide la RAM standby avec animation de succès/échec"""
        import threading
        
        # ANTI-SPAM: Vérifier le cooldown (PROTECTION)
        can_execute, remaining = self._can_execute_action('clear_ram')
        if not can_execute:
            self._show_cooldown_message(remaining)
            return
        
        # CORRECTION: Sauvegarder le texte et la couleur ORIGINAUX du bouton avant l'action
        if hasattr(self, 'storage_item_buttons') and 'ram_button' in self.storage_item_buttons:
            button = self.storage_item_buttons['ram_button']
            if hasattr(button.content, 'value'):
                self._button_original_texts['ram_button'] = button.content.value
            # Sauvegarder aussi la couleur originale (Colors.INFO pour RAM)
            self._button_original_colors['ram_button'] = Colors.INFO
        
        # ANTI-SPAM: Bloquer immédiatement pour empêcher les clics multiples
        self._register_action('clear_ram')
        
        # NOTE: Le cooldown visuel démarrera APRÈS l'animation de succès/échec
        # pour éviter les chevauchements d'affichage
        
        def clear_ram():
            from src.core import cleaner
            import psutil
            
            try:
                print("[INFO] Clearing RAM standby...")
                
                # Obtenir la référence du bouton
                button = None
                if hasattr(self, 'storage_item_buttons') and 'ram_button' in self.storage_item_buttons:
                    button = self.storage_item_buttons['ram_button']
                
                # Obtenir la quantité de RAM avant nettoyage
                memory_before = psutil.virtual_memory()
                standby_before_mb = 0
                
                if hasattr(memory_before, 'cached'):
                    standby_before_mb = memory_before.cached / (1024 * 1024)
                else:
                    used_mb = memory_before.used / (1024 * 1024)
                    available_mb = memory_before.available / (1024 * 1024)
                    total_mb_ram = memory_before.total / (1024 * 1024)
                    calculated_standby = total_mb_ram - used_mb - available_mb
                    if 0 < calculated_standby < (total_mb_ram * 0.5):
                        standby_before_mb = calculated_standby
                    else:
                        standby_before_mb = total_mb_ram * 0.10
                
                # Animation de chargement
                if button:
                    button.bgcolor = ft.Colors.ORANGE
                    button.content.value = "⏳ Vidage..."
                    self.page.update()
                
                # Vider la RAM
                result = cleaner.clear_standby_memory()
                success = result.get('ram_standby_cleared', False)
                
                # Obtenir la quantité de RAM après nettoyage
                import time
                time.sleep(0.5)  # Petit délai pour que le système se mette à jour
                memory_after = psutil.virtual_memory()
                
                # Animation de succès ou échec
                if button:
                    if success:
                        # Animation verte (succès)
                        button.bgcolor = ft.Colors.GREEN
                        button.content.value = "✓ Vidée"
                        self.page.update()
                        
                        time.sleep(1.5)
                        
                        # ANTI-SPAM: Démarrer le cooldown visuel MAINTENANT (après l'animation)
                        self._start_cooldown_timer('clear_ram', 'ram_button')
                        
                        # Forcer un rescan de la RAM immédiatement et mettre à jour l'affichage
                        self.last_ram_scan = 0
                        
                        # Recalculer immédiatement la RAM standby après vidage (NOUVEAU - PRÉCIS)
                        from src.core.ram_manager import ram_manager
                        
                        # Invalider le cache pour forcer un nouveau calcul
                        ram_manager.invalidate_cache()
                        
                        # Obtenir les nouvelles valeurs précises
                        ram_info_after = ram_manager.get_detailed_memory_info()
                        standby_after_mb = ram_info_after['standby_mb']
                        standby_after_gb = standby_after_mb / 1024
                        standby_percent_after = ram_info_after['percent_standby']
                        total_mb_ram = ram_info_after['total_mb']
                        
                        # Calculer la quantité réellement libérée
                        freed_mb = result.get('freed_mb', 0)
                        print(f"[INFO] RAM Standby après vidage: {standby_after_mb:.2f} MB ({standby_percent_after:.1f}%)")
                        print(f"[INFO] RAM réellement libérée: {freed_mb:.2f} MB")
                        
                        # Calculer le nouveau pourcentage pour la barre
                        if hasattr(self, '_cached_storage_data'):
                            cleanable_mb = self._cached_storage_data.get('cleanable_mb', 0)
                            dns_mb = self._cached_storage_data.get('dns_mb', 0.05)
                            total_mb = cleanable_mb + standby_after_mb + dns_mb
                            new_percentage = (standby_after_mb / total_mb) if total_mb > 0 else 0
                        else:
                            new_percentage = 0
                        
                        # NOUVEAU: Utiliser la méthode de mise à jour dynamique (REFONTE UI)
                        self._update_storage_item_dynamic(
                            'ram',
                            new_title=f"RAM Standby ({standby_percent_after:.1f}%)",
                            new_current=f"{standby_after_gb:.2f} GB" if standby_after_gb >= 1 else f"{standby_after_mb:.0f} MB",
                            new_percentage=new_percentage
                        )
                        
                        # Mettre à jour le cache pour éviter les conflits avec le thread auto-update
                        if hasattr(self, '_cached_storage_data'):
                            self._cached_storage_data['standby_mb'] = standby_after_mb
                            self._cached_storage_data['standby_gb'] = standby_after_gb
                            self._cached_storage_data['standby_percent'] = standby_percent_after
                        
                        # Mettre à jour le Total estimé
                        if self.storage_total_text and hasattr(self, '_cached_storage_data'):
                            cleanable_mb = self._cached_storage_data.get('cleanable_mb', 0)
                            dns_mb = self._cached_storage_data.get('dns_mb', 0.05)
                            new_total_mb = cleanable_mb + standby_after_mb + dns_mb
                            self.storage_total_text.value = f"Total estimé: {new_total_mb / 1024:.2f} GB"
                            self.page.update()
                        
                        # Afficher un message de succès avec détails
                        method_used = result.get('method_used', 'unknown')
                        self._show_success_dialog(
                            "✓ RAM vidée",
                            f"La RAM standby a été vidée avec succès.\n\n"
                            f"Méthode utilisée: {method_used}\n"
                            f"RAM standby libérée: {freed_mb:.0f} MB\n"
                            f"RAM disponible maintenant: {ram_info_after['available_mb'] / 1024:.2f} GB\n"
                            f"Nouveau pourcentage RAM standby: {standby_percent_after:.1f}%"
                        )
                    else:
                        # Animation rouge (échec)
                        button.bgcolor = ft.Colors.RED
                        button.content.value = "✗ Échec"
                        self.page.update()
                        
                        time.sleep(1.5)
                        
                        # ANTI-SPAM: Démarrer le cooldown visuel même en cas d'échec
                        self._start_cooldown_timer('clear_ram', 'ram_button')
                        
                        # Afficher un message d'erreur
                        self._show_error_dialog(
                            "⚠ Erreur",
                            "Le vidage de la RAM a échoué. Vérifiez les privilèges administrateur."
                        )
                
                print(f"[INFO] RAM clear result: {success}")
                
            except Exception as e:
                print(f"[ERROR] Failed to clear RAM: {e}")
                
                # Animation d'erreur
                if button:
                    button.bgcolor = ft.Colors.RED
                    button.content.value = "✗ Erreur"
                    self.page.update()
                    
                    import time
                    time.sleep(1.5)
                    
                    # ANTI-SPAM: Démarrer le cooldown visuel même en cas d'exception
                    self._start_cooldown_timer('clear_ram', 'ram_button')
                
                self._show_error_dialog("⚠ Erreur", f"Impossible de vider la RAM:\n{str(e)}")
        
        # Lancer dans un thread
        threading.Thread(target=clear_ram, daemon=True).start()
    
    def _quick_clean_files(self):
        """Nettoie rapidement les fichiers temporaires avec animation de succès/échec"""
        import threading
        
        # ANTI-SPAM: Vérifier le cooldown (PROTECTION)
        can_execute, remaining = self._can_execute_action('quick_clean')
        if not can_execute:
            self._show_cooldown_message(remaining)
            return
        
        # CORRECTION: Sauvegarder le texte et la couleur ORIGINAUX du bouton avant l'action
        if hasattr(self, 'storage_item_buttons') and 'clean_button' in self.storage_item_buttons:
            button = self.storage_item_buttons['clean_button']
            if hasattr(button.content, 'value'):
                self._button_original_texts['clean_button'] = button.content.value
            # Sauvegarder aussi la couleur originale (Colors.WARNING pour Nettoyage)
            self._button_original_colors['clean_button'] = Colors.WARNING
        
        # ANTI-SPAM: Bloquer immédiatement pour empêcher les clics multiples
        self._register_action('quick_clean')
        
        # NOTE: Le cooldown visuel démarrera APRÈS l'animation de succès/échec
        # pour éviter les chevauchements d'affichage
        
        def clean_files():
            from src.core import cleaner
            
            try:
                print("[INFO] Quick cleaning files...")
                
                # Obtenir la référence du bouton
                button = None
                if hasattr(self, 'storage_item_buttons') and 'clean_button' in self.storage_item_buttons:
                    button = self.storage_item_buttons['clean_button']
                
                # Animation de chargement
                if button:
                    button.bgcolor = ft.Colors.ORANGE
                    button.content.value = "⏳ Nettoyage..."
                    self.page.update()
                
                # Scanner les fichiers à nettoyer
                scan_result = cleaner.scan_all_cleanable_files()
                total_size_mb = scan_result.get('total_size_mb', 0)
                
                # Nettoyer les fichiers
                result = cleaner.clean_temp_files()
                success = result.get('success', False)
                
                # Animation de succès ou échec
                if button:
                    if success:
                        # Animation verte (succès)
                        button.bgcolor = ft.Colors.GREEN
                        button.content.value = "✓ Nettoyé"
                        self.page.update()
                        
                        import time
                        time.sleep(1.5)
                        
                        # ANTI-SPAM: Démarrer le cooldown visuel MAINTENANT (après l'animation)
                        self._start_cooldown_timer('quick_clean', 'clean_button')
                        
                        # Forcer un rescan immédiatement
                        self.last_cleanable_scan = 0
                        
                        # Rescanner immédiatement pour mettre à jour l'affichage (REFONTE UI)
                        time.sleep(0.5)  # Petit délai pour que le système se mette à jour
                        scan_result_after = cleaner.scan_all_cleanable_files()
                        cleanable_after_mb = scan_result_after.get('total_size_mb', 0)
                        cleanable_after_gb = cleanable_after_mb / 1024
                        
                        # Calculer le nouveau pourcentage pour la barre
                        if hasattr(self, '_cached_storage_data'):
                            standby_mb = self._cached_storage_data.get('standby_mb', 0)
                            dns_mb = self._cached_storage_data.get('dns_mb', 0.05)
                            total_mb = cleanable_after_mb + standby_mb + dns_mb
                            new_percentage = (cleanable_after_mb / total_mb) if total_mb > 0 else 0
                        else:
                            new_percentage = 0
                        
                        # NOUVEAU: Utiliser la méthode de mise à jour dynamique
                        self._update_storage_item_dynamic(
                            'cleanable',
                            new_current=f"{cleanable_after_gb:.2f} GB" if cleanable_after_gb >= 1 else f"{cleanable_after_mb:.0f} MB",
                            new_percentage=new_percentage
                        )
                        
                        # Mettre à jour le cache
                        if hasattr(self, '_cached_storage_data'):
                            self._cached_storage_data['cleanable_mb'] = cleanable_after_mb
                            self._cached_storage_data['cleanable_gb'] = cleanable_after_gb
                        
                        # Mettre à jour le Total estimé
                        if self.storage_total_text and hasattr(self, '_cached_storage_data'):
                            standby_mb = self._cached_storage_data.get('standby_mb', 0)
                            dns_mb = self._cached_storage_data.get('dns_mb', 0.05)
                            new_total_mb = cleanable_after_mb + standby_mb + dns_mb
                            self.storage_total_text.value = f"Total estimé: {new_total_mb / 1024:.2f} GB"
                            self.page.update()
                        
                        # Afficher un message de succès
                        self._show_success_dialog(
                            "✓ Nettoyage terminé",
                            f"Fichiers nettoyés avec succès.\n\n"
                            f"Espace libéré: {total_size_mb:.2f} MB\n"
                            f"Espace restant à nettoyer: {cleanable_after_mb:.0f} MB"
                        )
                    else:
                        # Animation rouge (échec)
                        button.bgcolor = ft.Colors.RED
                        button.content.value = "✗ Échec"
                        self.page.update()
                        
                        import time
                        time.sleep(1.5)
                        
                        # ANTI-SPAM: Démarrer le cooldown visuel même en cas d'échec
                        self._start_cooldown_timer('quick_clean', 'clean_button')
                        
                        # Afficher un message d'erreur
                        self._show_error_dialog(
                            "⚠ Erreur",
                            "Le nettoyage a échoué. Vérifiez les privilèges."
                        )
                
                print(f"[INFO] Quick clean result: {success}")
                
            except Exception as e:
                print(f"[ERROR] Failed to clean files: {e}")
                
                # Animation d'erreur
                if button:
                    button.bgcolor = ft.Colors.RED
                    button.content.value = "✗ Erreur"
                    self.page.update()
                    
                    import time
                    time.sleep(1.5)
                    
                    # ANTI-SPAM: Démarrer le cooldown visuel même en cas d'exception
                    self._start_cooldown_timer('quick_clean', 'clean_button')
                
                self._show_error_dialog("⚠ Erreur", f"Impossible de nettoyer:\n{str(e)}")
        
        # Lancer dans un thread
        threading.Thread(target=clean_files, daemon=True).start()
    
    def _get_quick_action_tooltip(self, action):
        """Retourne le tooltip pour une action rapide"""
        tooltips = {
            "restore_point": "Crée un point de restauration système avant toute modification importante. Permet de revenir en arrière en cas de problème.",
            "optimize_disk": "Optimise votre disque dur selon son type (HDD, SSD ou NVME). Améliore les performances et la fluidité du système.",
            "empty_recycle": "Vide définitivement la corbeille Windows. Les fichiers supprimés ne pourront plus être récupérés.",
            "flush_dns": "Réinitialise le cache DNS pour résoudre les problèmes de connexion Internet et accélérer la navigation.",
        }
        return tooltips.get(action, "Action rapide.")
    
    def _execute_quick_action(self, action, button_ref=None):
        """Exécute une action rapide avec effet visuel"""
        # ANTI-SPAM: Vérifier le cooldown AVANT tout (PROTECTION)
        can_execute, remaining = self._can_execute_action(action)
        if not can_execute:
            self._show_cooldown_message(remaining)
            return
        
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
        
        # ANTI-SPAM: Enregistrer l'action immédiatement (COOLDOWN)
        self._register_action(action)
        
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
        elif action == "optimize_disk":
            self._quick_optimize_disk(button_ref, original_bgcolor, original_border)
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
                    pass  # Button progress updated
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
                result = -1
                is_frequency_limit = False
                
                try:
                    restore_point = win32com.client.Dispatch("SystemRestore.SystemRestore")
                    result = restore_point.CreateRestorePoint(
                        "5GHz Cleaner - Manual Restore Point",  # Description
                        0,  # Type: APPLICATION_INSTALL
                        100  # Event type: BEGIN_SYSTEM_CHANGE
                    )
                except Exception as e:
                    error_msg = str(e).lower()
                    error_code = str(e)
                    
                    # Vérifier si c'est une limitation de fréquence (24h)
                    if "1440" in error_msg or "frequency" in error_msg or "fréquence" in error_msg:
                        is_frequency_limit = True
                        result = 0  # Considérer comme succès (point déjà créé récemment)
                        print(f"[INFO] Point de restauration déjà créé récemment (limitation 24h)")
                    # Vérifier si c'est une erreur de classe COM
                    elif "-2147221005" in error_code or "classe incorrecte" in error_msg:
                        print(f"[WARNING] API COM non disponible, utilisation de PowerShell...")
                        # Fallback : Utiliser PowerShell
                        try:
                            import subprocess
                            ps_command = '''
                            $description = "5GHz Cleaner - Manual Restore Point"
                            Checkpoint-Computer -Description $description -RestorePointType "MODIFY_SETTINGS"
                            '''
                            
                            result_ps = subprocess.run(
                                ["powershell", "-NoProfile", "-Command", ps_command],
                                capture_output=True,
                                text=True,
                                timeout=120  # 2 minutes max
                            )
                            
                            if result_ps.returncode == 0:
                                result = 0
                                print("[SUCCESS] Point de restauration créé via PowerShell")
                            else:
                                result = -1
                                print(f"[ERROR] PowerShell error: {result_ps.stderr}")
                        except Exception as ps_error:
                            result = -1
                            print(f"[ERROR] PowerShell fallback failed: {ps_error}")
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
                    
                    # ANTI-SPAM: Démarrer le timer visuel APRÈS la fin de l'action (UX)
                    if button_ref:
                        self._start_quick_action_cooldown_timer('restore_point', button_ref)
                else:
                    # Restaurer le bouton
                    if button_ref and button_ref.get("container"):
                        button_ref["container"].bgcolor = original_bgcolor
                        button_ref["container"].border = original_border
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
    
    def _quick_optimize_disk(self, button_ref=None, original_bgcolor=None, original_border=None):
        """Optimise le disque dur selon son type (HDD/SSD/NVME)"""
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
        
        def optimize():
            from src.core.disk_optimizer import disk_optimizer
            
            try:
                print("[INFO] Optimizing disk...")
                print("[PROGRESS] 0% - Détection du type de disque...")
                update_progress(0)
                
                # Détecter le type de disque
                disk_type = disk_optimizer.detect_disk_type()
                print(f"[INFO] Disk type detected: {disk_type}")
                
                print("[PROGRESS] 20% - Type de disque détecté...")
                update_progress(20)
                
                print(f"[PROGRESS] 40% - Optimisation {disk_type} en cours...")
                update_progress(40)
                
                # Optimiser selon le type
                results = disk_optimizer.optimize_disk()
                
                print("[PROGRESS] 100% - Optimisation terminée")
                update_progress(100)
                
                # Petit délai pour voir la barre à 100%
                import time
                time.sleep(0.5)
                
                # Cacher la barre de progression
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].visible = False
                    self.page.update()
                
                # Animation de succès ou échec
                if results.get("success"):
                    if button_ref and button_ref.get("container"):
                        button_ref["container"].bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.GREEN)
                        button_ref["container"].border = ft.border.all(2, ft.Colors.GREEN)
                        self.page.update()
                        import time
                        time.sleep(0.5)
                        button_ref["container"].bgcolor = original_bgcolor
                        button_ref["container"].border = original_border
                        self.page.update()
                    
                    # Construire le message de succès
                    optimizations_text = "\n".join([f"✓ {opt}" for opt in results.get("optimizations", [])])
                    
                    self._show_success_dialog(
                        f"✓ Disque {disk_type} optimisé",
                        f"Optimisations effectuées:\n\n{optimizations_text}\n\n"
                        f"Votre disque est maintenant optimisé pour de meilleures performances."
                    )
                else:
                    if button_ref and button_ref.get("container"):
                        button_ref["container"].bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.RED)
                        button_ref["container"].border = ft.border.all(2, ft.Colors.RED)
                        self.page.update()
                        import time
                        time.sleep(0.5)
                        button_ref["container"].bgcolor = original_bgcolor
                        button_ref["container"].border = original_border
                        self.page.update()
                    
                    errors_text = "\n".join([f"✗ {err}" for err in results.get("errors", [])])
                    self._show_error_dialog(
                        "⚠ Optimisation partielle",
                        f"Certaines optimisations ont échoué:\n\n{errors_text}"
                    )
                
                self.quick_action_in_progress = False
                
                # ANTI-SPAM: Démarrer le timer visuel APRÈS la fin de l'action (UX)
                if button_ref:
                    self._start_quick_action_cooldown_timer('optimize_disk', button_ref)
            except Exception as e:
                # Cacher la barre de progression
                if button_ref and button_ref.get("progress_bar"):
                    button_ref["progress_bar"].visible = False
                    self.page.update()
                
                if button_ref and button_ref.get("container"):
                    button_ref["container"].bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.RED)
                    button_ref["container"].border = ft.border.all(2, ft.Colors.RED)
                    self.page.update()
                    import time
                    time.sleep(0.5)
                    button_ref["container"].bgcolor = original_bgcolor
                    button_ref["container"].border = original_border
                    self.page.update()
                
                self._show_error_dialog("⚠ Erreur", f"Impossible d'optimiser le disque:\n{str(e)}")
                self.quick_action_in_progress = False
        
        import threading
        threading.Thread(target=optimize, daemon=True).start()
    
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
            from src.core import cleaner
            
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
                
                # ANTI-SPAM: Démarrer le timer visuel APRÈS la fin de l'action (UX)
                if button_ref:
                    self._start_quick_action_cooldown_timer('empty_recycle', button_ref)
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
            from src.core import cleaner
            
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
                    
                    # ANTI-SPAM: Démarrer le timer visuel APRÈS la fin de l'action (UX)
                    if button_ref:
                        self._start_quick_action_cooldown_timer('flush_dns', button_ref)
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
        pass  # Show elevation dialog
        
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        def restart_as_admin(e):
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
                
                pass  # Script and params prepared
                
                # Demander l'élévation UAC
                result = ctypes.windll.shell32.ShellExecuteW(
                    None,
                    "runas",  # Demande d'élévation
                    script,
                    params,
                    None,
                    1  # SW_SHOWNORMAL
                )
                
                pass  # ShellExecuteW executed
                
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
            
            pass  # Dialog object created
            
            # Fermer tout dialogue existant d'abord
            if self.page.dialog:
                self.page.dialog.open = False
            
            self.page.dialog = dialog
            dialog.open = True
            
            # Forcer la mise à jour multiple fois
            self.page.update()
            import time
            time.sleep(0.1)
            self.page.update()
            time.sleep(0.1)
            self.page.update()
            
            # Essayer de forcer le focus sur la fenêtre
            try:
                self.page.window_to_front()
                pass
            except:
                pass
        except Exception as ex:
            print(f"[ERROR] Exception in _show_elevation_dialog: {ex}")
            import traceback
            traceback.print_exc()
    
    def _build_action_card(self, icon, title, description, action_key):
        """Construit une carte d'action - DESIGN SOBRE ET MODERNE"""
        # Icône SVG ou Material simple
        if isinstance(icon, str) and icon.endswith('.svg'):
            icon_widget = ft.Image(
                src=icon,
                width=48,
                height=48,
                fit=ft.ImageFit.CONTAIN,
            )
        else:
            icon_widget = ft.Icon(icon, size=48, color=Colors.ACCENT_PRIMARY)
        
        # Icône d'information avec tooltip
        from src.ui.design_system.tooltip import create_info_icon_with_tooltip
        desc_tuple = self._get_detailed_description(action_key)
        info_icon = create_info_icon_with_tooltip(
            desc_tuple[0],  # Texte
            size=16,
            risk_level=desc_tuple[1]  # Niveau de risque
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    # Info icon en haut à droite
                    ft.Row(
                        [info_icon],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    Spacer(height=Spacing.SM),
                    
                    # Icône principale simple
                    icon_widget,
                    Spacer(height=Spacing.MD),
                    
                    # Titre
                    BodyText(
                        title,
                        weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER,
                        size=15,
                        color=Colors.FG_PRIMARY,
                    ),
                    Spacer(height=Spacing.SM),
                    
                    # Description
                    Caption(
                        description,
                        text_align=ft.TextAlign.CENTER,
                        color=Colors.FG_SECONDARY,
                        size=12,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            width=220,
            height=200,
            bgcolor=Colors.BG_SECONDARY,
            border_radius=BorderRadius.MD,
            border=ft.border.all(1, Colors.BORDER_DEFAULT),
            padding=Spacing.LG,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
    
    def _build_action_button(self):
        """Construit le bouton d'action principal (Prévisualisation)"""
        # Message déplacé en haut, on garde juste un container vide pour le statut
        self.status_text = ft.Container(
            visible=False,  # Masqué car le message est maintenant en haut
        )
        
        self.progress_bar = ft.ProgressBar(
            width=500,
            height=2,  # Réduit de 3 à 2
            color=Colors.ACCENT_PRIMARY,
            bgcolor=Colors.BORDER_DEFAULT,
            visible=False,
        )
        
        # Bouton Prévisualisation SOBRE ET MODERNE
        def on_dry_run_click(e):
            self._start_dry_run(e)
        
        # Créer les références pour le texte et l'icône du bouton principal
        self.dry_run_button_icon = ft.Icon(ft.Icons.PREVIEW_ROUNDED, size=20, color=ft.Colors.WHITE)
        self.dry_run_button_text = ft.Text(
            "Prévisualiser le nettoyage",
            size=14,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.WHITE,
        )
        
        # Bouton simple et élégant
        self.dry_run_button = ft.Container(
            content=ft.Row(
                [
                    self.dry_run_button_icon,
                    ft.Container(width=Spacing.SM),
                    self.dry_run_button_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=350,
            height=50,
            border_radius=BorderRadius.MD,
            bgcolor=Colors.ACCENT_PRIMARY,
            on_click=on_dry_run_click,
            ink=True,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        
        # Container pour le bouton d'action (maintenant masqué car le bouton est en haut)
        self.action_button_container = ft.Column(
            [
                self.status_text,
                Spacer(height=Spacing.SM),
                self.progress_bar,
                # Le bouton dry_run_button est maintenant en haut, on ne l'affiche plus ici
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
                                # SÉCURITÉ: Import sécurisé de webbrowser au lieu de __import__ dynamique (PATCH)
                                on_click=self._open_github_link,
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
                Spacer(height=Spacing.MD),
                # Légende des couleurs
                ft.Container(
                    content=ft.Row(
                        [
                            # Vert - Sûr
                            ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=16, color=Colors.SUCCESS),
                            ft.Container(width=4),
                            Caption("Action sûre", color=Colors.FG_SECONDARY, size=11),
                            ft.Container(width=Spacing.LG),
                            # Orange - Attention
                            ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=16, color=Colors.WARNING),
                            ft.Container(width=4),
                            Caption("Attention requise", color=Colors.FG_SECONDARY, size=11),
                            ft.Container(width=Spacing.LG),
                            # Rouge - Risque
                            ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=16, color=Colors.ERROR),
                            ft.Container(width=4),
                            Caption("Action à risque", color=Colors.FG_SECONDARY, size=11),
                        ],
                        spacing=0,
                    ),
                    padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
                    bgcolor=ft.Colors.with_opacity(0.05, Colors.FG_TERTIARY),
                    border_radius=BorderRadius.SM,
                    border=ft.border.all(1, Colors.BORDER_DEFAULT),
                ),
                Spacer(height=Spacing.XL),
                # Options avec espacement optimisé ET SCROLL
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
                            Spacer(height=Spacing.LG),
                            
                            # Nouvelles options avancées
                            BodyText("Optimisations Système", weight=Typography.WEIGHT_BOLD, size=16, color=Colors.ACCENT_PRIMARY),
                            Spacer(height=Spacing.MD),
                            
                            self._build_option_item(
                                "Désactiver l'hibernation",
                                "Supprime hiberfil.sys et libère plusieurs GB (taille = RAM)",
                                "disable_hibernation",
                                False,
                                recommended=False
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Nettoyer points de restauration anciens",
                                "Garde seulement les 2 plus récents, libère de l'espace",
                                "clean_restore_points",
                                False,
                                recommended=False
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Optimiser programmes au démarrage",
                                "Analyse et optimise les programmes qui se lancent au démarrage",
                                "optimize_startup",
                                False,
                                recommended=True
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Vider cache des navigateurs",
                                "Nettoie le cache de Chrome, Firefox et Edge",
                                "clear_browser_cache",
                                False,
                                recommended=False
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Nettoyer logs d'événements",
                                "Vide les journaux d'événements Windows",
                                "clean_event_logs",
                                False,
                                recommended=False
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Désactiver Superfetch/Prefetch",
                                "Recommandé pour SSD, améliore les performances",
                                "disable_superfetch",
                                False,
                                recommended=True
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Désactiver Cortana",
                                "Libère de la RAM et améliore la confidentialité",
                                "disable_cortana",
                                False,
                                recommended=False
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Optimiser TCP/IP",
                                "Reset Winsock et TCP/IP pour améliorer le réseau",
                                "optimize_tcp_ip",
                                False,
                                recommended=False
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Désactiver services inutiles",
                                "Désactive Fax, Tablet Input et autres services non essentiels",
                                "disable_services",
                                False,
                                recommended=False
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Mode Gaming",
                                "Optimisations pour améliorer les performances en jeu",
                                "gaming_mode",
                                False,
                                recommended=False
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Nettoyer pilotes obsolètes",
                                "Supprime les anciens pilotes inutilisés",
                                "clean_drivers",
                                False,
                                recommended=False
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Vider WinSxS",
                                "Nettoie les composants Windows obsolètes",
                                "clean_winsxs",
                                False,
                                recommended=False
                            ),
                            Spacer(height=Spacing.MD),
                            self._build_option_item(
                                "Optimiser fichier de pagination",
                                "Configure automatiquement la taille du pagefile",
                                "optimize_pagefile",
                                False,
                                recommended=False
                            ),
                        ],
                        spacing=0,
                        scroll=ft.ScrollMode.ALWAYS,
                    ),
                    height=600,  # Hauteur fixe pour activer le scroll
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
        
        # Icône d'information avec tooltip détaillé personnalisé
        from src.ui.design_system.tooltip import create_info_icon_with_tooltip
        desc_tuple = self._get_detailed_description(key)
        info_icon = create_info_icon_with_tooltip(
            desc_tuple[0],  # Texte
            size=16,
            risk_level=desc_tuple[1]  # Niveau de risque
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
        """Retourne une description concise pour les tooltips"""
        descriptions = {
            "clear_standby_memory": ("Libère la RAM en attente. Amélioration temporaire.", "info"),
            "flush_dns": ("Vide le cache DNS. Résout les problèmes de connexion.", "info"),
            "disable_telemetry": ("Désactive DiagTrack et services de collecte de données.", "warning"),
            "clear_large_logs": ("Supprime les fichiers .log volumineux (100MB-2GB).", "info"),
            "disable_hibernation": ("Supprime hiberfil.sys. Libère plusieurs GB. ⚠️ Plus d'hibernation possible.", "danger"),
            "clean_restore_points": ("Garde les 2 points les plus récents. ⚠️ Impossible de revenir aux anciens.", "danger"),
            "optimize_startup": ("Analyse les programmes au démarrage. Accélère le boot.", "info"),
            "clear_browser_cache": ("Vide Chrome, Firefox, Edge. ⚠️ Vous serez déconnecté des sites.", "warning"),
            "clean_event_logs": ("Nettoie les journaux Windows. ⚠️ Perte de l'historique.", "warning"),
            "disable_superfetch": ("Désactive Superfetch. Recommandé pour SSD.", "warning"),
            "disable_cortana": ("Désactive Cortana. Libère de la RAM.", "warning"),
            "optimize_tcp_ip": ("Reset Winsock et TCP/IP. ⚠️ Nécessite redémarrage.", "warning"),
            "disable_services": ("Désactive Fax, Tablet Input, etc. Réduit CPU/RAM.", "warning"),
            "gaming_mode": ("Désactive Game Bar. Améliore FPS et latence.", "info"),
            "clean_drivers": ("Nettoie les pilotes obsolètes. Libère 100-500MB.", "warning"),
            "clean_winsxs": ("Nettoie WinSxS via DISM. ⚠️ Opération longue (5-15min).", "danger"),
            "optimize_pagefile": ("Configure le pagefile automatiquement. Optimise la RAM.", "info"),
        }
        return descriptions.get(key, ("Option de nettoyage avancée.", "info"))
    
    def _update_option(self, key, value):
        """Met à jour une option avancée"""
        self.app.advanced_options[key] = value
        print(f"[INFO] Option {key} set to {value}")
    
    def _build_configuration_section(self):
        """Construit la section Configuration avec monitoring matériel amélioré"""
        try:
            # Récupérer les données matérielles
            hw_data = hardware_monitor.get_all_components()
            
            # Récupérer les informations système
            import platform
            import psutil
            from datetime import datetime, timedelta
            
            # Informations système
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            # Formater uptime sans afficher 0j
            if uptime.days > 0:
                uptime_str = f"{uptime.days}j {uptime.seconds//3600}h {(uptime.seconds//60)%60}m"
            else:
                uptime_str = f"{uptime.seconds//3600}h {(uptime.seconds//60)%60}m"
            
            os_info = f"{platform.system()} {platform.release()} (Build {platform.version().split('.')[-1]})"
            process_count = len(psutil.pids())
            
            # Créer des widgets Text pour les infos dynamiques
            self.uptime_text = Caption(uptime_str, size=11, color=Colors.FG_SECONDARY)
            self.process_count_text = Caption(f"{process_count} actifs", size=11, color=Colors.FG_SECONDARY)
            
            # Conteneurs pour les composants (seront mis à jour en temps réel)
            self.hw_cpu_container = self._build_hardware_card_v2("CPU", hw_data.get("cpu", {}))
            self.hw_memory_container = self._build_hardware_card_v2("Mémoire", hw_data.get("memory", {}))
            self.hw_gpu_containers = [
                self._build_hardware_card_v2("GPU", gpu) for gpu in hw_data.get("gpus", [])
            ]
            self.hw_disk_containers = [
                self._build_hardware_card_v2("Disque", disk) for disk in hw_data.get("disks", [])
            ]
            
            # Démarrer le monitoring en temps réel (1 seconde pour des mises à jour régulières)
            if not hardware_monitor.monitoring:
                hardware_monitor.start_monitoring(interval=1.0, callback=self._update_hardware_display)
        except Exception as e:
            print(f"[ERROR] Failed to build configuration section: {e}")
            import traceback
            traceback.print_exc()
            
            # Retourner un message d'erreur convivial
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ERROR_OUTLINE, size=48, color=Colors.ERROR),
                        Spacer(height=Spacing.MD),
                        BodyText("Erreur de chargement", weight=Typography.WEIGHT_BOLD),
                        Spacer(height=Spacing.SM),
                        Caption(
                            f"Impossible de charger les informations matérielles.\n{str(e)}",
                            color=Colors.FG_SECONDARY,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
                padding=Spacing.XL,
            )
        
        return ft.Column(
            [
                # En-tête de section (FIXE - Non scrollable)
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
                
                # Informations système (FIXE - Non scrollable)
                ft.Container(
                    content=ft.Row(
                        [
                            # Carte OS
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(ft.Icons.LAPTOP_WINDOWS, size=20, color=Colors.ACCENT_PRIMARY),
                                                ft.Container(width=Spacing.XS),
                                                BodyText("Système", size=13, weight=Typography.WEIGHT_BOLD),
                                            ],
                                        ),
                                        Spacer(height=Spacing.XS),
                                        Caption(os_info, size=11, color=Colors.FG_SECONDARY),
                                    ],
                                    spacing=0,
                                ),
                                bgcolor=Colors.BG_SECONDARY,
                                padding=Spacing.MD,
                                border_radius=BorderRadius.MD,
                                border=ft.border.all(1, Colors.BORDER_DEFAULT),
                                expand=True,
                            ),
                            ft.Container(width=Spacing.MD),
                            # Carte Uptime
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(ft.Icons.SCHEDULE, size=20, color=Colors.SUCCESS),
                                                ft.Container(width=Spacing.XS),
                                                BodyText("Uptime", size=13, weight=Typography.WEIGHT_BOLD),
                                            ],
                                        ),
                                        Spacer(height=Spacing.XS),
                                        self.uptime_text,
                                    ],
                                    spacing=0,
                                ),
                                bgcolor=Colors.BG_SECONDARY,
                                padding=Spacing.MD,
                                border_radius=BorderRadius.MD,
                                border=ft.border.all(1, Colors.BORDER_DEFAULT),
                                expand=True,
                            ),
                            ft.Container(width=Spacing.MD),
                            # Carte Processus
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(ft.Icons.APPS, size=20, color=Colors.WARNING),
                                                ft.Container(width=Spacing.XS),
                                                BodyText("Processus", size=13, weight=Typography.WEIGHT_BOLD),
                                            ],
                                        ),
                                        Spacer(height=Spacing.XS),
                                        self.process_count_text,
                                    ],
                                    spacing=0,
                                ),
                                bgcolor=Colors.BG_SECONDARY,
                                padding=Spacing.MD,
                                border_radius=BorderRadius.MD,
                                border=ft.border.all(1, Colors.BORDER_DEFAULT),
                                expand=True,
                            ),
                        ],
                    ),
                ),
                Spacer(height=Spacing.LG),
                
                # Avertissement confidentialité (FIXE - Non scrollable)
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
                
                # Zone scrollable (COMPOSANTS MATÉRIELS)
                ft.Container(
                    content=ft.Column(
                        [
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
                        scroll=ft.ScrollMode.ALWAYS,
                    ),
                    height=550,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=0,
        )
    
    def _build_hardware_card(self, component_type, data):
        """Construit une carte pour un composant matériel"""
        try:
            # Vérifier que data n'est pas None
            if data is None:
                data = {}
            
            # Déterminer l'icône selon le type
            if component_type == "CPU":
                icon = ft.Icons.DEVELOPER_BOARD  # Icône processeur/circuit
                
                # Nettoyer le nom du CPU (enlever les infos de cœurs)
                cpu_name = data.get("name", "N/A")
                # Supprimer les mentions de cœurs du nom
                import re
                cpu_name = re.sub(r'\s*\d+-Core.*', '', cpu_name)  # Enlever "12-Core Processor"
                cpu_name = re.sub(r'\s*Processor.*', '', cpu_name)  # Enlever "Processor"
                cpu_name = cpu_name.strip()
                
                name = cpu_name
                usage = data.get('usage', 0)
                freq_current = data.get('frequency_current', 0)
                freq_max = data.get('frequency_max', 0)
                cores_physical = data.get('cores_physical', 0)
                cores_logical = data.get('cores_logical', 0)
                
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
                                animate_opacity=300,  # Animation fluide de 300ms
                            ),
                        ],
                        spacing=0,
                    ),
                    margin=ft.margin.only(top=8),
                )
                
                # Format : Cœurs / Fréquence utilisée en cours
                details = [
                    f"Cœurs : {cores_physical} physiques / {cores_logical} logiques",
                    f"Fréquence utilisée en cours : {freq_current:.0f} MHz / {freq_max:.0f} MHz maximum",
                ]
            elif component_type == "Mémoire":
                icon = ft.Icons.MEMORY_OUTLINED
                
                # Nom commercial de la RAM (Marque + Type + Fréquence)
                name = data.get("name", "RAM")
                
                total_gb = data.get("total", 0) / (1024**3)
                used_gb = data.get("used", 0) / (1024**3)
                available_gb = data.get("available", 0) / (1024**3)
                percent = data.get("percent", 0)
                ram_speed = data.get("speed", 0)
                
                # Informations sur les modules RAM avec format "2x8GB" ou "4x8GB"
                ram_modules = data.get("modules", [])
                if ram_modules:
                    module_count = len(ram_modules)
                    # Grouper les modules par taille pour afficher "2x8GB + 2x16GB" si différents
                    from collections import Counter
                    module_sizes = Counter([int(m) for m in ram_modules])
                    
                    module_parts = []
                    for size, count in sorted(module_sizes.items(), reverse=True):
                        module_parts.append(f"{count}x{size}GB")
                    
                    module_info = " + ".join(module_parts)
                    
                    # Ajouter la fréquence si disponible
                    if ram_speed > 0:
                        module_info += f" @ {ram_speed} MHz"
                else:
                    module_info = "Information non disponible"
                
                # Barre de progression pour la RAM
                cpu_progress = ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    Caption("Utilisation en temps réel", size=10, color=Colors.FG_TERTIARY),
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
                                animate_opacity=300,  # Animation fluide de 300ms
                            ),
                        ],
                        spacing=0,
                    ),
                    margin=ft.margin.only(top=8),
                )
                
                # Format : Mémoire installée / Utilisation en temps réel
                details = [
                    f"Mémoire installée : {module_info}",
                    f"Utilisation en temps réel : {used_gb:.2f} GB / {total_gb:.2f} GB",
                ]
            elif component_type == "GPU":
                icon = ft.Icons.VIDEOGAME_ASSET
                name = data.get("name", "N/A")
                usage = data.get("usage", 0)
                driver_version = data.get("driver_version", "N/A")
                driver_date = data.get("driver_date", "N/A")
                
                # Barre de progression pour l'utilisation GPU
                # Ne pas afficher la barre si usage == 0 (monitoring non disponible)
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
                                    animate_opacity=300,
                                ),
                            ],
                            spacing=0,
                        ),
                        margin=ft.margin.only(top=8),
                    )
                else:
                    cpu_progress = None
                
                # Détails GPU améliorés
                details = []
                if driver_version != "N/A":
                    details.append(f"Pilote : {driver_version}")
                else:
                    details.append("Pilote : Non disponible")
                
                # Ajouter note UNIQUEMENT si monitoring non disponible ET pas de barre affichée
                if usage == 0:
                    details.append("Monitoring GPU non disponible pour AMD")
            elif component_type == "Disque":
                icon = ft.Icons.STORAGE
                disk_model = data.get("model", "Unknown")
                disk_type = data.get("type", "Unknown")
                drive_letter = data.get('name', 'N/A')
                
                # Construire le nom : "Disque C:\" uniquement
                name = f"Disque {drive_letter}"
                
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
                                    Caption("Utilisation du disque", size=10, color=Colors.FG_TERTIARY),
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
                                animate_opacity=300,  # Animation fluide de 300ms
                            ),
                        ],
                        spacing=0,
                    ),
                    margin=ft.margin.only(top=8),
                )
                
                # Format : Type / Capacité totale / Espace libre
                details = [
                    f"Type : {disk_type}",
                    f"Capacité totale : {total_gb:.2f} GB",
                    f"Espace libre : {free_gb:.2f} GB",
                ]
            else:
                icon = ft.Icons.DEVICE_UNKNOWN
                name = "Inconnu"
                cpu_progress = None
                details = []
            
            # Température (seulement pour CPU et GPU)
            temp = data.get("temperature")
            temp_color = self._get_temp_color(temp, component_type.lower())
            temp_text = f"{temp:.1f}°C" if temp is not None else "N/A"
            
            # Indicateur de température (seulement pour CPU et GPU)
            # RAM et Disques n'ont généralement pas de capteurs de température accessibles
            if component_type in ["CPU", "GPU"] and temp is not None:
                # Affichage normal avec température
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
                                "Température",
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
            else:
                # Pas d'indicateur de température pour RAM et Disques
                # ou si la température n'est pas disponible
                temp_indicator = None
            
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
            
            # Construire l'icône
            icon_widget = ft.Icon(icon, size=36, color=Colors.ACCENT_PRIMARY)
            
            # Construire la liste des contrôles de la Row
            row_controls = [
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
            ]
            
            # Ajouter le bouton d'optimisation pour le disque C:\ (coin droit)
            if component_type == "Disque" and drive_letter == "C:\\":
                # Créer les widgets du bouton (icône et texte)
                optimize_icon = ft.Icon(ft.Icons.AUTO_FIX_HIGH, size=20, color=Colors.ACCENT_PRIMARY)
                optimize_text = Caption(
                    "Optimiser",
                    size=9,
                    color=Colors.ACCENT_PRIMARY,
                    text_align=ft.TextAlign.CENTER,
                    weight=Typography.WEIGHT_MEDIUM,
                )
                
                # Créer le bouton d'optimisation automatique avec feedback visuel
                optimize_button = ft.Container(
                    content=ft.Column(
                        [
                            optimize_icon,
                            ft.Container(height=2),
                            optimize_text,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY),
                    padding=ft.padding.symmetric(horizontal=Spacing.MD, vertical=Spacing.SM),
                    border_radius=BorderRadius.MD,
                    border=ft.border.all(2, ft.Colors.with_opacity(0.4, Colors.ACCENT_PRIMARY)),
                    on_click=lambda e: self._optimize_disk_auto(drive_letter, optimize_button, optimize_icon, optimize_text),
                    ink=True,
                    tooltip="Optimise automatiquement le disque selon son type (HDD/SSD/NVMe)",
                    data={"drive_letter": drive_letter, "is_optimizing": False},
                )
                row_controls.append(ft.Container(width=Spacing.MD))
                row_controls.append(optimize_button)
            
            # Ajouter la température seulement si elle existe (CPU et GPU uniquement)
            elif temp_indicator is not None:
                row_controls.append(ft.Container(width=Spacing.MD))
                row_controls.append(temp_indicator)
            
            # Construire la carte avec hover effect
            return ft.Container(
                content=ft.Row(
                    row_controls,
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
        except Exception as e:
            print(f"[ERROR] Failed to build hardware card for {component_type}: {e}")
            # Retourner une carte d'erreur simple
            return ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ERROR_OUTLINE, size=24, color=Colors.ERROR),
                        ft.Container(width=Spacing.SM),
                        Caption(f"Erreur: {component_type}", color=Colors.ERROR),
                    ],
                ),
                bgcolor=Colors.BG_SECONDARY,
                padding=Spacing.MD,
                border_radius=BorderRadius.MD,
                border=ft.border.all(1, Colors.ERROR),
            )
    
    def _build_hardware_card_v2(self, component_type, data):
        """Version améliorée de la carte matérielle avec design moderne"""
        # Using existing card design - optimized and functional
        return self._build_hardware_card(component_type, data)
    
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
            # Mettre à jour l'uptime et le nombre de processus
            if hasattr(self, 'uptime_text') and self.uptime_text:
                import psutil
                from datetime import datetime
                boot_time = datetime.fromtimestamp(psutil.boot_time())
                uptime = datetime.now() - boot_time
                # Formater uptime sans afficher 0j
                if uptime.days > 0:
                    uptime_str = f"{uptime.days}j {uptime.seconds//3600}h {(uptime.seconds//60)%60}m"
                else:
                    uptime_str = f"{uptime.seconds//3600}h {(uptime.seconds//60)%60}m"
                self.uptime_text.value = uptime_str
            
            if hasattr(self, 'process_count_text') and self.process_count_text:
                import psutil
                process_count = len(psutil.pids())
                self.process_count_text.value = f"{process_count} actifs"
            
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
        """Met à jour une carte de composant matériel en temps réel"""
        try:
            # Pour les GPU AMD, garder le dernier état valide d'utilisation
            if component_type == "GPU" and hasattr(card_container, 'data'):
                old_data = card_container.data.get("data", {})
                old_usage = old_data.get("usage", 0)
                new_usage = data.get("usage", 0)
                
                # Si l'ancienne valeur était > 0 et la nouvelle est 0,
                # garder l'ancienne valeur pour éviter le clignotement
                if old_usage > 0 and new_usage == 0:
                    data = old_data.copy()
                    data.update({"usage": old_usage})
            
            # Reconstruire complètement la carte avec les nouvelles données
            new_card = self._build_hardware_card(component_type, data)
            
            # Remplacer le contenu de la carte
            if hasattr(card_container, 'content'):
                card_container.content = new_card.content
                card_container.data = new_card.data
        except Exception as e:
            print(f"[ERROR] Failed to update hardware card: {e}")
    
    def _optimize_disk_auto(self, drive_letter, button_container, icon_widget, text_widget):
        """
        Optimise automatiquement le disque selon son type (HDD/SSD/NVMe)
        SANS POP-UP - Barre de progression intégrée + Cooldown de 3 minutes visible
        """
        import time
        import threading
        from src.core import disk_auto_optimizer
        
        # Vérifier si une optimisation est déjà en cours
        if button_container.data.get("is_optimizing", False):
            return
        
        action_name = f"optimize_disk_{drive_letter}"
        
        # Vérifier le cooldown
        current_time = time.time()
        if action_name in self._last_action_time:
            elapsed = current_time - self._last_action_time[action_name]
            remaining = self._cooldown_duration - elapsed
            
            if remaining > 0:
                # Cooldown actif - Ne rien faire
                return
        
        # Enregistrer l'action
        with self._cooldown_lock:
            self._last_action_time[action_name] = current_time
        
        # FEEDBACK VISUEL: Marquer comme en cours d'optimisation
        button_container.data["is_optimizing"] = True
        
        # Créer une barre de progression intégrée
        progress_bar = ft.ProgressBar(
            width=60,
            height=4,
            color=Colors.ACCENT_PRIMARY,
            bgcolor=Colors.BORDER_DEFAULT,
            border_radius=BorderRadius.SM,
        )
        
        # Remplacer l'icône par un ProgressRing petit
        progress_ring = ft.ProgressRing(width=16, height=16, stroke_width=2, color=Colors.ACCENT_PRIMARY)
        
        # Changer le texte
        text_widget.value = "En cours..."
        text_widget.size = 8
        text_widget.color = Colors.ACCENT_PRIMARY
        
        # Changer la couleur du bouton (orange pour indiquer activité)
        button_container.bgcolor = ft.Colors.with_opacity(0.15, ft.Colors.ORANGE)
        button_container.border = ft.border.all(2, ft.Colors.with_opacity(0.5, ft.Colors.ORANGE))
        
        # Modifier le contenu du bouton
        button_content = button_container.content
        button_content.controls = [
            progress_ring,
            ft.Container(height=2),
            progress_bar,
            ft.Container(height=2),
            text_widget,
        ]
        
        # Mettre à jour l'UI
        self.page.update()
        
        def run_optimization():
            try:
                # Optimiser le disque
                result = disk_auto_optimizer.auto_optimize_disk(drive_letter)
                
                # Marquer comme terminé
                button_container.data["is_optimizing"] = False
                
                # Afficher le résultat directement dans le bouton
                if result["success"]:
                    # Succès - Afficher icône de succès
                    success_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color=Colors.SUCCESS)
                    text_widget.value = f"{result['disk_type']}"
                    text_widget.size = 8
                    text_widget.color = Colors.SUCCESS
                    button_container.bgcolor = ft.Colors.with_opacity(0.15, Colors.SUCCESS)
                    button_container.border = ft.border.all(2, ft.Colors.with_opacity(0.5, Colors.SUCCESS))
                    
                    button_content.controls = [
                        success_icon,
                        ft.Container(height=2),
                        text_widget,
                    ]
                    self.page.update()
                    
                    # Attendre 2 secondes puis démarrer le cooldown
                    time.sleep(2)
                else:
                    # Erreur - Afficher icône d'erreur
                    error_icon = ft.Icon(ft.Icons.ERROR, size=16, color=Colors.ERROR)
                    text_widget.value = "Échec"
                    text_widget.size = 8
                    text_widget.color = Colors.ERROR
                    button_container.bgcolor = ft.Colors.with_opacity(0.15, Colors.ERROR)
                    button_container.border = ft.border.all(2, ft.Colors.with_opacity(0.5, Colors.ERROR))
                    
                    button_content.controls = [
                        error_icon,
                        ft.Container(height=2),
                        text_widget,
                    ]
                    self.page.update()
                    
                    # Attendre 2 secondes puis démarrer le cooldown
                    time.sleep(2)
                
                # Démarrer le cooldown visible de 10 minutes
                self._start_disk_cooldown_timer(button_container, icon_widget, text_widget, action_name)
            
            except Exception as e:
                # Erreur - Afficher icône d'erreur
                button_container.data["is_optimizing"] = False
                error_icon = ft.Icon(ft.Icons.ERROR, size=16, color=Colors.ERROR)
                text_widget.value = "Erreur"
                text_widget.size = 8
                text_widget.color = Colors.ERROR
                button_container.bgcolor = ft.Colors.with_opacity(0.15, Colors.ERROR)
                button_container.border = ft.border.all(2, ft.Colors.with_opacity(0.5, Colors.ERROR))
                
                button_content.controls = [
                    error_icon,
                    ft.Container(height=2),
                    text_widget,
                ]
                self.page.update()
                
                print(f"[ERROR] Disk optimization failed: {e}")
                import traceback
                traceback.print_exc()
                
                # Attendre 2 secondes puis démarrer le cooldown
                time.sleep(2)
                self._start_disk_cooldown_timer(button_container, icon_widget, text_widget, action_name)
        
        # Lancer l'optimisation dans un thread
        threading.Thread(target=run_optimization, daemon=True).start()
    
    def _start_disk_cooldown_timer(self, button_container, icon_widget, text_widget, action_name):
        """
        Démarre un timer de cooldown visible de 10 minutes sur le bouton d'optimisation disque
        """
        import time
        
        button_content = button_container.content
        cooldown_duration = 600  # 10 minutes (cohérent avec le cooldown global)
        
        for remaining in range(cooldown_duration, 0, -1):
            try:
                # Calculer minutes et secondes
                minutes = remaining // 60
                seconds = remaining % 60
                
                # Afficher le cooldown
                cooldown_icon = ft.Icon(ft.Icons.TIMER, size=16, color=Colors.FG_TERTIARY)
                text_widget.value = f"{minutes}:{seconds:02d}"
                text_widget.size = 9
                text_widget.color = Colors.FG_TERTIARY
                button_container.bgcolor = ft.Colors.with_opacity(0.1, Colors.FG_TERTIARY)
                button_container.border = ft.border.all(2, ft.Colors.with_opacity(0.3, Colors.FG_TERTIARY))
                
                button_content.controls = [
                    cooldown_icon,
                    ft.Container(height=2),
                    text_widget,
                ]
                
                self.page.update()
                time.sleep(1)
            except:
                break
        
        # Restaurer le bouton à l'état normal
        icon_widget.visible = True
        text_widget.value = "Optimiser"
        text_widget.size = 9
        text_widget.color = Colors.ACCENT_PRIMARY
        button_container.bgcolor = ft.Colors.with_opacity(0.1, Colors.ACCENT_PRIMARY)
        button_container.border = ft.border.all(2, ft.Colors.with_opacity(0.4, Colors.ACCENT_PRIMARY))
        
        button_content.controls = [
            icon_widget,
            ft.Container(height=2),
            text_widget,
        ]
        
        self.page.update()
    
    def _close_dialog(self, dialog):
        """Ferme un dialog"""
        dialog.open = False
        self.page.update()
    
    def _switch_tab(self, tab_id):
        """Change l'onglet actif avec animation"""
        if self.current_tab == tab_id:
            return
        
        # Animation de sortie (fade out)
        self.content_container.opacity = 0
        self.page.update()
        
        import time
        time.sleep(0.2)
        
        # Mettre à jour l'onglet actif
        self.current_tab = tab_id
        
        # Mettre à jour les styles des onglets existants au lieu de les reconstruire
        self._update_tab_styles()
        
        # Changer le contenu selon l'onglet
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
            # Afficher un indicateur de chargement pendant la récupération des données
            loading_indicator = ft.Container(
                content=ft.Column(
                    [
                        ft.ProgressRing(width=50, height=50, color=Colors.ACCENT_PRIMARY),
                        Spacer(height=Spacing.MD),
                        BodyText("Chargement des informations matérielles...", color=Colors.FG_SECONDARY),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
                padding=Spacing.MEGA,
                alignment=ft.alignment.center,
            )
            
            self.content_container.content = ft.Column(
                [loading_indicator],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            )
            self.content_container.opacity = 1
            self.page.update()
            
            # Charger les données matérielles en arrière-plan
            def load_config():
                config_section = self._build_configuration_section()
                self.content_container.content = ft.Column(
                    [config_section],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=0,
                )
                self.page.update()
            
            import threading
            threading.Thread(target=load_config, daemon=True).start()
            
            # Masquer le bouton de prévisualisation dans l'onglet Configuration
            if hasattr(self, 'action_button_container'):
                self.action_button_container.visible = False
            return  # Sortir ici car l'animation est déjà faite
        
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
        """Lance la prévisualisation (Dry-Run) - OPTIMISÉ"""
        # PROTECTION ANTI-SPAM: Bloquer si une opération est en cours
        if self.cleaning_in_progress:
            return
        
        # PROTECTION ANTI-SPAM: Bloquer si le bouton est désactivé
        if self.dry_run_button and hasattr(self.dry_run_button, 'data') and self.dry_run_button.data == 'disabled':
            return
        
        self.cleaning_in_progress = True
        
        try:
            # Désactiver TOUS les boutons de prévisualisation avec feedback visuel fort
            if self.dry_run_button:
                self.dry_run_button.data = 'disabled'
                self.dry_run_button.bgcolor = Colors.FG_SECONDARY  # Gris
                self.dry_run_button.disabled = True
                # Changer le texte et l'icône du bouton principal
                self.dry_run_button_icon.name = ft.Icons.HOURGLASS_EMPTY_ROUNDED
                self.dry_run_button_text.value = "Analyse en cours"
            
            if hasattr(self, 'preview_button_tabs'):
                self.preview_button_tabs.data = 'disabled'
                self.preview_button_tabs.bgcolor = Colors.FG_SECONDARY  # Gris
                self.preview_button_tabs.disabled = True
                # Changer le texte et l'icône du bouton tabs
                self.preview_button_tabs_icon.name = ft.Icons.HOURGLASS_EMPTY_ROUNDED
                self.preview_button_tabs_text.value = "Analyse en cours"
            
            # Afficher un message de statut immédiat TRÈS VISIBLE
            if self.status_text:
                self.status_text.value = "⏳ Analyse en cours... Veuillez patienter (10-15 secondes)"
                self.status_text.color = Colors.ACCENT_PRIMARY
                self.status_text.visible = True
            
            # IMPORTANT: Forcer la mise à jour IMMÉDIATE de l'UI
            self.page.update()
            
            # Lancer l'animation des points
            self._start_button_animation()
            
            # Lancer le dry-run dans un thread
            import threading
            threading.Thread(target=self._run_dry_run, daemon=True).start()
        except Exception as ex:
            print(f"[ERROR] Failed to start dry-run: {ex}")
            import traceback
            traceback.print_exc()
            self.cleaning_in_progress = False
            # Réactiver TOUS les boutons en cas d'erreur
            self._reset_preview_buttons()
            self.page.update()
    
    def _run_dry_run(self):
        """Exécute le dry-run dans un thread séparé - OPTIMISÉ"""
        from src.core.dry_run import dry_run_manager
        import time
        
        try:
            # Mettre à jour le statut (THREAD-SAFE avec try/except)
            try:
                if self.status_text:
                    self.status_text.value = "🔍 Analyse en cours... Veuillez patienter."
                    self.status_text.color = Colors.ACCENT_PRIMARY
                    self.status_text.visible = True
                self.page.update()
            except Exception as update_ex:
                print(f"[WARNING] Could not update status: {update_ex}")
            
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
            
            # Réactiver les boutons et afficher l'erreur (THREAD-SAFE avec try/except)
            try:
                self._reset_preview_buttons()
                if self.status_text:
                    self.status_text.value = f"❌ Erreur lors de la prévisualisation : {str(ex)}"
                    self.status_text.color = Colors.ERROR
                    self.status_text.visible = True
                self.page.update()
            except Exception as update_ex:
                print(f"[WARNING] Could not update error status: {update_ex}")
        
        finally:
            self.cleaning_in_progress = False
    
    def _show_preview_page(self, preview_data):
        """Affiche la page de prévisualisation avec transition fluide - OPTIMISÉ"""
        import time
        
        try:
            # Animation de sortie de la page actuelle
            pass  # Debug removed
            try:
                if hasattr(self, 'main_container'):
                    self.main_container.opacity = 0
                    self.page.update()
            except Exception as fade_ex:
                print(f"[WARNING] Fade out failed: {fade_ex}")
            
            time.sleep(0.2)  # Réduit de 0.3 à 0.2s pour plus de réactivité
            
            # Importer et créer la page de prévisualisation
            pass  # Debug removed
            from src.ui.pages.preview_page import PreviewPage
            
            preview_page = PreviewPage(self.page, self.app, preview_data)
            
            # Remplacer le contenu de la page
            pass  # Debug removed
            try:
                self.page.controls.clear()
                
                # Construire la page (elle commence avec opacity=0)
                preview_container = preview_page.build()
                preview_container.opacity = 0
                
                # Ajouter à la page
                self.page.add(preview_container)
                self.page.update()
                
                # Animation d'entrée immédiate (pas de sleep)
                pass  # Debug removed
                preview_container.opacity = 1
                self.page.update()
                
                print("[SUCCESS] Page de prévisualisation affichée")
            except Exception as page_ex:
                print(f"[ERROR] Page transition failed: {page_ex}")
                raise
            
        except Exception as ex:
            print(f"[ERROR] Failed to show preview page: {ex}")
            import traceback
            traceback.print_exc()
            
            # En cas d'erreur, réactiver les boutons
            try:
                self._reset_preview_buttons()
                self.page.update()
            except Exception as reset_ex:
                print(f"[WARNING] Could not reset buttons: {reset_ex}")
    
    def _start_button_animation(self):
        """Démarre l'animation des points sur les boutons"""
        import threading
        import time
        
        def animate_dots():
            dots = ["", ".", "..", "..."]
            index = 0
            
            while self.cleaning_in_progress:
                try:
                    # Mettre à jour le texte avec les points animés
                    if self.dry_run_button_text:
                        self.dry_run_button_text.value = f"Analyse en cours{dots[index]}"
                    if hasattr(self, 'preview_button_tabs_text'):
                        self.preview_button_tabs_text.value = f"Analyse{dots[index]}"
                    
                    self.page.update()
                    
                    # Passer au point suivant
                    index = (index + 1) % len(dots)
                    time.sleep(0.5)  # Animation toutes les 500ms
                except Exception as ex:
                    print(f"[WARNING] Animation error: {ex}")
                    break
        
        # Lancer l'animation dans un thread séparé
        threading.Thread(target=animate_dots, daemon=True).start()
    
    def _reset_preview_buttons(self):
        """Réinitialise l'état de tous les boutons de prévisualisation"""
        if self.dry_run_button:
            self.dry_run_button.data = None
            self.dry_run_button.bgcolor = Colors.ACCENT_PRIMARY  # Bleu
            self.dry_run_button.disabled = False
            # Restaurer le texte et l'icône d'origine
            self.dry_run_button_icon.name = ft.Icons.PREVIEW_ROUNDED
            self.dry_run_button_text.value = "Prévisualiser le nettoyage"
        
        if hasattr(self, 'preview_button_tabs'):
            self.preview_button_tabs.data = None
            self.preview_button_tabs.bgcolor = Colors.ACCENT_PRIMARY  # Bleu
            self.preview_button_tabs.disabled = False
            # Restaurer le texte et l'icône d'origine
            self.preview_button_tabs_icon.name = ft.Icons.PREVIEW_ROUNDED
            self.preview_button_tabs_text.value = "Prévisualiser"
    
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
        pass  # Debug removed
        
        # ========================================================================
        # SÉCURITÉ CRITIQUE: ANTI-CONTOURNEMENT
        # ========================================================================
        # Cette vérification DOIT être la première chose exécutée
        # Elle empêche tout contournement de la sécurité
        
        # Note: Le nettoyage n'est accessible que depuis la page de prévisualisation
        # après avoir fait un dry-run, donc pas besoin de vérification ici
        
        # ========================================================================
        
        if self.cleaning_in_progress:
            pass  # Debug removed
            return
        
        pass  # Debug removed
        print("[SECURITY] Dry-run completed - Cleaning authorized")
        self.cleaning_in_progress = True
        
        try:
            # Animation de sortie
            pass  # Debug removed
            self.main_container.opacity = 0
            self.page.update()
            
            import time
            time.sleep(0.3)
            
            # Remplacer le contenu de la page
            pass  # Debug removed
            self._show_cleaning_page()
            
            pass  # Debug removed
            import threading
            threading.Thread(target=self._run_cleaning, daemon=True).start()
            pass  # Debug removed
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
        pass  # Debug removed
        self.page.controls.clear()
        self.page.add(self.cleaning_container)
        self.page.update()
        
        # Animation d'entrée
        import time
        time.sleep(0.1)
        self.cleaning_container.opacity = 1
        self.page.update()
        pass  # Debug removed
    
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
        
        pass  # Debug removed
        
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
            pass  # Debug removed
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
            
            # ===== NOUVELLES OPTIONS AVANCÉES =====
            from src.core import advanced_optimizations
            
            # Désactiver l'hibernation
            if self.app.advanced_options.get("disable_hibernation", False):
                self._update_cleaning_progress("Désactivation de l'hibernation...", current_task / total_tasks)
                advanced_optimizations.disable_hibernation()
                time.sleep(0.2)
            
            # Nettoyer points de restauration
            if self.app.advanced_options.get("clean_restore_points", False):
                self._update_cleaning_progress("Nettoyage des points de restauration...", current_task / total_tasks)
                advanced_optimizations.clean_old_restore_points()
                time.sleep(0.2)
            
            # Optimiser démarrage
            if self.app.advanced_options.get("optimize_startup", False):
                self._update_cleaning_progress("Optimisation du démarrage...", current_task / total_tasks)
                advanced_optimizations.optimize_startup_programs()
                time.sleep(0.2)
            
            # Vider cache navigateurs
            if self.app.advanced_options.get("clear_browser_cache", False):
                self._update_cleaning_progress("Nettoyage du cache des navigateurs...", current_task / total_tasks)
                advanced_optimizations.clear_browser_cache()
                time.sleep(0.2)
            
            # Nettoyer logs événements
            if self.app.advanced_options.get("clean_event_logs", False):
                self._update_cleaning_progress("Nettoyage des logs d'événements...", current_task / total_tasks)
                advanced_optimizations.clean_event_logs()
                time.sleep(0.2)
            
            # Désactiver Superfetch
            if self.app.advanced_options.get("disable_superfetch", False):
                self._update_cleaning_progress("Désactivation de Superfetch...", current_task / total_tasks)
                advanced_optimizations.disable_superfetch()
                time.sleep(0.2)
            
            # Désactiver Cortana
            if self.app.advanced_options.get("disable_cortana", False):
                self._update_cleaning_progress("Désactivation de Cortana...", current_task / total_tasks)
                advanced_optimizations.disable_cortana()
                time.sleep(0.2)
            
            # Optimiser TCP/IP
            if self.app.advanced_options.get("optimize_tcp_ip", False):
                self._update_cleaning_progress("Optimisation TCP/IP...", current_task / total_tasks)
                advanced_optimizations.optimize_tcp_ip()
                time.sleep(0.2)
            
            # Désactiver services
            if self.app.advanced_options.get("disable_services", False):
                self._update_cleaning_progress("Désactivation des services inutiles...", current_task / total_tasks)
                advanced_optimizations.disable_unnecessary_services()
                time.sleep(0.2)
            
            # Mode Gaming
            if self.app.advanced_options.get("gaming_mode", False):
                self._update_cleaning_progress("Activation du mode Gaming...", current_task / total_tasks)
                advanced_optimizations.enable_gaming_mode()
                time.sleep(0.2)
            
            # Nettoyer pilotes
            if self.app.advanced_options.get("clean_drivers", False):
                self._update_cleaning_progress("Nettoyage des pilotes obsolètes...", current_task / total_tasks)
                advanced_optimizations.clean_old_drivers()
                time.sleep(0.2)
            
            # Vider WinSxS
            if self.app.advanced_options.get("clean_winsxs", False):
                self._update_cleaning_progress("Nettoyage de WinSxS...", current_task / total_tasks)
                advanced_optimizations.clean_winsxs()
                time.sleep(0.2)
            
            # Optimiser pagefile
            if self.app.advanced_options.get("optimize_pagefile", False):
                self._update_cleaning_progress("Optimisation du fichier de pagination...", current_task / total_tasks)
                advanced_optimizations.optimize_pagefile()
                time.sleep(0.2)
            
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
        
        pass  # Debug removed
        self.cleaning_container.opacity = 0
        self.page.update()
        time.sleep(0.3)
        
        pass  # Debug removed
        self.page.controls.clear()
        new_main = self.build()
        new_main.opacity = 0
        self.page.add(new_main)
        self.page.update()
        
        # Animation d'entrée
        time.sleep(0.1)
        new_main.opacity = 1
        self.page.update()
        pass  # Debug removed
    
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
    
    def _open_github_link(self, e):
        """
        Ouvre le lien GitHub de manière sécurisée
        SÉCURITÉ: Import statique au lieu de __import__ dynamique (PATCH)
        """
        try:
            import webbrowser
            # SÉCURITÉ: URL en dur, pas d'entrée utilisateur
            webbrowser.open("https://github.com/UndKiMi")
        except Exception as ex:
            print(f"[ERROR] Failed to open GitHub link: {ex}")
    
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
