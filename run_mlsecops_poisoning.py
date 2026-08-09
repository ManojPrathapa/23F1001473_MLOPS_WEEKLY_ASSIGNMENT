import numpy as np
import pandas as pd
import mlflow
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def poison_data(X, y, corruption_rate):
    """Replaces a percentage of the data with random features and random labels."""
    if corruption_rate == 0.0:
        return X.copy(), y.copy()
    
    n_samples = len(X)
    n_poisoned = int(n_samples * corruption_rate)
    
    # Select random indices to corrupt
    np.random.seed(42)  # For reproducibility
    poison_indices = np.random.choice(n_samples, n_poisoned, replace=False)
    
    X_poisoned = X.copy()
    y_poisoned = y.copy()
    
    # Inject completely random noise (simulating a severe poisoning attack)
    for idx in poison_indices:
        # IRIS features are roughly between 0.1 and 8.0, we inject random uniform noise [0, 10]
        X_poisoned[idx] = np.random.uniform(0, 10, size=X.shape[1])
        # Random class label (0, 1, or 2)
        y_poisoned[idx] = np.random.choice([0, 1, 2])
        
    return X_poisoned, y_poisoned

if __name__ == "__main__":
    # 1. Load Clean Data
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # 2. Split into Train/Test (We ONLY poison the training data)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # 3. Setup MLflow Experiment
    experiment_name = "MLSecOps_Data_Poisoning"
    mlflow.set_experiment(experiment_name)
    
    corruption_levels = [0.0, 0.05, 0.10, 0.50]
    
    print("Starting MLSecOps Data Poisoning Simulation...\n")
    print("-" * 50)
    print(f"{'Poison %':<10} | {'Accuracy':<10} | {'F1 Score':<10}")
    print("-" * 50)
    
    for rate in corruption_levels:
        with mlflow.start_run(run_name=f"Poisoning_Level_{int(rate*100)}%"):
            # A. Poison the training data
            X_train_poisoned, y_train_poisoned = poison_data(X_train, y_train, rate)
            
            # B. Train the model
            clf = DecisionTreeClassifier(random_state=42)
            clf.fit(X_train_poisoned, y_train_poisoned)
            
            # C. Evaluate on the CLEAN test set
            y_pred = clf.predict(X_test)
            
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
            
            # D. Log to MLflow
            mlflow.log_param("corruption_rate", rate)
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("precision", prec)
            mlflow.log_metric("recall", rec)
            mlflow.log_metric("f1_score", f1)
            
            print(f"{int(rate*100):<9}% | {acc:<10.4f} | {f1:<10.4f}")
            
    print("-" * 50)
    print("\nSimulation complete. Metrics logged to MLflow.")
