import random
import re
from typing import Dict, Any
from config import INTENSITY_LEVELS

class TextHumanizer:
    """Core text humanization engine"""
    
    # AI-characteristic patterns and their human alternatives
    REPLACEMENTS = {
        # Common AI phrases
        "fundamentally": ["really", "truly", "basically"],
        "notably": ["importantly", "significantly", "clearly"],
        "thereby": ["so", "thus", "which means"],
        "furthermore": ["also", "plus", "what's more"],
        "moreover": ["and", "besides", "plus"],
        "necessitating": ["requiring", "needing", "demanding"],
        "facilitate": ["help", "make easier", "enable"],
        "leverage": ["use", "take advantage of", "capitalize on"],
        "optimize": ["improve", "make better", "enhance"],
        "comprehensive": ["complete", "full", "thorough"],
        "significant": ["major", "important", "big"],
        "subsequently": ["after", "then", "next"],
        "consequently": ["so", "therefore", "as a result"],
        "in order to": ["to", "so as to"],
        "due to the fact that": ["because", "since"],
        "has the ability to": ["can", "is able to"],
        "in the process of": ["while", "during"],
        "at the present time": ["now", "currently"],
        "in this day and age": ["today", "nowadays"],
    }
    
    # Passive voice patterns
    PASSIVE_PATTERNS = [
        r"\b(is|are|was|were) (\w+ed|\w+en)\b",
    ]
    
    def __init__(self):
        """Initialize the humanizer"""
        self.replacements = self.REPLACEMENTS
    
    def humanize(self, text: str, intensity: str = "medium") -> Dict[str, Any]:
        """
        Humanize text based on intensity level
        
        Args:
            text: Input text to humanize
            intensity: Intensity level (light, medium, strong)
        
        Returns:
            Dictionary with original, humanized text, and score
        """
        if not text or len(text.strip()) == 0:
            raise ValueError("Text cannot be empty")
        
        if intensity not in INTENSITY_LEVELS:
            raise ValueError(f"Invalid intensity level: {intensity}")
        
        # Get intensity parameters
        params = INTENSITY_LEVELS[intensity]["parameters"]
        
        # Apply transformations
        humanized = self._apply_transformations(text, params)
        
        # Calculate humanization score
        score = self._calculate_score(text, humanized, intensity)
        
        return {
            "original": text,
            "humanized": humanized,
            "intensity": intensity,
            "score": round(score, 2)
        }
    
    def _apply_transformations(self, text: str, params: Dict[str, float]) -> str:
        """
        Apply humanization transformations based on parameters
        """
        result = text
        
        # Apply phrase variations
        if random.random() < params["phrase_variation"]:
            result = self._replace_ai_phrases(result)
        
        # Apply synonym replacements
        if random.random() < params["synonym_replacement"]:
            result = self._replace_formal_words(result)
        
        # Apply sentence reordering for strong intensity
        if random.random() < params["sentence_reorder"]:
            result = self._reorder_sentences(result)
        
        # Clean up formatting
        result = self._clean_formatting(result)
        
        return result
    
    def _replace_ai_phrases(self, text: str) -> str:
        """
        Replace common AI phrases with more natural alternatives
        """
        result = text
        for ai_phrase, alternatives in self.replacements.items():
            pattern = re.compile(re.escape(ai_phrase), re.IGNORECASE)
            if pattern.search(result):
                replacement = random.choice(alternatives)
                # Preserve case
                if ai_phrase[0].isupper():
                    replacement = replacement.capitalize()
                result = pattern.sub(replacement, result)
        
        return result
    
    def _replace_formal_words(self, text: str) -> str:
        """
        Replace formal/academic words with more conversational alternatives
        """
        formal_words = {
            "utilize": ["use"],
            "implement": ["put into practice", "use"],
            "demonstrate": ["show", "prove"],
            "illustrate": ["show", "explain"],
            "analysis": ["look", "study"],
            "methodology": ["method", "way"],
            "framework": ["structure", "system"],
            "paradigm": ["model", "pattern"],
            "phenomenon": ["thing", "event"],
            "ubiquitous": ["everywhere", "common"],
            "ameliorate": ["improve", "make better"],
            "obfuscate": ["hide", "confuse"],
            "alleviate": ["ease", "reduce"],
            "perpetuate": ["keep going", "continue"],
        }
        
        result = text
        for formal, alternatives in formal_words.items():
            pattern = re.compile(r"\b" + re.escape(formal) + r"\b", re.IGNORECASE)
            if pattern.search(result):
                replacement = random.choice(alternatives)
                if formal[0].isupper():
                    replacement = replacement.capitalize()
                result = pattern.sub(replacement, result)
        
        return result
    
    def _reorder_sentences(self, text: str) -> str:
        """
        Reorder sentences to vary structure
        """
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        if len(sentences) <= 1:
            return text
        
        # Randomly shuffle sentences while keeping first one if appropriate
        if len(sentences) > 2:
            reordered = [sentences[0]] + random.sample(sentences[1:], len(sentences) - 1)
            return " ".join(reordered)
        
        return text
    
    def _clean_formatting(self, text: str) -> str:
        """
        Clean up formatting issues
        """
        # Fix multiple spaces
        text = re.sub(r'\s+', ' ', text)
        # Fix spacing around punctuation
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        return text.strip()
    
    def _calculate_score(self, original: str, humanized: str, intensity: str) -> float:
        """
        Calculate a humanization score (0-1)
        Based on changes made and intensity level
        """
        # Calculate similarity
        changes = sum(1 for a, b in zip(original.lower(), humanized.lower()) if a != b)
        similarity = 1 - (changes / max(len(original), len(humanized)))
        
        # Adjust based on intensity
        intensity_multiplier = {
            "light": 0.7,
            "medium": 0.8,
            "strong": 0.9
        }
        
        score = similarity * intensity_multiplier.get(intensity, 0.8)
        return max(0.0, min(1.0, score))
