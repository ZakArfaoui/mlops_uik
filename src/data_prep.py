import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# DYNAMIC PATHS: Resolves relative to this script's location
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "california_housing_raw.csv"

def load_and_split_data():
    """Loads data, splits it, and scales it without data leakage."""
    print(f"Loading data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)

    X = df.drop('MedHouseVal', axis=1)
    y = df['MedHouseVal']

    # FIX: Split FIRST to prevent data leakage
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # FIX: Fit scaler ONLY on training data
    scaler = StandardScaler()

    # Scale specific features
    features_to_scale = ['MedInc', 'HouseAge']
    X_train.loc[:, features_to_scale] = scaler.fit_transform(X_train[features_to_scale])

    # Transform test data using the training data's distribution
    X_test.loc[:, features_to_scale] = scaler.transform(X_test[features_to_scale])

    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Quick local test
    X_tr, X_te, y_tr, y_te = load_and_split_data()
    print(f"Training data shape: {X_tr.shape}")