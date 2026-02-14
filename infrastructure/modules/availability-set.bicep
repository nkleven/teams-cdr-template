// Availability Set Module - Project Eden

@description('Availability set name')
param name string

@description('Azure region')
param location string

@description('Resource tags')
param tags object

@description('Fault domain count')
@minValue(1)
@maxValue(3)
param faultDomainCount int = 2

@description('Update domain count')
@minValue(1)
@maxValue(20)
param updateDomainCount int = 5

// Availability Set
resource availabilitySet 'Microsoft.Compute/availabilitySets@2023-09-01' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: 'Aligned' // Required for managed disks
  }
  properties: {
    platformFaultDomainCount: faultDomainCount
    platformUpdateDomainCount: updateDomainCount
  }
}

// Outputs
output id string = availabilitySet.id
output name string = availabilitySet.name
