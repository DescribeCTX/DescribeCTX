# DescribeCTX

## Introduction
This is the implementation of DescribeCtx. Our works aims at synthesizing precise descriptions for sensitive behaviors in Android apps. DescribeCtx contains two phases: (1) training phase, and (2) prediction phase.

During the training phase, DescribeCtx first extracts both source-code-level and GUI-level contextual text from apk files of Android apps, additionally, DescribeCtx also extract permission descriptions from apps' privacy policy. These information is formally encoded and passed to a seq2seq-based language model to synthesize sensitive behavior descriptions.

During the prediction phase, given an app's GUI context and sensitive API call graph, DescribeCtx using the most similar permission description from other apps, to synthesize the description for the given sensitive behavior.

![image](https://github.com/DescribeCTX/DescribeCTX/blob/main/overview.jpg)

## Requirements
* Java version: 1.8.0_181
* Python version: 3.7.2
* Tensorflow version: 1.15.0
* Other dependencies: numpy, scikit-learn, networkx, pandas
* APKTool: Check https://ibotpeaches.github.io/Apktool/ for more details and download.

## Usage
Before extracting features from apps, APKTool is required to decompile each .apk file and obtain the apk resources. For more detailed instruction on feature extraction and how to train and predict, please go to https://github.com/DescribeCTX/DescribeCTX/tree/main/Code.
