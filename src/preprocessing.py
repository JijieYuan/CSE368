import pandas as pd
import os

all_data = []

files = os.listdir("datasets")
for file in files:
    if file.endswith(".csv") == False:
        continue
    if file == "processed_dataset.csv":
        continue

    df = pd.read_csv("datasets/" + file, on_bad_lines='skip')

    if "label" not in df.columns:
        continue

    if "text_combined" in df.columns:
        df["text"] = df["text_combined"]
    elif "body" in df.columns:
        if "subject" in df.columns:
            df["subject"] = df["subject"].fillna("")
            df["body"] = df["body"].fillna("")
            df["text"] = df["subject"] + " " + df["body"]
        else:
            df["text"] = df["body"]
    else:
        continue

    temp = pd.DataFrame()
    temp["text"] = df["text"]
    temp["label"] = df["label"]
    all_data.append(temp)

combined = pd.concat(all_data)

cleaned_texts = []
cleaned_labels = []

for i in range(len(combined)):
    text = combined.iloc[i]["text"]
    label = combined.iloc[i]["label"]

    if pd.isna(text):
        continue

    text = str(text)
    text = text.lower()

    words = text.split()
    text = ""
    for word in words:
        text = text + word + " "
    text = text.strip()

    if len(text) == 0:
        continue

    cleaned_texts.append(text)
    cleaned_labels.append(label)

final = pd.DataFrame()
final["text"] = cleaned_texts
final["label"] = cleaned_labels

final = final.drop_duplicates(subset=["text"])
final["label"] = final["label"].astype(int)
final = final.sample(frac=1)

final.to_csv("datasets/processed_dataset.csv", index=False)

print("data is ready")
