"""
Uzbek transliteration utility
Converts between Latin and Cyrillic scripts
"""

def latin_to_cyrillic(text: str) -> str:
    """
    Convert Latin script to Cyrillic script
    """
    latin_to_cyrillic_map = {
        'a': 'а', 'b': 'б', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г', 'h': 'ҳ',
        'i': 'и', 'j': 'ж', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о',
        'p': 'п', 'q': 'қ', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'v': 'в',
        'x': 'х', 'y': 'й', 'z': 'з', 'ch': 'ч', 'sh': 'ш', 'ng': 'ң', 'g\'': 'ғ',
        'o\'': 'ў', "'": 'ъ', 'c': 'ц',
        'A': 'А', 'B': 'Б', 'D': 'Д', 'E': 'Е', 'F': 'Ф', 'G': 'Г', 'H': 'Ҳ',
        'I': 'И', 'J': 'Ж', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О',
        'P': 'П', 'Q': 'Қ', 'R': 'Р', 'S': 'С', 'T': 'Т', 'U': 'У', 'V': 'В',
        'X': 'Х', 'Y': 'Й', 'Z': 'З', 'Ch': 'Ч', 'Sh': 'Ш', 'Ng': 'Ң', 'G\'': 'Ғ',
        'O\'': 'Ў', 'C': 'Ц'
    }
    
    result = text
    
    # Handle multi-character mappings first (order matters)
    for latin, cyrillic in latin_to_cyrillic_map.items():
        if len(latin) > 1:  # Multi-character mappings
            result = result.replace(latin, cyrillic)
    
    # Handle single character mappings
    for latin, cyrillic in latin_to_cyrillic_map.items():
        if len(latin) == 1:  # Single character mappings
            result = result.replace(latin, cyrillic)
    
    return result

def cyrillic_to_latin(text: str) -> str:
    """
    Convert Cyrillic script to Latin script
    """
    cyrillic_to_latin_map = {
        'а': 'a', 'б': 'b', 'д': 'd', 'е': 'e', 'ф': 'f', 'г': 'g', 'ҳ': 'h',
        'и': 'i', 'ж': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'қ': 'q', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'в': 'v',
        'х': 'x', 'й': 'y', 'з': 'z', 'ч': 'ch', 'ш': 'sh', 'ң': 'ng', 'ғ': 'g\'',
        'ў': 'o\'', 'ъ': "'", 'ц': 'c',
        'А': 'A', 'Б': 'B', 'Д': 'D', 'Е': 'E', 'Ф': 'F', 'Г': 'G', 'Ҳ': 'H',
        'И': 'I', 'Ж': 'J', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
        'П': 'P', 'Қ': 'Q', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'В': 'V',
        'Х': 'X', 'Й': 'Y', 'З': 'Z', 'Ч': 'Ch', 'Ш': 'Sh', 'Ң': 'Ng', 'Ғ': 'G\'',
        'Ў': 'O\'', 'Ц': 'C'
    }
    
    result = text
    
    # Handle multi-character mappings first (order matters)
    for cyrillic, latin in cyrillic_to_latin_map.items():
        if len(cyrillic) > 1:  # Multi-character mappings
            result = result.replace(cyrillic, latin)
    
    # Handle single character mappings
    for cyrillic, latin in cyrillic_to_latin_map.items():
        if len(cyrillic) == 1:  # Single character mappings
            result = result.replace(cyrillic, latin)
    
    return result

def detect_script(text: str) -> str:
    """
    Detect if text is in Latin or Cyrillic script
    Returns 'latin', 'cyrillic', or 'mixed'
    """
    latin_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    cyrillic_chars = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯҳқғўңҲҚҒЎҢ')
    
    latin_count = sum(1 for char in text if char in latin_chars)
    cyrillic_count = sum(1 for char in text if char in cyrillic_chars)
    
    if latin_count > cyrillic_count:
        return 'latin'
    elif cyrillic_count > latin_count:
        return 'cyrillic'
    else:
        return 'mixed'
