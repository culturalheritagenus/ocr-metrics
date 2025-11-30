"""
Jawi OCR Evaluation Metrics

This module provides Character Error Rate (CER) and Word Error Rate (WER) 
calculations optimized for Jawi script OCR evaluation.
"""

import re
import unicodedata
import string
from typing import Union


def normalize_text(
    text: str,
    remove_punctuation: bool = True,
    remove_numbers: bool = True
) -> str:
    """
    Normalize Jawi text for evaluation.
    
    Args:
        text: Input text to normalize
        remove_punctuation: Whether to remove punctuation marks (default: True)
        remove_numbers: Whether to remove digit characters (default: True)
    
    Returns:
        Normalized text string
    
    Raises:
        TypeError: If text is not a string or cannot be converted to string
    """
    if text is None:
        raise TypeError("Text cannot be None")
    
    if not isinstance(text, str):
        try:
            text = str(text)
        except Exception as e:
            raise TypeError(f"Cannot convert input to string: {e}")
    
    # Use NFC normalization for Arabic script
    text = unicodedata.normalize('NFC', text)
    
    # Remove punctuation if requested
    if remove_punctuation:
        arabic_punctuation = '،؛؟٪۔٬'
        all_punctuation = string.punctuation + arabic_punctuation
        translator = str.maketrans('', '', all_punctuation)
        text = text.translate(translator)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove numbers if requested
    if remove_numbers:
        text = re.sub(r'\d', '', text).strip()
    
    return text


def levenshtein_distance(s1: list, s2: list) -> int:
    """
    Calculate Levenshtein distance between two sequences.
    
    Args:
        s1: First sequence (list of characters or words)
        s2: Second sequence (list of characters or words)
    
    Returns:
        Minimum edit distance as an integer
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i  # Deletion
    for j in range(n + 1):
        dp[0][j] = j  # Insertion
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = int(s1[i - 1] != s2[j - 1])
            dp[i][j] = min(
                dp[i - 1][j] + 1,        # Deletion
                dp[i][j - 1] + 1,        # Insertion
                dp[i - 1][j - 1] + cost  # Substitution
            )
    
    return dp[m][n]


def cer(
    reference: str,
    hypothesis: str,
    normalize: bool = True,
    remove_punctuation: bool = True,
    remove_numbers: bool = True
) -> float:
    """
    Calculate Character Error Rate (CER) for a single pair of strings.
    
    CER is defined as: (insertions + deletions + substitutions) / length of reference
    
    Args:
        reference: Ground truth text
        hypothesis: Predicted/OCR text
        normalize: Whether to normalize text before comparison (default: True)
        remove_punctuation: Whether to remove punctuation during normalization (default: True)
        remove_numbers: Whether to remove numbers during normalization (default: True)
    
    Returns:
        Character error rate as a float (0.0 means perfect match, >1.0 means 
        hypothesis is much longer/different than reference)
    
    Raises:
        TypeError: If inputs are not strings or cannot be converted
        ValueError: If reference is empty after normalization
    
    Examples:
        >>> cer("سلام", "سلام")
        0.0
        >>> cer("كتاب", "كتب")
        0.4
    """
    if normalize:
        reference = normalize_text(
            reference,
            remove_punctuation=remove_punctuation,
            remove_numbers=remove_numbers
        )
        hypothesis = normalize_text(
            hypothesis,
            remove_punctuation=remove_punctuation,
            remove_numbers=remove_numbers
        )
    
    ref_chars = list(reference)
    hyp_chars = list(hypothesis)
    
    # Handle edge case: empty reference
    if len(ref_chars) == 0:
        if len(hyp_chars) == 0:
            return 0.0
        raise ValueError("Reference text is empty after normalization")
    
    dist = levenshtein_distance(ref_chars, hyp_chars)
    return dist / len(ref_chars)


def wer(
    reference: str,
    hypothesis: str,
    normalize: bool = True,
    remove_punctuation: bool = True,
    remove_numbers: bool = True
) -> float:
    """
    Calculate Word Error Rate (WER) for a single pair of strings.
    
    WER is defined as: (insertions + deletions + substitutions) / number of words in reference
    
    Args:
        reference: Ground truth text
        hypothesis: Predicted/OCR text
        normalize: Whether to normalize text before comparison (default: True)
        remove_punctuation: Whether to remove punctuation during normalization (default: True)
        remove_numbers: Whether to remove numbers during normalization (default: True)
    
    Returns:
        Word error rate as a float (0.0 means perfect match, >1.0 means 
        hypothesis has many more/different words than reference)
    
    Raises:
        TypeError: If inputs are not strings or cannot be converted
        ValueError: If reference is empty after normalization
    
    Examples:
        >>> wer("hello world", "hello world")
        0.0
        >>> wer("hello world", "hello")
        0.5
    """
    if normalize:
        reference = normalize_text(
            reference,
            remove_punctuation=remove_punctuation,
            remove_numbers=remove_numbers
        )
        hypothesis = normalize_text(
            hypothesis,
            remove_punctuation=remove_punctuation,
            remove_numbers=remove_numbers
        )
    
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    
    # Handle edge case: empty reference
    if len(ref_words) == 0:
        if len(hyp_words) == 0:
            return 0.0
        raise ValueError("Reference text is empty after normalization")
    
    dist = levenshtein_distance(ref_words, hyp_words)
    return dist / len(ref_words)


# Backward compatibility aliases
cer_pair = cer
wer_pair = wer