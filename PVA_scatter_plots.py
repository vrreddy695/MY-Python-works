import pandas as pd
import qgrid as v
v.set_grid_option('forceFitColumns', False)
v.set_grid_option('defaultColumnWidth', 200)
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)
%matplotlib inline
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

final=pd.read_excel('C:/vrreddy/Desktop/Price Volatility Analysis.xlsx', sheetname='results')
final1=final.groupby(['Category','product Name', 'offers_lastupdated']).size()
final1=final1.reset_index()
final1.columns.values[3]='cnt'
final2=final1[final1['cnt'] == final1.groupby(['product Name'])['cnt'].transform(max)]
final2=final2.drop_duplicates(subset=['Category','product Name'], keep='last')
final_vr= pd.merge(final, final2, on=['product Name', 'offers_lastupdated'],how='inner')
v.show_grid(final_vr)


data=final_vr[final_vr['Category']=='Apparel & Dresses']
data['porduct_name'] = ' '
data['porduct_name'][data['product Name']=="adidas Men's Tiro 15 Training Pant"]='adidas Men Training Pant'
data['porduct_name'][data['product Name']=="Columbia Men's Watertight II Front-Zip Hooded Rain Jacket"]='Columbia Men Hooded Rain Jacket'
data['porduct_name'][data['product Name']=="Columbia Men's Watertight Ii Packable Rain Jacket, Collegiate"]='Columbia Men Rain Jacket, Collegiate'
data['porduct_name'][data['product Name']=="Men's 5.0 Tactical Military Jacket"]='Men Tactical Military Jacket'
data['porduct_name'][data['product Name']=="Wantdo Men's Waterproof Mountain Jacket Fleece Windproof Ski Jacket"]='Men Waterproof Mountain Jacket'
data['porduct_name'][data['product Name']=="Pampers Swaddlers Diapers Size 4, 144 Count"]='Pampers Diapers Size 4, 144 Count'


data=final_vr[final_vr['Category']=='Apparel & Dresses']
sns.stripplot(x="product Name", y="offers_price", data=data, jitter=True)



# R code
library(ggplot2)
library(xlsx)
library(ggrepel)
df=read.xlsx("C:/Users/v-vekop/Desktop/Price Volatility Analysis - new.xlsx", 3 , stringsAsFactors=F)
df=df[df$Category=='Appliances', ]
p1=ggplot(df, aes(Product, Price)) +
  geom_point(color = 'green') +
  geom_label_repel(aes(label = lable), size=2.5) +
  theme_classic(base_size = 10)+
theme(axis.text.x = element_text(angle = 25, hjust = 1))+
ggtitle("Toys & Games")+ theme(plot.title = element_text(hjust = 0.5))
ggsave(p1, file = "C:/Users/v-vekop/Downloads/Toys & Games.png", width = 10, height = 5)