from dataloader import DataLoader
from processing import RecordEncoder, RecordDecoder
from utils import dupplicate_record_by_quintuple
from sklearn_crfsuite import CRF

crf = CRF(
    algorithm="lbfgs",
    c1=0.01,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True,
)


trainset = DataLoader.load_data("../data/train")
devset = DataLoader.load_data("../data/dev")

cleaned_trainset = []
for record in trainset:
    if not record.quintuples:
        continue

    cleaned_trainset.extend(dupplicate_record_by_quintuple(record))


encoder = RecordEncoder()
decoder = RecordDecoder()


x = [encoder.record2features(record) for record in cleaned_trainset]
# We are sure that record only have 1 quintuple -> 1 tag list.
y = [encoder.record2tags(record) for record in cleaned_trainset]
crf.fit(x, y)


x_val = [encoder.record2features(record) for record in devset]
sample_x_val = x_val[1]

prediction = crf.predict_single(sample_x_val)

print(devset[1])
print([decoder.parse_tag(_id) for _id in prediction])
