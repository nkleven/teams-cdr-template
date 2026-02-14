"""Text analysis tool for AI agent."""

import re
from typing import Any, Dict
from collections import Counter
from .base import BaseTool, ToolDefinition


class TextAnalysisTool(BaseTool):
    """Tool for analyzing text content."""
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="text_analysis",
            description="Analyze text for statistics, sentiment, readability, and patterns",
            input_schema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze"
                    },
                    "analysis_type": {
                        "type": "string",
                        "enum": ["statistics", "sentiment", "readability", "keywords", "all"],
                        "description": "Type of analysis to perform",
                        "default": "all"
                    }
                },
                "required": ["text"]
            }
        )
    
    async def execute(self, text: str, analysis_type: str = "all") -> Dict[str, Any]:
        """Execute text analysis.
        
        Args:
            text: Text to analyze
            analysis_type: Type of analysis
            
        Returns:
            Analysis results
        """
        results = {}
        
        if analysis_type in ("statistics", "all"):
            results["statistics"] = self._analyze_statistics(text)
        
        if analysis_type in ("sentiment", "all"):
            results["sentiment"] = self._analyze_sentiment(text)
        
        if analysis_type in ("readability", "all"):
            results["readability"] = self._analyze_readability(text)
        
        if analysis_type in ("keywords", "all"):
            results["keywords"] = self._extract_keywords(text)
        
        return results
    
    def _analyze_statistics(self, text: str) -> Dict[str, Any]:
        """Calculate text statistics."""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        characters = len(text)
        characters_no_spaces = len(text.replace(' ', ''))
        word_count = len(words)
        sentence_count = len(sentences)
        
        avg_word_length = characters_no_spaces / word_count if word_count > 0 else 0
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        return {
            "characters": characters,
            "characters_no_spaces": characters_no_spaces,
            "words": word_count,
            "sentences": sentence_count,
            "paragraphs": text.count('\n\n') + 1,
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2)
        }
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Simple sentiment analysis based on keywords."""
        text_lower = text.lower()
        
        # Simple sentiment keywords
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
                         'love', 'happy', 'joy', 'beautiful', 'perfect', 'best', 'awesome'}
        negative_words = {'bad', 'terrible', 'awful', 'horrible', 'hate', 'sad', 'angry',
                         'worst', 'poor', 'disappointing', 'failed', 'error', 'problem'}
        
        words = set(re.findall(r'\b\w+\b', text_lower))
        positive_count = len(words & positive_words)
        negative_count = len(words & negative_words)
        
        total = positive_count + negative_count
        if total == 0:
            sentiment = "neutral"
            score = 0
        else:
            score = (positive_count - negative_count) / total
            if score > 0.2:
                sentiment = "positive"
            elif score < -0.2:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "score": round(score, 3),
            "positive_words": positive_count,
            "negative_words": negative_count,
            "confidence": "low" if total < 3 else "medium" if total < 6 else "high"
        }
    
    def _analyze_readability(self, text: str) -> Dict[str, Any]:
        """Calculate readability metrics."""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        word_count = len(words)
        sentence_count = len(sentences) if sentences else 1
        
        # Count syllables (approximate)
        def count_syllables(word: str) -> int:
            word = word.lower()
            vowels = 'aeiouy'
            syllable_count = 0
            previous_was_vowel = False
            
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not previous_was_vowel:
                    syllable_count += 1
                previous_was_vowel = is_vowel
            
            # Adjust for silent e
            if word.endswith('e'):
                syllable_count -= 1
            
            return max(1, syllable_count)
        
        total_syllables = sum(count_syllables(word) for word in words)
        
        # Flesch Reading Ease
        if word_count > 0 and sentence_count > 0:
            avg_sentence_length = word_count / sentence_count
            avg_syllables = total_syllables / word_count
            flesch_score = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables
            flesch_score = max(0, min(100, flesch_score))  # Clamp between 0-100
        else:
            flesch_score = 0
        
        # Interpret score
        if flesch_score >= 90:
            difficulty = "Very Easy"
        elif flesch_score >= 80:
            difficulty = "Easy"
        elif flesch_score >= 70:
            difficulty = "Fairly Easy"
        elif flesch_score >= 60:
            difficulty = "Standard"
        elif flesch_score >= 50:
            difficulty = "Fairly Difficult"
        elif flesch_score >= 30:
            difficulty = "Difficult"
        else:
            difficulty = "Very Difficult"
        
        return {
            "flesch_reading_ease": round(flesch_score, 2),
            "difficulty": difficulty,
            "total_syllables": total_syllables,
            "avg_syllables_per_word": round(total_syllables / word_count, 2) if word_count > 0 else 0
        }
    
    def _extract_keywords(self, text: str) -> Dict[str, Any]:
        """Extract keywords from text."""
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                     'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                     'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
                     'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'them'}
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter stop words
        filtered_words = [word for word in words if word not in stop_words]
        
        # Count frequency
        word_freq = Counter(filtered_words)
        
        # Get top keywords
        top_keywords = word_freq.most_common(10)
        
        return {
            "top_keywords": [{"word": word, "count": count} for word, count in top_keywords],
            "unique_words": len(word_freq),
            "total_words": len(words)
        }
