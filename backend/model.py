import pickle

# simple "trained" model parameters
model = {
    "weights": {
        "rain": 0.4,
        "temp": 0.3,
        "activity": 0.3
    },
    "bias": -0.2
}

# save as model artifact
pickle.dump(model, open("model.pkl", "wb"))

print("Custom model saved!")