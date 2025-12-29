# Local Travel Recommendation Engine in India

This project implements a **Python-based travel recommendation system**
that suggests the **best nearby weekend destinations** in India based on a
given **source city**.

The system ranks destinations using **geographical distance, tourist rating,
and popularity**, and was built as part of a practical assignment focused on
data processing and recommendation logic using Pandas.

---

## Approach

- The dataset is cleaned to remove missing or invalid location and rating data.
- Real-world distances between cities are calculated using the **Haversine
  formula** based on latitude and longitude.
- Each destination is scored using a weighted combination of:
  - Distance (closer destinations preferred)
  - Tourist rating
  - Popularity (if available in the dataset)
- Destinations are ranked by a final composite score and the top results are
  returned as weekend recommendations.

The logic is intentionally kept simple and explainable, avoiding unnecessary
complexity while maintaining practical accuracy.


## Results

The recommendation engine produces meaningful and realistic suggestions for
short trips.

Example:

> **Input:** Mumbai  
> **Output:** Lonavala, Alibaug, Mahabaleshwar (ranked by proximity and rating)

Sample outputs are included in the notebook for:
- Mumbai
- Delhi
- Bengaluru

---

## How to Run

```bash
pip install -r requirements.txt
jupyter notebook travel_recommendation.ipynb
