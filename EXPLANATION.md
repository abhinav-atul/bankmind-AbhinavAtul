# EXPLANATION.md — BankMind Challenge, Track A

**Author:** Abhinav Atul  
**Track:** A — Data Analyst  

## 1. What percentage of customers in your dataset have y = yes? What does this imbalance mean for how you'd evaluate a model?

Approximately **11.7%** of the customers in the dataset subscribed to the term deposit (`y = yes`), making the dataset heavily imbalanced (roughly 88.3% "no"). 
Because of this imbalance, evaluating a future ML model using simple "accuracy" would be misleading—a "dumb" model that always predicts "no" would achieve 88% accuracy without learning anything. Instead, metrics like Precision, Recall, and the F1-score for the positive class are required to see if the model can actually identify the rare positive cases without generating too many false alarms.

## 2. Which job category had the highest subscription rate? Does this make sense to you intuitively?

The **Student** (28.7%) and **Retired** (22.8%) job categories had the highest subscription rates. 
Yes, this makes intuitive sense. Retired individuals generally have accumulated savings, no active income requirements, and are highly receptive to safe, passive-income products like term deposits. Students are often young, financially curious, and starting to build their foundational savings, making them prime targets for basic entry-level banking products. Conversely, middle-aged working professionals (like blue-collar workers) tend to have more immediate financial commitments like mortgages and living expenses, resulting in lower liquid savings for term deposits.
