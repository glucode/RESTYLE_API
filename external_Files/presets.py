

class GenerateOutfitsConfig:
    COLOR_WHEEL = {
        "Red": ["Red-Orange", "Red-Purple", "Blue-Green", "Yellow-Green"],
        "Red-Orange": ["Red", "Orange", "Blue-Purple", "Green"],
        "Orange": ["Red-Orange", "Yellow-Orange", "Blue", "Purple"],
        "Yellow-Orange": ["Orange", "Yellow", "Blue-Green", "Red-Purple"],
        "Yellow": ["Yellow-Orange", "Yellow-Green", "Purple", "Red"],
        "Yellow-Green": ["Yellow", "Green", "Red-Purple", "Red-Orange"],
        "Green": ["Yellow-Green", "Blue-Green", "Red", "Red-Orange"],
        "Blue-Green": ["Green", "Blue", "Red-Orange", "Yellow-Orange"],
        "Blue": ["Blue-Green", "Blue-Purple", "Orange", "Yellow"],
        "Blue-Purple": ["Blue", "Purple", "Yellow-Orange", "Green"],
        "Purple": ["Blue-Purple", "Red-Purple", "Yellow", "Blue"],
        "Red-Purple": ["Purple", "Red", "Green", "Yellow-Green"],
        "White": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"],
        "Black": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
    }

    # Color Profiles
    COLOR_PROFILES = {
    "Triads": {
        "Red": ["Blue-Green", "Yellow-Green"],
        "Red-Orange": ["Blue", "Green"],
        "Orange": ["Blue-Purple", "Yellow-Green"],
        "Yellow-Orange": ["Purple", "Blue-Green"],
        "Yellow": ["Blue", "Red-Purple"],
        "Yellow-Green": ["Red", "Blue-Purple"],
        "Green": ["Red", "Blue"],
        "Blue-Green": ["Red-Orange", "Red-Purple"],
        "Blue": ["Red-Orange", "Yellow-Orange"],
        "Blue-Purple": ["Yellow", "Green"],
        "Purple": ["Yellow", "Blue-Green"],
        "Red-Purple": ["Yellow-Green", "Blue"]
    },
    "Complementary": {
        "Red": ["Red-Orange", "Red-Purple", "Blue-Green", "Yellow-Green"],
        "Red-Orange": ["Red", "Orange", "Blue-Purple", "Green"],
        "Orange": ["Red-Orange", "Yellow-Orange", "Blue", "Purple"],
        "Yellow-Orange": ["Orange", "Yellow", "Blue-Green", "Red-Purple"],
        "Yellow": ["Yellow-Orange", "Yellow-Green", "Purple", "Red"],
        "Yellow-Green": ["Yellow", "Green", "Red-Purple", "Red-Orange"],
        "Green": ["Yellow-Green", "Blue-Green", "Red", "Red-Orange"],
        "Blue-Green": ["Green", "Blue", "Red-Orange", "Yellow-Orange"],
        "Blue": ["Blue-Green", "Blue-Purple", "Orange", "Yellow"],
        "Blue-Purple": ["Blue", "Purple", "Yellow-Orange", "Green"],
        "Purple": ["Blue-Purple", "Red-Purple", "Yellow", "Blue"],
        "Red-Purple": ["Purple", "Red", "Green", "Yellow-Green"],
    },
    "Monotone": {color: [color] for color in COLOR_WHEEL.keys()},
    "Analogous": {
        "Red": ["Red-Orange", "Red-Purple"],
        "Red-Orange": ["Red", "Orange"],
        "Orange": ["Red-Orange", "Yellow-Orange"],
        "Yellow-Orange": ["Orange", "Yellow"],
        "Yellow": ["Yellow-Orange", "Yellow-Green"],
        "Yellow-Green": ["Yellow", "Green"],
        "Green": ["Yellow-Green", "Blue-Green"],
        "Blue-Green": ["Green", "Blue"],
        "Blue": ["Blue-Green", "Blue-Purple"],
        "Blue-Purple": ["Blue", "Purple"],
        "Purple": ["Blue-Purple", "Red-Purple"],
        "Red-Purple": ["Purple", "Red"]
    }
}
    
    # Color Temperatures
    WARM_COLORS = ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow"]
    COOL_COLORS = ["Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
    
    # Base Category Constraints
    base_category_constraints = {
        "tops": ["t-shirt", "shirts", "polo", "vests", "sweaters"],
        "trousers": ["pants", "shorts", "denim", "jeans"],
        "shoes": ["slides", "trainers", "boots", "sandals", "heels", "slip-ons"]
    }
    
    # Other configurations
    MAX_OUTFITS = 10
    TOP_N_ITEMS_TO_SORT = 5
    PRIORITY_RANDOM_SELECTION = 0.7