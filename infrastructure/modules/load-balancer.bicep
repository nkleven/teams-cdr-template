// Internal Load Balancer Module - Project Eden

@description('Load balancer name')
param name string

@description('Azure region')
param location string

@description('Resource tags')
param tags object

@description('Subnet ID for internal LB')
param subnetId string

@description('Backend pool name')
param backendPoolName string

@description('Health probe path')
param healthProbePath string

@description('Health probe port')
param healthProbePort int

// Load Balancer (Internal)
resource lb 'Microsoft.Network/loadBalancers@2023-09-01' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: 'Standard'
    tier: 'Regional'
  }
  properties: {
    frontendIPConfigurations: [
      {
        name: 'frontend'
        properties: {
          privateIPAllocationMethod: 'Dynamic'
          subnet: {
            id: subnetId
          }
        }
      }
    ]
    backendAddressPools: [
      {
        name: backendPoolName
      }
    ]
    probes: [
      {
        name: 'health-probe-http'
        properties: {
          protocol: 'Http'
          port: healthProbePort
          requestPath: healthProbePath
          intervalInSeconds: 15
          numberOfProbes: 2
        }
      }
      {
        name: 'health-probe-tcp'
        properties: {
          protocol: 'Tcp'
          port: healthProbePort
          intervalInSeconds: 15
          numberOfProbes: 2
        }
      }
    ]
    loadBalancingRules: [
      {
        name: 'http-rule'
        properties: {
          frontendIPConfiguration: {
            id: resourceId('Microsoft.Network/loadBalancers/frontendIPConfigurations', name, 'frontend')
          }
          backendAddressPool: {
            id: resourceId('Microsoft.Network/loadBalancers/backendAddressPools', name, backendPoolName)
          }
          probe: {
            id: resourceId('Microsoft.Network/loadBalancers/probes', name, 'health-probe-http')
          }
          protocol: 'Tcp'
          frontendPort: 80
          backendPort: 8080
          enableFloatingIP: false
          idleTimeoutInMinutes: 4
          loadDistribution: 'Default'
        }
      }
      {
        name: 'https-rule'
        properties: {
          frontendIPConfiguration: {
            id: resourceId('Microsoft.Network/loadBalancers/frontendIPConfigurations', name, 'frontend')
          }
          backendAddressPool: {
            id: resourceId('Microsoft.Network/loadBalancers/backendAddressPools', name, backendPoolName)
          }
          probe: {
            id: resourceId('Microsoft.Network/loadBalancers/probes', name, 'health-probe-tcp')
          }
          protocol: 'Tcp'
          frontendPort: 443
          backendPort: 8443
          enableFloatingIP: false
          idleTimeoutInMinutes: 4
          loadDistribution: 'Default'
        }
      }
      {
        name: 'api-rule'
        properties: {
          frontendIPConfiguration: {
            id: resourceId('Microsoft.Network/loadBalancers/frontendIPConfigurations', name, 'frontend')
          }
          backendAddressPool: {
            id: resourceId('Microsoft.Network/loadBalancers/backendAddressPools', name, backendPoolName)
          }
          probe: {
            id: resourceId('Microsoft.Network/loadBalancers/probes', name, 'health-probe-http')
          }
          protocol: 'Tcp'
          frontendPort: 3000
          backendPort: 3000
          enableFloatingIP: false
          idleTimeoutInMinutes: 4
          loadDistribution: 'SourceIP' // Session affinity for API
        }
      }
    ]
  }
}

// Outputs
output id string = lb.id
output name string = lb.name
output privateIp string = lb.properties.frontendIPConfigurations[0].properties.privateIPAddress
output backendPoolId string = lb.properties.backendAddressPools[0].id
output frontendId string = lb.properties.frontendIPConfigurations[0].id
