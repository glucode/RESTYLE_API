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

# 1. Data Loading and Preprocessing
df = pd.read_csv("external_files/Dataset/Cleaned_Dataset.csv", delimiter=",", on_bad_lines='skip')
df["Season"] = df["Season"].apply(lambda x: x.split(", ") if isinstance(x, str) else [])
image_folder = "external_files/Dataset_images"

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
        score = 0
        if item1["Colors"] == item2["Colors"]:
            score += 1
        if item1["Main Category"] == item2["Main Category"]:
            score += 1
        if item1["Subcategory"] == item2["Subcategory"]:
            score += 1
        overlapping_seasons = set(item1["Season"]).intersection(set(item2["Season"]))
        score += len(overlapping_seasons)
        return score
    
def determine_current_season():
    month = datetime.now().month
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"
    
def get_top_similar_items_regression_fixed_with_constraints(reference_item, df, categories, similarity_function, gender, top_n=5):
    category_items = {}
    for category, subcategories in base_category_constraints.items():
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
    
    # Use the user's item as the reference item
    reference_item = {"Product ID": refrence_category, "Image Path": user_item_path}  # Add other necessary attributes
    
    base_categories = ["tops", "trousers", "shoes"]
    accessory_categories = ["jewellery", "bags", "caps", "belts", "socks", "bracelets", "eyewear"]

    base_items = get_top_similar_items_regression_fixed(refrence_category, df, base_categories, compute_advanced_similarity_v3_updated)
    accessory_items = get_top_similar_items_regression_fixed(refrence_category, df, accessory_categories, compute_advanced_similarity_v3_updated)

    outfits = set()
    while len(outfits) < max_outfits:
        base = [generate_url(random.choice(base_items[category])["Product ID"]) for category in base_categories]
        
        # Replace the item in the outfit that matches the main category of the reference item with the user's item
        base[base_categories.index(refrence_category)] = user_item_path  # Assuming the user's item is a "top". Modify as needed.
        
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
    current_season = determine_current_season()
    if current_season in item2["Season"] or len(item2["Season"]) == 4:  # If the item is for all seasons
        score += 1

    return score
    
def get_feature_difference(item1, item2):
    color_diff = int(item1["Colors"] != item2["Colors"])
    main_category_diff = int(item1["Main Category"] != item2["Main Category"])
    subcategory_diff = int(item1["Subcategory"] != item2["Subcategory"])
    overlapping_seasons = len(set(item1["Season"]).intersection(set(item2["Season"])))
    return [color_diff, main_category_diff, subcategory_diff, overlapping_seasons]

# Assume df is your DataFrame
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

# Splitting the dataset into training and testing sets
X_train_sample, X_test_sample, y_train_sample, y_test_sample = train_test_split(X_sample, y_sample, test_size=0.2, random_state=42)

# Normalizing/Standardizing the data
scaler = StandardScaler()
X_train_sample_scaled = scaler.fit_transform(X_train_sample)
X_test_sample_scaled = scaler.transform(X_test_sample)

# Training the model
model_sample = LinearRegression().fit(X_train_sample_scaled, y_train_sample)

# Making predictions
y_pred_train = model_sample.predict(X_train_sample_scaled)
y_pred_test = model_sample.predict(X_test_sample_scaled)

# Evaluating the model
# Mean Squared Error (MSE)
mse_train = mean_squared_error(y_train_sample, y_pred_train)
mse_test = mean_squared_error(y_test_sample, y_pred_test)

# R-squared (R2)
r2_train = r2_score(y_train_sample, y_pred_train)
r2_test = r2_score(y_test_sample, y_pred_test)

# Mean Absolute Error (MAE)
mae_train = mean_absolute_error(y_train_sample, y_pred_train)
mae_test = mean_absolute_error(y_test_sample, y_pred_test)

# Print the evaluation metrics
# print(f'Training MSE: {mse_train}, Testing MSE: {mse_test}')
# print(f'Training R2: {r2_train}, Testing R2: {r2_test}')
# print(f'Training MAE: {mae_train}, Testing MAE: {mae_test}')


def generate_outfits_regression_v5_urls(reference_item, df, gender, max_outfits=40):
    base_categories = list(base_category_constraints.keys())

    # Identify the main category of the reference item
    reference_subcategory = reference_item["Subcategory"]
    reference_main_category = None
    for category, subcategories in base_category_constraints.items():
        if reference_subcategory.lower() in [sub.lower() for sub in subcategories]:
            reference_main_category = category
            break

    base_items = get_top_similar_items_regression_fixed_with_constraints(reference_item, df, base_categories, compute_advanced_similarity_v3_updated, gender)
    accessory_items = df[(df["Main Category"] == "Accessories") & ((df["Gender"].str.lower() == gender.lower()) | (df["Gender"].str.lower() == "any") | df["Gender"].isnull())].to_dict(orient="records")
   
    
    outfits = set()
    while len(outfits) < max_outfits:
        chosen_colors = [reference_item["Colors"]]
        base = []

        for category in base_categories:
            if category != reference_main_category:
                # Prioritize complementary colors but sometimes pick random colors for variety
                if random.random() > 0.7:
                    item_choice = random.choice(base_items[category])
                else:
                    complementary_colors = COLOR_WHEEL.get(chosen_colors[-1], [])
                    item_choice = next((item for item in base_items[category] if item["Colors"] in complementary_colors), random.choice(base_items[category]))
                chosen_colors.append(item_choice["Colors"])
                base.append(generate_url(item_choice["Product ID"]))

        # Insert reference item in its corresponding position
        if reference_main_category and reference_main_category in base_categories:
            base.insert(base_categories.index(reference_main_category), generate_url(reference_item["Product ID"]))

        chosen_accessories = random.sample(accessory_items, min(4, len(accessory_items)))
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
    def compute_color_similarity_updated(item1, item2):
        color1 = item1["Colors"]
        color2 = item2["Colors"]

        if not color1 or not color2:
            return 0

        if color1 in ["White", "Black"] or color2 in ["White", "Black"]:
            return 2

        if color1 == color2:
            return 2  # Monochrome

        if color2 in COLOR_WHEEL.get(color1, []):
            if COLOR_WHEEL[color1].index(color2) == 0:
                return 2  # Complementary
            elif COLOR_WHEEL[color1].index(color2) < 3:
                return 1  # Analogous or Split Complementary
            else:
                return 0.5  # Triadic or Tetradic
        return 0
    
    # Generate outfits and structure them as a dictionary
    def start_genertation(categoryName):
        reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
        reference_item_title = reference_item["Product Title"]
        outfit_combinations_regression_v5_urls = generate_outfits_regression_v5_urls(reference_item, df, "Men")
        output_dict = {reference_item_title: outfit_combinations_regression_v5_urls}
        return output_dict
    
    def generate_with_image(category_name, refrence_image):
        reference_item = df[df["Subcategory"].str.contains(category_name, case=False, na=False)].sample(n=1).iloc[0]
        reference_item_title = reference_item["Product Title"]
        outfit_combinations_regression_v5_urls = generate_outfits_regression_v5_urls(reference_item , df, "Men")
        output_dict = {category_name: outfit_combinations_regression_v5_urls}
        return output_dict
    
        
    def start_genertation_html(categoryName):
        reference_item = df[df["Subcategory"].str.contains(categoryName, case=False, na=False)].sample(n=1).iloc[0]
        reference_item_title = reference_item["Product Title"]
        outfit_combinations_regression_v5_urls = generate_outfits_regression_v5_urls(reference_item, df, "Men")

        image_tag_template = '<img src="{}" style="object-fit: contain; width: 400px; height: 400px; margin: 5px;">'
        outfit_divs = ""

        for outfit in outfit_combinations_regression_v5_urls:
            outfit_divs += f'<div class="outfit-combination"><h2>{reference_item_title}</h2>'
            for i in range(3):  # 3 rows
                outfit_divs += '<div class="outfit-row">'
                for j in range(3):  # 3 columns
                    if i * 3 + j < len(outfit):
                        outfit_divs += image_tag_template.replace("{}", outfit[i * 3 + j])
                outfit_divs += '</div>'
            outfit_divs += '</div>'

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




