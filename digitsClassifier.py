from commonfunctions import *
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import svm
import cv2 as cv2
import os
import random
from sklearn.model_selection import train_test_split
import pickle

random_seed = 42  
random.seed(random_seed)
np.random.seed(random_seed)
path_to_dataset = r'numbers'
target_img_size = (32, 32)
untrained=svm.LinearSVC(random_state=random_seed)
def extract_hog_features(img):
    img = cv2.resize(img, target_img_size)
    win_size = (32, 32)
    cell_size = (4, 4)
    block_size_in_cells = (2, 2)
    block_size = (block_size_in_cells[1] * cell_size[1], block_size_in_cells[0] * cell_size[0])
    block_stride = (cell_size[1], cell_size[0])
    nbins = 9  # Number of orientation bins
    hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)
    h = hog.compute(img)
    h = h.flatten()
    return h.flatten()


def load_dataset(feature_set='hog'):
    features = []
    labels = []
   
    img_filenames = os.listdir(path_to_dataset)

    for i, fn in enumerate(img_filenames):
        if fn.split('.')[-1] != 'png':
            continue

        label = fn.split('.')[0][0]
        labels.append(label)
    

        path = os.path.join(path_to_dataset, fn)
        img = cv2.imread(path,flags=cv2.IMREAD_GRAYSCALE)
        features.append(extract_hog_features(img))
        if i > 0 and i % 1000 == 0:
            print("[INFO] processed {}/{}".format(i, len(img_filenames)))
    return features, labels 



def run_experiment(feature_set):
    if os.path.exists("trained_model.pickle"):
        return
    else:
        features, labels = load_dataset(feature_set)
        train_features, test_features, train_labels, test_labels = train_test_split(
            features, labels, test_size=0.2, random_state=random_seed)
        untrained.fit(train_features, train_labels)
        accuracy = untrained.score(test_features, test_labels)
        print('SVM:', accuracy*100, '%')
        with open("trained_model.pickle", "wb") as file:
            pickle.dump(untrained, file)

def runTest(img):
    if os.path.exists("trained_model.pickle"):
        trained_model = pickle.load(open("trained_model.pickle", "rb"))
        features = extract_hog_features(img)
        return(trained_model.predict([features]))
    else:
        features = extract_hog_features(img)
        return(untrained.predict([features]))
