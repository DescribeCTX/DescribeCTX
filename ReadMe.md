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

## Related Work
Zhang et al.[1] also aimed to extract textual features from Android APKs, and to generate descriptions for sensitive behaviors. Similarly, they extract call graphs based on sensitive API calls, GUI text from layout files. The main difference between their work and DescribeCTX is that they applied a ***template-based*** language model, which directly combined the pre-defined template with the text features. However, DescribeCTX extract more feature (i.e. permission descriptions) from apps' privacy policies to provide vocabularies to the model. Besides, DescribeCTX is a ***learning-based*** model which applies seq-to-seq model with two attention mechanisms to generate descriptions for the sensitive behaviors. 

Since Zhang did not open source any of their work, we can only find some examples and templates from their paper, as shown below. Compared to our results, it is clear that their results is generic and not app-specific at all. It is obvious that template-based approach is not able to handle unseen apps, and it completely depends on the quality of templates, not to mention their approach is not able to scale to a large number of apps. The fact is that they only evaluate on 100 Android apps which is significantly biased.

![image](https://github.com/DescribeCTX/DescribeCTX/blob/main/DescribeMe_Description.png)
