from loaders import DataLoader, RecordEncoder, RecordDecoder
from sklearn_crfsuite import CRF

crf = CRF(
    algorithm="lbfgs",
    c1=0.01,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True,
)


trainset = DataLoader.load_data("data/train")
devset = DataLoader.load_data("data/dev")
clean_trainset = [record for record in trainset if len(record.quintuples) > 0]

encoder = RecordEncoder()
decoder = RecordDecoder()


x = [encoder.record2features(record) for record in clean_trainset]
y = [encoder.record2tags(record)[0] for record in clean_trainset]


crf.fit(x, y)


x_val = [encoder.record2features(record) for record in devset]

sample_x_val = x_val[3]

prediction = crf.predict_single(sample_x_val)

print([decoder.id2tag(_id) for _id in prediction])
