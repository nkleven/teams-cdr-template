// Project Eden - Multi-VM Redundant Worker Infrastructure
// Deploys multiple worker VMs across availability zones with load balancing
// Owner: Nathan Kleven | EIN: 41-3131704 | Name Control: KLEV

targetScope = 'resourceGroup'

@description('Environment name')
@allowed(['dev', 'staging', 'prod'])
param environment string = 'dev'

@description('Azure region for deployment')
param location string = resourceGroup().location

@description('Number of worker VMs to deploy')
@minValue(2)
@maxValue(10)
param workerCount int = 3

@description('VM size for worker nodes')
@allowed(['Standard_B2s', 'Standard_B2ms', 'Standard_D2s_v3', 'Standard_D4s_v3'])
param vmSize string = 'Standard_B2s'

@description('Admin username for VMs')
param adminUsername string = 'edenadmin'

@description('SSH public key for VM authentication')
@secure()
param sshPublicKey string

@description('Enable auto-shutdown for cost optimization')
param enableAutoShutdown bool = true

@description('Auto-shutdown time (24h format, e.g., 1900 for 7:00 PM)')
param autoShutdownTime string = '1900'

@description('Auto-shutdown timezone')
param autoShutdownTimezone string = 'Pacific Standard Time'

@description('Tags for all resources')
param tags object = {
  project: 'Eden'
  environment: environment
  owner: 'Nathan Kleven'
  costCenter: 'KLEV-41-3131704'
  managedBy: 'Bicep'
}

// Variables
var namePrefix = 'eden-${environment}'
var vnetName = '${namePrefix}-vnet'
var subnetName = 'workers'
var lbName = '${namePrefix}-lb'
var availabilitySetName = '${namePrefix}-avset'
var nsgName = '${namePrefix}-nsg'

// Virtual Network
module vnet 'modules/vnet.bicep' = {
  name: 'vnet-deployment'
  params: {
    name: vnetName
    location: location
    tags: tags
    addressPrefix: '10.0.0.0/16'
    subnets: [
      {
        name: subnetName
        addressPrefix: '10.0.1.0/24'
        nsgId: nsg.outputs.id
      }
      {
        name: 'management'
        addressPrefix: '10.0.2.0/24'
        nsgId: nsg.outputs.id
      }
    ]
  }
}

// Network Security Group
module nsg 'modules/nsg.bicep' = {
  name: 'nsg-deployment'
  params: {
    name: nsgName
    location: location
    tags: tags
  }
}

// Availability Set for VM redundancy
module availabilitySet 'modules/availability-set.bicep' = {
  name: 'avset-deployment'
  params: {
    name: availabilitySetName
    location: location
    tags: tags
    faultDomainCount: 2
    updateDomainCount: 5
  }
}

// Internal Load Balancer
module loadBalancer 'modules/load-balancer.bicep' = {
  name: 'lb-deployment'
  params: {
    name: lbName
    location: location
    tags: tags
    subnetId: vnet.outputs.subnetIds[0]
    backendPoolName: 'workers'
    healthProbePath: '/health'
    healthProbePort: 8080
  }
}

// Worker VMs
module workers 'modules/worker-vm.bicep' = [for i in range(0, workerCount): {
  name: 'worker-${i}-deployment'
  params: {
    name: '${namePrefix}-worker-${i}'
    location: location
    tags: union(tags, { role: 'worker', index: string(i) })
    vmSize: vmSize
    adminUsername: adminUsername
    sshPublicKey: sshPublicKey
    subnetId: vnet.outputs.subnetIds[0]
    availabilitySetId: availabilitySet.outputs.id
    loadBalancerBackendPoolId: loadBalancer.outputs.backendPoolId
    enableAutoShutdown: enableAutoShutdown
    autoShutdownTime: autoShutdownTime
    autoShutdownTimezone: autoShutdownTimezone
    workerIndex: i
  }
}]

// Outputs
output vnetId string = vnet.outputs.id
output loadBalancerIp string = loadBalancer.outputs.privateIp
output workerVmIds array = [for i in range(0, workerCount): workers[i].outputs.vmId]
output workerPrivateIps array = [for i in range(0, workerCount): workers[i].outputs.privateIp]
output resourceGroupName string = resourceGroup().name
output deploymentInfo object = {
  environment: environment
  workerCount: workerCount
  vmSize: vmSize
  autoShutdownEnabled: enableAutoShutdown
  autoShutdownTime: autoShutdownTime
}
