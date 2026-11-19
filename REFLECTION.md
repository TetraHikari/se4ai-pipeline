# Reflection

Name:

Answer each question in 2–3 sentences.

**1. Which antipatterns from the lecture did `train_all.py` show? Point to the lines.**

> The whole thing is one monolithic script with the input file (line 15), the date format (line 19) and the tree depth (line 35) hard-coded, so adding a second CSV or trying another depth meant editing the code. Lines 28-30 are a dead experimental code path (`USE_LOG_PRICE`) that nobody remembered the result of. And line 44 saves the model no matter what the MAE on line 39 says, with no tests anywhere, so a bad model would ship as quietly as a good one.

**2. Suppose there were no test and no evaluation gate. What would have happened when the 2026 batch arrived? Think about both the crash and the missing `sqft` values.**

> The date crash is actually the good case: it fails loudly on line 19, and someone would notice. The scary part is what happens after a quick fix like `format="mixed"`. The tree trains on the 12 rows with no `sqft` without complaining, and when I tried it the MAE was $35,233, still under the $50,000 gate, so even the gate would not have caught it. Only `test_no_missing_sqft_after_cleaning` stops it, which is why the test matters more than I expected.

**3. In the real marketplace, which non-ML parts of the system should trigger this pipeline or feed it data?**

> The sales system that produces the exports is the main data source. A new export landing (or a schedule, say weekly) should trigger a run instead of someone remembering once a year. Listing data from agents and sellers feeds in too, and that is where missing `sqft` comes from, so the listing form should probably make it a required field. On the other end, the website that shows the fair-value estimate should only pick up a model that passed the gate.
