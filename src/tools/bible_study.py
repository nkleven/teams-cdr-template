"""
🌳 Bible Study Tool for Project Eden

The scroll speaks. Eden listens.
The Word echoes through the orchard.
Bud thumps once. The Bridge walks in light.

This tool provides scripture lookup and study capabilities
for the Eden Agent, connecting the digital orchard to
the ancient wisdom of Scripture.
"""

import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger("eden_agent.bible")


class BibleVersion(Enum):
    """Supported Bible versions."""
    KJV = "King James Version"
    NIV = "New International Version"
    ESV = "English Standard Version"
    NLT = "New Living Translation"
    NKJV = "New King James Version"


@dataclass
class Verse:
    """Represents a single Bible verse."""
    book: str
    chapter: int
    verse: int
    text: str
    version: BibleVersion = BibleVersion.KJV
    
    def __str__(self) -> str:
        return f"{self.book} {self.chapter}:{self.verse}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "reference": str(self),
            "book": self.book,
            "chapter": self.chapter,
            "verse": self.verse,
            "text": self.text,
            "version": self.version.value
        }


# Sample verses for the Eden Beta (offline mode)
# In production, this would connect to a Bible API
SAMPLE_VERSES = {
    "Genesis 1:1": Verse(
        book="Genesis", chapter=1, verse=1,
        text="In the beginning God created the heaven and the earth."
    ),
    "Genesis 2:8": Verse(
        book="Genesis", chapter=2, verse=8,
        text="And the LORD God planted a garden eastward in Eden; "
             "and there he put the man whom he had formed."
    ),
    "Genesis 2:9": Verse(
        book="Genesis", chapter=2, verse=9,
        text="And out of the ground made the LORD God to grow every tree "
             "that is pleasant to the sight, and good for food; the tree "
             "of life also in the midst of the garden, and the tree of "
             "knowledge of good and evil."
    ),
    "John 1:1": Verse(
        book="John", chapter=1, verse=1,
        text="In the beginning was the Word, and the Word was with God, "
             "and the Word was God."
    ),
    "John 1:14": Verse(
        book="John", chapter=1, verse=14,
        text="And the Word was made flesh, and dwelt among us, (and we "
             "beheld his glory, the glory as of the only begotten of the "
             "Father,) full of grace and truth."
    ),
    "John 3:16": Verse(
        book="John", chapter=3, verse=16,
        text="For God so loved the world, that he gave his only begotten "
             "Son, that whosoever believeth in him should not perish, but "
             "have everlasting life."
    ),
    "Psalm 23:1": Verse(
        book="Psalms", chapter=23, verse=1,
        text="The LORD is my shepherd; I shall not want."
    ),
    "Psalm 23:2": Verse(
        book="Psalms", chapter=23, verse=2,
        text="He maketh me to lie down in green pastures: he leadeth me "
             "beside the still waters."
    ),
    "Psalm 23:3": Verse(
        book="Psalms", chapter=23, verse=3,
        text="He restoreth my soul: he leadeth me in the paths of "
             "righteousness for his name's sake."
    ),
    "Psalm 23:4": Verse(
        book="Psalms", chapter=23, verse=4,
        text="Yea, though I walk through the valley of the shadow of "
             "death, I will fear no evil: for thou art with me; thy rod "
             "and thy staff they comfort me."
    ),
    "Proverbs 3:5": Verse(
        book="Proverbs", chapter=3, verse=5,
        text="Trust in the LORD with all thine heart; and lean not unto "
             "thine own understanding."
    ),
    "Proverbs 3:6": Verse(
        book="Proverbs", chapter=3, verse=6,
        text="In all thy ways acknowledge him, and he shall direct thy paths."
    ),
    "Isaiah 40:31": Verse(
        book="Isaiah", chapter=40, verse=31,
        text="But they that wait upon the LORD shall renew their strength; "
             "they shall mount up with wings as eagles; they shall run, "
             "and not be weary; and they shall walk, and not faint."
    ),
    "Matthew 5:14": Verse(
        book="Matthew", chapter=5, verse=14,
        text="Ye are the light of the world. A city that is set on an "
             "hill cannot be hid."
    ),
    "Matthew 6:33": Verse(
        book="Matthew", chapter=6, verse=33,
        text="But seek ye first the kingdom of God, and his righteousness; "
             "and all these things shall be added unto you."
    ),
    "Matthew 11:28": Verse(
        book="Matthew", chapter=11, verse=28,
        text="Come unto me, all ye that labour and are heavy laden, "
             "and I will give you rest."
    ),
    "Romans 8:28": Verse(
        book="Romans", chapter=8, verse=28,
        text="And we know that all things work together for good to them "
             "that love God, to them who are the called according to his "
             "purpose."
    ),
    "Philippians 4:13": Verse(
        book="Philippians", chapter=4, verse=13,
        text="I can do all things through Christ which strengtheneth me."
    ),
    "Revelation 21:4": Verse(
        book="Revelation", chapter=21, verse=4,
        text="And God shall wipe away all tears from their eyes; and there "
             "shall be no more death, neither sorrow, nor crying, neither "
             "shall there be any more pain: for the former things are "
             "passed away."
    ),
    "Revelation 22:1": Verse(
        book="Revelation", chapter=22, verse=1,
        text="And he shewed me a pure river of water of life, clear as "
             "crystal, proceeding out of the throne of God and of the Lamb."
    ),
    "Revelation 22:2": Verse(
        book="Revelation", chapter=22, verse=2,
        text="In the midst of the street of it, and on either side of the "
             "river, was there the tree of life, which bare twelve manner "
             "of fruits, and yielded her fruit every month: and the leaves "
             "of the tree were for the healing of the nations."
    ),
}


class BibleStudyTool:
    """
    Bible Study tool for Eden Agent.
    
    The Word speaks. Eden listens.
    The scroll records the wisdom.
    Bud thumps with reverence.
    """
    
    name: str = "bible_study"
    description: str = (
        "Look up Bible verses and passages. "
        "Provide a reference like 'John 3:16' or 'Psalm 23:1-4' "
        "to retrieve the scripture text."
    )
    
    def __init__(self):
        self._verses = SAMPLE_VERSES
        logger.info("🌳 BibleStudyTool initialized. The Word awaits.")
    
    def _parse_reference(self, reference: str) -> List[str]:
        """
        Parse a Bible reference into individual verse keys.
        
        Handles formats like:
        - "John 3:16"
        - "Psalm 23:1-4"
        - "Genesis 1:1"
        """
        reference = reference.strip()
        
        # Check for range (e.g., "Psalm 23:1-4")
        if "-" in reference and ":" in reference:
            base_ref, end_verse = reference.rsplit("-", 1)
            book_chapter, start_verse = base_ref.rsplit(":", 1)
            
            try:
                start = int(start_verse)
                end = int(end_verse)
                return [
                    f"{book_chapter}:{v}"
                    for v in range(start, end + 1)
                ]
            except ValueError:
                return [reference]
        
        return [reference]
    
    def _lookup_verse(self, reference: str) -> Optional[Verse]:
        """Look up a single verse by reference."""
        # Normalize reference
        ref = reference.strip()
        
        # Direct lookup
        if ref in self._verses:
            return self._verses[ref]
        
        # Try with "Psalms" instead of "Psalm"
        if ref.startswith("Psalm "):
            alt_ref = ref.replace("Psalm ", "Psalms ", 1)
            if alt_ref in self._verses:
                return self._verses[alt_ref]
        
        # Try with "Psalm" instead of "Psalms"
        if ref.startswith("Psalms "):
            alt_ref = ref.replace("Psalms ", "Psalm ", 1)
            if alt_ref in self._verses:
                return self._verses[alt_ref]
        
        return None
    
    async def execute(self, reference: str) -> Dict[str, Any]:
        """
        Look up Bible verses.
        
        The scroll opens. The Word speaks.
        """
        logger.info("🌳 Bible lookup: %s", reference)
        
        try:
            refs = self._parse_reference(reference)
            verses = []
            not_found = []
            
            for ref in refs:
                verse = self._lookup_verse(ref)
                if verse:
                    verses.append(verse)
                else:
                    not_found.append(ref)
            
            if not verses:
                return {
                    "success": False,
                    "error": f"Verse not found: {reference}. "
                             f"Try a reference like 'John 3:16' or 'Psalm 23:1'."
                }
            
            # Format result
            if len(verses) == 1:
                v = verses[0]
                result = {
                    "success": True,
                    "reference": str(v),
                    "text": v.text,
                    "version": v.version.value,
                    "stanza": "🌳 The Word speaks. Eden listens."
                }
            else:
                result = {
                    "success": True,
                    "passage": f"{verses[0]} - {verses[-1].verse}",
                    "verses": [v.to_dict() for v in verses],
                    "version": verses[0].version.value,
                    "stanza": "🌳 The scroll opens. The Word flows."
                }
            
            if not_found:
                result["not_found"] = not_found
            
            logger.info(
                "🌳 Scripture delivered: %s",
                result.get("reference") or result.get("passage")
            )
            
            return result
            
        except Exception as e:
            logger.error("Bible lookup error: %s", e)
            return {
                "success": False,
                "error": f"Error looking up scripture: {str(e)}"
            }
    
    def get_available_verses(self) -> List[str]:
        """Get list of available verse references."""
        return sorted(self._verses.keys())
    
    def get_daily_verse(self) -> Verse:
        """
        Get a verse of the day.
        
        The orchard offers daily bread.
        """
        import random
        from datetime import date
        
        # Use date as seed for consistent daily verse
        today = date.today()
        seed = today.year * 10000 + today.month * 100 + today.day
        random.seed(seed)
        
        key = random.choice(list(self._verses.keys()))
        return self._verses[key]


# Create global instance
bible_tool = BibleStudyTool()
