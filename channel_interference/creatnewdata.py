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


#creat data connect

def creatdataconnect(_edgeAgent,channeldata):
    config = __generateConfig(channeldata)
    _edgeAgent.uploadConfig(action = constant.ActionType['Create'], edgeConfig = config)
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
data=channel_interference.catch_channelinterference('AP', 'Controller4')
channeldata=channel_interference.setup_alarm(data=data)
creatdataconnect(_edgeAgent,channeldata)
_edgeAgent.disconnect()

