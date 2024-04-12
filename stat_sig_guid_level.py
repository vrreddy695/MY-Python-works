from scipy.stats import norm
import numpy as np
import pandas as pd
import math


trtmt_id = 232875
cntrl_id = 232876


# data summarized at guid & treatment level
dsn = """p_merch_analytics_t.vr_item_desc_top_Android"""
cols = ['migmb_1d', 'migmb_7d', 'vigmb_1d','vigmb_7d','mi_purchases_1d','mi_purchases_7d','vi_purchases_1d',
'vi_purchases_7d','mi_pl_rev_1d','mi_pl_rev_7d', 'vi_pl_rev_1d','vi_pl_rev_7d','pl_rev_1d','pl_rev_7d']

# compute the standard deviation of whole population given
# Nx: number of guids; Sx: std of buyer GPW; Mx: mean of buyer GPW; Nzero: number of non-buyers
def stdevNzero(Nx, Sx, Mx, Nzero):
    WMx = Nx * Mx / (Nx + Nzero)
    stdevNzero = ((1 / (Nx + Nzero - 1)) * (((Nx - 1) * Sx ** 2) +
                                            (Nx * Mx ** 2) - ((Nx + Nzero) * WMx ** 2))) ** 0.5
    return stdevNzero


p_crit = 0.1
z = norm.ppf(1 - p_crit / 2)


# getting dataset from Hermes

sql = "select * from " +dsn+";"
df = pd.read_sql(sql, conn)
cursor.close()
conn.close()

df.rename(columns={'sample_guid': 'guid'}, inplace=True)


guids_t = df[df['treatment_id']==trtmt_id]['guid'].nunique()
guids_c = df[df['treatment_id']==cntrl_id]['guid'].nunique()
print("Treatment guids count:",guids_t)
print("Control guids count:",guids_c)


# create lists for eatch metric & stat value
metric = []
test = []
control = []
difference = []
p_val = []
lc = []
uc = []


for col in cols:
    metric.append(col)
    df = df[df[col].notnull()]
    cap_v = 0.997
    percentiles = df[col].quantile([0, cap_v]).values
    df[col] = np.clip(df[col], percentiles[0], percentiles[1])
    globals()[col + '_t'] = df[df['treatment_id'] == trtmt_id][col].values
    globals()[col + '_c'] = df[df['treatment_id'] == cntrl_id][col].values
    test.append('{:,.2f}'.format(sum(globals()[col + '_t'])))
    control.append('{:,.2f}'.format(sum(globals()[col + '_c'])))
    lift = (sum(globals()[col + '_t']) / guids_t) / \
        (sum(globals()[col + '_c']) / guids_c) - 1
    difference.append("{:.2%}".format(lift))
    obs_t = df[df['treatment_id'] == trtmt_id].size
    obs_c = df[df['treatment_id'] == cntrl_id].size
    globals()[col + '_sd_t'] = stdevNzero(obs_t, np.std(globals()
                                                        [col + '_t']), np.mean(globals()[col + '_t']), (guids_t - obs_t))
    globals()[col + '_sd_c'] = stdevNzero(obs_c, np.std(globals()
                                                        [col + '_c']), np.mean(globals()[col + '_c']), (guids_c - obs_c))
    se = ((globals()[col + '_sd_c'] ** 2 / guids_c) +
          (globals()[col + '_sd_t'] ** 2 / guids_t)) ** 0.5
    if math.isnan(se):
        se=0
    p_value = 2.0000 * \
        (1.000 - norm.cdf(abs(((sum(globals()
                                    [col + '_t']) / guids_t) - (sum(globals()[col + '_c']) / guids_c)) / se)))
    p_val.append(p_value)
    ci = se * z / (sum(globals()[col + '_c']) / guids_c)
    lc.append("{:.2%}".format(lift - ci))
    uc.append("{:.2%}".format(lift + ci))


out_df = pd.DataFrame({'metric': metric, 'test': test, 'control': control,
                       'lift': difference, 'p-val': p_val, 'LC': lc, 'UC': uc})

out_df