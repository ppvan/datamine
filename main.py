from loaders import DataLoader


loader = DataLoader()
trainset = loader.load_data("data/train")

print(trainset[:5])
