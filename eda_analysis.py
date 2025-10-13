import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def perform_eda(file_path):
    """Run basic Exploratory Data Analysis (EDA) on a given CSV file."""
    try:
        if not file_path.lower().endswith(".csv"):
            return "Unsupported file format. Please provide a CSV file."

        # Load dataset into DataFrame
        data = pd.read_csv(file_path)

        # Collecting basic dataset information
        eda_summary = {
            "Shape": data.shape,
            "Columns": list(data.columns),
            "Missing Values": data.isnull().sum().to_dict(),
            "Basic Stats": data.describe().to_dict()
        }

        # Generate and save correlation heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(data.corr(), annot=True, cmap="coolwarm", fmt=".2f")
        heatmap_file = "eda_heatmap.png"
        plt.savefig(heatmap_file)
        plt.close()

        return eda_summary, heatmap_file

    except Exception as error:
        return f"Error during EDA: {error}"

