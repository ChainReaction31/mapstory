/*
 *  OSH_INTEG
 *
 *  CreateSensorLayer & CreateSensorLayerModal
 */
(function() {
  'use strict';

  angular
    .module('mapstory')
    .controller('createSensorLayerCtrl', createSensorLayerCtrl)
    .controller('createSensorLayerModalCtrl', createSensorLayerModalCtrl);

  function createSensorLayerCtrl($scope, $uibModal) {
    $scope.open = function (templateUrl, modalImage, staticUrl) {
      var modalInstance = $uibModal.open({
        animation: true,
        templateUrl: templateUrl || 'importWizard.html',
        controller:  'createSensorLayerModalCtrl',
        resolve: {
          modalImage: function () {
            return modalImage;
          },
          staticUrl: function () {
            return staticUrl;
          }
        }
      });

      modalInstance.result.then(function (selectedItem) {
        $scope.selected = selectedItem;
      }, function () {
        console.log('Modal dismissed at: ' + new Date());
      });
    };
  }

  function createSensorLayerModalCtrl($scope, $modalInstance, $http, modalImage, staticUrl) {
    $scope.staticUrl = staticUrl;
    $scope.modalImage = modalImage;
    $scope.processing = false;
    $scope.layer = {
        sensors: [],
        hub: {
            url:'',
        },
        configuration_options: {
 //         nativeCRS: 'EPSG:4326',
 //         srs: 'EPSG:4326',
 //         store: {name: 'mapstory_geogig'},
 //         namespace: {'name': 'geonode'},
 //         configureTime: true,
            editable: true,
         },
    };

    $scope.selectedSensors = [];

    $scope.offerings = '';

    // Structure maintains the necessary data from
    $scope.defaultSensor = {
        offeringIdx:'',
        observedProperty:'',
        user_start_time:'',
        user_end_time:'',
        syncMasterTime:false,       
    };

    /* Initialize the selected sensors with a default sensor */
    $scope.selectedSensors.push(angular.copy($scope.defaultSensor));

    $scope.createSensorLayer = function() {
      var sensorTemplate = {
              offeringId:'',
              endPointUrl:'',
              observedProperty:'',
              startTime:'',
              endTime:'',
              syncMasterTime:false,
              sourceType:'',
              name:'',             
          };

      for (var idx = 0; idx < $scope.selectedSensors.length; ++idx ) {

        $scope.layer.sensors.push(angular.copy(sensorTemplate));
        $scope.layer.sensors[idx].name = $scope.offerings[$scope.selectedSensors[idx].offeringIdx].name;
        $scope.layer.sensors[idx].syncMasterTime = $scope.selectedSensors[idx].syncMasterTime;
        $scope.layer.sensors[idx].endTime = $scope.selectedSensors[idx].user_end_time;
        $scope.layer.sensors[idx].startTime = $scope.selectedSensors[idx].user_start_time;
        $scope.layer.sensors[idx].observedProperty = $scope.selectedSensors[idx].observedProperty;
        $scope.layer.sensors[idx].endPointUrl = $scope.layer.hub.url;
        $scope.layer.sensors[idx].offeringId = $scope.offerings[$scope.selectedSensors[idx].offeringIdx].offering_id;
        $scope.layer.sensors[idx].sourceType = $scope.offerings[$scope.selectedSensors[idx].offeringIdx].description;
      }

      $scope.processing = true;
      $scope.errors = [];
//      $scope.setDefaultPermissions($scope.layer.configuration_options.editable);
      $http.post('/opensensorhub/layers/create', {'layer': $scope.layer}).then(function(response){
        $scope.processing = false;
        $scope.success = true;
        $scope.created_layers = response['data']['layers'];
      }, function(response){
        $scope.processing = false;
        $scope.errors = response['data']['errors'];
      })
     };

//    $scope.setDefaultPermissions = function(edit) {
//      $scope.layer.configuration_options.permissions = {
//        'users': {'AnonymousUser': ['change_layer_data', 'download_resourcebase', 'view_resourcebase']},
//        'groups': {'registered': ['change_layer_data', 'download_resourcebase', 'view_resourcebase']}
//      };

//      if(edit === false) {
//        $scope.layer.configuration_options.permissions = {
//          'users': {'AnonymousUser': ['download_resourcebase', 'view_resourcebase']},
//          'groups': {'registered': ['download_resourcebase', 'view_resourcebase']}
//        };
//       }
//       $scope.layer.configuration_options.storeCreateGeogig = true;
//    };

    $scope.nameValid = function() {
      if (!$scope.layer.configuration_options.hasOwnProperty('name')) {
        return false;
      }
      return true;
    };

    $scope.ok = function () {
      $modalInstance.dismiss('cancel');
    };

    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };

    $scope.hubValid = function() {
      if (!$scope.layer.hub.url) {
        return false;
      }
      return true;
    };

    $scope.initUserTimes = function(index) {
        var offeringIndex = $scope.selectedSensors[index].offeringIdx;
	$scope.selectedSensors[index].user_start_time = $scope.offerings[offeringIndex].user_start_time;
	$scope.selectedSensors[index].user_end_time = $scope.offerings[offeringIndex].user_end_time;
    };

    $scope.getHubOfferings = function (address) {
      $scope.errors = [];
      $http.post('/opensensorhub/get_capabilities', {'hubAddress': $scope.layer.hub.url}).then(function(response) {
        $scope.offerings = angular.fromJson(response.data.offerings);
      }, function(response){
        $scope.processing = false;
        $scope.errors = response;
      })
    };

    $scope.addDefaultSensor = function() {
      var sensor = angular.copy($scope.defaultSensor);
      $scope.selectedSensors.push(sensor);
    };

    $scope.removeSensor = function(item) {
      var index = $scope.selectedSensors.indexOf(item);
      $scope.selectedSensors.splice(index, 1);
    };
  }
})();
