"""
Pipe Standards Pro v12 - Utility Functions
Helper functions for various tasks
"""

import json
import pickle
from typing import Any, Dict, Optional
from pathlib import Path


def save_json(data: Dict, filepath: str) -> bool:
    """
    Save data to JSON file
    
    Args:
        data: Dictionary to save
        filepath: Path to save file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False


def load_json(filepath: str) -> Optional[Dict]:
    """
    Load data from JSON file
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        Dictionary if successful, None otherwise
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None


def save_favorites(favorites: list, filepath: str = "favorites.json") -> bool:
    """Save favorites list to file"""
    return save_json({"favorites": favorites}, filepath)


def load_favorites(filepath: str = "favorites.json") -> list:
    """Load favorites list from file"""
    data = load_json(filepath)
    return data.get("favorites", []) if data else []


def save_recent(recent: list, filepath: str = "recent.json") -> bool:
    """Save recent items list to file"""
    return save_json({"recent": recent}, filepath)


def load_recent(filepath: str = "recent.json") -> list:
    """Load recent items list from file"""
    data = load_json(filepath)
    return data.get("recent", []) if data else []


def format_number(value: float, decimals: int = 3, unit: str = "") -> str:
    """
    Format number with specified decimals and optional unit
    
    Args:
        value: Number to format
        decimals: Number of decimal places
        unit: Optional unit string
    
    Returns:
        Formatted string
    """
    formatted = f"{value:.{decimals}f}"
    return f"{formatted} {unit}" if unit else formatted


def validate_positive_number(value: str) -> Optional[float]:
    """
    Validate and convert string to positive number
    
    Args:
        value: String to validate
    
    Returns:
        Float value if valid, None otherwise
    """
    try:
        num = float(value)
        return num if num > 0 else None
    except (ValueError, TypeError):
        return None


def create_backup(filepath: str) -> bool:
    """
    Create backup of file
    
    Args:
        filepath: Path to file to backup
    
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(filepath)
        if path.exists():
            backup_path = path.with_suffix(path.suffix + '.bak')
            import shutil
            shutil.copy2(path, backup_path)
            return True
        return False
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False


def get_app_data_dir() -> Path:
    """
    Get application data directory
    
    Returns:
        Path to app data directory
    """
    import os
    
    if os.name == 'nt':  # Windows
        base = Path(os.environ.get('APPDATA', Path.home()))
    elif os.name == 'posix':  # Linux/Mac
        base = Path.home() / '.local' / 'share'
    else:
        base = Path.home()
    
    app_dir = base / 'PipeStandardsPro'
    app_dir.mkdir(parents=True, exist_ok=True)
    
    return app_dir


def load_user_settings() -> Dict:
    """Load user settings from file"""
    settings_file = get_app_data_dir() / 'settings.json'
    settings = load_json(str(settings_file))
    
    # Default settings
    defaults = {
        'default_standard': 'ASME',
        'default_view_mode': '2D',
        'show_dimensions': True,
        'units': 'imperial',
        'theme': 'dark'
    }
    
    return {**defaults, **(settings or {})}


def save_user_settings(settings: Dict) -> bool:
    """Save user settings to file"""
    settings_file = get_app_data_dir() / 'settings.json'
    return save_json(settings, str(settings_file))


class Cache:
    """Simple cache for expensive operations"""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        return self._cache.get(key)
    
    def set(self, key: str, value: Any):
        """Set value in cache"""
        self._cache[key] = value
    
    def clear(self):
        """Clear entire cache"""
        self._cache.clear()
    
    def remove(self, key: str) -> bool:
        """Remove specific key from cache"""
        if key in self._cache:
            del self._cache[key]
            return True
        return False


# Global cache instance
visualization_cache = Cache()
