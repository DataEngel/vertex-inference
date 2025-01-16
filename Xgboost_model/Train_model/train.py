import xgboost as xgb
import numpy as np

# Create a small dummy dataset
X = np.random.rand(10, 3)  # 10 samples, 3 features
y = np.random.randint(0, 2, size=10)  # Binary target

# Convert to DMatrix
dtrain = xgb.DMatrix(X, label=y)

# Train a simple model
params = {
    "objective": "binary:logistic",  # Binary classification
    "max_depth": 2,
    "eta": 0.1,
    "verbosity": 0
}
model = xgb.train(params, dtrain, num_boost_round=1)

# Save the model to 'model.bst'
model.save_model('model.bst')
print("Dummy model saved as 'model.bst'")
