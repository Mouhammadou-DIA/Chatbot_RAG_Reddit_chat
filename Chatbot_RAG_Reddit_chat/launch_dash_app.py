#!/usr/bin/env python3
"""
Script de lancement de l'application Dash Reddit RAG Chatbot
Vérifie les dépendances et lance l'application
"""

import sys
import os
import subprocess
from pathlib import Path


class DashAppLauncher:
    """Gestionnaire de lancement de l'application"""
    
    def __init__(self):
        self.required_packages = [
            'dash',
            'dash-bootstrap-components',
            'plotly',
            'pandas',
            'numpy'
        ]
        
        self.rag_files = [
            'reddit_optimized_rag_index.faiss',
            'reddit_optimized_rag_chunks.pkl',
            'reddit_optimized_rag_metadata.json'
        ]
    
    def print_header(self, text):
        """Afficher un en-tête"""
        print("\n" + "="*70)
        print(f"  {text}")
        print("="*70 + "\n")
    
    def check_packages(self):
        """Vérifier les packages Python"""
        self.print_header("VÉRIFICATION DES DÉPENDANCES")
        
        missing = []
        for package in self.required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"✅ {package}")
            except ImportError:
                print(f"❌ {package} (non installé)")
                missing.append(package)
        
        if missing:
            print(f"\n⚠️  Packages manquants: {', '.join(missing)}")
            print("\nVoulez-vous les installer maintenant? (o/n): ", end='')
            
            if input().strip().lower() == 'o':
                self.install_packages(missing)
                return True
            else:
                print("\n❌ Installation annulée. L'application ne peut pas démarrer.")
                return False
        
        return True
    
    def install_packages(self, packages):
        """Installer les packages manquants"""
        print(f"\n📦 Installation de {len(packages)} package(s)...")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-q"
            ] + packages)
            print("✅ Installation réussie!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation: {e}")
            return False
        
        return True
    
    def check_rag_system(self):
        """Vérifier la présence du système RAG"""
        self.print_header("VÉRIFICATION DU SYSTÈME RAG")
        
        all_present = True
        for file in self.rag_files:
            if Path(file).exists():
                print(f"✅ {file}")
            else:
                print(f"❌ {file} (manquant)")
                all_present = False
        
        if not all_present:
            print("\n⚠️  Système RAG incomplet!")
            print("\nOptions:")
            print("1. Construire le système RAG maintenant (15-20 min)")
            print("2. Quitter et construire manuellement")
            
            choice = input("\nVotre choix (1/2): ").strip()
            
            if choice == "1":
                return self.build_rag_system()
            else:
                print("\n💡 Pour construire le système RAG:")
                print(">>> python reddit_rag_optimized.py")
                return False
        
        # Vérifier les métadonnées
        try:
            import json
            with open('reddit_optimized_rag_metadata.json', 'r') as f:
                metadata = json.load(f)
            
            print(f"\n📊 Informations du système:")
            print(f"   - Conversations: {metadata.get('num_conversations', 0):,}")
            print(f"   - Chunks indexés: {metadata.get('num_chunks', 0):,}")
            print(f"   - Modèle: {metadata.get('model_name', 'N/A')}")
        except Exception as e:
            print(f"\n⚠️  Impossible de lire les métadonnées: {e}")
        
        return True
    
    def build_rag_system(self):
        """Construire le système RAG"""
        print("\n🚀 Construction du système RAG...")
        print("⏱️  Temps estimé: 15-20 minutes\n")
        
        try:
            from reddit_rag_optimized import run_pipeline
            
            # Vérifier la présence du fichier CSV
            csv_path = 'reddit_data/raw/casual_data_windows.csv'
            if not Path(csv_path).exists():
                print(f"❌ Fichier de données introuvable: {csv_path}")
                print("\n💡 Assurez-vous que le fichier est au bon emplacement")
                return False
            
            rag = run_pipeline(csv_path, save_prefix='reddit_optimized_rag')
            print("\n✅ Système RAG construit avec succès!")
            return True
            
        except ImportError:
            print("❌ Module reddit_rag_optimized.py introuvable")
            return False
        except Exception as e:
            print(f"❌ Erreur lors de la construction: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def check_llm_availability(self):
        """Vérifier la disponibilité du LLM"""
        self.print_header("VÉRIFICATION DU LLM (OPTIONNEL)")
        
        try:
            from llm_generator import LLM_AVAILABLE
            
            if LLM_AVAILABLE:
                print("✅ Module LLM disponible")
                print("\n💡 Pour activer le mode génératif:")
                print("   1. Configurez le LLM: python llm_setup.py")
                print("   2. Activez l'option dans l'interface")
            else:
                print("ℹ️  Module LLM non disponible (mode RAG uniquement)")
                print("\n💡 Pour activer le LLM:")
                print("   pip install llama-cpp-python transformers")
        
        except ImportError:
            print("ℹ️  Module llm_generator.py non trouvé (mode RAG uniquement)")
        
        print("\nL'application fonctionnera en mode RAG classique")
        return True
    
    def launch_app(self, debug=False, port=8050, host="127.0.0.1"):
        """Lancer l'application Dash"""
        self.print_header("LANCEMENT DE L'APPLICATION")
        
        print(f"🌐 Serveur: http://{host}:{port}")
        print(f"🔧 Mode debug: {'Activé' if debug else 'Désactivé'}")
        print("\n💡 Appuyez sur Ctrl+C pour arrêter\n")
        print("-"*70 + "\n")
        
        try:
            # Importer et lancer l'app
            import reddit_rag_dash_app
            reddit_rag_dash_app.app.run(
                debug=debug,
                host=host,
                port=port
            )
        
        except KeyboardInterrupt:
            print("\n\n👋 Arrêt de l'application...")
            sys.exit(0)
        
        except Exception as e:
            print(f"\n❌ Erreur lors du lancement: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run(self, debug=False, port=8050, host="127.0.0.1"):
        """Exécuter le processus complet de lancement"""
        self.print_header("🤖 REDDIT RAG CHATBOT - DASH APPLICATION")
        
        # 1. Vérifier les packages
        if not self.check_packages():
            return False
        
        # 2. Vérifier le système RAG
        if not self.check_rag_system():
            return False
        
        # 3. Vérifier le LLM (optionnel)
        self.check_llm_availability()
        
        # 4. Lancer l'application
        print("\n" + "="*70)
        input("Appuyez sur Entrée pour lancer l'application...")
        
        self.launch_app(debug=debug, port=port, host=host)
        
        return True


def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Reddit RAG Chatbot - Application Dash"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8050, 
        help="Port du serveur (défaut: 8050)"
    )
    parser.add_argument(
        "--host", 
        type=str, 
        default="127.0.0.1", 
        help="Host du serveur (défaut: 127.0.0.1)"
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Activer le mode debug"
    )
    parser.add_argument(
        "--quick", 
        action="store_true", 
        help="Lancement rapide sans vérifications"
    )
    
    args = parser.parse_args()
    
    if args.quick:
        # Lancement rapide
        print("🚀 Lancement rapide...")
        try:
            import reddit_rag_dash_app
            reddit_rag_dash_app.app.run(
                debug=args.debug,
                host=args.host,
                port=args.port
            )
        except KeyboardInterrupt:
            print("\n👋 Au revoir!")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
    else:
        # Lancement avec vérifications
        launcher = DashAppLauncher()
        launcher.run(
            debug=args.debug,
            port=args.port,
            host=args.host
        )


if __name__ == "__main__":
    main()
