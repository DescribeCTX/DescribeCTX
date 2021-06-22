# Introduction
This user study is to evaluate the performance of DescribeCTX against the baseline approach in terms of semantic closeness, syntactical correctness, and length appropriateness, on the synthesized descriptions. The goal of our user study is to measure whether users can understand the sensitive behavior description synthesized by DescribeCTX, and how well the synthesized descriptions are according to the above metrics.  
In addition, we design another user study to compare the performance of DescribeCTX to the baseline approach, which does not include app context such as GUI contextual text and PACG. We use the same metrics to evaluate both approaches.  
We recruited 8 graduate students and 4 undergraduate students with mobile app development experiences for the study. Formally, each student is required to read the consent form, and provide necessary information such as the number of years of mobile app development experience. Next, we sent the survey form to each participated student. Each survey form contains 4668 result records (DescribeCTX + 2 Baseline approaches, 1556 records for each). To mitigate the bias, each student was given half of the records from both approaches randomly, and the apporaches are invisible to the students. In other words, survey participants do not know the descriptions are synthesized by which method. Therefore, there are 6 `.csv` files of rated descriptions. The ratings for each aspect (***Semantic/Syntax/Length***) ranges from **1** to **5**: Very Bad (1), Bad (2), So-so (3), Good (4), and Very Good (5). 
# Columns
  ***Permission***: Which permission does the reference sentence describe.  
  ***Original Description***: Reference sentences labeled by manual.  
  ***Synthesized Descritpion 1***: Synthesized description by DescribeCTX-CTX (baseline approach 1).  
  ***Semantic/Syntax/Length***: Ratings of semantic closeness/syntactical correctness/length appropriateness (**Baseline Approach 1**).  
  ***Synthesized Description 2***: Synthesized description by DescribeCTX.  
  ***Semantic/Syntax/Length***: Ratings of semantic closeness/syntactical correctness/length appropriateness (**DescribeCTX**).  
  ***Synthesized Description 3***: Synthesized description by Code2Vec+PP.  
  ***Semantic/Syntax/Length***: Ratings of semantic closeness/syntactical correctness/length appropriateness (**Baseline Approach 2**).
# How to Interpret
Files `merge_rating_1.csv` to `merge_rating_6.csv` contains our user study for both DescribeCTX and baseline approachs. Column 1 represents the reference sentences we manually extracted from apps' descriptions. Columns from 3 to 6 represents the synthesized description of DescribeCTX-CTX (baseline approach 1), semantic ratings, syntactic ratings, and length ratings. Columns from 7 to 10 represents the synthesized descriptions of DescribeCTX, and corresponding ratings. Columns from 11 to 15 represents the synthesized descriptions using Code2Vec and permission descriptions (baseline approache 2)
## Example:
Reference Sentence: ***QR code reader is designed with the permission of the camera to scan QR code.***  
Synthesized Description by DescribeCTX: ***open camera of your camera you can use scan qr code or barcode***  
Ratings: semantic closeness (***5***), syntactical correctness (***4***), and length appropriateness (***5***).  
Synthesized Description by Baseline Approach 1 (DescribeCTX-CTX): ***the app can use camera permission***  
Ratings: semantic closeness (***3***), syntactical correctness (***5***), and length appropriateness (***3***).  
Synthesized Description by Baseline Approach 2 (Code2Vec+PP): ***the app can use camera permission***  
Ratings: semantic closeness (***3***), syntactical correctness (***5***), and length appropriateness (***4***).

# User Study via MTurk
We resort to Amazon Mechanical Turk (MTurk) for an open survey. We divide 1,556 data samples into 50 splits (each containing 31 or 32 samples), and send out 300 splits (i.e., 6 for each split). Each sample consists of a reference sentence as the question and three synthesized sentences from the three approaches as the answers. Users are asked to pick one or more answers that most resemble the question in terms of semantic closeness. The order of the three answers is randomly shuffled. Each sample is displayed for at least 10 seconds before it can be moved to the next sample. For each data split, we also intentionally plug in an additional data sample with one obvious answer and two irrelevant answers. If the user chose the irrelevant answers, we consider all his/her ratings invalid and remove them all. There are 275 unique users participating in our study, and 174 out of them are considered valid. Example survey quesiton can be found in `example.html`.
## Result
A full, detailed result is presented in `User_Study_2.csv`. In particular, we calculate the pick ratio of each anwser. On average, descriptions synthesized by DescribeCTX have higher pick ratio than the baseline approach, indicates that DescribeCTX can synthesize more accurate, app-specific descriptions for the test apps. 

***Correction: The numbers of pick ratio and increasement in the submitted paper are falsely calculated. The correct numbers are listed here. The pick ratio of DescribeCTX is 57.06%, the pick ratio of baseline approach is 47.56%, the increasement is 19.97%. We will correct the numbers accordingly in the paper.***
