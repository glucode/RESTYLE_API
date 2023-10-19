import pandas as pd
import random
import json
import os
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import base64

# 1. Data Loading and Preprocessing
df = pd.read_csv("external_files/Dataset/Demo_metadata.csv", delimiter=";", on_bad_lines='skip')
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

# def generate_url(product_id, folder_path=image_folder):
#     for filename in os.listdir(folder_path):
#         if product_id in filename:
#             file_path = os.path.join(folder_path, filename)
#             with open(file_path, "rb") as image_file:
#                 encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#             return encoded_string
#     return None  # Return None if no matching file is found

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
        feature_diffs = []
        items_in_category = []
        for _, item in df.iterrows():
            if item["Product ID"] != reference_item["Product ID"]:
                main_category = str(item["Main Category"]).lower()
                subcategory = str(item["Subcategory"]).lower()
                is_category = any(sub in subcategory for sub in subcategories)
                item_gender = str(item.get("Gender", "")).lower()
                is_gender_suitable = item_gender in [gender.lower(), "any", ""]
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

def generate_outfits_regression_v5_urls(reference_item, df, gender, max_outfits=30):
    base_categories = ["tops", "trousers", "shoes"]
    accessory_categories = ["jewellery", "bags", "caps", "belts", "socks", "bracelets", "eyewear"]

    # Identify the main category of the reference item
    reference_subcategory = reference_item["Subcategory"]
    reference_main_category = None
    for category, subcategories in base_category_constraints.items():
        if reference_subcategory.lower() in [sub.lower() for sub in subcategories]:
            reference_main_category = category
            break

    base_items = get_top_similar_items_regression_fixed(reference_item, df, base_categories, compute_advanced_similarity_v3_updated)
    accessory_items = get_top_similar_items_regression_fixed(reference_item, df, accessory_categories, compute_advanced_similarity_v3_updated)

    outfits = set()
    while len(outfits) < max_outfits:
        base = [generate_url(random.choice(base_items[category])["Product ID"]) for category in base_categories]
        
        # Replace the item in the outfit that matches the main category of the reference item with the reference item
        if reference_main_category:
            base[base_categories.index(reference_main_category)] = generate_url(reference_item["Product ID"])
        
        accessory_count = random.randint(0, len(accessory_items))
        chosen_accessories = random.sample(accessory_categories, accessory_count)
        accessories = [generate_url(random.choice(accessory_items[category])["Product ID"]) for category in chosen_accessories]
        accessories[:3]
        outfit = tuple(base + accessories)
        outfits.add(outfit)
        
    return list(outfits)


def generate_outfits_regression_v6_urls(reference_item,user_image, df, gender, max_outfits=30):
    base_categories = ["tops", "trousers", "shoes"]
    accessory_categories = ["jewellery", "bags", "caps", "belts", "socks", "bracelets", "eyewear"]

    # Identify the main category of the reference item
    reference_subcategory = reference_item["Subcategory"]
    reference_main_category = None
    for category, subcategories in base_category_constraints.items():
        if reference_subcategory.lower() in [sub.lower() for sub in subcategories]:
            reference_main_category = category
            break

    base_items = get_top_similar_items_regression_fixed(reference_item, df, base_categories, compute_advanced_similarity_v3_updated)
    accessory_items = get_top_similar_items_regression_fixed(reference_item, df, accessory_categories, compute_advanced_similarity_v3_updated)

    outfits = set()
    while len(outfits) < max_outfits:
        base = [generate_url(random.choice(base_items[category])["Product ID"]) for category in base_categories]
        
        # Replace the item in the outfit that matches the main category of the reference item with the reference item
        if reference_main_category:
            base[base_categories.index(reference_main_category)] = user_image
        
        accessory_count = random.randint(0, len(accessory_items))
        chosen_accessories = random.sample(accessory_categories, accessory_count)
        accessories = [generate_url(random.choice(accessory_items[category])["Product ID"]) for category in chosen_accessories]
        accessories[:3]
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

        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Image Display</title>
        </head>
        <body>
            <table border="1">
                <tr>
                    <th>Uploaded Image name</th>
                    <th>Look</th>
                </tr>
                {}
            </table>
        </body>
        </html>
        """

        image_template = """
        <tr>
            <td>{key}</td>
            <td>
                {images}
            </td>
        </tr>
        """

        image_tag_template = '<img src="{}" style="margin: 5px;object-fit: cover; width: 100px;">'

        table_rows = ""
        for combination in outfit_combinations_regression_v5_urls:
            image_tags = "".join([image_tag_template.format(image) for image in combination])
            table_rows += image_template.format(key=reference_item_title, images=image_tags)

        final_html = html_template.format(table_rows)
        return final_html




