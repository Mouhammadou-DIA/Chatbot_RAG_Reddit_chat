"""
Module de g\u00e9n\u00e9ration LLM pour le syst\u00e8me RAG Reddit
Supporte llama-cpp-python (CPU optimis\u00e9) et HuggingFace Transformers
"""

import os
from typing import List, Dict, Optional
from abc import ABC, abstractmethod


class BaseLLMGenerator(ABC):
    """Classe de base pour les g\u00e9n\u00e9rateurs LLM"""

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass


class LlamaCppGenerator(BaseLLMGenerator):
    """
    G\u00e9n\u00e9rateur utilisant llama-cpp-python avec mod\u00e8les GGUF
    Optimis\u00e9 pour CPU - utilise des mod\u00e8les quantifi\u00e9s 4-bit
    """

    def __init__(self, model_path: Optional[str] = None, n_ctx: int = 4096, n_threads: int = None):
        """
        Args:
            model_path: Chemin vers le fichier .gguf du mod\u00e8le
            n_ctx: Taille du contexte (tokens)
            n_threads: Nombre de threads CPU (None = auto)
        """
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_threads = n_threads or os.cpu_count()
        self.model = None
        self._available = None

    def is_available(self) -> bool:
        if self._available is not None:
            return self._available

        try:
            from llama_cpp import Llama
            self._available = True
        except ImportError:
            self._available = False
            print("llama-cpp-python non install\u00e9. Installez avec: pip install llama-cpp-python")

        return self._available

    def load_model(self, model_path: Optional[str] = None):
        """Charger le mod\u00e8le GGUF"""
        if not self.is_available():
            raise RuntimeError("llama-cpp-python n'est pas install\u00e9")

        from llama_cpp import Llama

        path = model_path or self.model_path
        if not path:
            raise ValueError("Aucun chemin de mod\u00e8le sp\u00e9cifi\u00e9")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Mod\u00e8le non trouv\u00e9: {path}")

        print(f"Chargement du mod\u00e8le: {path}")
        print(f"Threads CPU: {self.n_threads}")

        self.model = Llama(
            model_path=path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            verbose=False
        )

        print("Mod\u00e8le charg\u00e9 avec succ\u00e8s!")
        return self

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7,
                 top_p: float = 0.9, stop: List[str] = None) -> str:
        """G\u00e9n\u00e9rer une r\u00e9ponse"""
        if self.model is None:
            raise RuntimeError("Mod\u00e8le non charg\u00e9. Appelez load_model() d'abord.")

        output = self.model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stop=stop or ["</s>", "[/INST]", "User:", "Human:"],
            echo=False
        )

        return output['choices'][0]['text'].strip()


class HuggingFaceGenerator(BaseLLMGenerator):
    """
    G\u00e9n\u00e9rateur utilisant HuggingFace Transformers
    Pour mod\u00e8les plus petits (Phi-2, TinyLlama) en CPU
    """

    def __init__(self, model_name: str = "microsoft/phi-2", device: str = "cpu"):
        self.model_name = model_name
        self.device = device
        self.model = None
        self.tokenizer = None
        self._available = None

    def is_available(self) -> bool:
        if self._available is not None:
            return self._available

        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
            self._available = True
        except ImportError:
            self._available = False
            print("transformers non install\u00e9. Installez avec: pip install transformers torch")

        return self._available

    def load_model(self):
        """Charger le mod\u00e8le HuggingFace"""
        if not self.is_available():
            raise RuntimeError("transformers n'est pas install\u00e9")

        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        print(f"Chargement du mod\u00e8le: {self.model_name}")
        print(f"Device: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )

        # Configuration pour CPU avec m\u00e9moire limit\u00e9e
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,
            device_map=self.device,
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )

        self.model.eval()
        print("Mod\u00e8le charg\u00e9 avec succ\u00e8s!")
        return self

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7,
                 top_p: float = 0.9, **kwargs) -> str:
        """G\u00e9n\u00e9rer une r\u00e9ponse"""
        if self.model is None:
            raise RuntimeError("Mod\u00e8le non charg\u00e9. Appelez load_model() d'abord.")

        import torch

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # D\u00e9coder seulement les nouveaux tokens
        response = self.tokenizer.decode(
            outputs[0][inputs['input_ids'].shape[1]:],
            skip_special_tokens=True
        )

        return response.strip()


class RAGGenerator:
    """
    G\u00e9n\u00e9rateur de r\u00e9ponses pour le syst\u00e8me RAG
    Combine la recherche RAG avec la g\u00e9n\u00e9ration LLM
    """

    # Templates de prompts pour diff\u00e9rents mod\u00e8les
    PROMPT_TEMPLATES = {
        'mistral': """<s>[INST] Tu es un assistant conversationnel bas\u00e9 sur des discussions Reddit.
Utilise le contexte suivant pour r\u00e9pondre \u00e0 la question de l'utilisateur.
R\u00e9ponds de mani\u00e8re naturelle et conversationnelle, comme sur Reddit.
Si le contexte ne contient pas assez d'informations, dis-le clairement.

CONTEXTE:
{context}

QUESTION: {question}

R\u00e9ponds en fran\u00e7ais si la question est en fran\u00e7ais, sinon en anglais. [/INST]""",

        'phi': """Instruct: Tu es un assistant conversationnel. Utilise le contexte des discussions Reddit ci-dessous pour r\u00e9pondre.

Contexte:
{context}

Question: {question}

Output:""",

        'default': """Tu es un assistant conversationnel bas\u00e9 sur des discussions Reddit.

Contexte pertinent:
{context}

Question de l'utilisateur: {question}

R\u00e9ponse:"""
    }

    def __init__(self, llm_generator: BaseLLMGenerator, prompt_template: str = 'mistral'):
        """
        Args:
            llm_generator: Instance du g\u00e9n\u00e9rateur LLM
            prompt_template: Template de prompt \u00e0 utiliser
        """
        self.llm = llm_generator
        self.template_name = prompt_template
        self.prompt_template = self.PROMPT_TEMPLATES.get(
            prompt_template,
            self.PROMPT_TEMPLATES['default']
        )

    def format_context(self, results: List[Dict], max_results: int = 3) -> str:
        """Formater les r\u00e9sultats RAG en contexte pour le LLM"""
        context_parts = []

        for i, result in enumerate(results[:max_results], 1):
            text = result.get('text', '')
            similarity = result.get('similarity', 0) * 100

            # Extraire question et r\u00e9ponse si format\u00e9 ainsi
            if 'Question:' in text and 'R\u00e9ponse:' in text:
                parts = text.split('R\u00e9ponse:', 1)
                question = parts[0].replace('Question:', '').strip()
                answer = parts[1].strip() if len(parts) > 1 else ''

                context_parts.append(
                    f"[Source {i} - Pertinence: {similarity:.0f}%]\n"
                    f"Q: {question}\n"
                    f"R: {answer}"
                )
            else:
                context_parts.append(
                    f"[Source {i} - Pertinence: {similarity:.0f}%]\n{text}"
                )

        return "\n\n".join(context_parts)

    def build_prompt(self, question: str, context: str) -> str:
        """Construire le prompt complet"""
        return self.prompt_template.format(
            context=context,
            question=question
        )

    def generate_response(self, question: str, rag_results: List[Dict],
                         max_context_results: int = 3,
                         max_tokens: int = 512,
                         temperature: float = 0.7) -> Dict:
        """
        G\u00e9n\u00e9rer une r\u00e9ponse bas\u00e9e sur les r\u00e9sultats RAG

        Args:
            question: Question de l'utilisateur
            rag_results: R\u00e9sultats de la recherche RAG
            max_context_results: Nombre max de r\u00e9sultats \u00e0 inclure dans le contexte
            max_tokens: Nombre max de tokens \u00e0 g\u00e9n\u00e9rer
            temperature: Temp\u00e9rature de g\u00e9n\u00e9ration

        Returns:
            Dict avec la r\u00e9ponse g\u00e9n\u00e9r\u00e9e et les m\u00e9tadonn\u00e9es
        """
        import time
        start_time = time.time()

        # Formater le contexte
        context = self.format_context(rag_results, max_context_results)

        # Construire le prompt
        prompt = self.build_prompt(question, context)

        # G\u00e9n\u00e9rer la r\u00e9ponse
        try:
            response = self.llm.generate(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            generation_time = time.time() - start_time

            return {
                'question': question,
                'response': response,
                'context_used': context,
                'num_sources': min(len(rag_results), max_context_results),
                'generation_time': generation_time,
                'success': True
            }

        except Exception as e:
            return {
                'question': question,
                'response': f"Erreur lors de la g\u00e9n\u00e9ration: {str(e)}",
                'context_used': context,
                'num_sources': 0,
                'generation_time': 0,
                'success': False,
                'error': str(e)
            }


def download_mistral_gguf(output_dir: str = "models") -> str:
    """
    T\u00e9l\u00e9charger le mod\u00e8le Mistral-7B-Instruct au format GGUF

    Utilise huggingface_hub pour t\u00e9l\u00e9charger le mod\u00e8le quantifi\u00e9 Q4_K_M
    qui offre un bon compromis qualit\u00e9/performance pour CPU
    """
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print("Installez huggingface_hub: pip install huggingface_hub")
        return None

    os.makedirs(output_dir, exist_ok=True)

    # Mod\u00e8le quantifi\u00e9 Q4_K_M de TheBloke (tr\u00e8s populaire)
    repo_id = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
    filename = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"

    print(f"T\u00e9l\u00e9chargement de {filename}...")
    print("Cela peut prendre plusieurs minutes (fichier ~4.4GB)")

    model_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=output_dir,
        local_dir_use_symlinks=False
    )

    print(f"Mod\u00e8le t\u00e9l\u00e9charg\u00e9: {model_path}")
    return model_path


def create_generator(backend: str = "llama-cpp", model_path: str = None,
                     model_name: str = None) -> BaseLLMGenerator:
    """
    Factory function pour cr\u00e9er un g\u00e9n\u00e9rateur LLM

    Args:
        backend: "llama-cpp" ou "huggingface"
        model_path: Chemin vers le mod\u00e8le GGUF (pour llama-cpp)
        model_name: Nom du mod\u00e8le HuggingFace (pour huggingface)
    """
    if backend == "llama-cpp":
        generator = LlamaCppGenerator(model_path=model_path)
        if generator.is_available() and model_path:
            generator.load_model()
        return generator

    elif backend == "huggingface":
        generator = HuggingFaceGenerator(
            model_name=model_name or "microsoft/phi-2",
            device="cpu"
        )
        if generator.is_available():
            generator.load_model()
        return generator

    else:
        raise ValueError(f"Backend inconnu: {backend}. Utilisez 'llama-cpp' ou 'huggingface'")


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("="*70)
    print("TEST DU MODULE LLM GENERATOR")
    print("="*70)

    # V\u00e9rifier les backends disponibles
    print("\n1. V\u00e9rification des backends disponibles...")

    llama_gen = LlamaCppGenerator()
    print(f"   - llama-cpp-python: {'Disponible' if llama_gen.is_available() else 'Non install\u00e9'}")

    hf_gen = HuggingFaceGenerator()
    print(f"   - HuggingFace Transformers: {'Disponible' if hf_gen.is_available() else 'Non install\u00e9'}")

    print("\n2. Pour utiliser ce module:")
    print("""
    # Option A: Avec llama-cpp-python (recommand\u00e9 pour CPU)
    from llm_generator import LlamaCppGenerator, RAGGenerator, download_mistral_gguf

    # T\u00e9l\u00e9charger le mod\u00e8le (une seule fois)
    model_path = download_mistral_gguf("models")

    # Cr\u00e9er le g\u00e9n\u00e9rateur
    llm = LlamaCppGenerator(model_path=model_path)
    llm.load_model()

    # Int\u00e9grer avec RAG
    rag_gen = RAGGenerator(llm, prompt_template='mistral')
    response = rag_gen.generate_response(question, rag_results)

    # Option B: Avec HuggingFace (mod\u00e8le plus petit)
    from llm_generator import HuggingFaceGenerator, RAGGenerator

    llm = HuggingFaceGenerator(model_name="microsoft/phi-2")
    llm.load_model()

    rag_gen = RAGGenerator(llm, prompt_template='phi')
    response = rag_gen.generate_response(question, rag_results)
    """)
