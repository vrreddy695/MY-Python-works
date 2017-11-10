import pandas as pd
import xlsxwriter
writer = pd.ExcelWriter('C:/vrreddy/Top100K_queries_Jun_Aug_Srpvs.xlsx', engine='xlsxwriter')
sheets=['Autos','ClothesAndShoes','Commerce','ConsumerElectronics','Education','Flight','Health',
'Hotels','IsJobs','IsList','Local']

for sheet in sheets:
    df1=pd.read_excel('C:/Users/v-vekop/Desktop/json/Top100K_Queries_June16.xlsx', sheetname=sheet)
    df1=df1[['Query', 'SRPVs']]
    df1.rename(columns={'SRPVs': 'Jun16_SRPVs'}, inplace=True)

    df2=pd.read_excel('C:/Users/v-vekop/Desktop/json/Top100K_Queries_July16.xlsx', sheetname=sheet)
    df2=df2[['Query', 'SRPVs']]
    df2.rename(columns={'SRPVs': 'July16_SRPVs'}, inplace=True)

    df3=pd.read_excel('C:/Users/v-vekop/Desktop/json/Top100K_Queries_August16.xlsx', sheetname=sheet)
    df3=df3[['Query', 'SRPVs']]
    df3.rename(columns={'SRPVs': 'August16_SRPVs'}, inplace=True)
    dfs=[df1,df2,df3]
    df=pd.concat(dfs)
    unique_q=df['Query'].unique()
    ndf=pd.DataFrame(unique_q)
    ndf["Query"]=ndf.ix[:,0]
    ndf=ndf[['Query']]
    for f in dfs:
             ndf = pd.merge(ndf, f, on=['Query'],how='left')

    # Convert the dataframe to an XlsxWriter Excel object.
    ndf.to_excel(writer, sheet_name=sheet,index=False)
# Close the Pandas Excel writer and output the Excel file.
writer.close()
