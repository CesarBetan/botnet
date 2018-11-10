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
    for index, values in dataframe.iterrows():
        if values['destination_IP'] in counted_dataframe:
            counted_dataframe[values['destination_IP']] += 1;
        else:
            counted_dataframe[values['destination_IP']] = 1;
    
    for key, values in counted_dataframe.items():
        #Change value to number of desire repeats for botnet
        if values > 1 :
            print(str(key) + " Es botnet")
    #print(counted_dataframe)




def detectErrors(rec):
    coincide = rec['destination_MAC'].isin(['00000000000'])

data = [['197.1.2.3','6667'], ['192.10.2.10','5364'], ['192.37.1.20','25'], ['192.123.45.1','1080'], ['192.234.53.1','27384'], ['192.34.5.7','13894'],['192.123.45.1','1080']]
test = pd.DataFrame(data,columns=['destination_IP','destination_Port'])
detectBadPorts(test)