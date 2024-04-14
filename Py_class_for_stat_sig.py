import pandas as pd
import numpy as np
import scipy.stats as stats

class ABTest:
    def __init__(self, df, variant, metric, confidence_level=0.95):
        self.df=df
        self.variant=variant
        self.metric=metric
        self.confidence_level=confidence_level
        for i in df[variant].unique().tolist():
            setattr(self, i.lower(), i.lower())

    def calculate_p_value(self):
        result={}
        control_data = self.df[self.df[self.variant]==self.control][self.metric]
        treatment_data = self.df[self.df[self.variant]==self.test][self.metric]

        control_mean = np.mean(control_data)
        treatment_mean = np.mean(treatment_data)
        control_std = np.std(control_data, ddof=1)
        treatment_std = np.std(treatment_data, ddof=1)
        n_control = len(control_data)
        n_treatment = len(treatment_data)

        result['test_mean']=treatment_mean
        result['control_mean']=control_mean

        result['test_std']=treatment_std
        result['control_std']=control_std
        result['n_treatment']=n_treatment
        result['n_control']=n_control

        #lift calculation
        result['lift'] = "{:.2%}".format((treatment_mean/control_mean)-1)

        #confidence interval calculation

        # Calculate standard errors
        se_treatment = treatment_std / np.sqrt(n_treatment)
        se_control = control_std / np.sqrt(n_control)

        # Calculate standard error of the lift
        se_lift = np.sqrt(se_treatment**2 + se_control**2)

        # Calculate z-score for the desired confidence level
        z_score = stats.norm.ppf((1 + self.confidence_level) / 2)
        # Calculate confidence interval for the lift
        lift = treatment_mean - control_mean
        result['ci_lift'] = ('{:.2%}'.format(lift - z_score * se_lift), '{:.2%}'.format(lift + z_score * se_lift))

        #P-Value calculation
        # Calculate pooled standard deviation
        pooled_std = np.sqrt(((n_treatment - 1) * treatment_std ** 2 + (n_control - 1) * control_std ** 2) / (n_treatment + n_control - 2))

        # Calculate t-statistic
        t_statistic = (treatment_mean - control_mean) / (pooled_std * np.sqrt(1/n_treatment + 1/n_control))

        # Calculate degrees of freedom
        degrees_of_freedom = n_treatment + n_control - 2

        # Calculate p-value
        p_value = 2 * (1 - stats.t.cdf(abs(t_statistic), df=degrees_of_freedom))
        return result








#usage 
import pandas as pd
import numpy as np

# Create user_id
user_ids = ['user_' + str(i) for i in range(1, 201)]

# Generate random values for variant (test or control)
variants = np.random.choice(['test', 'control'], size=200)

# Generate random values for visits
visits = np.random.randint(1, 10, size=200)

# Create DataFrame
df = pd.DataFrame({
    'user_id': user_ids,
    'variant': variants,
    'visits': visits
})

df.head()


#calling the method
my_ob=ABTest(df, 'variant', 'visits')
print(my_ob.control)
print(my_ob.test)

print(my_ob.calculate_p_value())