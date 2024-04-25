import pandas as pd
import numpy as np
from scipy.stats import norm
import math

class ABTest:
    def __init__(self, df, variant, metric):
        self.df=df
        self.variant=variant
        self.metric=metric
        for i in df[variant].unique().tolist():
            setattr(self, i.lower(), i.lower())
    
    # compute the standard deviation of whole population given
    # Nx: number of guids; Sx: std of buyer GPW; Mx: mean of buyer GPW; Nzero: number of non-buyers
    def stdevNzero(self, Nx, Sx, Mx, Nzero):
        WMx = Nx * Mx / (Nx + Nzero)
        stdevNzero = ((1 / (Nx + Nzero - 1)) * (((Nx - 1) * Sx ** 2) +
                                            (Nx * Mx ** 2) - ((Nx + Nzero) * WMx ** 2))) ** 0.5
        return stdevNzero

    def calculate_p_value(self):
        result={}
        p_crit = 0.1
        z = norm.ppf(1 - p_crit / 2)

        guids_t = self.df[self.df[self.variant]==self.test]['guid'].nunique()
        guids_c = self.df[self.df[self.variant]==self.control]['guid'].nunique()

        # capping at 99.7 pecentile

        self.df = self.df[self.df[self.metric].notnull()]
        cap_v = 0.997
        percentiles = self.df[self.metric].quantile([0, cap_v]).values
        self.df[self.metric] = np.clip(self.df[self.metric], percentiles[0], percentiles[1])


        control_data = self.df[self.df[self.variant]==self.control][self.metric].values
        treatment_data = self.df[self.df[self.variant]==self.test][self.metric].values

        control_mean = sum(control_data)/guids_c
        treatment_mean = sum(treatment_data)/guids_t

        obs_t = self.df[self.df[self.variant]==self.test]['guid'].nunique()
        obs_c = self.df[self.df[self.variant]==self.control]['guid'].nunique()



        control_std = self.stdevNzero(obs_c, np.std(control_data), np.mean(control_data), (guids_c - obs_c))
        treatment_std = self.stdevNzero(obs_c, np.std(treatment_data), np.mean(treatment_data), (guids_t - obs_t))


        result['test_mean']=treatment_mean
        result['control_mean']=control_mean

        result['test_std']=treatment_std
        result['control_std']=control_std
        result['n_treatment']=guids_t
        result['n_control']=guids_c

        #lift calculation
        lift= (treatment_mean/control_mean)-1
        result['lift'] ="{:.2%}".format(lift)
    

        # Calculate standard errors
        se = ((control_std ** 2 / guids_c) +(treatment_std ** 2 / guids_t)) ** 0.5
        if math.isnan(se):
            se=0

        #confidence interval calculation
        ci = se * z / control_mean
        result['ci_lift'] = ("{:.2%}".format(lift - ci), "{:.2%}".format(lift + ci))

        

        #P-Value calculation
        result['p_value'] = 2.0000 * (1.000 - norm.cdf(abs((treatment_mean - control_mean) / se)))
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
    'guid': user_ids,
    'variant': variants,
    'visits': visits
})

df.head()


#calling the method

result=ABTest(df, 'variant', 'visits').calculate_p_value()

pd.DataFrame(result)

