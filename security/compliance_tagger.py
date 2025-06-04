# Basic keyword list for compliance flagging (Examples - needs expansion for real-world use)
COMPLIANCE_KEYWORDS = [
    "confidential",
    "proprietary",
    "internal use only",
    "regulated data",
    "nda"
]

def tag_compliance(text):
    """Tags text based on the presence of compliance-related keywords."""
    tags = []
    if text:
        text_lower = text.lower()
        for keyword in COMPLIANCE_KEYWORDS:
            if keyword in text_lower:
                tags.append(keyword)
    return list(set(tags)) # Return unique tags

# Example usage (optional - for testing)
if __name__ == "__main__":
    sample_text_1 = "This document contains confidential and proprietary information."
    sample_text_2 = "Standard business communication."
    sample_text_3 = "Please sign the NDA."
    
    print("Text 1:")
    print(sample_text_1)
    print("Compliance Tags:", tag_compliance(sample_text_1))
    
    print("\nText 2:")
    print(sample_text_2)
    print("Compliance Tags:", tag_compliance(sample_text_2))
    
    print("\nText 3:")
    print(sample_text_3)
    print("Compliance Tags:", tag_compliance(sample_text_3)) 