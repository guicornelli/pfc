variaveis = ['ActivePower', 'ActivePowerSetpoint', 'AmbientTemperature', 'AuxReactivePower', 'BusVoltage',
             'CapacityFactor', 'ControlModuleTemp', 'ConvAirTemp', 'CoolerTemp', 'CosPhi', 'DeltaControlSP',
             'FG8AirTemp', 'GearboxBearingTemp', 'GearboxOilParticleFlow', 'GearboxOilTemp',
             'GearboxShaftBearingGrease', 'GenActivePower', 'GenCSBearingTemp', 'GenNCSBearingTemp', 'GenRingTemp',
             'GenSpeed', 'GenSpeedOGS', 'GenSpeedTop', 'GenWinding1Temp', 'GenWinding2Temp', 'GenWinding3Temp',
             'GreaseGenBearingTank', 'GridCurrent', 'GridFrec', 'GridFrecPLC', 'GridHAvailability', 'GridIndTemp',
             'GridRectTemp', 'GridVoltage', 'HAvailability', 'HPauseIceTotal', 'HService', 'HydrOilTemp', 'HydrPress',
             'IceDetTemp', 'NacelleOrientation', 'NacelleTemp', 'NoiseLevel', 'NoiseLevelCommLost', 'NoiseLeverLowWind',
             'PitchAngle', 'PLimitAvailableStator', 'ProduciblePower', 'ProducibleQCap', 'ProducibleQInd',
             'Radiator1Temp', 'Radiator2Temp', 'ReactivePower', 'RectActivePower', 'RectCurrent', 'RotorCurrent',
             'RotorInvTemp', 'RotorSpeed', 'ServoVoltage', 'SPCosPhi', 'SPGenSpeed', 'SPPitchAngle', 'SPStatorP',
             'SPStatorQ', 'StatorActivePower', 'StatorCurrent', 'StatorReactivePower', 'StatusWT', 'StoopedByTool',
             'TotalProduction', 'TowerFrecuency', 'TrafoWinding1Temp', 'TrafoWinding2Temp', 'TrafoWinding3Temp',
             'TurbHAvailability', 'WindDirection', 'WindDirectionRelNac', 'WindSpeed', 'WindSpeedNotF', 'YawBrakePress']

# -------------------------------------------------------------------------------------------------------------------- #
temperature = ['AmbientTemperature', 'ControlModuleTemp', 'ConvAirTemp', 'CoolerTemp', 'FG8AirTemp',
               'GearboxBearingTemp', 'GearboxOilTemp', 'GenCSBearingTemp', 'GenNCSBearingTemp', 'GenRingTemp',
               'GenWinding1Temp', 'GenWinding2Temp', 'GenWinding3Temp', 'GridIndTemp', 'GridRectTemp', 'HydrOilTemp',
               'IceDetTemp', 'NacelleTemp', 'Radiator1Temp', 'Radiator2Temp', 'RotorInvTemp', 'TrafoWinding1Temp',
               'TrafoWinding2Temp', 'TrafoWinding3Temp']

performance = ['ActivePower', 'ActivePowerSetpoint', 'AuxReactivePower', 'CapacityFactor', 'CosPhi', 'GenActivePower',
               'GenSpeed', 'GenSpeedOGS', 'GenSpeedTop', 'NacelleOrientation', 'PitchAngle', 'PLimitAvailableStator',
               'ProduciblePower', 'ProducibleQCap', 'ProducibleQInd', 'ReactivePower', 'RectActivePower', 'RotorSpeed',
               'StatorActivePower', 'StatorReactivePower', 'TotalProduction', 'WindDirection', 'WindDirectionRelNac',
               'WindSpeed', 'WindSpeedNotF']

eletric = ['BusVoltage', 'GridCurrent', 'GridFrecPLC', 'GridFrec', 'GridVoltage', 'RectCurrent', 'RotorCurrent',
           'ServoVoltage', 'StatorCurrent', 'TowerFrecuency']

oil = ['GearboxOilParticleFlow', 'GearboxOilTemp', 'GearboxShaftBearingGrease', 'GreaseGenBearingTank', 'HydrOilTemp',
       'HydrPress', 'YawBrakePress']

vibration = ['NoiseLevel', 'NoiseLevelCommLost', 'NoiseLeverLowWind']

availability = ['GridHAvailability', 'HAvailability', 'HPauseIceTotal', 'HService', 'TurbHAvailability']

status = ['StatusWT', 'StoopedByTool']

setpoints = ['DeltaControlSP', 'SPCosPhi', 'SPGenSpeed', 'SPPitchAngle', 'SPStatorP', 'SPStatorQ']

# -------------------------------------------------------------------------------------------------------------------- #
gearbox = ['GearboxBearingTemp', 'GearboxOilParticleFlow', 'GearboxOilTemp', 'GearboxShaftBearingGrease']
generator = ['GenActivePower', 'GenCSBearingTemp', 'GenRingTemp', 'GenSpeed', 'GenSpeedOGS', 'GenSpeedTop',
             'GenWinding1Temp', 'GenWinding2Temp', 'GenWinding3Temp', 'GreaseGenBearingTank', 'StatorActivePower',
             'StatorCurrent', 'StatorReactivePower']
wind = ['WindDirectionRelNac', 'WindSpeed', 'WindSpeedNotF']
trafo = ['TrafoWinding1Temp', 'TrafoWinding2Temp', 'TrafoWinding3Temp']
rotor = ['RotorCurrent', 'RotorInvTemp', 'RotorSpeed']
nacelle = ['NacelleOrientation', 'NacelleTemp', 'ServoVoltage']

# -------------------------------------------------------------------------------------------------------------------- #
labels_gender = ['AmbientTemperature', 'ControlModuleTemp', 'ConvAirTemp', 'CoolerTemp', 'FG8AirTemp',
                 'GearboxBearingTemp', 'GearboxOilTemp', 'GenCSBearingTemp', 'GenRingTemp', 'GenWinding1Temp',
                 'GenWinding2Temp', 'GenWinding3Temp', 'GridIndTemp', 'GridRectTemp', 'HydrOilTemp',
                 'NacelleTemp', 'Radiator1Temp', 'Radiator2Temp', 'RotorInvTemp', 'TrafoWinding1Temp',
                 'TrafoWinding2Temp', 'TrafoWinding3Temp',

                 'ActivePower', 'ActivePowerSetpoint', 'AuxReactivePower', 'GenActivePower', 'GenSpeed', 'GenSpeedOGS',
                 'GenSpeedTop', 'NacelleOrientation', 'PitchAngle', 'PLimitAvilableStator', 'ProduciblePower',
                 'ProducibleQCap', 'ProducibleQInd', 'ReactivePower', 'RectActivePower', 'RotorSpeed',
                 'StatorActivePower', 'StatorReactivePower', 'TotalProduction', 'WindDirectionRelNac', 'WindSpeed',
                 'WindSpeedNotF',

                 'BusVoltage', 'GridCurrent', 'GridFrec', 'GRidFrecPLC', 'GridVoltage', 'RectCurrent', 'RotorCurrent',
                 'ServoVoltage', 'StatorCurrent', 'TowerFrecuency',

                 'GearboxOilParticleFlow', 'GearboxShaftBearingGrease', 'GreaseGenBearingTank', 'HydrPress',
                 'YawBrakePress',

                 'NoiseLevel', 'NoiseLevelCommLost', 'NoiseLeverLowWind',

                 'GridHAvailability', 'HAvailability', 'HService', 'TurbHAvailability',

                 'StatusWT', 'StoopedByTool']

group_names = ['Temperatura', 'Performance', 'Elétrico', 'Óleo', 'Vibração', 'Disponibilidade', 'Status']
group_size = [len(temperature), len(performance), len(eletric), len(oil), len(vibration), len(availability),
              len(status)]

# -------------------------------------------------------------------------------------------------------------------- #
#                          = [temp, perf, eel, oil, vib, avail, status]
AmbientTemperature         = [1, 0, 0, 0, 0, 0, 0]
ControlModuleTemp          = [1, 0, 0, 0, 0, 0, 0]
ConvAirTemp                = [1, 0, 0, 0, 0, 0, 0]
CoolerTemp                 = [1, 0, 0, 0, 0, 0, 0]
FG8AirTemp                 = [1, 0, 0, 0, 0, 0, 0]
GearboxBearingTemp         = [1, 0, 0, 0, 0, 0, 0]
GearboxOilTemp             = [1, 0, 0, 0, 0, 0, 0]
GenCSBearingTemp           = [1, 0, 0, 0, 0, 0, 0]
GenRingTemp                = [1, 0, 0, 0, 0, 0, 0]
GenWinding1Temp            = [1, 0, 0, 0, 0, 0, 0]
GenWinding2Temp            = [1, 0, 0, 0, 0, 0, 0]
GenWinding3Temp            = [1, 0, 0, 0, 0, 0, 0]
GridIndTemp                = [1, 0, 0, 0, 0, 0, 0]
GridRectTemp               = [1, 0, 0, 0, 0, 0, 0]
HydrOilTemp                = [1, 0, 0, 0, 0, 0, 0]
NacelleTemp                = [1, 0, 0, 0, 0, 0, 0]
Radiator1Temp              = [1, 0, 0, 0, 0, 0, 0]
Radiator2Temp              = [1, 0, 0, 0, 0, 0, 0]
RotorInvTemp               = [1, 0, 0, 0, 0, 0, 0]
TrafoWinding1Temp          = [1, 0, 0, 0, 0, 0, 0]
TrafoWinding2Temp          = [1, 0, 0, 0, 0, 0, 0]
TrafoWinding3Temp          = [1, 0, 0, 0, 0, 0, 0]
ActivePower                = [0, 1, 0, 0, 0, 0, 0]
ActivePowerSetpoint        = [0, 1, 0, 0, 0, 0, 0]
AuxReactivePower           = [0, 1, 0, 0, 0, 0, 0]
GenActivePower             = [0, 1, 0, 0, 0, 0, 0]
GenSpeed                   = [0, 1, 0, 0, 0, 0, 0]
GenSpeedOGS                = [0, 1, 0, 0, 0, 0, 0]
GenSpeedTop                = [0, 1, 0, 0, 0, 0, 0]
NacelleOrientation         = [0, 1, 0, 0, 0, 0, 0]
PLimitAvilableStator       = [0, 1, 0, 0, 0, 0, 0]
PitchAngle                 = [0, 1, 0, 0, 0, 0, 0]
ProduciblePower            = [0, 1, 0, 0, 0, 0, 0]
ProducibleQCap             = [0, 1, 0, 0, 0, 0, 0]
ProducibleQInd             = [0, 1, 0, 0, 0, 0, 0]
ReactivePower              = [0, 1, 0, 0, 0, 0, 0]
RectActivePower            = [0, 1, 0, 0, 0, 0, 0]
RotorSpeed                 = [0, 1, 0, 0, 0, 0, 0]
StatorActivePower          = [0, 1, 0, 0, 0, 0, 0]
StatorReactivePower        = [0, 1, 0, 0, 0, 0, 0]
TotalProduction            = [0, 1, 0, 0, 0, 0, 0]
WindDirectionRelNac        = [0, 1, 0, 0, 0, 0, 0]
WindSpeed                  = [0, 1, 0, 0, 0, 0, 0]
WindSpeedNotF              = [0, 1, 0, 0, 0, 0, 0]
BusVoltage                 = [0, 0, 1, 0, 0, 0, 0]
GRidFrecPLC                = [0, 0, 1, 0, 0, 0, 0]
GridCurrent                = [0, 0, 1, 0, 0, 0, 0]
GridFrec                   = [0, 0, 1, 0, 0, 0, 0]
GridVoltage                = [0, 0, 1, 0, 0, 0, 0]
RectCurrent                = [0, 0, 1, 0, 0, 0, 0]
RotorCurrent               = [0, 0, 1, 0, 0, 0, 0]
ServoVoltage               = [0, 0, 1, 0, 0, 0, 0]
StatorCurrent              = [0, 0, 1, 0, 0, 0, 0]
TowerFrecuency             = [0, 0, 1, 0, 0, 0, 0]
GearboxOilParticleFlow     = [0, 0, 0, 1, 0, 0, 0]
GearboxOilTemp             = [0, 0, 0, 1, 0, 0, 0]
GearboxShaftBearingGrease  = [0, 0, 0, 1, 0, 0, 0]
GreaseGenBearingTank       = [0, 0, 0, 1, 0, 0, 0]
HydrOilTemp                = [0, 0, 0, 1, 0, 0, 0]
HydrPress                  = [0, 0, 0, 1, 0, 0, 0]
YawBrakePress              = [0, 0, 0, 1, 0, 0, 0]
NoiseLevel                 = [0, 0, 0, 0, 1, 0, 0]
NoiseLevelCommLost         = [0, 0, 0, 0, 1, 0, 0]
NoiseLeverLowWind          = [0, 0, 0, 0, 1, 0, 0]
GridHAvailability          = [0, 0, 0, 0, 0, 1, 0]
HAvailability              = [0, 0, 0, 0, 0, 1, 0]
HService                   = [0, 0, 0, 0, 0, 1, 0]
TurbHAvailability          = [0, 0, 0, 0, 0, 1, 0]
StatusWT                   = [0, 0, 0, 0, 0, 0, 1]
StoopedByTool              = [0, 0, 0, 0, 0, 0, 1]
