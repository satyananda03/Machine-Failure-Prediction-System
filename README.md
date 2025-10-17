# Machine Failure Prediction Systems
Predict machine failure based on machine process parameters 

## Technology Used

![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=matplotlib&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-4C9A2A?style=for-the-badge&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## Features 
- Predict machine failure based on process parameter - Air temperature (K), Process temperature (K), Rotational speed (rpm), Torque (Nm) : Torsi mesin, Tool wear (min)
- Classify failure type into : TWF (Tool ware failure), HDF (Heat dissipation failure), PWF (Power failure), OSF (Overstrain failure), RNF(Random failure)
- Realtime dahsboard to analyze data & prediction history

## Dataset
Open Source Machine Predictive Maintenance Dataset (10k rows) : https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset

## Model & Result
- Random Forest for Failure Prediction
<p align="center">
  <img src="./img/randomforest.jpg" alt="Logo" width="400"/>
</p>

- SVM for Failure Type Multiclass Clasification
<p align="center">
  <img src="./img/svm.jpg" alt="Logo" width="400"/>
</p>