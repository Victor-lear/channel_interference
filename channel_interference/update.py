#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: victor
"""
from wisepaasdatahubedgesdk.EdgeAgent import EdgeAgent
import wisepaasdatahubedgesdk.Common.Constants as constant
from wisepaasdatahubedgesdk.Model.Edge import EdgeAgentOptions, MQTTOptions, DCCSOptions, EdgeData, EdgeTag, EdgeStatus, EdgeDeviceStatus, EdgeConfig, NodeConfig, DeviceConfig, AnalogTagConfig, DiscreteTagConfig, TextTagConfig
from wisepaasdatahubedgesdk.Common.Utils import RepeatedTimer
import channel_interference
import time
import datetime
nodeID="51842f8b-ea50-4e8a-86ca-6c7506bad6f9"
apiURL="https://api-dccs-ensaas.education.wise-paas.com/"
CredentialKEY="f9d3d143e3407c268cac338d2184a3ob"
edgeAgentOptions = EdgeAgentOptions(nodeId = nodeID)#nodeID
edgeAgentOptions.connectType = constant.ConnectType['DCCS']
dccsOptions = DCCSOptions(apiUrl = apiURL, credentialKey = CredentialKEY)
edgeAgentOptions.DCCS = dccsOptions
_edgeAgent = EdgeAgent(edgeAgentOptions)
_edgeAgent.connect()



#update data connect
def updatedataconnect(_edgeAgent,channeldata):
    config = __generateConfig(channeldata)
    _edgeAgent.uploadConfig(action = constant.ActionType['Update'], edgeConfig = config)

#send data
def senddata(_edgeAgent,channeldata):
    data = __generateData(channeldata)
    _edgeAgent.sendData(data)
def __generateConfig(channeldata):
    config = EdgeConfig()
    nodeConfig = NodeConfig(nodeType = constant.EdgeType['Gateway'])
    config.node = nodeConfig
    for i in range(1):
        deviceConfig = DeviceConfig(id = 'Interference',
          name = 'Interference',
          description = 'Interference',
          deviceType = 'Smart Device',
          retentionPolicyName = '')
        for j in range(len(channeldata)):
            analog = AnalogTagConfig(name = channeldata[j]['ap_name'],
                description = channeldata[j]['ap_name'],
                readOnly = False,
                arraySize = 0,
                spanHigh = 1000,
                spanLow = 0,
                engineerUnit = '',
                integerDisplayFormat = 4,
                fractionDisplayFormat = 2)
            deviceConfig.analogTagList.append(analog)
        config.node.deviceList.append(deviceConfig)
    
    return config       

def __generateData(channeldata):
      edgeData = EdgeData()
      for i in range(1):
        for j in range(len(channeldata)):
            deviceId = 'Interference'
            tagName = channeldata[j]['ap_name']
            value = channeldata[j]['channel_interference']
            tag = EdgeTag(deviceId, tagName, value)
            edgeData.tagList.append(tag)
      edgeData.timestamp = datetime.datetime.now()
      return edgeData
data=channel_interference.catch_channelinterference('AP','Controller4')
channeldata=channel_interference.setup_alarm(data=data)
updatedataconnect(_edgeAgent,channeldata)
while(1):
    senddata(_edgeAgent,channeldata)
    print(1)
    time.sleep(300)
    data=channel_interference.catch_channelinterference('AP','Controller4')
    channeldata=channel_interference.setup_alarm(data=data)
