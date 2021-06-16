## Compared to Related Work
Zhang et al.[1] propose DescribeMe, that extracts textual features from Android APKs, and uses templates to generate descriptions for the sequence of statements that lead to the invocation of a permission-protected API call. The main difference between their work and DescribeCTX is that they applied a ***template-based*** approach, which directly combined the pre-defined template with the text features. However, DescribeCTX extract more feature (i.e. permission descriptions) from apps' privacy policies to provide vocabularies to the model. Besides, DescribeCTX is a ***learning-based*** model which applies seq-to-seq model with two attention mechanisms to generate descriptions for the sensitive behaviors. 

Due to the limitation of the fixed set of templates, the generated descriptions have fixed formats and have very limited capabilities to describe various types of app behaviors. 
Also, it lacks the vocabularies for describing sensitive behaviors, and focuses on explaining the statements (such as sending data to network) rather than their purposes.
DescribeCTX addresses the limitations of DescribeMe by learning a seq2seq model that leverages GUI, code, and privacy policies to generate descriptions for sensitive behaviors. The generated descriptions are not limited to a fixed set of formats, and the vocabularies from the text in the GUIs and privacy policies help explain the purposes of the sensitive behaviors.

Since Zhang et al. do not open source any of their work, we can only find some examples and templates from their paper, as shown below. We compare only three permission groups (i.e., SMS, STORAGE, and CONTACT) since we can only find these three templates from their paper1. We can see that DESCRIBECTX significantly outperforms DESCRIBEME on both BLEU and ROUGE-L scores in these three permission groups, especially the SMS group (BLEU scores: 24.55 versus 4.88). Compared to our results, it is clear that their results are too generic and not app-specific. Further, these descriptions do not reflect the purposes of using sensitive permissions, and do not provide specific information regarding sensitive behaviors of the apps to the end users.

![image](https://github.com/DescribeCTX/DescribeCTX/blob/main/Comparison/DescribeMe_Descriptions.png)

## Result
We have presented our comparison results (DescribeCTX, DescribeCTX-CTX, and Code2Vec+PP). Detailed results can be found in the corresponding files. The first column represents the permission group, the second column represents the original descriptions written by the developers (reference sentences we used to evaluate our tool), the third column represents the synthesized descriptions from DescribeCTX/DescribeCTX-CTX/Code2Vec+PP.

[1] Mu Zhang, Yue Duan, Qian Feng, and Heng Yin. 2015. Towards Automatic Generation of Security-Centric Descriptions for Android Apps. In Proceedings of the ACM SIGSAC Conference on Computer and Communications Security (CCS). 518–529.
