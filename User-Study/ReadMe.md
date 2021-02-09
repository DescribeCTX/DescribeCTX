# Introduction
This user study is to evaluate the performance of DescribeCTX against the baseline approach in terms of semantic closeness, syntactical correctness, and length appropriateness, on the synthesized descriptions. The goal of our user study is to measure whether general users can understand the sensitive behavior description synthesized by DescribeCTX, and how well the synthesized descriptions are based on above metrics.  
We recruited 8 graduate students and 4 undergraduate students with mobile app experiences for the study. The total number of records is 3112 (DescribeCTX + Baseline, 1556 for each), each student was given half of the records from both approach randomly. Therefore, there are 6 .csv rating files. The ratings for each aspect (***Semantic/Syntax/Length***) range from **1** to **5**: Very Bad (1), Bad (2), So-so (3), Good (4), and Very Good (5). 
# Columns
  ***Permission***: Which permission does the reference sentence describe.  
  ***Original Description***: Reference sentences labeled by manual.  
  ***Synthesized Descritpion 1***: Synthesized description by DescribeCTX.  
  ***Semantic/Syntax/Length***: Ratings of semantic closeness/syntactical correctness/length appropriateness (**DescribeCTX**).  
  ***Synthesized Description 2***: Synthesized description by baseline approach.  
  ***Semantic/Syntax/Length***: Ratings of semantic closeness/syntactical correctness/length appropriateness (**Baseline approach**).  
# How to Interpret
Files `rating_1.csv` to `rating_6.csv` contains our user study for both DescribeCTX and baseline approach. Column 1 represents the reference sentences we manually extracted from apps' descriptions. Columns from 3 to 6 represents the synthesized description of DescribeCTX, semantic ratings, syntactic ratings, and length ratings. Columns from 7 to 10 represents the synthesized descriptions of baseline approach, and corresponding ratings.
## Example:
Reference Sentence: ***QR code reader is designed with the permission of the camera to scan QR code.***  
Synthesized Description by DescribeCTX: ***open camera of your camera you can use scan qr code or barcode***  
Ratings: semantic closeness (***5***), syntactical correctness (***4***), and length appropriateness (***5***).  
Synthesized Description by Baseline Approach: ***the app can use camera permission***  
Ratings: semantic closeness (***3***), syntactical correctness (***5***), and length appropriateness (***3***).  
