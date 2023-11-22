from enum import Enum

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
class GenerateOutfitsConfig:

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

   
class WomensBohemianConfig(GenerateOutfitsConfig):

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
        "tops": ["dresses"],
        "shoes": ["slides", "trainers", "boots", "sandals", "heels", "slip-ons"]
    }
    
    # Other configurations
    MAX_OUTFITS = 5
    TOP_N_ITEMS_TO_SORT = 2
    PRIORITY_RANDOM_SELECTION = 0.7
   
    
class StreetwearConfig(GenerateOutfitsConfig):
    
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
        "tops": ["t-shirt", "shirts", "jumpsuits", "vests", "sweaters","hoodie", "sweatshirts"],
        "trousers": ["pants", "shorts", "denim", "jeans"],
        "shoes": ["slides", "trainers", "boots", "sandals", "heels", "slip-ons"]
    }
    
    # Other configurations
    MAX_OUTFITS = 15
    TOP_N_ITEMS_TO_SORT = 2
    PRIORITY_RANDOM_SELECTION = 0.7
   
    
class WomensRomanticConfig(GenerateOutfitsConfig):
        
    COLOR_PROFILES = {
        "Triads": {
            "Red": ["Blue-Green", "Yellow-Green"],
            "Red-Orange": ["Blue", "Green"],
            "Orange": ["Blue-Purple", "Yellow-Green"],
            "Yellow-Orange": ["Purple", "Blue-Green"],
            "Yellow": ["Blue", "Red-Purple"],
            "Yellow-Green": ["Red", "Blue-Purple"],
            "Green": ["Red", "Blue"],
            "Purple": ["Yellow", "Blue-Green"],
            "Red-Purple": ["Yellow-Green", "Blue"]
        },
        "Complementary": {
            "Red": ["Red-Orange", "Red-Purple", "Blue-Green", "Yellow-Green"],
            "Red-Orange": ["Red", "Orange", "Blue-Purple", "Green"],
            "Orange": ["Red-Orange", "Yellow-Orange", "Blue", "Purple"],
            "Yellow-Orange": ["Orange", "Yellow", "Blue-Green", "Red-Purple"],
            "Blue-Purple": ["Blue", "Purple", "Yellow-Orange", "Green"],
            "Purple": ["Blue-Purple", "Red-Purple", "Yellow", "Blue"],
            "Red-Purple": ["Purple", "Red", "Green", "Yellow-Green"],
        },
        "Monotone": {color: [color] for color in COLOR_WHEEL.keys()},
        "Analogous": {
            "Red": ["Red-Orange", "Red-Purple"],
            "Red-Orange": ["Red", "Orange"],
            "Orange": ["Red-Orange", "Yellow-Orange"],
            "Purple": ["Blue-Purple", "Red-Purple"],
            "Red-Purple": ["Purple", "Red"]
        }
    }
    
        # Color Temperatures
    WARM_COLORS = ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow"]
    COOL_COLORS = ["Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]

    # Base Category Constraints

    base_category_constraints = {
        "tops": ["t-shirt", "shirts", "vests", "blouses"],
        "trousers": ["pants", "shorts", "denim", "jeans"],
        "shoes": ["slides", "trainers", "boots", "sandals", "heels", "slip-ons"]
    }
    
    # Other configurations
    MAX_OUTFITS = 15
    TOP_N_ITEMS_TO_SORT = 2
    PRIORITY_RANDOM_SELECTION = 0.7
   
    
class ClassyConfig(GenerateOutfitsConfig):
        
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
        "tops": ["dresses"],
        "shoes": ["boots", "heels"]
    }
    
    # Other configurations
    MAX_OUTFITS = 15
    TOP_N_ITEMS_TO_SORT = 2
    PRIORITY_RANDOM_SELECTION = 0.7
    
    
class MenMinimalConfig(GenerateOutfitsConfig):
    
    COLOR_PROFILES = {
        "Triads": {
            "Red-Orange": ["Blue", "Green"],
            "Green": ["Red", "Blue"],
            "Blue-Green": ["Red-Orange", "Red-Purple"],
            "Blue": ["Red-Orange", "Yellow-Orange"],
            "Blue-Purple": ["Yellow", "Green"],
            "White": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"],
            "Black": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
        },
        "Complementary": {
            "Red": ["Red-Orange", "Red-Purple", "Blue-Green", "Yellow-Green"],
            "Red-Orange": ["Red", "Orange", "Blue-Purple", "Green"],
            "Orange": ["Red-Orange", "Yellow-Orange", "Blue", "Purple"],
            "Green": ["Yellow-Green", "Blue-Green", "Red", "Red-Orange"],
            "Blue-Green": ["Green", "Blue", "Red-Orange", "Yellow-Orange"],
            "Blue": ["Blue-Green", "Blue-Purple", "Orange", "Yellow"],
            "Blue-Purple": ["Blue", "Purple", "Yellow-Orange", "Green"],
            "Purple": ["Blue-Purple", "Red-Purple", "Yellow", "Blue"],
            "White": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"],
            "Black": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
        
        },
        "Monotone": {color: [color] for color in COLOR_WHEEL.keys()},
        "Analogous": {
            "Red": ["Red-Orange", "Red-Purple"],
            "Red-Orange": ["Red", "Orange"],
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
        "shoes": ["slides", "trainers", "boots", "sandals", "slip-ons"]
    }
    
    # Other configurations
    MAX_OUTFITS = 10
    TOP_N_ITEMS_TO_SORT = 5
    PRIORITY_RANDOM_SELECTION = 0.7

    
class MenSmartConfig(GenerateOutfitsConfig):
    
    COLOR_PROFILES = {
        "Triads": {
            "Red-Orange": ["Blue", "Green"],
            "Green": ["Red", "Blue"],
            "Blue-Green": ["Red-Orange", "Red-Purple"],
            "Blue": ["Red-Orange", "Yellow-Orange"],
            "Blue-Purple": ["Yellow", "Green"],
            "White": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"],
            "Black": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
        },
        "Complementary": {
            "Red": ["Red-Orange", "Red-Purple", "Blue-Green", "Yellow-Green"],
            "Red-Orange": ["Red", "Orange", "Blue-Purple", "Green"],
            "Orange": ["Red-Orange", "Yellow-Orange", "Blue", "Purple"],
            "Green": ["Yellow-Green", "Blue-Green", "Red", "Red-Orange"],
            "Blue-Green": ["Green", "Blue", "Red-Orange", "Yellow-Orange"],
            "Blue": ["Blue-Green", "Blue-Purple", "Orange", "Yellow"],
            "Blue-Purple": ["Blue", "Purple", "Yellow-Orange", "Green"],
            "Purple": ["Blue-Purple", "Red-Purple", "Yellow", "Blue"],
            "White": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"],
            "Black": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
        
        },
        "Monotone": {color: [color] for color in COLOR_WHEEL.keys()},
        "Analogous": {
            "Red": ["Red-Orange", "Red-Purple"],
            "Red-Orange": ["Red", "Orange"],
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
        "trousers": ["trousers", "pants"],
        "shoes": ["trainers", "boots"]
    }
    
    # Other configurations
    MAX_OUTFITS = 10
    TOP_N_ITEMS_TO_SORT = 5
    PRIORITY_RANDOM_SELECTION = 0.4
    
    
class MenClassyConfig(GenerateOutfitsConfig):
    
    COLOR_PROFILES = {
        "Triads": {
            "Red-Orange": ["Blue", "Green"],
            "Green": ["Red", "Blue"],
            "Blue-Green": ["Red-Orange", "Red-Purple"],
            "Blue": ["Red-Orange", "Yellow-Orange"],
            "Blue-Purple": ["Yellow", "Green"],
            "White": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"],
            "Black": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
        },
        "Complementary": {
            "Red": ["Red-Orange", "Red-Purple", "Blue-Green", "Yellow-Green"],
            "Orange": ["Red-Orange", "Yellow-Orange", "Blue", "Purple"],
            "Green": ["Yellow-Green", "Blue-Green", "Red", "Red-Orange"],
            "Blue-Green": ["Green", "Blue", "Red-Orange", "Yellow-Orange"],
            "Blue": ["Blue-Green", "Blue-Purple", "Orange", "Yellow"],
            "Purple": ["Blue-Purple", "Red-Purple", "Yellow", "Blue"],
            "White": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"],
            "Black": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
        
        },
        "Monotone": {color: [color] for color in COLOR_WHEEL.keys()},
        "Analogous": {
            "Red": ["Red-Orange", "Red-Purple"],
            "Green": ["Yellow-Green", "Blue-Green"],
            "Blue-Green": ["Green", "Blue"],
            "Blue": ["Blue-Green", "Blue-Purple"],
            "Blue-Purple": ["Blue", "Purple"],
            "Purple": ["Blue-Purple", "Red-Purple"],
            "White": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"],
            "Black": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
        }
    }
    
    # Color Temperatures
    WARM_COLORS = ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow"]
    COOL_COLORS = ["Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
    
    # Base Category Constraints
    base_category_constraints = {
        "tops": ["t-shirt", "shirts", "polo", "vests", "sweaters"],
        "trousers": ["trousers", "pants"],
        "shoes": ["trainers", "boots"]
    }
    
    # Other configurations
    MAX_OUTFITS = 10
    TOP_N_ITEMS_TO_SORT = 5
    PRIORITY_RANDOM_SELECTION = 0.7
    
      
class MenOutdoorConfig(GenerateOutfitsConfig):
    COLOR_PROFILES = {
        
        "Triads": {
            "Red": ["Blue-Green", "Yellow-Green"],
            "Red-Orange": ["Blue", "Green"],
            "Orange": ["Blue-Purple", "Yellow-Green"],
            "Yellow-Orange": ["Purple", "Blue-Green"],
            "Yellow": ["Blue", "Red-Purple"],
            "Yellow-Green": ["Red", "Blue-Purple"],
            "Green": ["Red", "Blue"],
            "White": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"],
            "Black": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
        },
        "Complementary": {
            "Red": ["Red-Orange", "Red-Purple", "Blue-Green", "Yellow-Green"],
            "Red-Orange": ["Red", "Orange", "Blue-Purple", "Green"],
            "Orange": ["Red-Orange", "Yellow-Orange", "Blue", "Purple"],
            "Yellow-Orange": ["Orange", "Yellow", "Blue-Green", "Red-Purple"],
            "Yellow": ["Yellow-Orange", "Yellow-Green", "Purple", "Red"],
            "Yellow-Green": ["Yellow", "Green", "Red-Purple", "Red-Orange"],
            "Green": ["Yellow-Green", "Blue-Green", "Red", "Red-Orange"],
            "Purple": ["Blue-Purple", "Red-Purple", "Yellow", "Blue"],
            "Red-Purple": ["Purple", "Red", "Green", "Yellow-Green"],
            "White": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"],
            "Black": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
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
            "Purple": ["Blue-Purple", "Red-Purple"],
            "Red-Purple": ["Purple", "Red"],
            "White": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"],
            "Black": ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow", "Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
        }
    }
    
    # Color Temperatures
    WARM_COLORS = ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow"]
    COOL_COLORS = ["Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]
    
    # Base Category Constraints
    base_category_constraints = {
        "tops": ["t-shirt", "shirts", "hoodie", "vests", "sweaters","cardigans"],
        "trousers": ["shorts", "denim"],
        "shoes": ["slides", "trainers", "sandals","slip-ons"]
    }
    
    # Other configurations
    MAX_OUTFITS = 10
    TOP_N_ITEMS_TO_SORT = 5
    PRIORITY_RANDOM_SELECTION = 0.7