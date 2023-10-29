# Information Extraction from Nineteenth-Century knowledge Project

This repository explores methods to extract information from the [Knowledge Project ](https://tu-plogan.github.io/source/r_releases.html).

Note that, the methods we developed so far only utilised the txt files. For example, in eb07/TXT_V2/v21/ folder, there are many xml files, we won't process them, but just txt files in that folder.

---

## Term name and description extraction

Take a line of text from [a txt file](https://github.com/TU-plogan/kp-editions/blob/main/eb07/TXT_v2/a2/kp-eb0702-000501-9874-v2.txt) for example : 

``
Aba, Abas, Abos, or Abus, in Ancient Geography, the name of a mountain in Greater Armenia, situated between the mountains Niphatos and Nibonis. According to Strabo, the Euphrates and Araxes rose from this mountain; the former running eastward, and the latter westward. It is in N. lat. 39½. and connects at its eastern extremity with Mount Ararat Aba. See Abae. Aba, Albon, or Ovon, a king of Hungary. He married the sister of Stephen I. and was elected king on the deposition of Peter in 1041. The emperor Henry III. preparing to reinstate Peter on the throne, Aba made an incursion into his dominions, and returned loaded with booty; but was next year obliged to make restitution, by paying a large sum, in order to prevent a threatened invasion from the emperor. He indulged in great familiarity with the lower class of the people; on account of which, and his severity to their order, he became universally odious to the nobility. The fugitive nobles, aided by the emperor, excited a revolt against him. After a bloody battle, Aba was put to flight; and was murdered by his own soldiers in 1044, having reigned three years.``

Create_DataFrame_7ed_EB.ipynb can extract the following information:
1. **primary term name** (ABA, although there is another called "Aba, Albon, or Ovon", since it is inside this line, we will not consider it until they provide better version of this txt file.)
2. **alternative term names** ([ABA, ABAS, ABOS, ABUS])
3. **note of a term** (None, this example does not have note, if it does, it should look like "Aba (this is a note), Abas, ....")
4. **term description** (in Ancient Geography, the name of a mountain in Greater Armenia, ....)
5. **reference terms** (Abae, term name after word "see")
6. **the page number of a term starts** 
7. **the page number of a term ends** 
8. the **position** of a term in a page term type 
9. **file path** where this information was extracted 
10. the **number of words** in a term description 
11. **volume number**

and some other hard coded information, such volume id, editor, etc.

This notebook can extract term name in **various patterns**, here are some examples for these patterns:

1. ANAXIMENES, an eminent Greek philosopher ... 
2. AAM, or Haλm, a liquid measure in common ... 
3. AHOLIB ΛH and Aπolah are two feigned names made use 
4. ABA (or rather ABAU) HANIFA or HANFA, surnamed Al-Nooma, was the son of ..... 
5. ABACK (a sea term), the situation of the sails when the surfaces ..... 
6. ABA, Abas, Abos, or Abus, in Ancient Geography, the name ..... 
7. A. The first letter of the alphabet in every kn 
8. ABBOTS-BROMLEY, a town in Staffordshire. .... 
9. AGARIC Mineral, a marly earth, resembling the vegetable of that name in 
10. ACCISMUS denotes a feigned refusal of something which 
11. ARC, Joan of, generally called the Maid of Orleans 
12. ARMSTRONG, John, M.D. an eminent physician, poet, and miscellaneous writer 
13. ACCOUNTANT-general, a new officer in the court of chancery, 
14. See Bangog, a small island in the Eastern Seas, near ... 
15. ADANSONIA, Ethiopian Sour-gourd, Monkeys-bread, or African Calabash-tree. 
16. AiD-de-Camp, in military affairs, an officer employed

We evaluated this extraction method by comparing it with [Alex's Work](https://github.com/alexyoung13/frances_dissertation_ay55)

The result shows that:
* Overall, our method can extract **more information**, such as alternative names, reference terms, note
* Information extracted using our method is **more accurate**, such as term name (supporting more patterns), term description, the page number where a term starts or ends, position, term type
* we had **less text files to process** (due to incomplete work of version 2) than Alex's work, while we **extracted 850 more terms**. However, it does not imply our method generally extracts more terms, since version 2 separates more terms for us. More experiments are required to confirm this.
* Classifying term type only by the number of words (Alex's work) is rather inaccurate, we spot that almost half of _Topic_ extracted using Alex's method are actually _Article_, and the number of _Topic_ extracted using our method is nearly half of his.
* There are some terms cannot be extracted or wrongly extracted because of the quality of the txt file itself. 
