"""
Unit tests for jawi_metrics
"""

import pytest
from ocr_metrics import cer, wer, normalize_text


class TestNormalizeText:
    """Test text normalization function"""
    
    def test_basic_normalization(self):
        text = "Hello, World!"
        result = normalize_text(text)
        assert result == "Hello World"
    
    def test_remove_numbers_default(self):
        text = "Hello 123 World"
        result = normalize_text(text)
        assert result == "Hello World"
    
    def test_keep_numbers(self):
        text = "Hello 123 World"
        result = normalize_text(text, remove_numbers=False)
        assert result == "Hello 123 World"
    
    def test_remove_punctuation_default(self):
        text = "Hello, World!"
        result = normalize_text(text)
        assert result == "Hello World"
    
    def test_keep_punctuation(self):
        text = "Hello, World!"
        result = normalize_text(text, remove_punctuation=False)
        assert result == "Hello, World!"
    
    def test_arabic_punctuation(self):
        text = "مرحبا، كيف حالك؟"
        result = normalize_text(text)
        assert "،" not in result
        assert "؟" not in result
    
    def test_whitespace_normalization(self):
        text = "Hello    World"
        result = normalize_text(text)
        assert result == "Hello World"
    
    def test_unicode_normalization(self):
        # Test NFC normalization
        text = "café"  # é can be composed or decomposed
        result = normalize_text(text, remove_punctuation=False)
        assert result == "café"
    
    def test_none_input(self):
        with pytest.raises(TypeError):
            normalize_text(None)
    
    def test_empty_string(self):
        result = normalize_text("")
        assert result == ""


class TestCER:
    """Test Character Error Rate function"""
    
    def test_identical_strings(self):
        assert cer("hello", "hello") == 0.0
    
    def test_completely_different(self):
        result = cer("abc", "xyz")
        assert result == 1.0  # 3 substitutions / 3 chars
    
    def test_one_substitution(self):
        result = cer("hello", "hallo")
        assert result == 0.2  # 1 substitution / 5 chars
    
    def test_one_insertion(self):
        result = cer("hello", "helllo")
        assert result == 0.2  # 1 insertion / 5 chars
    
    def test_one_deletion(self):
        result = cer("hello", "helo")
        assert result == 0.2  # 1 deletion / 5 chars
    
    def test_error_rate_over_100_percent(self):
        # Hypothesis much longer than reference
        result = cer("hi", "this is a very long sentence")
        assert result > 1.0
    
    def test_empty_hypothesis(self):
        result = cer("hello", "")
        assert result == 1.0  # All deletions
    
    def test_empty_reference_raises_error(self):
        with pytest.raises(ValueError):
            cer("", "hello")
    
    def test_both_empty_after_normalization(self):
        with pytest.raises(ValueError):
            cer("123", "456", remove_numbers=True)
    
    def test_jawi_text(self):
        result = cer("سلام", "سلام")
        assert result == 0.0
    
    def test_jawi_with_error(self):
        result = cer("كتاب", "كتب")
        assert 0 < result < 1
    
    def test_no_normalization(self):
        result = cer("Hello!", "Hello", normalize=False)
        assert result == 0.2  # 1 deletion / 5 chars in "Hello!"
    
    def test_with_punctuation_normalization(self):
        result = cer("Hello!", "Hello", normalize=True)
        assert result == 0.0  # Punctuation removed, identical
    
    def test_none_input(self):
        with pytest.raises(TypeError):
            cer(None, "hello")


class TestWER:
    """Test Word Error Rate function"""
    
    def test_identical_strings(self):
        assert wer("hello world", "hello world") == 0.0
    
    def test_one_word_different(self):
        result = wer("hello world", "hello earth")
        assert result == 0.5  # 1 substitution / 2 words
    
    def test_one_word_missing(self):
        result = wer("hello world", "hello")
        assert result == 0.5  # 1 deletion / 2 words
    
    def test_one_extra_word(self):
        result = wer("hello world", "hello beautiful world")
        assert result == 0.5  # 1 insertion / 2 words
    
    def test_completely_different(self):
        result = wer("hello world", "goodbye earth")
        assert result == 1.0  # 2 substitutions / 2 words
    
    def test_error_rate_over_100_percent(self):
        result = wer("hello", "this is a very long sentence")
        assert result > 1.0
    
    def test_empty_hypothesis(self):
        result = wer("hello world", "")
        assert result == 1.0
    
    def test_empty_reference_raises_error(self):
        with pytest.raises(ValueError):
            wer("", "hello world")
    
    def test_single_word(self):
        result = wer("hello", "hello")
        assert result == 0.0
    
    def test_jawi_words(self):
        result = wer("سلام عليكم", "سلام عليكم")
        assert result == 0.0
    
    def test_jawi_with_error(self):
        result = wer("كيف حالك", "كيف حالكم")
        assert result == 0.5  # 1 word different / 2 words (after normalization)
    
    def test_no_normalization(self):
        result = wer("Hello, World!", "Hello World", normalize=False)
        # Without normalization, punctuation makes "Hello," != "Hello"
        assert result > 0


class TestBackwardCompatibility:
    """Test backward compatibility aliases"""
    
    def test_cer_pair_exists(self):
        from jawi_metrics import cer_pair
        result = cer_pair("hello", "hello")
        assert result == 0.0
    
    def test_wer_pair_exists(self):
        from jawi_metrics import wer_pair
        result = wer_pair("hello world", "hello world")
        assert result == 0.0


class TestEdgeCases:
    """Test edge cases and corner scenarios"""
    
    def test_unicode_edge_cases(self):
        # Test various Unicode normalizations
        text1 = "café"
        text2 = "café"  # Same visual, potentially different encoding
        result = cer(text1, text2)
        assert result == 0.0
    
    def test_very_long_strings(self):
        # Test performance doesn't degrade significantly
        long_ref = "a" * 1000
        long_hyp = "a" * 1000
        result = cer(long_ref, long_hyp)
        assert result == 0.0
    
    def test_mixed_scripts(self):
        # Test mixing different scripts
        result = cer("Hello سلام", "Hello سلام")
        assert result == 0.0
    
    def test_numbers_in_text(self):
        # Default removes numbers
        result = cer("test123", "test456")
        assert result == 0.0  # Both become "test"
        
        # Keep numbers
        result = cer("test123", "test456", remove_numbers=False)
        assert result > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])