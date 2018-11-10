import pandas as pd

def detectBadIp(rec):
    ips = pd.read_csv('ip_database.csv')
    coincide = ips['ip'].isin(rec['destination_IP'])
    nuevoDF = coincide.to_frame()
    nuevoDF['index1'] = nuevoDF.index
    nuevoDF = nuevoDF[nuevoDF['ip'] == True]
    print(ips.ix[nuevoDF['index1']])
    print("Acaba")

def detectBadPorts(rec):
    coincide = rec['destination_Port'].isin(["6667", "25", "1080"])
    nuevoDF = coincide.to_frame()
    nuevoDF['index1'] = nuevoDF.index
    nuevoDF = nuevoDF[nuevoDF['destination_Port'] == True]
    dataframe = rec.ix[nuevoDF['index1']]
    counted_dataframe = {}
    indices=[]
    for index, values in dataframe.iterrows():
        if values['destination_IP'] in counted_dataframe:
            counted_dataframe[values['destination_IP']] += 1;
            if counted_dataframe[values['destination_IP']]>1:
                indices.append(index)
        else:
            counted_dataframe[values['destination_IP']] = 1;
            
    
    for key, values in counted_dataframe.items():
        #Change value to number of desire repeats for botnet
        if values > 1 :
            print(str(key) + " Es botnet")
    print(rec.ix[indices])
    #print(counted_dataframe)




def detectErrors(rec):
    print('verga')
    coincide = rec['destination_MAC'].isin(['000000000000'])
    nuevoDF = coincide.to_frame()
    nuevoDF['index1']= nuevoDF.index
    nuevoDF = nuevoDF[nuevoDF['destination_MAC'] == True]
    dataframe = rec.ix[nuevoDF['index1']]
    counted_dataframe={}
    indices=[]
    for index, values in dataframe.iterrows():
        if values['destination_MAC'] in counted_dataframe:
            counted_dataframe[values['destination_MAC']] += 1;
            if counted_dataframe[values['destination_MAC']]>1:
                indices.append(index)
        else:
            counted_dataframe[values['destination_MAC']] = 1;
            
    for key, values in counted_dataframe.items():
        #Change value to number of desire repeats for botnet
        if values > 1 :
            print(str(key) + " Es botnet")
    print(rec.ix[indices])



data = [['197.1.2.3','000000000000'], ['192.10.2.10','pacu189fab68'], ['192.37.1.20','asdfgh765432'], ['192.123.45.1','000000000000'], ['192.234.53.1','plmoknijb875'], ['192.34.5.7','000000000000'],['192.123.45.1','1ef9hb76gko9']]
test = pd.DataFrame(data,columns=['destination_IP','destination_MAC'])
detectErrors(test)