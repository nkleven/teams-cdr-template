// Worker VM Module - Project Eden
// Deploys individual worker VM with auto-shutdown capability

@description('VM name')
param name string

@description('Azure region')
param location string

@description('Resource tags')
param tags object

@description('VM size')
param vmSize string

@description('Admin username')
param adminUsername string

@description('SSH public key')
@secure()
param sshPublicKey string

@description('Subnet resource ID')
param subnetId string

@description('Availability set resource ID')
param availabilitySetId string

@description('Load balancer backend pool ID')
param loadBalancerBackendPoolId string

@description('Enable auto-shutdown')
param enableAutoShutdown bool

@description('Auto-shutdown time')
param autoShutdownTime string

@description('Auto-shutdown timezone')
param autoShutdownTimezone string

@description('Worker index for identification')
param workerIndex int

// Network Interface
resource nic 'Microsoft.Network/networkInterfaces@2023-09-01' = {
  name: '${name}-nic'
  location: location
  tags: tags
  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig1'
        properties: {
          privateIPAllocationMethod: 'Dynamic'
          subnet: {
            id: subnetId
          }
          loadBalancerBackendAddressPools: [
            {
              id: loadBalancerBackendPoolId
            }
          ]
        }
      }
    ]
    enableAcceleratedNetworking: vmSize != 'Standard_B2s' // B-series doesn't support accelerated networking
  }
}

// Virtual Machine
resource vm 'Microsoft.Compute/virtualMachines@2023-09-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    availabilitySet: {
      id: availabilitySetId
    }
    hardwareProfile: {
      vmSize: vmSize
    }
    storageProfile: {
      imageReference: {
        publisher: 'Canonical'
        offer: '0001-com-ubuntu-server-jammy'
        sku: '22_04-lts-gen2'
        version: 'latest'
      }
      osDisk: {
        name: '${name}-osdisk'
        createOption: 'FromImage'
        managedDisk: {
          storageAccountType: 'Standard_LRS'
        }
        diskSizeGB: 30
      }
    }
    osProfile: {
      computerName: 'worker${workerIndex}'
      adminUsername: adminUsername
      linuxConfiguration: {
        disablePasswordAuthentication: true
        ssh: {
          publicKeys: [
            {
              path: '/home/${adminUsername}/.ssh/authorized_keys'
              keyData: sshPublicKey
            }
          ]
        }
      }
      customData: base64(loadTextContent('../scripts/worker-init.sh'))
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: nic.id
        }
      ]
    }
    diagnosticsProfile: {
      bootDiagnostics: {
        enabled: true
      }
    }
  }
}

// Auto-shutdown schedule
resource autoShutdown 'Microsoft.DevTestLab/schedules@2018-09-15' = if (enableAutoShutdown) {
  name: 'shutdown-computevm-${name}'
  location: location
  tags: tags
  properties: {
    status: 'Enabled'
    taskType: 'ComputeVmShutdownTask'
    dailyRecurrence: {
      time: autoShutdownTime
    }
    timeZoneId: autoShutdownTimezone
    targetResourceId: vm.id
    notificationSettings: {
      status: 'Enabled'
      timeInMinutes: 30
      emailRecipient: 'nathan@edencrafted.net'
      notificationLocale: 'en'
    }
  }
}

// Outputs
output vmId string = vm.id
output vmName string = vm.name
output privateIp string = nic.properties.ipConfigurations[0].properties.privateIPAddress
output nicId string = nic.id
