import argparse
from imutils import paths
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from pyimagesearch.preprocessing import SimplePreprocessor
from pyimagesearch.datasets import SimpleDatasetLoader


#construct the argument parse and parse the arguments
ap=argparse.ArgumentParser()
ap.add_argument("-d","--dataset",required=True,
                help="path to input dataset")
ap.add_argument("-k","--neighbors",type=int,default=1,
                help="# of nearest neighbors for classification")
ap.add_argument("-j","--jobs",type=int,default=-1,
                help="# of jobs for k-NN distance (-1 uses all available cores)")
args = vars(ap.parse_args())

#grab the list of images that we'll describe
imagePaths=list(paths.list_images(args["dataset"]))

#load data
print("[INFO] loading images...")
sp=SimplePreprocessor(32,32)
sdl=SimpleDatasetLoader(preprocessors=[sp])
(data,labels) = sdl.load(imagePaths, verbose=500)

data=data.reshape((data.shape[0],3072))

print("[INFO] features matrix: {:.1f}MB".format(data.nbytes/(1024*1000)))

#encode the labels as intergers
le=LabelEncoder()
labels=le.fit_transform(labels)

(trainX,testX,trainY,testY)=train_test_split(data,labels,test_size=0.25,random_state=42)
print("[INFO] evaluating k-NN classifier...")
model=KNeighborsClassifier(n_neighbors=args["neighbors"],
                            n_jobs=args["jobs"])
model.fit(trainX,trainY)
print(classification_report(testY,model.predict(testX),target_names=le.classes_))



