import os
import pickle
from functools import lru_cache             # load pkl file in cache
from django.conf import settings            # get base directory access

@lru_cache(maxsize=1)
def load_pkl():
    pkl_path = os.path.join(settings.BASE_DIR, 'recommend', 'pkl_folder', 'crop_recommend.pkl')

    with open(pkl_path, 'rb') as f:
        lod = pickle.load(f)

    assert 'model' in lod and 'features' in lod, "Invalid loaded structure!"
    return lod

def start_prediction(feature_dict):
    loaded = load_pkl()
    model = loaded["model"]
    features_col = loaded["features"]       #['N','P', 'K', 'temperature', 'humidity','ph' ,'rainfall']

    X = [[float(feature_dict[c]) for c in features_col]]
    pred = model.predict(X)[0]
    return pred