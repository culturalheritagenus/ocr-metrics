"""
Jawi Metrics - CER and WER evaluation for Jawi OCR
"""

from .metrics import cer, wer, cer_pair, wer_pair, normalize_text

__version__ = "0.1.0"
__all__ = ["cer", "wer", "cer_pair", "wer_pair", "normalize_text"]