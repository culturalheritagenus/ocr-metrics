# Jawi Metrics

CER (Character Error Rate) and WER (Word Error Rate) metrics for Jawi OCR evaluation.

## Installation

```bash
pip install git+https://github.com/culturalheritagenus/ocr-metrics.git
```

## Usage

### Basic Example

```python
from jawi_metrics import cer, wer

# Character Error Rate
reference = "سلام عليكم"
hypothesis = "سلام عليكم"
print(cer(reference, hypothesis))  # 0.0

# Word Error Rate
reference = "hello world"
hypothesis = "hello earth"
print(wer(reference, hypothesis))  # 0.5
```

### Parameters

Both `cer()` and `wer()` accept the following parameters:

- `reference` (str): Ground truth text
- `hypothesis` (str): Predicted/OCR text
- `normalize` (bool): Enable text normalization (default: True)
- `remove_punctuation` (bool): Remove punctuation marks (default: True)
- `remove_numbers` (bool): Remove digit characters (default: True)

### Examples

```python
from ocr_metrics import cer, wer, normalize_text

# Keep punctuation
cer("Hello, World!", "Hello World", remove_punctuation=False)

# Keep numbers
cer("Test 123", "Test 456", remove_numbers=False)

# No normalization
cer("Raw text!", "raw text", normalize=False)

# Normalize text separately
text = normalize_text("سلام، كيف حالك؟ 123")
print(text)  # "سلام كيف حالك"

# Batch processing
references = ["text1", "text2", "text3"]
hypotheses = ["pred1", "pred2", "pred3"]
scores = [cer(ref, hyp) for ref, hyp in zip(references, hypotheses)]
avg_cer = sum(scores) / len(scores)
```

## API Reference

### `cer(reference, hypothesis, normalize=True, remove_punctuation=True, remove_numbers=True)`

Calculate Character Error Rate.

**Returns:** Float between 0.0 (perfect match) and >1.0 (hypothesis much longer/different than reference)

**Raises:**
- `TypeError`: If inputs cannot be converted to strings
- `ValueError`: If reference is empty after normalization

### `wer(reference, hypothesis, normalize=True, remove_punctuation=True, remove_numbers=True)`

Calculate Word Error Rate.

**Returns:** Float between 0.0 (perfect match) and >1.0 (hypothesis much longer/different than reference)

**Raises:**
- `TypeError`: If inputs cannot be converted to strings
- `ValueError`: If reference is empty after normalization

### `normalize_text(text, remove_punctuation=True, remove_numbers=True)`

Normalize Jawi text for evaluation.

**Returns:** Normalized text string

**Raises:**
- `TypeError`: If text cannot be converted to string

## Running Tests

```bash
# Clone the repository
git clone https://github.com/culturalheritagenus/ocr-metrics.git
cd ocr-metrics

# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=ocr_metrics
```

## Notes

- Uses NFC Unicode normalization (appropriate for Arabic script)
- Error rates can exceed 100% when hypothesis is much longer than reference
- Zero dependencies - pure Python implementation

## License

MIT