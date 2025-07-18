# analysis/eda_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import os

# Load the scraped CSV
data_path = os.path.join("..", "scraper", "data", "alibaba_all_products.csv")
df = pd.read_csv(data_path)

print("📊 Data Overview:")
print(df.head())

# === Clean & preprocess ===
df = df[df["Title"] != "N/A"]
df = df[df["Image_URL"] != "N/A"]

# Normalize price
df["Price_clean"] = df["Price"].str.extract(r'([\d.,]+)')
df["Price_clean"] = df["Price_clean"].replace(",", "", regex=True).astype(float)

# === Summary statistics ===
print("\n📈 Price Summary:")
print(df["Price_clean"].describe())

print("\n📦 Top MOQ Values:")
print(df["MOQ"].value_counts().head())

# === Frequent keywords ===
words = []
for title in df["Title"]:
    tokens = re.findall(r'\b\w+\b', title.lower())
    words.extend([word for word in tokens if len(word) > 3])

top_keywords = Counter(words).most_common(15)
print("\n📝 Top Keywords in Product Titles:")
for word, count in top_keywords:
    print(f"{word}: {count}")

# === Visuals ===
plt.figure(figsize=(10, 6))
sns.histplot(df["Price_clean"], bins=30, kde=True)
plt.title("Price Distribution")
plt.xlabel("Price (USD)")
plt.ylabel("Product Count")
plt.tight_layout()
plt.savefig("price_distribution.png")
plt.show()

# === Check for anomalies ===
print("\n❗ Price Outliers (above $100,000):")
print(df[df["Price_clean"] > 100000])

print("\n🧼 Duplicate rows:", df.duplicated().sum())
