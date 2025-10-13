"""
Script de restructuration du projet
Réorganise les fichiers selon la nouvelle structure professionnelle
"""
import os
import shutil
import sys

# Ajouter encodage UTF-8
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Racine du projet
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_directory_structure():
    """Crée la nouvelle structure de dossiers"""
    print("="*80)
    print("CRÉATION DE LA STRUCTURE DE DOSSIERS")
    print("="*80)
    print()
    
    directories = [
        "docs",
        "docs/guides",
        "docs/technical",
        "src",
        "src/backend",
        "src/frontend",
        "src/frontend/design_system",
        "src/frontend/pages",
        "src/config",
        "scripts/build",
        "scripts/signing",
        "scripts/verification",
    ]
    
    for directory in directories:
        path = os.path.join(PROJECT_ROOT, directory)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"✅ Créé: {directory}")
        else:
            print(f"ℹ️  Existe: {directory}")
    
    print()


def move_documentation():
    """Déplace la documentation dans docs/"""
    print("="*80)
    print("DÉPLACEMENT DE LA DOCUMENTATION")
    print("="*80)
    print()
    
    # Fichiers à déplacer vers docs/
    doc_files = [
        "QUICK_START.md",
        "INSTALLATION.md",
        "SECURITY.md",
        "PRIVACY.md",
        "CONTRIBUTING.md",
        "WINDOWS_11_ONLY.md",
    ]
    
    for file in doc_files:
        src = os.path.join(PROJECT_ROOT, file)
        dst = os.path.join(PROJECT_ROOT, "docs", file)
        if os.path.exists(src):
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
                print(f"✅ Copié: {file} → docs/")
            else:
                print(f"ℹ️  Existe déjà: docs/{file}")
        else:
            print(f"⚠️  Non trouvé: {file}")
    
    # Déplacer Documentations/ vers docs/guides/
    src_dir = os.path.join(PROJECT_ROOT, "Documentations")
    dst_dir = os.path.join(PROJECT_ROOT, "docs", "guides")
    if os.path.exists(src_dir):
        for item in os.listdir(src_dir):
            src_item = os.path.join(src_dir, item)
            dst_item = os.path.join(dst_dir, item)
            if os.path.isfile(src_item) and not os.path.exists(dst_item):
                shutil.copy2(src_item, dst_item)
                print(f"✅ Copié: Documentations/{item} → docs/guides/")
    
    print()


def move_technical_docs():
    """Déplace la documentation technique dans docs/technical/"""
    print("="*80)
    print("DÉPLACEMENT DOCUMENTATION TECHNIQUE")
    print("="*80)
    print()
    
    # Fichiers techniques à déplacer
    tech_files = {
        "ARCHITECTURE_MAJOR_UPDATE.md": "ARCHITECTURE.md",
        "PROJECT_STRUCTURE.md": "PROJECT_STRUCTURE.md",
        "GPU_TEMP_DETECTION.md": "GPU_TEMP_DETECTION.md",
        "TEST_REPORT_FINAL.md": "TEST_REPORT.md",
    }
    
    for src_name, dst_name in tech_files.items():
        src = os.path.join(PROJECT_ROOT, src_name)
        dst = os.path.join(PROJECT_ROOT, "docs", "technical", dst_name)
        if os.path.exists(src):
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
                print(f"✅ Copié: {src_name} → docs/technical/{dst_name}")
            else:
                print(f"ℹ️  Existe déjà: docs/technical/{dst_name}")
        else:
            print(f"⚠️  Non trouvé: {src_name}")
    
    print()


def move_source_code():
    """Déplace le code source dans src/"""
    print("="*80)
    print("DÉPLACEMENT DU CODE SOURCE")
    print("="*80)
    print()
    
    # Déplacer backend/
    src_backend = os.path.join(PROJECT_ROOT, "backend")
    dst_backend = os.path.join(PROJECT_ROOT, "src", "backend")
    if os.path.exists(src_backend) and not os.path.exists(dst_backend):
        shutil.copytree(src_backend, dst_backend)
        print(f"✅ Copié: backend/ → src/backend/")
    else:
        print(f"ℹ️  src/backend/ existe déjà ou backend/ non trouvé")
    
    # Déplacer frontend/
    src_frontend = os.path.join(PROJECT_ROOT, "frontend")
    dst_frontend = os.path.join(PROJECT_ROOT, "src", "frontend")
    if os.path.exists(src_frontend) and not os.path.exists(dst_frontend):
        shutil.copytree(src_frontend, dst_frontend)
        print(f"✅ Copié: frontend/ → src/frontend/")
    else:
        print(f"ℹ️  src/frontend/ existe déjà ou frontend/ non trouvé")
    
    # Déplacer config/
    src_config = os.path.join(PROJECT_ROOT, "config")
    dst_config = os.path.join(PROJECT_ROOT, "src", "config")
    if os.path.exists(src_config) and not os.path.exists(dst_config):
        shutil.copytree(src_config, dst_config)
        print(f"✅ Copié: config/ → src/config/")
    else:
        print(f"ℹ️  src/config/ existe déjà ou config/ non trouvé")
    
    print()


def organize_scripts():
    """Organise les scripts dans des sous-dossiers"""
    print("="*80)
    print("ORGANISATION DES SCRIPTS")
    print("="*80)
    print()
    
    # Scripts de build
    build_scripts = [
        "build.bat",
        "compile.ps1",
    ]
    
    # Scripts de signature
    signing_scripts = [
        "create_self_signed_cert.ps1",
        "sign_executable.ps1",
    ]
    
    # Scripts de vérification
    verification_scripts = [
        "generate_checksum.py",
        "verify_checksum.py",
        "verify_no_powershell.py",
    ]
    
    scripts_dir = os.path.join(PROJECT_ROOT, "scripts")
    
    # Déplacer scripts de build
    for script in build_scripts:
        src = os.path.join(scripts_dir, script)
        dst = os.path.join(scripts_dir, "build", script)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"✅ Copié: scripts/{script} → scripts/build/")
    
    # Déplacer scripts de signature
    for script in signing_scripts:
        src = os.path.join(scripts_dir, script)
        dst = os.path.join(scripts_dir, "signing", script)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"✅ Copié: scripts/{script} → scripts/signing/")
    
    # Déplacer scripts de vérification
    for script in verification_scripts:
        src = os.path.join(scripts_dir, script)
        dst = os.path.join(scripts_dir, "verification", script)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"✅ Copié: scripts/{script} → scripts/verification/")
    
    print()


def list_obsolete_files():
    """Liste les fichiers obsolètes à supprimer manuellement"""
    print("="*80)
    print("FICHIERS OBSOLÈTES À SUPPRIMER MANUELLEMENT")
    print("="*80)
    print()
    
    obsolete_files = [
        "CHANGELOG_MAJOR_UPDATE.md",
        "FINAL_SUMMARY.md",
        "GITHUB_READY.md",
        "RELEASE_READY.md",
        "SUMMARY_MAJOR_UPDATE.md",
        "COMPATIBILITY_UPDATE.md",
        "SECURITY_IMPROVEMENTS.md",
        "test_hardware_monitor.py",
        "5Ghz_Cleaner.spec",
        "CHECKSUMS.txt",
        "SIGNATURE.json",
    ]
    
    print("⚠️  Les fichiers suivants peuvent être supprimés après vérification:")
    print()
    for file in obsolete_files:
        path = os.path.join(PROJECT_ROOT, file)
        if os.path.exists(path):
            print(f"  - {file}")
    
    print()
    print("Note: Vérifiez que les informations importantes ont été migrées avant de supprimer!")
    print()


def create_readme_files():
    """Crée des fichiers README dans les nouveaux dossiers"""
    print("="*80)
    print("CRÉATION DES FICHIERS README")
    print("="*80)
    print()
    
    readmes = {
        "docs/README.md": "# Documentation\n\nCe dossier contient toute la documentation du projet.\n",
        "docs/guides/README.md": "# Guides\n\nGuides détaillés pour l'utilisation et la configuration.\n",
        "docs/technical/README.md": "# Documentation Technique\n\nDocumentation technique et architecture du projet.\n",
        "src/README.md": "# Code Source\n\nCode source de l'application.\n",
        "scripts/build/README.md": "# Scripts de Build\n\nScripts pour compiler l'application.\n",
        "scripts/signing/README.md": "# Scripts de Signature\n\nScripts pour signer l'exécutable.\n",
        "scripts/verification/README.md": "# Scripts de Vérification\n\nScripts pour vérifier l'intégrité et la sécurité.\n",
    }
    
    for path, content in readmes.items():
        full_path = os.path.join(PROJECT_ROOT, path)
        if not os.path.exists(full_path):
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Créé: {path}")
        else:
            print(f"ℹ️  Existe: {path}")
    
    print()


def main():
    """Fonction principale"""
    print()
    print("="*80)
    print("RESTRUCTURATION DU PROJET 5GH'Z CLEANER")
    print("="*80)
    print()
    print("Ce script va réorganiser le projet selon une structure professionnelle.")
    print()
    
    response = input("Continuer? (y/n): ")
    if response.lower() != 'y':
        print("Annulé.")
        return
    
    print()
    
    # Exécuter les étapes
    create_directory_structure()
    move_documentation()
    move_technical_docs()
    move_source_code()
    organize_scripts()
    create_readme_files()
    list_obsolete_files()
    
    print("="*80)
    print("RESTRUCTURATION TERMINÉE")
    print("="*80)
    print()
    print("✅ Structure créée")
    print("✅ Documentation déplacée")
    print("✅ Code source déplacé")
    print("✅ Scripts organisés")
    print()
    print("⚠️  PROCHAINES ÉTAPES:")
    print("1. Vérifier que tout fonctionne")
    print("2. Mettre à jour les imports dans le code")
    print("3. Supprimer les anciens dossiers après vérification")
    print("4. Mettre à jour main.py pour utiliser src/")
    print()


if __name__ == "__main__":
    main()
