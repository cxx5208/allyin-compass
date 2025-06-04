import re

# Basic regex patterns for common PII (Examples - these may need refinement for real-world use)
# This is not exhaustive and should be treated as a demonstration.
PII_PATTERNS = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', # Basic U.S. phone number format
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b' # Basic U.S. SSN format
}

def find_pii(text):
    """Finds occurrences of defined PII patterns in text."""
    found_pii = {}
    if text:
        for pii_type, pattern in PII_PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                found_pii[pii_type] = matches
    return found_pii

def filter_pii(text, replacement="[REDACTED]"):
    """Replaces occurrences of defined PII patterns in text with a replacement string."""
    filtered_text = text
    if text:
        for pattern in PII_PATTERNS.values():
            filtered_text = re.sub(pattern, replacement, filtered_text)
    return filtered_text

# Example usage (optional - for testing)
if __name__ == "__main__":
    sample_text = "Contact us at test.email@example.com or call 123-456-7890. My SSN is 999-99-9999."
    
    print("Original Text:")
    print(sample_text)
    
    found = find_pii(sample_text)
    print("\nFound PII:")
    print(found)
    
    filtered = filter_pii(sample_text)
    print("\nFiltered Text:")
    print(filtered) 