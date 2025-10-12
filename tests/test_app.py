"""
Test rapide de l'application
"""
import sys
import flet as ft

def main(page: ft.Page):
    page.title = "Test 5GH'z Cleaner"
    page.window_width = 800
    page.window_height = 600
    
    page.add(
        ft.Text("Application de test - Si vous voyez ceci, Flet fonctionne!", size=20)
    )

if __name__ == "__main__":
    print("Lancement du test...")
    try:
        ft.app(target=main)
        print("Test terminé avec succès")
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        input("Appuyez sur Entrée...")
