"""
Frontend module for 5GH'z Cleaner using Flet
Modern, clean interface with all original functionality
"""
import flet as ft
import threading
import time
import webbrowser
from backend import cleaner
from .constants import *
from .ui_components import (
    create_shield_icon,
    create_warning_box,
    create_terms_list,
    create_checkbox,
    create_footer
)
from .pages import MainPage


class CleanerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self._configure_window()
        self.disclaimer_accepted = False
        self.menu_visible = False
        self.progress_bar = None
        self.status_text = None
        self.advanced_options = {
            "clear_standby_memory": True,
            "flush_dns": True,
            "disable_telemetry": False,
            "clear_large_logs": True
        }
        self.show_disclaimer()
    
    def _configure_window(self):
        """Configure window properties"""
        self.page.title = "5GH'z Cleaner"
        self.page.window.width = WINDOW_WIDTH
        self.page.window.height = WINDOW_HEIGHT
        self.page.window.resizable = True
        self.page.window.maximizable = False
        self.page.window.min_width = WINDOW_MIN_WIDTH
        self.page.window.min_height = WINDOW_MIN_HEIGHT
        self.page.window.frameless = False
        self.page.bgcolor = BG_MAIN
        self.page.padding = 0
    
    def build_title_bar(self, title="5GH'z Cleaner"):
        """Build custom title bar with window controls"""
        def minimize_window(e):
            self.page.window.minimized = True
            self.page.update()
        
        def close_window(e):
            self.page.window.close()
        
        def start_drag(e):
            self.page.window_drag_start()
        
        return ft.WindowDragArea(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.SHIELD_OUTLINED, color=BLUE_ACCENT, size=18),
                        ft.Container(width=8),
                        ft.Text(
                            title,
                            size=13,
                            color=FG_SECONDARY,
                            weight=ft.FontWeight.W_500,
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.MINIMIZE,
                            icon_size=18,
                            icon_color=FG_SECONDARY,
                            on_click=minimize_window,
                            tooltip="Réduire",
                            style=ft.ButtonStyle(
                                overlay_color=ft.Colors.with_opacity(0.1, FG_SECONDARY),
                            ),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_size=18,
                            icon_color=FG_SECONDARY,
                            on_click=close_window,
                            tooltip="Fermer",
                            style=ft.ButtonStyle(
                                overlay_color=ft.Colors.with_opacity(0.2, "#ff5555"),
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=0,
                ),
                bgcolor="#0a1929",
                padding=ft.padding.only(left=12, right=4, top=0, bottom=0),
                height=40,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                    offset=ft.Offset(0, 2),
                ),
            ),
        )
    
    def show_disclaimer(self):
        """Show disclaimer dialog before main app"""
        def close_disclaimer(e):
            if checkbox.value:
                self._animate_button_press(accept_button)
                self._transition_to_main_ui(disclaimer_container)
            else:
                self.show_warning("Veuillez cocher la case pour continuer.")
        
        # Create UI components
        checkbox, checkbox_row = create_checkbox()
        shield_container = create_shield_icon()
        warning_box = create_warning_box()
        terms_list = create_terms_list()
        footer = create_footer()
        
        # Accept button
        accept_button = ft.ElevatedButton(
            "J'accepte les conditions",
            on_click=close_disclaimer,
            bgcolor=BLUE_ACCENT,
            color="#ffffff",
            height=45,
            width=250,
            scale=1,
            animate_scale=ft.Animation(BUTTON_PRESS_DURATION, ft.AnimationCurve.EASE_OUT),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        )
        
        # Main card
        main_card = self._build_disclaimer_card(
            shield_container, checkbox_row, warning_box, terms_list, accept_button
        )
        
        
        # Full disclaimer container
        disclaimer_container = ft.Container(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=50),
                        main_card,
                        ft.Container(height=50),
                        footer,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=20),
            ),
            bgcolor=BG_MAIN,
            expand=True,
            opacity=1,
            animate_opacity=ft.Animation(FADE_DURATION, ft.AnimationCurve.EASE_OUT),
        )
        
        # Add content and start animations
        self.page.add(disclaimer_container)
        self._fade_in_container(disclaimer_container)
        self._start_shield_glow_animation(shield_container)
    
    def _build_disclaimer_card(self, shield, checkbox_row, warning_box, terms_list, accept_button):
        """Build the main disclaimer card"""
        return ft.Container(
            content=ft.Column(
                [
                    shield,
                    ft.Container(height=20),
                    ft.Text(
                        "Conditions d'utilisation",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ACCENT_COLOR,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=5),
                    ft.Text(
                        "Il est recommandé de lire attentivement les conditions d'utilisation avant de poursuivre.",
                        size=13,
                        color=FG_MAIN,
                        text_align=ft.TextAlign.CENTER,
                        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                    ),
                    ft.Container(height=25),
                    warning_box,
                    ft.Container(height=20),
                    terms_list,
                    ft.Container(height=25),
                    checkbox_row,
                    ft.Container(height=25),
                    accept_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
            ),
            bgcolor=BG_MAIN,
            padding=40,
            border_radius=12,
            border=ft.border.all(1, "#2a3342"),
            width=700,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
        )
    
    def _animate_button_press(self, button):
        """Animate button press effect"""
        button.scale = 0.95
        button.update()
        time.sleep(0.1)
        button.scale = 1
        button.update()
    
    def _transition_to_main_ui(self, container):
        """Transition from disclaimer to main UI"""
        self.disclaimer_accepted = True
        container.opacity = 0
        self.page.update()
        time.sleep(0.3)
        
        try:
            self.page.controls.clear()
            self.build_main_ui()
            self.page.update()
        except Exception as ex:
            print(f"[ERROR] Failed to build main UI: {ex}")
            import traceback
            traceback.print_exc()
    
    def _fade_in_container(self, container):
        """Fade in animation for container"""
        container.opacity = 0
        self.page.update()
        time.sleep(0.1)
        container.opacity = 1
        self.page.update()
    
    def _start_shield_glow_animation(self, shield_container):
        """Start shield glow pulsation animation"""
        def animate_glow():
            pulse_out = True
            while True:
                try:
                    if pulse_out:
                        shield_container.shadow = [
                            ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=SHADOW_BLUR_RADIUS,
                                color=ft.Colors.with_opacity(SHADOW_OPACITY, ft.Colors.BLACK),
                                offset=ft.Offset(0, 2),
                            ),
                            ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=GLOW_BLUR_MAX,
                                color=ft.Colors.with_opacity(GLOW_OPACITY_MAX, BLUE_ACCENT),
                                offset=ft.Offset(0, 0),
                            ),
                        ]
                    else:
                        shield_container.shadow = [
                            ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=SHADOW_BLUR_RADIUS,
                                color=ft.Colors.with_opacity(SHADOW_OPACITY, ft.Colors.BLACK),
                                offset=ft.Offset(0, 2),
                            ),
                            ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=GLOW_BLUR_MIN,
                                color=ft.Colors.with_opacity(GLOW_OPACITY_MIN, BLUE_ACCENT),
                                offset=ft.Offset(0, 0),
                            ),
                        ]
                    
                    shield_container.update()
                    pulse_out = not pulse_out
                    time.sleep(SHIELD_PULSE_INTERVAL)
                except:
                    break
        
        threading.Thread(target=animate_glow, daemon=True).start()
    
    def show_warning(self, message):
        """Show warning dialog"""
        def close_dlg(e):
            dlg.open = False
            self.page.update()
        
        dlg = ft.AlertDialog(
            title=ft.Row(
                [
                    ft.Text("⚠️", size=28),
                    ft.Text("Attention", size=20, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            content=ft.Text(message, text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor=BG_SECONDARY,
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def toggle_menu(self, e):
        """Toggle advanced options menu"""
        self.menu_visible = not self.menu_visible
        self.side_menu.visible = self.menu_visible
        print(f"[INFO] Advanced options menu {'opened' if self.menu_visible else 'closed'}")
        self.page.update()
    
    def build_main_ui(self):
        """Build the main application UI"""
        main_page = MainPage(self.page, self)
        self.page.add(main_page.build())
        self.page.update()
    
    def build_main_ui_old(self):
        """Build the main application UI"""
        print("[INFO] Constructing main UI components...")
        # Header with hamburger menu
        def open_github(e):
            print("[INFO] Opening GitHub profile in browser...")
            webbrowser.open("https://github.com/UndKiMi")
        
        # Side menu for advanced options
        self.side_menu = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Options avancées",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ACCENT_COLOR,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color=ACCENT_COLOR,
                                on_click=self.toggle_menu,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(color=FG_MAIN),
                    ft.Checkbox(
                        label="Libérer RAM Standby",
                        value=self.advanced_options["clear_standby_memory"],
                        on_change=lambda e: self.update_option("clear_standby_memory", e.control.value),
                        fill_color=ACCENT_COLOR,
                    ),
                    ft.Checkbox(
                        label="Flush DNS",
                        value=self.advanced_options["flush_dns"],
                        on_change=lambda e: self.update_option("flush_dns", e.control.value),
                        fill_color=ACCENT_COLOR,
                    ),
                    ft.Checkbox(
                        label="Désactiver télémétrie",
                        value=self.advanced_options["disable_telemetry"],
                        on_change=lambda e: self.update_option("disable_telemetry", e.control.value),
                        fill_color=ACCENT_COLOR,
                    ),
                    ft.Checkbox(
                        label="Nettoyer logs volumineux",
                        value=self.advanced_options["clear_large_logs"],
                        on_change=lambda e: self.update_option("clear_large_logs", e.control.value),
                        fill_color=ACCENT_COLOR,
                    ),
                ],
                spacing=10,
            ),
            bgcolor=BG_SECONDARY,
            padding=20,
            border_radius=10,
            width=280,
            visible=False,
        )
        
        # Main content
        hamburger_button = ft.IconButton(
            icon=ft.Icons.MENU,
            icon_color=ACCENT_COLOR,
            on_click=self.toggle_menu,
        )
        
        title_section = ft.Column(
            [
                ft.Container(height=20),
                ft.Text(
                    "5GH'z Cleaner",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ACCENT_COLOR,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Windows Cleaning & Optimisation LITE",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=FG_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=20),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # Progress bar
        self.progress_bar = ft.ProgressBar(
            height=20,
            value=0,
            bgcolor=BG_SECONDARY,
            color=ACCENT_COLOR,
            expand=True,
        )
        
        # Status text
        self.status_text = ft.Text(
            "Prêt à nettoyer !",
            size=14,
            weight=ft.FontWeight.BOLD,
            color=FG_MAIN,
            text_align=ft.TextAlign.CENTER,
        )
        
        # Launch button
        launch_button = ft.Container(
            content=ft.ElevatedButton(
                "🚀 Lancer le nettoyage",
                on_click=self.launch_cleaning,
                bgcolor=ACCENT_COLOR,
                color=FG_MAIN,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
                expand=True,
            ),
            width=300,
        )
        
        # Footer
        footer = ft.Row(
            [
                ft.Text(
                    "Ce script élève les droits automatiquement (UAC) • Tous droits réservés par ",
                    size=10,
                    color=FG_SECONDARY,
                ),
                ft.TextButton(
                    "UndKiMi",
                    on_click=open_github,
                    style=ft.ButtonStyle(
                        color=ACCENT_COLOR,
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            wrap=True,
        )
        
        # Layout with stack for menu overlay
        main_content = ft.Column(
            [
                ft.Row(
                    [hamburger_button],
                    alignment=ft.MainAxisAlignment.START,
                ),
                title_section,
                ft.Container(
                    content=self.progress_bar,
                    padding=ft.padding.symmetric(horizontal=40),
                ),
                ft.Container(height=10),
                self.status_text,
                ft.Container(height=30),
                launch_button,
                ft.Container(expand=True),
                footer,
                ft.Container(height=20),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
        
        # Stack to overlay menu
        content_stack = ft.Stack(
            [
                main_content,
                ft.Container(
                    content=self.side_menu,
                    left=10,
                    top=60,
                ),
            ],
            expand=True,
        )
        
        # Main container with fade-in animation
        main_container = ft.Container(
            content=content_stack,
            bgcolor=BG_MAIN,
            expand=True,
            animate_opacity=300,
        )
        
        # Add content directly (no custom title bar needed)
        self.page.add(main_container)
        
        # Fade in animation
        main_container.opacity = 0
        self.page.update()
        time.sleep(0.1)
        main_container.opacity = 1
        self.page.update()
    
    def update_option(self, key, value):
        """Update advanced option state"""
        self.advanced_options[key] = value
        print(f"[INFO] Advanced option '{key}' set to {value}")
    
    def update_progress(self, value, status):
        """Update progress bar and status text"""
        self.progress_bar.value = value / 100
        self.status_text.value = status
        self.status_text.color = ACCENT_COLOR
        self.page.update()
    
    def launch_cleaning(self, e):
        """Launch the cleaning process in a separate thread"""
        print("[INFO] ========================================")
        print("[INFO] Starting cleaning process...")
        print("[INFO] ========================================")
        threading.Thread(target=self.run_cleaning, daemon=True).start()
    
    def run_cleaning(self):
        """Execute all cleaning operations"""
        results = {}
        
        try:
            # Clear temp files
            print("[TASK] Clearing temporary system files...")
            self.update_progress(10, "Nettoyage des éléments système temporaires…")
            results.update(cleaner.clear_temp())
            print(f"[RESULT] Temp files cleared: {results.get('temp_deleted', 0)} items")
            time.sleep(0.3)
            
            # Clear prefetch
            print("[TASK] Optimizing Windows prefetch...")
            self.update_progress(20, "Optimisation du préchargement Windows…")
            results.update(cleaner.clear_prefetch())
            print(f"[RESULT] Prefetch cleared: {results.get('prefetch_cleared', 0)} items")
            time.sleep(0.3)
            
            # Clear recent
            print("[TASK] Purging recent history...")
            self.update_progress(30, "Purge des historiques techniques…")
            results.update(cleaner.clear_recent())
            print(f"[RESULT] Recent history cleared: {results.get('recent_cleared', 0)} items")
            time.sleep(0.3)
            
            # Clear thumbnail cache
            print("[TASK] Refreshing thumbnail cache...")
            self.update_progress(40, "Rafraîchissement du cache des miniatures…")
            results.update(cleaner.clear_thumbnail_cache())
            print(f"[RESULT] Thumbnail cache cleared: {results.get('thumbs_cleared', 0)} items")
            time.sleep(0.3)
            
            # Clear crash dumps
            print("[TASK] Cleaning crash dumps...")
            self.update_progress(50, "Nettoyage des journaux techniques…")
            results.update(cleaner.clear_crash_dumps())
            print(f"[RESULT] Crash dumps deleted: {results.get('dumps_deleted', 0)} items")
            time.sleep(0.3)
            
            # Clear Windows.old
            print("[TASK] Cleaning previous Windows installation...")
            self.update_progress(65, "Nettoyage installation précédente…")
            results.update(cleaner.clear_windows_old())
            print(f"[RESULT] Windows.old deleted: {results.get('windows_old_deleted', 0)}")
            time.sleep(0.3)
            
            # Clear Windows Update cache
            print("[TASK] Cleaning Windows Update cache...")
            self.update_progress(75, "Nettoyage du cache Windows Update…")
            results.update(cleaner.clear_windows_update_cache())
            print(f"[RESULT] Update cache cleared: {results.get('update_deleted', 0)} items")
            time.sleep(0.3)
            
            # Empty recycle bin
            print("[TASK] Emptying recycle bin...")
            self.update_progress(85, "Vidage de la corbeille…")
            results.update(cleaner.empty_recycle_bin())
            print(f"[RESULT] Recycle bin emptied: {results.get('recycle_bin_deleted', 0)} items")
            time.sleep(0.3)
            
            # Stop services
            print("[TASK] Stopping optional system services...")
            self.update_progress(90, "Arrêt de modules système optionnels…")
            results.update(cleaner.stop_services(cleaner.SERVICES_TO_STOP))
            stopped_services = results.get('services_stopped', [])
            print(f"[RESULT] Services stopped: {len(stopped_services)} ({', '.join(stopped_services) if stopped_services else 'none'})")
            time.sleep(0.3)
            
            # Advanced options
            if self.advanced_options["clear_standby_memory"]:
                print("[TASK] Clearing standby memory...")
                self.update_progress(93, "Libération de la RAM Standby…")
                results.update(cleaner.clear_standby_memory())
                print(f"[RESULT] Standby memory cleared: {results.get('ram_standby_cleared', False)}")
                time.sleep(0.2)
            
            if self.advanced_options["flush_dns"]:
                print("[TASK] Flushing DNS cache...")
                self.update_progress(96, "Flush DNS…")
                results.update(cleaner.flush_dns())
                print(f"[RESULT] DNS flushed: {results.get('dns_flushed', False)}")
                time.sleep(0.2)
            
            if self.advanced_options["clear_large_logs"]:
                print("[TASK] Cleaning large log files...")
                self.update_progress(98, "Nettoyage logs volumineux…")
                results.update(cleaner.clear_large_logs())
                print(f"[RESULT] Large logs deleted: {results.get('logs_deleted', 0)} items")
                time.sleep(0.2)
            
            if self.advanced_options["disable_telemetry"]:
                print("[TASK] Disabling telemetry/diagnostics...")
                self.update_progress(99, "Désactivation télémétrie/diagnostic…")
                results.update(cleaner.disable_telemetry())
                print(f"[RESULT] Telemetry disabled: {results.get('diag_disabled', False)}")
                time.sleep(0.2)
            
            # Complete
            self.update_progress(100, "Opération terminée !")
            print("[SUCCESS] Cleaning process completed successfully!")
            print("[INFO] ========================================")
            time.sleep(0.5)
            
            # Show summary
            print("[INFO] Displaying summary dialog...")
            self.show_summary(results)
            
        except Exception as ex:
            print(f"[ERROR] Cleaning process failed: {str(ex)}")
            print(f"[ERROR] Exception type: {type(ex).__name__}")
            self.status_text.value = f"Erreur: {str(ex)}"
            self.status_text.color = "#ff5555"
            self.page.update()
    
    def show_summary(self, results):
        """Show cleaning summary dialog"""
        def close_dlg(e):
            print("[INFO] Closing summary dialog...")
            dlg.open = False
            self.page.update()
            # Reset progress
            self.progress_bar.value = 0
            self.status_text.value = "Prêt à nettoyer !"
            self.status_text.color = FG_MAIN
            self.page.update()
            print("[INFO] Application ready for next cleaning cycle")
        
        def open_github(e):
            print("[INFO] Opening GitHub profile from summary dialog...")
            webbrowser.open("https://github.com/UndKiMi")
        
        # Build summary details
        details = [
            ("Éléments système temporaires supprimés", results.get('temp_deleted', 0)),
            ("Préchargements Windows optimisés", results.get('prefetch_cleared', 0)),
            ("Historique technique purgé", results.get('recent_cleared', 0)),
            ("Cache de miniatures rafraîchi", results.get('thumbs_cleared', 0)),
            ("Journaux techniques allégés", results.get('dumps_deleted', 0)),
            ("Installation précédente nettoyée", "Oui" if results.get('windows_old_deleted', 0) else "Non"),
            ("Cache Windows Update nettoyé", results.get('update_deleted', 0)),
            ("Corbeille vidée", results.get('recycle_bin_deleted', 0)),
            ("Modules optionnels arrêtés", len(results.get('services_stopped', []))),
            ("RAM Standby libérée", "Oui" if results.get('ram_standby_cleared') else "Non"),
            ("DNS flush", "Oui" if results.get('dns_flushed') else "Non"),
            ("Logs volumineux supprimés", results.get('logs_deleted', 0)),
            ("Télémétrie désactivée", "Oui" if results.get('diag_disabled') else "Non"),
        ]
        
        detail_rows = []
        for label, value in details:
            detail_rows.append(
                ft.Row(
                    [
                        ft.Text(f"{label}:", size=12, color=FG_MAIN, expand=True),
                        ft.Text(f"{value}", size=12, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )
        
        # Services stopped details
        services = results.get('services_stopped', [])
        if services:
            detail_rows.append(ft.Container(height=10))
            detail_rows.append(
                ft.Text(
                    "Détail des modules arrêtés:",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=FG_SECONDARY,
                )
            )
            for svc in services:
                detail_rows.append(
                    ft.Text(f"→ {svc}", size=11, color=FG_SECONDARY)
                )
        
        summary_content = ft.Column(
            [
                ft.Text(
                    "Bilan du nettoyage",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ACCENT_COLOR,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=10),
                ft.Container(
                    content=ft.Column(
                        detail_rows,
                        spacing=5,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    height=300,
                ),
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Fermer",
                    on_click=close_dlg,
                    bgcolor=ACCENT_COLOR,
                    color=FG_MAIN,
                ),
                ft.Container(height=10),
                ft.Row(
                    [
                        ft.Text("Tous droits réservés par ", size=10, color=FG_SECONDARY),
                        ft.TextButton(
                            "UndKiMi",
                            on_click=open_github,
                            style=ft.ButtonStyle(color=ACCENT_COLOR),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )
        
        dlg = ft.AlertDialog(
            content=ft.Container(
                content=summary_content,
                width=500,
                height=550,
            ),
            bgcolor=BG_MAIN,
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()


def main(page: ft.Page):
    """Main entry point for Flet app"""
    app = CleanerApp(page)


if __name__ == "__main__":
    ft.app(target=main)
