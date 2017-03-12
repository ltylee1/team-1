function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 11,
        center: {
            lat: 49.1609273,
            lng: -122.74400347
        }
    });
    var geocoder = new google.maps.Geocoder();

    document.getElementById('submit').addEventListener('click', function() {
        geocodeAddress(geocoder, map);
        //run geocodeAddress(geocoder,map for every parsed address string)
    });
}

function geocodeAddress(geocoder, resultsMap) {
    //var address = document.getElementById('address').value;
    var addresses = ['V2Y 2N1','V1M 2R6']
    for (count = 0; count < addresses.length; count++) {
            geocoder.geocode({
        'address': addresses[count]
    }, function(results, status) {
        if (status === 'OK') {
            //resultsMap.setCenter(results[0].geometry.location);
            resultsMap.setCenter(49.1609273,-122.74400347);
            var marker = new google.maps.Marker({
                map: resultsMap,
                position: results[0].geometry.location
            });
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
    }
}