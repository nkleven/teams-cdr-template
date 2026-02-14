// Virtual Network Module - Project Eden

@description('VNet name')
param name string

@description('Azure region')
param location string

@description('Resource tags')
param tags object

@description('VNet address prefix')
param addressPrefix string

@description('Subnet configurations')
param subnets array

// Virtual Network
resource vnet 'Microsoft.Network/virtualNetworks@2023-09-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    addressSpace: {
      addressPrefixes: [
        addressPrefix
      ]
    }
    subnets: [for subnet in subnets: {
      name: subnet.name
      properties: {
        addressPrefix: subnet.addressPrefix
        networkSecurityGroup: {
          id: subnet.nsgId
        }
        privateEndpointNetworkPolicies: 'Disabled'
        privateLinkServiceNetworkPolicies: 'Enabled'
      }
    }]
  }
}

// Outputs
output id string = vnet.id
output name string = vnet.name
output subnetIds array = [for (subnet, i) in subnets: vnet.properties.subnets[i].id]
output addressSpace string = vnet.properties.addressSpace.addressPrefixes[0]
