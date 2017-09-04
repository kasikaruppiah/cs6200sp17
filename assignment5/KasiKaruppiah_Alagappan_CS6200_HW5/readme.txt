Requirements:
	python 2.7

Steps:
	Navigate to the directory of the source code, directory containing nbtrain.py and nbtest.py
	To train the classifier run the command "python nbtrain.py textcat/train model_file.txt"
	To classify the test data run the command "python nbtest.py model_file.txt textcat/test predictions_file.txt"
	"predictions_file.txt" file contains the prediction data, document name with class and weighted probabilities of all classes for the document

Dev Data Classification:
	Directory: textcat/dev/pos
		Percentage of docs correctly classified = 73%
	Directory: textcat/dev/neg
		Percentage of docs correctly classified = 85%
	Classifier overall correctness = 79%

Sample Run:
kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17/assignment5 $ python nbtrain.py textcat/train model_file.txt

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17/assignment5 $ python nbtest.py model_file.txt textcat/dev/pos predictions_file.txt
Document Classification:
Test Directory: textcat/dev/pos
Class   Document
neg     27
pos     73

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17/assignment5 $ python nbtest.py model_file.txt textcat/dev/neg predictions_file.txt
Document Classification:
Test Directory: textcat/dev/neg
Class   Document
neg     85
pos     15

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17/assignment5 $ python nbtest.py model_file.txt textcat/test predictions_file.txt
Document Classification:
Test Directory: textcat/test
Class   Document
neg     114
pos     86