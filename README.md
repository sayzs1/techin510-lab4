# TECHIN 510 Lab 4 

## Regular expression, datetime, and real-time data

### Overview

- datetime.ipynb: This notebook contains the code for the datetime exercise.
- regex.ipynb: This notebook contains the code for the regex exercise.
- app.py: a world clock that displays time in different locations around the world，including the Unix number convert time page and real-time stock information fetch page

## how to run
first, use command to install the package list in reqirement

```bash
pip install -r requirements.txt
```

To run the streamliit app use the following command:

```bash
streamlit run app.py
```

### Lessions Learned
- How to fetch more real-time data into app?
  - We can use the appropriate Python library or API to fetch the data, for example, the `yfinance` library is used here to get the stock information.
- What if I want to add more features or pages to the app?
  - We can extend the pages dictionary in the code and add more functions to handle additional features or pages. Update the navigation accordingly.

### Future improvement
We can make the app more interactive by adding widgets like buttons, sliders, and input fields. We can organize elements using columns, add headers, and use different widgets to enhance the layout.