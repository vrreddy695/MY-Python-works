#Read json file
import csv, json, os
import pandas as pd
file_names = os.listdir("C:/Users/v-vemede/Desktop/Price Analysis/GetShoppingSources_dump")
yr_month=['2016_08','2016_09', '2016_10', '2016_11', '2016_12', '2017_01', '2017_02', '2017_03', '2017_04', '2017_05']
for month in yr_month:
    final_df=pd.DataFrame()
    for i in file_names:
        if (i.split("-")[0]==month.split("_")[0])and (i.split("-")[1]==month.split("_")[1]):
            k = i.split('.')[0]
            print i
            if os.stat('C:/Users/v-vemede/Desktop/Price Analysis/GetShoppingSources_dump/' + i).st_size > 7:
                input = open('C:/Users/v-vemede/Desktop/Price Analysis/GetShoppingSources_dump/'+i).read()
                data = json.loads(input)

                #dictionary flatten function
                def flattenDict(d,result=None,index=None,Key=None):
                    if result is None:
                        result = {}
                    if isinstance(d, (list, tuple)):
                        for indexB, element in enumerate(d):
                            if Key is not None:
                                newkey = Key
                            flattenDict(element,result,index=indexB,Key=newkey)            
                    elif isinstance(d, dict):        
                        for key in d:
                            value = d[key]         
                            if Key is not None and index is not None:
                                newkey = ".".join([Key,(str(key).replace(" ", "") + str(index))])
                            elif Key is not None:
                                newkey = ".".join([Key,(str(key).replace(" ", ""))])
                            else:
                                newkey= str(key).replace(" ", "")
                            flattenDict(value,result,index=None,Key=newkey)        
                    else:
                        result[Key]=d        
                    return result

                #Flatten dictionary
                new_data=[]     
                for i in data:
                    i = flattenDict(i)
                    new_data.append(i)

                # convert dictionaries list to pandas dataframe
                import pandas as pd
                df= pd.DataFrame.from_records(new_data)
                #del data
                #del new_data
                #Transpose offers columns as rows
                col_trans_list=['offers.seller_name','offers.description','offers.availability','offers.lastUpdated', 'offers.name','offers.price', 'offers.priceCurrency', 'offers.url', 'offers.urlPingSuffix','offers.image.url']

                del_cols=[]
                for i in col_trans_list:
                    if i=='offers.seller_name':
                        df_i=df.filter(regex='offers.seller+[0-9]+.name' , axis=1)
                    elif i=='offers.image.url':
                        df_i=df.filter(regex='offers.seller+[0-9]+.image.url' , axis=1)
                    elif i=='offers.urlPingSuffix':
                        df_i=df.filter(regex='offers.urlPingSuffix+[0-9]' , axis=1)
                    elif i=='offers.description':
                        df_i=df.filter(regex='offers.description+[0-9]' , axis=1)  
                    elif i=='offers.availability':
                        df_i=df.filter(regex='offers.availability+[0-9]' , axis=1)
                    elif i=='offers.lastUpdated':
                        df_i=df.filter(regex='offers.lastUpdated+[0-9]' , axis=1)
                    elif i=='offers.name':
                        df_i=df.filter(regex='offers.name+[0-9]' , axis=1)  
                    elif i=='offers.price':
                        df_i=df.filter(regex='offers.price+[0-9]' , axis=1)
                    elif i=='offers.priceCurrency':
                        df_i=df.filter(regex='offers.priceCurrency+[0-9]' , axis=1)  
                    else:
                        df_i=df.filter(regex='offers.url+[0-9]' , axis=1)
                    cols=list(df_i.columns.values)
                    if len(cols)==0:
                        print 'name not found in the file'
                    else:
                        del_cols.extend(cols)
                        cols.extend(['distinct_id', 'properties.result.LastAccessTime'])
                        df_i=df[cols]
                        df_i=pd.melt(df_i,id_vars=['distinct_id','properties.result.LastAccessTime'])
                        df_i.columns.values[3]= i
                        df_i['variable']=df_i['variable'].str.extract('(\d)', expand=True)
                        if i=='offers.seller_name':
                            offers=df_i
                        else:
                            offers = pd.merge(offers, df_i, on=['distinct_id', 'properties.result.LastAccessTime', 'variable'],how='left')

                for col in del_cols:
                    try:
                        df.drop(col, axis=1, inplace=True)
                    except Exception:
                        pass

                final= pd.merge(offers, df, on=['distinct_id', 'properties.result.LastAccessTime'],how='outer')
                final['source_file']= k
                final = final[pd.notnull(final['offers.seller_name'])]
                #del df_i
                #del offers
                fcols=['distinct_id',
                        'offers.seller_name',
                        'offers.lastUpdated',
                        'offers.name',
                        'offers.price',
                        'offers.priceCurrency',
                        'name',
                        'properties.$LoginState',
                        'properties.$city',
                        'properties.$region',
                        'properties.ChangeTime',
                        'properties.Currency',
                        'properties.ExtractionSource',
                        'properties.FirstAccessTime',
                        'properties.FirstCurrency',
                        'properties.FirstPrice',
                        'properties.Id',
                        'properties.LastAccessTime',
                        'properties.LastCurrency',
                        'properties.LastPrice',
                        'properties.Name',
                        'properties.Price',
                        'properties.ProdId',
                        'properties.Seller',
                        'properties.mp_country_code',
                        'properties.results',
                        'time',
                        'source_file']
                prop_cols=['distinct_id',
                        'offers_seller_name',
                        'offers_lastUpdated',
                        'offers_name',
                        'offers_price',
                        'offers_priceCurrency',
                        'name',
                        'properties_LoginState',
                        'properties_city',
                        'properties_region',
                        'properties_ChangeTime',
                        'properties_Currency',
                        'properties_ExtractionSource',
                        'properties_FirstAccessTime',
                        'properties_FirstCurrency',
                        'properties_FirstPrice',
                        'properties_Id',
                        'properties_LastAccessTime',
                        'properties_LastCurrency',
                        'properties_LastPrice',
                        'properties_Name',
                        'properties_Price',
                        'properties_ProdId',
                        'properties_Seller',
                        'properties_mp_country_code',
                        'properties_results',
                        'time',
                        'source_file']
        
                for j in fcols:
                        if j not in final.columns:
                            final[j]=''
                final=final[fcols]
                for c in range(0,27):
                    final.columns.values[c] = prop_cols[c] 
                    
                tfmt=lambda x: pd.to_datetime(x, unit='ms')
                final.ix[:,'properties_FirstAccessTime']=final["properties_FirstAccessTime"].apply(tfmt)
                final.ix[:,'properties_LastAccessTime']=final["properties_LastAccessTime"].apply(tfmt)
                final.ix[:,'properties_ChangeTime']=final["properties_ChangeTime"].apply(tfmt)
                final.ix[:,'time']=final["time"].apply(tfmt)
                final_df=final_df.append(final,ignore_index=True)
                
                #del final
            else:
                print "Empty file"
        else:
            print "Other Months files"

    final_df.to_csv('C:/Users/v-vekop/Desktop/Getshoppingsources/Getshoppingsources_consolidated_'+month+'.csv', sep = ',', index = False, encoding = 'utf-8')