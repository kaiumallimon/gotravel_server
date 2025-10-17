"""
Utility Functions
Helper functions for the GoTravel AI Backend
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dateutil import parser
import re
import logging

logger = logging.getLogger(__name__)


# ==================== DATE UTILITIES ====================

def parse_natural_date(date_string: str) -> Optional[datetime]:
    """
    Parse natural language date strings into datetime objects
    
    Examples:
        - "tomorrow" -> tomorrow's date
        - "next weekend" -> next Saturday
        - "in 2 weeks" -> date 2 weeks from now
        - "December 15" -> Dec 15 of current/next year
    
    Args:
        date_string: Natural language date string
    
    Returns:
        datetime object or None if parsing fails
    """
    try:
        date_string = date_string.lower().strip()
        today = datetime.now()
        
        # Handle relative dates
        if date_string in ["today"]:
            return today
        elif date_string in ["tomorrow"]:
            return today + timedelta(days=1)
        elif "next week" in date_string:
            return today + timedelta(weeks=1)
        elif "next weekend" in date_string:
            # Find next Saturday
            days_until_saturday = (5 - today.weekday()) % 7
            if days_until_saturday == 0:
                days_until_saturday = 7
            return today + timedelta(days=days_until_saturday)
        elif "in" in date_string and "week" in date_string:
            # Extract number of weeks
            match = re.search(r'in (\d+) weeks?', date_string)
            if match:
                weeks = int(match.group(1))
                return today + timedelta(weeks=weeks)
        elif "in" in date_string and "day" in date_string:
            # Extract number of days
            match = re.search(r'in (\d+) days?', date_string)
            if match:
                days = int(match.group(1))
                return today + timedelta(days=days)
        
        # Try parsing with dateutil
        return parser.parse(date_string, fuzzy=True)
        
    except Exception as e:
        logger.warning(f"Failed to parse date '{date_string}': {e}")
        return None


def format_date(dt: datetime, format: str = "medium") -> str:
    """
    Format datetime object to readable string
    
    Args:
        dt: datetime object
        format: 'short', 'medium', or 'long'
    
    Returns:
        Formatted date string
    """
    if format == "short":
        return dt.strftime("%Y-%m-%d")
    elif format == "long":
        return dt.strftime("%A, %B %d, %Y")
    else:  # medium
        return dt.strftime("%b %d, %Y")


def calculate_duration(start_date: datetime, end_date: datetime) -> Dict[str, int]:
    """
    Calculate duration between two dates
    
    Returns:
        Dictionary with days, weeks, and months
    """
    delta = end_date - start_date
    days = delta.days
    weeks = days // 7
    months = days // 30
    
    return {
        "days": days,
        "weeks": weeks,
        "months": months
    }


# ==================== PRICE FORMATTING ====================

def format_price(amount: float, currency: str = "BDT") -> str:
    """
    Format price with currency symbol
    
    Args:
        amount: Price amount
        currency: Currency code
    
    Returns:
        Formatted price string
    """
    currency_symbols = {
        "BDT": "৳",
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "INR": "₹"
    }
    
    symbol = currency_symbols.get(currency, currency)
    
    # Format with commas for thousands
    if amount >= 1000:
        formatted = f"{amount:,.0f}"
    else:
        formatted = f"{amount:.2f}"
    
    return f"{symbol}{formatted}"


def parse_price_range(price_string: str) -> Dict[str, Optional[float]]:
    """
    Parse price range from natural language
    
    Examples:
        - "under 5000" -> {"min": None, "max": 5000}
        - "between 10000 and 20000" -> {"min": 10000, "max": 20000}
        - "at least 15000" -> {"min": 15000, "max": None}
    
    Returns:
        Dictionary with min and max prices
    """
    price_string = price_string.lower()
    result = {"min": None, "max": None}
    
    # Extract numbers
    numbers = re.findall(r'\d+(?:,\d{3})*(?:\.\d+)?', price_string)
    numbers = [float(n.replace(',', '')) for n in numbers]
    
    if not numbers:
        return result
    
    if "under" in price_string or "below" in price_string or "less than" in price_string:
        result["max"] = numbers[0]
    elif "over" in price_string or "above" in price_string or "more than" in price_string or "at least" in price_string:
        result["min"] = numbers[0]
    elif "between" in price_string and len(numbers) >= 2:
        result["min"] = numbers[0]
        result["max"] = numbers[1]
    else:
        # Single number, assume it's max
        result["max"] = numbers[0]
    
    return result


# ==================== TEXT PROCESSING ====================

def extract_location(text: str) -> Dict[str, Optional[str]]:
    """
    Extract location information from text
    
    Returns:
        Dictionary with potential city and country
    """
    # Common Bangladesh cities
    bd_cities = [
        "dhaka", "chittagong", "sylhet", "cox's bazar", "coxs bazar", "khulna",
        "rajshahi", "rangpur", "barisal", "mymensingh", "comilla", "gazipur",
        "narayanganj", "bogra", "jessore", "sundarbans", "kuakata"
    ]
    
    text_lower = text.lower()
    
    result = {
        "city": None,
        "country": None
    }
    
    # Check for Bangladesh cities
    for city in bd_cities:
        if city in text_lower:
            result["city"] = city.title()
            result["country"] = "Bangladesh"
            break
    
    # Check for country mentions
    if "bangladesh" in text_lower:
        result["country"] = "Bangladesh"
    
    return result


def extract_numbers(text: str) -> List[int]:
    """
    Extract all numbers from text
    
    Returns:
        List of integers found in text
    """
    # Find all numbers including written numbers
    numbers = []
    
    # Find digit numbers
    digit_matches = re.findall(r'\d+', text)
    numbers.extend([int(n) for n in digit_matches])
    
    # Map written numbers to digits
    written_numbers = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }
    
    text_lower = text.lower()
    for word, num in written_numbers.items():
        if word in text_lower:
            numbers.append(num)
    
    return numbers


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Input text
    
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    # Trim
    text = text.strip()
    
    return text


# ==================== VALIDATION ====================

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number (Bangladesh format)"""
    # Remove spaces, dashes, and plus signs
    cleaned = re.sub(r'[\s\-+]', '', phone)
    
    # Check if it matches common patterns
    # Bangladesh: 11 digits starting with 01 or 13-15 digits with country code
    if re.match(r'^01\d{9}$', cleaned):  # Local format
        return True
    if re.match(r'^8801\d{9}$', cleaned):  # With country code
        return True
    if re.match(r'^\d{10,15}$', cleaned):  # Generic international
        return True
    
    return False


# ==================== RESPONSE FORMATTING ====================

def format_list_response(items: List[Dict[str, Any]], item_type: str = "item") -> str:
    """
    Format a list of items into a readable response
    
    Args:
        items: List of item dictionaries
        item_type: Type of items (hotel, package, place)
    
    Returns:
        Formatted string response
    """
    if not items:
        return f"No {item_type}s found matching your criteria."
    
    response = f"I found {len(items)} {item_type}{'s' if len(items) != 1 else ''}:\n\n"
    
    for i, item in enumerate(items[:5], 1):  # Limit to top 5
        if item_type == "hotel":
            response += f"{i}. **{item.get('name')}**\n"
            response += f"   📍 {item.get('city')}, {item.get('country')}\n"
            if item.get('rating'):
                response += f"   ⭐ Rating: {item.get('rating')}/5.0\n"
            response += "\n"
        
        elif item_type == "package":
            response += f"{i}. **{item.get('name')}**\n"
            response += f"   📍 {item.get('destination')}\n"
            response += f"   ⏱️ {item.get('duration_days')} days\n"
            if item.get('price'):
                response += f"   💰 {format_price(item.get('price'), item.get('currency', 'BDT'))}\n"
            response += "\n"
        
        elif item_type == "place":
            response += f"{i}. **{item.get('name')}**\n"
            response += f"   📍 {item.get('city')}, {item.get('country')}\n"
            if item.get('category'):
                response += f"   🏷️ {item.get('category').title()}\n"
            response += "\n"
    
    if len(items) > 5:
        response += f"\n_...and {len(items) - 5} more options available._"
    
    return response


# ==================== INTENT CLASSIFICATION ====================

def classify_simple_intent(text: str) -> str:
    """
    Simple rule-based intent classification
    
    Returns:
        Intent category: 'hotel', 'package', 'place', 'weather', 'booking', 'general'
    """
    text_lower = text.lower()
    
    # Hotel keywords
    if any(word in text_lower for word in ["hotel", "accommodation", "stay", "room", "lodge"]):
        return "hotel"
    
    # Package keywords
    if any(word in text_lower for word in ["package", "tour", "trip", "travel package"]):
        return "package"
    
    # Place keywords
    if any(word in text_lower for word in ["place", "destination", "tourist", "visit", "attraction", "sightseeing"]):
        return "place"
    
    # Weather keywords
    if any(word in text_lower for word in ["weather", "temperature", "climate", "forecast"]):
        return "weather"
    
    # Booking keywords
    if any(word in text_lower for word in ["book", "reserve", "reservation", "booking"]):
        return "booking"
    
    return "general"
