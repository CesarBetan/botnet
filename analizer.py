import pandas as pd
import requests
import json

def detectBadIp(rec):
    ips = pd.read_csv('ip_database.csv')
    coincide = ips['ip'].isin(rec['destination_IP'])
    nuevoDF = coincide.to_frame()
    nuevoDF['index1'] = nuevoDF.index
    nuevoDF = nuevoDF[nuevoDF['ip'] == True]
    nuevoDF = ips.ix[nuevoDF['index1']]['ip']
    return rec.loc[rec['destination_IP'].isin(nuevoDF)]['destination_IP'].value_counts()

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
            counted_dataframe[values['destination_IP']] += 1
            if counted_dataframe[values['destination_IP']]>1:
                indices.append(index)
        else:
            counted_dataframe[values['destination_IP']] = 1
            
    posBots = []
    for key, values in counted_dataframe.items():
        if values > 1 :
            posBots.append(str(key))
    return rec.loc[rec['destination_IP'].isin(posBots)]['destination_IP'].value_counts()




def detectErrors(rec):
    coincide = rec['destination_MAC'].isin(['000000000000'])
    nuevoDF = coincide.to_frame()
    nuevoDF['index1']= nuevoDF.index
    nuevoDF = nuevoDF[nuevoDF['destination_MAC'] == True]
    dataframe = rec.ix[nuevoDF['index1']]
    counted_dataframe={}
    indices=[]
    for index, values in dataframe.iterrows():
        if values['destination_MAC'] in counted_dataframe:
            counted_dataframe[values['destination_MAC']] += 1
            if counted_dataframe[values['destination_MAC']]>1:
                indices.append(index)
        else:
            counted_dataframe[values['destination_MAC']] = 1
    posBots = []        
    for key, values in counted_dataframe.items():
        #Change value to number of desire repeats for botnet
        if values > 1 :
            posBots.append(str(key))
    return rec.loc[rec['destination_IP'].isin(posBots)]['destination_IP'].value_counts()


def getIpInfo(ip):
    ip_requests = 'http://ip-api.com/json/' + str(ip) 
    response = ''
    try:
        r = requests.get(ip_requests)
        print(ip_requests)
        if r.status_code == 200:
            response = r.json()
    except requests.exceptions as e:
        print(e)
    print(response["city"] + " " + response["country"] + " " + response["regionName"] +
     " " + response["org"])
    

def anlyzeLog(df):
    bad_ip = detectBadIp(df)
    bad_port = detectBadPorts(df)
    err = detectErrors(df)

    posBots = {}

    for ip, count in bad_ip.iteritems():
        if ip in posBots:
            posBots[ip]['reasons'].append({'reason':'BAD_IP', 'count':count})
        else:
            posBots[ip] = {
                'ip': ip,
                'reasons': [{'reason':'BAD_IP', 'count':count}]
            }
    for ip, count in bad_port.iteritems():
        if ip in posBots:
            posBots[ip]['reasons'].append({'reason':'BAD_PORT', 'count':count})
        else:
            posBots[ip] = {
                'ip': ip,
                'reasons': [{'reason':'BAD_PORT', 'count':count}]
            }
    for ip, count in err.iteritems():
        if ip in posBots:
            posBots[ip]['reasons'].append({'reason':'ERR', 'count':count})
        else:
            posBots[ip] = {
                'ip': ip,
                'reasons': [{'reason':'ERR', 'count':count}]
            }
    return posBots