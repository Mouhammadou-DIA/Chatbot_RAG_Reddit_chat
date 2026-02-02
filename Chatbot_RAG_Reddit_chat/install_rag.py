
#!/usr/bin/env python3
"""
Script d'installation et de lancement automatique
Reddit RAG Chatbot
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class ChatbotInstaller:
    """Installation et configuration automatique du chatbot"""
    
    def __init__(self):
        self.project_dir = Path.cwd()
        self.required_files = [
            'reddit_data/raw/casual_data_windows.csv',
            'reddit_rag_optimized.py',
            'reddit_rag_ui.py'
        ]
        self.required_packages = [
            'pandas',
            'numpy',
            'sentence-transformers',
            'faiss-cpu',
            'gradio',
            'tqdm'
        ]
        
    def print_header(self, text):
        """Afficher un en-tête"""
        print("\n" + "="*70)
        print(f"  {text}")
        print("="*70 + "\n")
    
    def print_step(self, step, text):
        """Afficher une étape"""
        print(f"[Étape {step}] {text}")
    
    def check_python_version(self):
        """Vérifier la version de Python"""
        self.print_step(1, "Vérification de la version Python...")
        
        version = sys.version_info
        print(f"   Python {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("   ❌ Python 3.8+ requis!")
            print("   Téléchargez Python depuis: https://www.python.org/downloads/")
            return False
        
        print("   ✅ Version compatible")
        return True
    
    def check_files(self):
        """Vérifier la présence des fichiers requis"""
        self.print_step(2, "Vérification des fichiers...")
        
        missing_files = []
        for file in self.required_files:
            if not Path(file).exists():
                missing_files.append(file)
                print(f"   ❌ Fichier manquant: {file}")
            else:
                file_size = Path(file).stat().st_size / (1024**2)  # MB
                print(f"   ✅ {file} ({file_size:.1f} MB)")
        
        if missing_files:
            print("\n   ⚠️  Fichiers manquants:")
            for f in missing_files:
                print(f"      - {f}")
            return False
        
        return True
    
    def install_packages(self):
        """Installer les packages Python requis"""
        self.print_step(3, "Installation des dépendances...")
        
        print("   📦 Packages à installer:")
        for pkg in self.required_packages:
            print(f"      - {pkg}")
        
        print("\n   Installation en cours (cela peut prendre quelques minutes)...\n")
        
        try:
            for pkg in self.required_packages:
                print(f"   Installation de {pkg}...")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-q", pkg],
                    stdout=subprocess.DEVNULL
                )
                print(f"   ✅ {pkg} installé")
            
            print("\n   ✅ Toutes les dépendances sont installées!")
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"\n   ❌ Erreur lors de l'installation: {e}")
            print("   Essayez manuellement: pip install [package]")
            return False
    
    def verify_installation(self):
        """Vérifier que les packages sont bien installés"""
        self.print_step(4, "Vérification de l'installation...")
        
        test_imports = {
            'pandas': 'import pandas as pd',
            'numpy': 'import numpy as np',
            'sentence_transformers': 'from sentence_transformers import SentenceTransformer',
            'faiss': 'import faiss',
            'gradio': 'import gradio as gr',
            'tqdm': 'from tqdm import tqdm'
        }
        
        all_ok = True
        for name, import_stmt in test_imports.items():
            try:
                exec(import_stmt)
                print(f"   ✅ {name}")
            except ImportError as e:
                print(f"   ❌ {name}: {e}")
                all_ok = False
        
        return all_ok
    
    def check_existing_system(self):
        """Vérifier si le système RAG existe déjà"""
        self.print_step(5, "Vérification du système RAG...")
        
        required_files = [
            'reddit_optimized_rag_index.faiss',
            'reddit_optimized_rag_chunks.pkl',
            'reddit_optimized_rag_metadata.json'
        ]
        
        all_exist = all(Path(f).exists() for f in required_files)
        
        if all_exist:
            print("   ✅ Système RAG déjà construit")
            
            # Afficher les infos
            import json
            with open('reddit_optimized_rag_metadata.json', 'r') as f:
                metadata = json.load(f)
            
            print(f"\n   📊 Informations:")
            print(f"      - Conversations: {metadata['num_conversations']:,}")
            print(f"      - Chunks: {metadata['num_chunks']:,}")
            
            return True
        else:
            print("   ⚠️  Système RAG non trouvé")
            print("   Le système doit être construit (15-20 minutes)")
            return False
    
    def build_system(self):
        """Construire le système RAG"""
        self.print_step(6, "Construction du système RAG...")
        
        print("\n   ⏱️  Temps estimé: 15-20 minutes")
        print("   💻 Processus intensif en CPU")
        print("\n   Voulez-vous continuer? (o/n): ", end='')
        
        response = input().strip().lower()
        
        if response != 'o':
            print("\n   ⏸️  Construction annulée")
            print("   Vous pouvez construire plus tard avec:")
            print("   >>> from reddit_rag_optimized import run_optimized_pipeline")
            print("   >>> rag = run_optimized_pipeline('casual_data_windows.csv')")
            return False
        
        print("\n   🚀 Démarrage de la construction...\n")
        
        try:
            # Import ici pour éviter l'erreur si pas encore installé
            from reddit_rag_optimized import run_optimized_pipeline
            
            start_time = time.time()
            rag = run_optimized_pipeline('casual_data_windows.csv')
            elapsed = time.time() - start_time
            
            print(f"\n   ✅ Système construit en {elapsed/60:.1f} minutes!")
            return True
        
        except Exception as e:
            print(f"\n   ❌ Erreur lors de la construction: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def launch_interface(self):
        """Lancer l'interface utilisateur"""
        self.print_step(7, "Lancement de l'interface...")
        
        print("\n   🌐 Démarrage du serveur Gradio...")
        
        try:
            from reddit_rag_ui import launch_ui
            from reddit_rag_optimized import OptimizedRedditRAG
            
            # Charger le système
            print("   📂 Chargement du système RAG...")
            rag = OptimizedRedditRAG()
            rag.load('reddit_optimized_rag')
            
            print("   ✅ Système chargé!")
            print("\n" + "="*70)
            print("   🎉 CHATBOT PRÊT!")
            print("="*70)
            print("\n   📍 Accédez à l'interface:")
            print("      - Local: http://localhost:7860")
            print("      - Réseau: http://[votre-ip]:7860")
            print("\n   💡 Appuyez sur Ctrl+C pour arrêter\n")
            
            # Lancer
            launch_ui(rag, share=False, server_port=7860)
        
        except KeyboardInterrupt:
            print("\n\n   👋 Arrêt du serveur...")
            sys.exit(0)
        
        except Exception as e:
            print(f"\n   ❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run(self):
        """Exécuter l'installation complète"""
        self.print_header("🤖 REDDIT RAG CHATBOT - INSTALLATION AUTOMATIQUE")
        
        # 1. Vérifier Python
        if not self.check_python_version():
            return False
        
        # 2. Vérifier les fichiers
        if not self.check_files():
            print("\n⚠️  Placez tous les fichiers requis dans le même dossier")
            return False
        
        # 3. Installer les packages
        print("\n   Voulez-vous installer les dépendances? (o/n): ", end='')
        if input().strip().lower() == 'o':
            if not self.install_packages():
                return False
        else:
            print("   ⏭️  Installation des dépendances ignorée")
        
        # 4. Vérifier l'installation
        if not self.verify_installation():
            print("\n   ❌ Certains packages ne sont pas installés correctement")
            return False
        
        # 5. Vérifier le système RAG
        system_exists = self.check_existing_system()
        
        # 6. Construire si nécessaire
        if not system_exists:
            if not self.build_system():
                print("\n   ⚠️  Le système n'a pas été construit")
                print("   Vous pouvez le faire plus tard et relancer ce script")
                return False
        
        # 7. Lancer l'interface
        print("\n   Voulez-vous lancer l'interface maintenant? (o/n): ", end='')
        if input().strip().lower() == 'o':
            self.launch_interface()
        else:
            print("\n   ✅ Installation terminée!")
            print("\n   Pour lancer plus tard:")
            print("   >>> python reddit_rag_ui.py")
        
        return True


class QuickLauncher:
    """Lancement rapide si le système existe déjà"""
    
    @staticmethod
    def check_system_ready():
        """Vérifier si le système est prêt"""
        required_files = [
            'reddit_optimized_rag_index.faiss',
            'reddit_optimized_rag_chunks.pkl',
            'reddit_rag_optimized.py',
            'reddit_rag_ui.py'
        ]
        
        return all(Path(f).exists() for f in required_files)
    
    @staticmethod
    def launch():
        """Lancement rapide"""
        print("="*70)
        print("  🚀 LANCEMENT RAPIDE - REDDIT RAG CHATBOT")
        print("="*70)
        
        if not QuickLauncher.check_system_ready():
            print("\n❌ Système non prêt. Lancez l'installation complète avec:")
            print(">>> python install_and_run.py --install")
            return False
        
        try:
            from reddit_rag_ui import launch_ui
            from reddit_rag_optimized import OptimizedRedditRAG
            
            print("\n📂 Chargement du système...")
            rag = OptimizedRedditRAG()
            rag.load('reddit_optimized_rag')
            
            print("✅ Système chargé!")
            print("\n🌐 Lancement de l'interface...")
            print("\n   URL: http://localhost:7860")
            print("   Appuyez sur Ctrl+C pour arrêter\n")
            
            launch_ui(rag, share=False, server_port=7860)
        
        except KeyboardInterrupt:
            print("\n\n👋 Arrêt du serveur...")
        
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Point d'entrée principal"""
    
    # Vérifier les arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--install':
            # Installation complète
            installer = ChatbotInstaller()
            installer.run()
        
        elif sys.argv[1] == '--quick' or sys.argv[1] == '--launch':
            # Lancement rapide
            QuickLauncher.launch()
        
        elif sys.argv[1] == '--help':
            print("""
Usage: python install_and_run.py [OPTION]

Options:
  --install    Installation complète (première fois)
  --quick      Lancement rapide (si déjà installé)
  --launch     Alias pour --quick
  --help       Afficher cette aide

Sans option: Mode interactif
            """)
        
        else:
            print(f"Option inconnue: {sys.argv[1]}")
            print("Utilisez --help pour voir les options")
    
    else:
        # Mode interactif
        print("="*70)
        print("  🤖 REDDIT RAG CHATBOT")
        print("="*70)
        print("\nQue voulez-vous faire?")
        print("  1. Installation complète (première fois)")
        print("  2. Lancement rapide (déjà installé)")
        print("  3. Quitter")
        
        choice = input("\nVotre choix (1/2/3): ").strip()
        
        if choice == '1':
            installer = ChatbotInstaller()
            installer.run()
        
        elif choice == '2':
            QuickLauncher.launch()
        
        elif choice == '3':
            print("👋 Au revoir!")
        
        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    main()