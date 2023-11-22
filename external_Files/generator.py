import os
import random
import json
import base64
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from external_Files import presets

# 1. Data Loading and Preprocessing
df = pd.read_csv("external_files/Dataset/Cleaned_Dataset.csv", delimiter=",", on_bad_lines='skip')
df["Season"] = df["Season"].apply(lambda x: x.split(", ") if isinstance(x, str) else [])
image_folder = "external_files/Dataset_images"
config = presets.GenerateOutfitsConfig

# 2. Complementary, Matching, and Seasonal colors definitions
seasonal_colors = {
    "Winter": "cool, clear",
    "Summer": "cool, muted",
    "Autumn": "warm, muted",
    "Spring": "warm, clear"
}

# 3. Color Matching System
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

# Define the color profiles
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
        "Red": ["Green"],
        "Red-Orange": ["Blue-Green"],
        "Orange": ["Blue"],
        "Yellow-Orange": ["Blue-Purple"],
        "Yellow": ["Purple"],
        "Yellow-Green": ["Red-Purple"],
        "Green": ["Red"],
        "Blue-Green": ["Red-Orange"],
        "Blue": ["Orange"],
        "Blue-Purple": ["Yellow-Orange"],
        "Purple": ["Yellow"],
        "Red-Purple": ["Yellow-Green"]
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

# Define warm and cool colors
WARM_COLORS = ["Red", "Red-Orange", "Orange", "Yellow-Orange", "Yellow"]
COOL_COLORS = ["Yellow-Green", "Green", "Blue-Green", "Blue", "Blue-Purple", "Purple", "Red-Purple"]

COLOR_PROFILES, WARM_COLORS, COOL_COLORS
# 5. Functions for Outfit Generation
base_category_constraints = {
    "tops": ["t-shirt", "shirts", "polo", "vests", "sweaters"],
    "trousers": ["pants", "shorts", "denim", "jeans"],
    "shoes": ["slides", "trainers", "boots", "sandals", "heels", "slip-ons"]
}
def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode('utf-8')


# 4. Functions to compute similarity
def compute_similarity(item1, item2):
    """
    Calculates a similarity score between two fashion items, considering color vibrancy and season appropriateness.

    Parameters:
    - item1, item2 (dict): Dictionaries representing the two items being compared.

    Returns:
    - int: The calculated similarity score.
    """
    vibrant_colors = ["Red", "Blue", "Yellow", "Pink", "Orange", "Purple", "Bright Green"]
    dull_colors = ["Brown", "Grey", "Olive", "Navy", "Maroon", "Taupe", "Beige", "Black", "White"]

    sunny_seasons = ["Spring", "Summer"]
    cold_seasons = ["Autumn", "Winter"]

    score = 0
    if item1["Colors"] == item2["Colors"]:
        score -= 2

    # Adjust score based on color and season
    for season in sunny_seasons:
        if season in item1["Season"] and any(vibrant in item1["Colors"] for vibrant in vibrant_colors):
            score += 1
        if season in item2["Season"] and any(vibrant in item2["Colors"] for vibrant in vibrant_colors):
            score += 1

    for season in cold_seasons:
        if season in item1["Season"] and any(dull in item1["Colors"] for dull in dull_colors):
            score += 1
        if season in item2["Season"] and any(dull in item2["Colors"] for dull in dull_colors):
            score += 1

    # Other attribute comparisons
    if item1["Main Category"] == item2["Main Category"]:
        score += 1
    if item1["Subcategory"] == item2["Subcategory"]:
        score += 1
    if item1["Brands"] == item2["Brands"]:
        score -= 2

    overlapping_seasons = set(item1["Season"]).intersection(set(item2["Season"]))
    score += len(overlapping_seasons)
    return score
    
def determine_current_season():
    month = datetime.now().month
    if month in [12, 1, 2]:
        return "Spring"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"
    
def get_top_similar_items_regression_fixed_with_constraints(reference_item, df, categories, similarity_function, gender,config_class=config,top_n=5):
    category_items = {}
    for category, subcategories in config_class.base_category_constraints.items():
        # Check if the current category is in the categories list
        if category not in categories:
            continue

        feature_diffs = []
        items_in_category = []
        for _, item in df.iterrows():
            if item["Product ID"] != reference_item["Product ID"]:
                is_category = any(sub.lower() in str(item["Subcategory"]).lower() for sub in subcategories)
                
                # Gender suitability check
                item_gender = str(item.get("Gender", "")).lower()
                is_gender_suitable = item_gender == gender.lower() or item_gender == "any"
                
                if is_category and is_gender_suitable:
                    feature_diff = get_feature_difference(reference_item, item)
                    feature_diffs.append(feature_diff)
                    items_in_category.append(item)
        predicted_scores = model_sample.predict(feature_diffs)
        sorted_items = [x for _, x in sorted(zip(predicted_scores, items_in_category), key=lambda pair: similarity_function(reference_item, pair[1]), reverse=True)]
        category_items[category] = sorted_items[:top_n]
    return category_items

def save_user_item_locally(user_image_file, save_path="external_files/User_Items/"):
    """
    Save the user's item locally.
    
    Parameters:
    - user_image_file (File): The user's image file.
    - save_path (str): The directory to save the image in.
    
    Returns:
    - str: The path to the saved image.
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    image_path = os.path.join(save_path, user_image_file.filename)
    
    user_image_file.save(image_path)
    
    return image_path

def generate_outfits_with_user_item(refrence_category,user_image_file, df, gender, max_outfits=30):
    # Save the user's item locally
    user_item_path = save_user_item_locally(user_image_file)
    
    reference_item = {"Product ID": refrence_category, "Image Path": user_item_path}  
    
    base_categories = ["tops", "trousers", "shoes"]
    accessory_categories = ["jewellery", "bags", "caps", "belts", "socks", "bracelets", "eyewear"]

    base_items = get_top_similar_items_regression_fixed(refrence_category, df, base_categories, compute_advanced_similarity_v3_updated)
    accessory_items = get_top_similar_items_regression_fixed(refrence_category, df, accessory_categories, compute_advanced_similarity_v3_updated)

    outfits = set()
    while len(outfits) < max_outfits:
        base = [generate_url(random.choice(base_items[category])["Product ID"]) for category in base_categories]
        
        # Replace the item in the outfit that matches the main category of the reference item with the user's item
        base[base_categories.index(refrence_category)] = user_item_path  # Assuming the user's item is a "top"
        
        accessory_count = random.randint(0, len(accessory_items))
        chosen_accessories = random.sample(accessory_categories, accessory_count)
        accessories = [generate_url(random.choice(accessory_items[category])["Product ID"]) for category in chosen_accessories]
        accessories[:3]
        outfit = tuple(base + accessories)
        outfits.add(outfit)
        
    return list(outfits)

def get_top_similar_items_regression_fixed(reference_item, df, categories, similarity_function, top_n=5):
    category_items = {}
    for category in categories:
        feature_diffs = []
        items_in_category = []
        for _, item in df.iterrows():
            if item["Product ID"] != reference_item["Product ID"]:
                main_category = str(item["Main Category"]).lower()
                subcategory = str(item["Subcategory"]).lower()
                is_category = category in main_category or category in subcategory
                if is_category:
                    feature_diff = get_feature_difference(reference_item, item)
                    feature_diffs.append(feature_diff)
                    items_in_category.append(item)
        predicted_scores = model_sample.predict(feature_diffs)
        sorted_items = [x for _, x in sorted(zip(predicted_scores, items_in_category), key=lambda pair: similarity_function(reference_item, pair[1]), reverse=True)]
        top_n = int(top_n)
        category_items[category] = sorted_items[:top_n]
    return category_items

def generate_url(product_id, folder_path=image_folder):
    for filename in os.listdir(folder_path):
        if product_id in filename:
            return f"https://firebasestorage.googleapis.com/v0/b/restyle-fbd67.appspot.com/o/demodataset%2F{filename}?alt=media"
    return product_id

def compute_advanced_similarity_v3_updated(item1, item2):
    score = compute_similarity(item1, item2)

    # Pattern consideration
    if "pattern" in str(item1["Patterns"]).lower() and "pattern" not in str(item2["Patterns"]).lower():
        score += 1

    # Seasonal color analysis consideration
    item1_seasons = set(item1["Season"])
    item2_seasons = set(item2["Season"])
    overlapping_seasons = item1_seasons.intersection(item2_seasons)
    for season in overlapping_seasons:
        item1_colors = str(item1["Colors"]).lower()
        item2_colors = str(item2["Colors"]).lower()
        if seasonal_colors[season] in item1_colors and seasonal_colors[season] in item2_colors:
            score += 1

    # Seasonality consideration
    current_season = determine_current_season() #Expose the current season
    if current_season in item2["Season"] or len(item2["Season"]) == 4:  # If the item is for all seasons
        score += 1

    return score
    
def get_feature_difference(item1, item2):
    color_diff = int(item1["Colors"] != item2["Colors"])
    main_category_diff = int(item1["Main Category"] != item2["Main Category"])
    subcategory_diff = int(item1["Subcategory"] != item2["Subcategory"])
    overlapping_seasons = len(set(item1["Season"]).intersection(set(item2["Season"])))
    return [color_diff, main_category_diff, subcategory_diff, overlapping_seasons]


sample_df = df.sample(n=200, random_state=42)

X_sample = []
y_sample = []

for idx1, item1 in sample_df.iterrows():
    for idx2, item2 in sample_df.iterrows():
        if idx1 != idx2:
            feature_diff = get_feature_difference(item1, item2)
            similarity_score = compute_advanced_similarity_v3_updated(item1, item2)
            X_sample.append(feature_diff)
            y_sample.append(similarity_score)

# Splitting the dataset 
X_train_sample, X_test_sample, y_train_sample, y_test_sample = train_test_split(X_sample, y_sample, test_size=0.2, random_state=42)

# Normalizing/
scaler = StandardScaler()
X_train_sample_scaled = scaler.fit_transform(X_train_sample)
X_test_sample_scaled = scaler.transform(X_test_sample)


model_sample = LinearRegression().fit(X_train_sample_scaled, y_train_sample)


def generate_outfits_regression_v6_urls(reference_item, df, gender, color_profile="Complementary", color_temp=None, config_class=config, excluded_accessories=["headband"], num_accessories=3):
    base_categories = list(config_class.base_category_constraints.keys())

    reference_subcategory = reference_item["Subcategory"]
    reference_main_category = None
    for category, subcategories in config_class.base_category_constraints.items():
        if reference_subcategory.lower() in [sub.lower() for sub in subcategories]:
            reference_main_category = category
            break

    base_items = get_top_similar_items_regression_fixed_with_constraints(reference_item, df, base_categories, compute_advanced_similarity_v3_updated, gender)
    accessory_items = df[(df["Main Category"] == "Accessories") & ((df["Gender"].str.lower() == gender.lower()) | (df["Gender"].str.lower() == "any") | df["Gender"].isnull())].to_dict(orient="records")
    accessory_items = [item for item in accessory_items if item["Subcategory"] not in excluded_accessories]

    for category, items in base_items.items():
        # Sort the top 10 items 
        top_items = sorted(items[:10], key=lambda x: (
            (x["Colors"] in config.COLOR_PROFILES.get(color_profile, {}).get(reference_item["Colors"], [])) * 2 + 
            (color_temp == "warm" and x["Colors"] in config.WARM_COLORS) + 
            (color_temp == "cool" and x["Colors"] in config.COOL_COLORS)), reverse=True)
        
        # Randomize the remaining items
        remaining_items = random.sample(items[10:], len(items[10:]))
        base_items[category] = top_items + remaining_items

    outfits = set()
    while len(outfits) < config_class.MAX_OUTFITS:
        chosen_colors = [reference_item["Colors"]] # Starting with the reference item's color
        base = []

        for category in base_categories:
            if category != reference_main_category:
                # Prioritize the sorted items but sometimes pick random items for variety
                if random.random() > config_class.PRIORITY_RANDOM_SELECTION:
                    item_choice = random.choice(base_items.get(category, [reference_item]))  # Default to reference item if list is empty
                else:
                    # profile_colors = config_class.COLOR_PROFILES.get(color_profile, {}).get(chosen_colors[-1], [])
                    # sorted_items = sorted(base_items.get(category, []), key=lambda x: profile_colors.index(x["Colors"]) if x["Colors"] in profile_colors else config_class.TOP_N_ITEMS_TO_SORT)
                    # item_choice = sorted_items[0] if sorted_items else random.choice(base_items.get(category, [reference_item]))
                    item_choice = base_items[category][0]  # Get the top item from the sorted list
                # chosen_colors.append(item_choice["Colors"])
                base.append(generate_url(item_choice["Product ID"]))

        # Insert reference item in its corresponding position
        if reference_main_category and reference_main_category in base_categories:
            base.insert(base_categories.index(reference_main_category), generate_url(reference_item["Product ID"]))

        chosen_accessories = random.sample(accessory_items, min(num_accessories, len(accessory_items)))
        unique_subcategories = set()
        final_accessories = []
        for accessory in chosen_accessories:
            if accessory["Subcategory"] not in unique_subcategories:
                unique_subcategories.add(accessory["Subcategory"])
                final_accessories.append(accessory)

        accessories = [generate_url(item["Product ID"]) for item in final_accessories]

        outfit = tuple(base + accessories)
        outfits.add(outfit)

    return list(outfits)



class Generator():   

     
    def start_genertation(categoryName, preset= "bohemian", gender = "Women"):
        general_preset = presets
        if gender == "Women" :
            if preset == "normal":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.GenerateOutfitsConfig)
                output_dict = {categoryName: outfit_combinations_regression_v5_urls}
            elif preset == "bohemian":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.WomensBohemianConfig)
                output_dict = {categoryName: outfit_combinations_regression_v5_urls}
            elif preset == "colourful":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.GenerateOutfitsConfig)
                output_dict = {categoryName: outfit_combinations_regression_v5_urls}
            elif preset == "streetwear":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.StreetwearConfig)
                output_dict = {categoryName: outfit_combinations_regression_v5_urls}
            elif preset == "classy": 
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.ClassyConfig)
                output_dict = {categoryName: outfit_combinations_regression_v5_urls}
            elif preset == "romantic":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.WomensRomanticConfig)
                output_dict = {categoryName: outfit_combinations_regression_v5_urls}
        return output_dict
    
    def start_genertation_advanced(categoryName, preset= "bohemian", gender="Women", color_profile= "Complimentary", color_temp="warm"):
        general_preset = presets
        if gender == "Women" :
            if preset == "normal":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women", color_profile=color_profile, color_temp=color_temp,config_class= general_preset.GenerateOutfitsConfig)
                output_dict = {categoryName: outfit_combinations_regression_v5_urls}
            elif preset == "bohemian":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.WomensBohemianConfig)
                output_dict = {categoryName: outfit_combinations_regression_v5_urls}
            elif preset == "colourful":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.GenerateOutfitsConfig)
                output_dict = {categoryName: outfit_combinations_regression_v5_urls}
            elif preset == "streetwear":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.StreetwearConfig)
                output_dict = {categoryName: outfit_combinations_regression_v5_urls}
            elif preset == "classy": 
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.ClassyConfig)
                output_dict = {categoryName: outfit_combinations_regression_v5_urls}
            elif preset == "romantic":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.WomensRomanticConfig)
                output_dict = {categoryName: outfit_combinations_regression_v5_urls}
        return output_dict
    
    
    
    def generate_with_image(category_name, refrence_image):
        reference_item = df[df["Subcategory"].str.contains(category_name, case=False, na=False)].sample(n=1).iloc[0]
        reference_item_title = reference_item["Product Title"]
        outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Men", color_profile="Triads", color_temp="warm")
        output_dict = {category_name: outfit_combinations_regression_v5_urls}
        return output_dict
    
    # Generate outfits allow the user to select presets 
    
    def start_genertation_html(categoryName, preset, gender = "Women"):
        general_preset = presets
        if gender == "Women" :
            if preset == "normal":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.GenerateOutfitsConfig)
            elif preset == "bohemian":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.WomensBohemianConfig)
            elif preset == "colourful":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.GenerateOutfitsConfig)
            elif preset == "streetwear":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.StreetwearConfig)
            elif preset == "classy": 
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.ClassyConfig)
            elif preset == "romantic":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Women",config_class= general_preset.WomensRomanticConfig)
        elif gender == "Men" : 
            if preset == "normal":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Men",config_class= general_preset.GenerateOutfitsConfig)
            elif preset == "minimal":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Men",config_class= general_preset.MenMinimalConfig)
            elif preset == "smart":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Men",config_class= general_preset.MenSmartConfig)
            elif preset == "streetwear":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Men",config_class= general_preset.StreetwearConfig)
            elif preset == "outdoor": 
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Men",config_class= general_preset.MenOutdoorConfig)
            elif preset == "classy":
                reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
                reference_item_title = reference_item["Product Title"]
                outfit_combinations_regression_v5_urls = generate_outfits_regression_v6_urls(reference_item, df, "Men",config_class= general_preset.ClassyConfig)
                     
            

        image_tag_template = '<img src="{}" style="object-fit: contain; width: 400px; height: 400px; margin: 5px;">'
        outfit_divs = ""
        outfit_id = 1  # Initialize outfit ID

        for outfit in outfit_combinations_regression_v5_urls:
            outfit_divs += f'<div class="outfit-combination" id="outfit-{outfit_id}"><h2>Outfit ID: {outfit_id}</h2><h3>{reference_item_title}</h3>'
            for i in range(3):  # 3 rows
                outfit_divs += '<div class="outfit-row">'
                for j in range(3):  # 3 columns
                    if i * 3 + j < len(outfit):
                        outfit_divs += image_tag_template.replace("{}", outfit[i * 3 + j])
                outfit_divs += '</div>'
            outfit_divs += '</div>'
            outfit_id += 1  # Increment the outfit ID

        html_template = f"""
    <html>
    <head>
    <title>
    Outfit Combinations
    </title>
    <style>
    .outfit-combination {{
        border: 1px solid #ddd;
        padding: 20px;
        margin-bottom: 20px;
        display: none;
    }}
    .outfit-combination:first-of-type {{
        display: block;
    }}
    .outfit-row {{
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .navigation-buttons {{
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }}
    button {{
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        margin: 0 10px;
    }}
    </style>
    </head>
    <body>
    {outfit_divs}
    <div class="navigation-buttons">
    <button id="prev-button">
    Previous
    </button>
    <button id="next-button">
    Next
    </button>
    </div>
    <script>
    document.getElementById("prev-button").addEventListener("click", function() {{
        navigateOutfit(-1);
    }});
    document.getElementById("next-button").addEventListener("click", function() {{
        navigateOutfit(1);
    }});
    function navigateOutfit(direction) {{
        let outfits = document.querySelectorAll(".outfit-combination");
        let currentIndex = -1;
        for (let i = 0; i < outfits.length; i++) {{
            if (getComputedStyle(outfits[i]).display !== 'none') {{
                currentIndex = i;
                break;
            }}
        }}
        if (currentIndex !== -1) {{
            outfits[currentIndex].style.display = 'none';
            let newIndex = currentIndex + direction;
            if (newIndex < 0) newIndex = outfits.length - 1;
            if (newIndex >= outfits.length) newIndex = 0;
            outfits[newIndex].style.display = 'block';
        }}
    }}
    </script>
    </body>
    </html>
        """

        return html_template




