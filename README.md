# Covid-19-detection-from-X-ray-images-using-deep-learning

COVID-2019, which first appeared in Wuhan city of China in December 2019, spread rapidly around the world and became a pandemic. Its very common for doctors to frequently use X-rays and CT scans to diagnose pneumonia, lung inflammation, abscesses, and/or enlarged lymph nodes. Since COVID-19 attacks the epithelial cells that line our respiratory tract, X-rays can be used to analyze the health of a patient’s lungs. It could be possible to use X-rays to test for COVID-19 without the dedicated test kits.
In this repository, a new model for detecting COVID-19 using raw chest X-ray images is presented. The model developed presents accurate diagnostics for binary classification and morever achieved a good accuracy and very less loss rate.

# Present testing methods for Covid-19 

The most common test technique currently used for COVID-19 diagnosis is a real-time reverse transcription-polymerase chain reaction (RT-PCR). Chest radiological imaging such as computed tomography (CT) and X-ray have vital roles in early diagnosis and treatment of this disease. Due to the low RT-PCR sensitivity of 60%–70%, even if negative results are obtained, symptoms can be detected by examining radiological images of patients. It is stated that CT is a sensitive method to detect COVID-19 pneumonia, and can be considered as a screening tool with RT-PRC. CT findings are observed over a long interval after the onset of symptoms, and patients usually have a normal CT in the first 0–2 days. In a study on lung CT of patients who survived COVID-19 pneumonia, the most significant lung disease is observed ten days after the onset of symptoms.  
Reference to this information can be found at - https://www.sciencedirect.com/science/article/pii/S0010482520301621?via%3Dihub

# X-ray Image dataset used for classifier

The image dataset used for creating this classifier can be collected at - https://github.com/BIMCV-CSUSP/BIMCV-COVID-19  
Number of positive covid images are - 100  
Number of negative covid images are - 100  

A sample image from the dataset for covid-19 positve is shown below :   
![1 CXRCTThoraximagesofCOVID-19fromSingapore pdf-000-fig1a](https://user-images.githubusercontent.com/39157936/89102153-02da6600-d424-11ea-8ce1-c0c0e6fc9162.png)

A sample image from the dataset for covid-19 negative is shown below :   
![IM-0115-0001](https://user-images.githubusercontent.com/39157936/89102231-9f046d00-d424-11ea-805c-a052adba3f4e.jpeg)

# Project structure

├── yolo_app  
│   ├── admin.py  
│   ├── apps.py  
│   ├── Data  
│   │   ├── __init__.py  
│   │   ├── Model_Weights  
│   │   │   └── data_classes.txt  
│   │   └── Source_Images  
│   │       ├── Test_Image_Detection_Results  
│   │       │   ├── CCryct.2020200034.fig5-day7.jpeg  
│   │       │   ├── Detection_Results.csv  
│   │       │   ├── IM-0251-0001.jpeg  
│   │       │   ├── IM-0253-0001.jpeg  
│   │       │   ├── IM-0261-0001.jpeg  
│   │       └── Test_Images  
│   ├── Inference  
│   │   ├── Detector.py  
│   ├── __init__.py  
│   ├── migrations  
│   │   ├── 0001_initial.py  
│   │   ├── __init__.py  
│   ├── models.py  
│   ├── requirements.txt  
│   ├── tests.py  
│   ├── urls.py  
│   └── views.py    

# How Model is created     
**Step 1:** Positive Samples has been taken from [BIMCV-COVID-19](https://github.com/BIMCV-CSUSP/BIMCV-COVID-19) repository, Whereas negative samples has bee taken from [kaggle](https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia). So one got two folder one for positive and another for negative. I have used Visual Object Tagging Tool (VoTT) of microsoft to perform tagging. Have a look at the next mentioned link [How to install and use VoTT](https://github.com/microsoft/VoTT). Once you are finished with step, you can export csv file from the VoTT software which is needed for the next step. See the link below for viewing the status when annotation has been completed by me using VoTT.   

![imgpsh_fullsize_anim](https://user-images.githubusercontent.com/39157936/89147877-b010c380-d575-11ea-8e4e-d9660c6c92e0.png)   

**Step 2:** Convert the annotation to the yolo format. To achieve this step use [convert to yolo format](https://github.com/AntonMu/TrainYourOwnYOLO/tree/master/1_Image_Annotation/Convert_to_YOLO_format.py)  

**Step 3:** Download the pre-trained dark-net weights and convert them to YOLO format.TO achieve this step, please use the below code [Download and convert to yolo](https://github.com/AntonMu/TrainYourOwnYOLO/blob/master/2_Training/Download_and_Convert_YOLO_weights.py)  

**Step 4:** It is the time for the training of the detector. We got the images as well as its annotation from the step 2. We got the weights from the step 3 in yolo format. Now please execute the below code to get trained the model with the customized images. [Train the yolo model with the customized images](https://github.com/AntonMu/TrainYourOwnYOLO/blob/master/2_Training/Train_YOLO.py)  

**Step 5:** Once the training is finished you will get the new weights in  form of h5 file. For this model I have made the file which one can find in the below link   

[Trained keras H5 file for the customized Dataset](https://drive.google.com/file/d/1K7Dhi5wnsSDul5A6RF0Ec0FpGMW3Y9DZ/view)  

Please keep these weights inside the Folder **Data>>Model_Weights**









