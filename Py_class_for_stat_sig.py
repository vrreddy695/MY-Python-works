import pandas as pd
import numpy as np
from scipy.stats import t


class ABTest:
    def __init__(self, df, control_column, treatment_column, confidence_level=0.95):
        self.df = df
        self.control_column = control_column
        self.treatment_column = treatment_column
        self.confidence_level = confidence_level

    def calculate_p_value(self):
        control_data = self.df[self.control_column]
        treatment_data = self.df[self.treatment_column]

        control_mean = np.mean(control_data)
        treatment_mean = np.mean(treatment_data)
        control_std = np.std(control_data, ddof=1)
        treatment_std = np.std(treatment_data, ddof=1)
        n_control = len(control_data)
        n_treatment = len(treatment_data)

        pooled_std = np.sqrt((control_std ** 2 / n_control) + (treatment_std ** 2 / n_treatment))
        t_statistic = (control_mean - treatment_mean) / pooled_std

        degrees_of_freedom = n_control + n_treatment - 2
        p_value = 2 * (1 - t.cdf(np.abs(t_statistic), df=degrees_of_freedom))

        return p_value

    def calculate_confidence_interval(self):
        control_data = self.df[self.control_column]
        treatment_data = self.df[self.treatment_column]

        control_mean = np.mean(control_data)
        treatment_mean = np.mean(treatment_data)
        control_std = np.std(control_data, ddof=1)
        treatment_std = np.std(treatment_data, ddof=1)
        n_control = len(control_data)
        n_treatment = len(treatment_data)

        pooled_std = np.sqrt((control_std ** 2 / n_control) + (treatment_std ** 2 / n_treatment))
        margin_of_error = t.ppf((1 + self.confidence_level) / 2, df=n_control + n_treatment - 2) * pooled_std * np.sqrt(
            1 / n_control + 1 / n_treatment)

        lower_bound = (control_mean - treatment_mean) - margin_of_error
        upper_bound = (control_mean - treatment_mean) + margin_of_error

        return lower_bound, upper_bound

    def calculate_lift(self):
        control_data = self.df[self.control_column]
        treatment_data = self.df[self.treatment_column]

        control_mean = np.mean(control_data)
        treatment_mean = np.mean(treatment_data)

        lift = ((treatment_mean - control_mean) / control_mean) * 100

        return lift


# Example usage
data = {
    'UserID': [1, 2, 3, 4, 5],
    'Control': [10, 12, 15, 17, 20],
    'Treatment': [13, 14, 16, 18, 22]
}

df = pd.DataFrame(data)

ab_test = ABTest(df, 'Control', 'Treatment')

p_value = ab_test.calculate_p_value()
lower_ci, upper_ci = ab_test.calculate_confidence_interval()
lift = ab_test.calculate_lift()

print("P-value:", p_value)
print("Confidence Interval:", (lower_ci, upper_ci))
print("Lift:", lift)
