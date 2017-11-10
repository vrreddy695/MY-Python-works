#Read json file
import csv, json, os
import pandas as pd
file_names = os.listdir("C:/Users/v-vemede/Desktop/Price Analysis/ExtractProductInfo_dump")
for i in file_names:
    j = i.split('.')[0]
    print i
    if os.stat('C:/Users/v-vemede/Desktop/Price Analysis/ExtractProductInfo_dump/' + i).st_size > 5:
        input = open('C:/Users/v-vemede/Desktop/Price Analysis/ExtractProductInfo_dump/'+i).read()
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

        #Export dataFrame to csv file
        df.to_csv('C:/Users/v-vemede/Desktop/Extraproductinfo_exls/' + j + '.csv', sep = ',', index = False, encoding = 'utf-8')
    else:
        print "Empty file"
