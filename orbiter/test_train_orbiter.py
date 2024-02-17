print("[test_train_orbiter] import libraries")
import train_orbiter as train_orbiter

clf, vectoriser, len_train = train_orbiter.train("source data/test.csv")
print(f'[test_train_orbiter] orbiter was trained on {len_train} items')
