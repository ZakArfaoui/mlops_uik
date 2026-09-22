import pickle
from pathlib import Path
from xgboost import XGBRegressor
from data_prep import load_and_split_data

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = BASE_DIR / "artifacts"

def train_and_save_model():
    """Trains the XGBoost model and saves it to the local artifacts folder."""
    # Ensure the artifacts directory exists
    ARTIFACT_DIR.mkdir(exist_ok=True)

    # Fetch clean, properly scaled data
    X_train, X_test, y_train, y_test = load_and_split_data()

    print("Training XGBoost Regressor...")
    # Modularized model instantiation
    model = XGBRegressor(n_estimators=100, max_depth=3)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Model R2 Score on Test Set: {score:.4f}")

    # DYNAMIC SAVE PATH
    model_path = ARTIFACT_DIR / "model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print(f"Model successfully saved to: {model_path}")

if __name__ == "__main__":
    train_and_save_model()