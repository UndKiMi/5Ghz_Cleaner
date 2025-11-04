"""
CPU Action Handler - Fonction d'optimisation CPU pour main_page.py
À intégrer dans la classe MainPage
"""

def _optimize_cpu_action(self):
    """Optimise l'utilisation CPU avec animation de succès/échec"""
    import threading
    
    # ANTI-SPAM: Vérifier le cooldown (PROTECTION)
    can_execute, remaining = self._can_execute_action('optimize_cpu')
    if not can_execute:
        self._show_cooldown_message(remaining)
        return
    
    # Sauvegarder le texte et la couleur ORIGINAUX du bouton avant l'action
    if hasattr(self, 'storage_item_buttons') and 'cpu_button' in self.storage_item_buttons:
        button = self.storage_item_buttons['cpu_button']
        if hasattr(button.content, 'value'):
            self._button_original_texts['cpu_button'] = button.content.value
        # Sauvegarder la couleur originale (PURPLE pour CPU)
        import flet as ft
        self._button_original_colors['cpu_button'] = ft.Colors.PURPLE_400
    
    # ANTI-SPAM: Bloquer immédiatement pour empêcher les clics multiples
    self._register_action('optimize_cpu')
    
    def optimize_cpu():
        from src.core.cpu_optimizer import cpu_optimizer
        import psutil
        import time
        import flet as ft
        
        try:
            print("[INFO] Optimizing CPU usage...")
            
            # Obtenir la référence du bouton
            button = None
            if hasattr(self, 'storage_item_buttons') and 'cpu_button' in self.storage_item_buttons:
                button = self.storage_item_buttons['cpu_button']
            
            # Obtenir l'utilisation CPU avant optimisation
            cpu_before = psutil.cpu_percent(interval=1)
            
            # Animation de chargement
            if button:
                button.bgcolor = ft.Colors.ORANGE
                button.content.value = "⏳ Optimisation..."
                self.page.update()
            
            # Optimiser le CPU
            result = cpu_optimizer.optimize_cpu(aggressive=False)
            success = result.get('success', False)
            terminated_count = result.get('terminated_count', 0)
            terminated_procs = result.get('terminated_processes', [])
            
            # Attendre un peu pour que le système se stabilise
            time.sleep(2)
            
            # Obtenir l'utilisation CPU après optimisation
            cpu_after = psutil.cpu_percent(interval=1)
            cpu_reduced = max(0, cpu_before - cpu_after)
            
            # Animation de succès ou échec
            if button:
                if success and terminated_count > 0:
                    # Animation verte (succès)
                    button.bgcolor = ft.Colors.GREEN
                    button.content.value = f"✓ {terminated_count} processus"
                    self.page.update()
                    
                    time.sleep(1.5)
                    
                    # ANTI-SPAM: Démarrer le cooldown visuel
                    self._start_cooldown_timer('optimize_cpu', 'cpu_button')
                    
                    # Forcer la mise à jour de l'affichage CPU
                    if 'cpu' in self.storage_item_refs:
                        try:
                            from src.services.hardware_monitor import hardware_monitor
                            cpu_usage = hardware_monitor.get_cpu_usage()
                            cpu_temp = hardware_monitor.get_cpu_temperature()
                            
                            refs = self.storage_item_refs['cpu']
                            refs['title'].value = f"Utilisation CPU ({cpu_usage:.1f}%)" + (f" • {cpu_temp}°C" if cpu_temp else "")
                            refs['current'].value = f"{cpu_usage:.1f}% utilisé"
                            refs['progress'].value = cpu_usage / 100 if cpu_usage > 0 else 0
                            self.page.update()
                        except Exception:
                            pass
                    
                    # Construire le message de succès
                    procs_text = "\n".join([
                        f"• {p['name']} (CPU: {p['cpu_percent']:.1f}%)"
                        for p in terminated_procs[:5]  # Afficher max 5 processus
                    ])
                    
                    self._show_success_dialog(
                        "✓ CPU optimisé",
                        f"{terminated_count} processus non essentiels fermés.\n\n"
                        f"Processus terminés:\n{procs_text}\n\n"
                        f"Utilisation CPU avant: {cpu_before:.1f}%\n"
                        f"Utilisation CPU après: {cpu_after:.1f}%\n"
                        f"Réduction: {cpu_reduced:.1f}%"
                    )
                else:
                    # Animation orange (aucun processus à optimiser)
                    button.bgcolor = ft.Colors.ORANGE
                    button.content.value = "ℹ Déjà optimisé"
                    self.page.update()
                    
                    time.sleep(1.5)
                    
                    # ANTI-SPAM: Démarrer le cooldown visuel
                    self._start_cooldown_timer('optimize_cpu', 'cpu_button')
                    
                    # Afficher un message d'information
                    self._show_success_dialog(
                        "ℹ CPU déjà optimisé",
                        f"Aucun processus non essentiel utilisant beaucoup de CPU détecté.\n\n"
                        f"Utilisation CPU actuelle: {cpu_after:.1f}%\n\n"
                        f"Votre système est déjà optimisé."
                    )
            
            print(f"[INFO] CPU optimization result: {success}, terminated: {terminated_count}")
            
        except Exception as e:
            print(f"[ERROR] Failed to optimize CPU: {e}")
            import traceback
            traceback.print_exc()
            
            # Animation d'erreur
            if button:
                button.bgcolor = ft.Colors.RED
                button.content.value = "✗ Erreur"
                self.page.update()
                
                import time
                time.sleep(1.5)
                
                # ANTI-SPAM: Démarrer le cooldown visuel même en cas d'exception
                self._start_cooldown_timer('optimize_cpu', 'cpu_button')
            
            self._show_error_dialog("⚠ Erreur", f"Impossible d'optimiser le CPU:\n{str(e)}")
    
    # Lancer dans un thread
    threading.Thread(target=optimize_cpu, daemon=True).start()
