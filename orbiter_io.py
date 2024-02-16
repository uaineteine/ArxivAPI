print("[orbiter_io] importing libraries")
import pickle

def save_model(clf, vectoriser, filename):
    # Save to file
    with open(filename, 'wb') as f:
        pickle.dump((clf, vectoriser), f)

def load_model(filename):
    # Load from file
    with open(filename, 'rb') as f:
        clf, vectoriser = pickle.load(f)
    return clf, vectoriser
