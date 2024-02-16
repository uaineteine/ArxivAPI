print("[test_train_orbiter] import libraries")
import train_orbiter

train_orbiter.train("source data/test_data.csv")

# Save the model
#dump(clf, "trained_models/processing/filename.joblib") 

# Load the model
#clf = load('filename.joblib') 