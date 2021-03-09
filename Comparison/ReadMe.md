## Compared to Related Work
Zhang et al.[1] also aimed to extract textual features from Android APKs, and to generate descriptions for sensitive behaviors. Similarly, they extract call graphs based on sensitive API calls, GUI text from layout files. The main difference between their work and DescribeCTX is that they applied a ***template-based*** language model, which directly combined the pre-defined template with the text features. However, DescribeCTX extract more feature (i.e. permission descriptions) from apps' privacy policies to provide vocabularies to the model. Besides, DescribeCTX is a ***learning-based*** model which applies seq-to-seq model with two attention mechanisms to generate descriptions for the sensitive behaviors. 

Since Zhang did not open source any of their work, we can only find some examples and templates from their paper, as shown below. Compared to our results, it is clear that their results is generic and not app-specific at all. It is obvious that template-based approach is not able to handle unseen apps, and it completely depends on the quality of templates, not to mention their approach is not able to scale to a large number of apps.

![image](https://github.com/DescribeCTX/DescribeCTX/blob/main/Comparison/DescribeMe_Descriptions.png)

[1] Mu Zhang, Yue Duan, Qian Feng, and Heng Yin. 2015. Towards Automatic Generation of Security-Centric Descriptions for Android Apps. In Proceedings of the ACM SIGSAC Conference on Computer and Communications Security (CCS). 518–529.
