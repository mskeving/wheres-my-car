$(document).ready(function() {
    if ($('.new-location-content').length > 0) {
        currentLocationMap();
    } else if ($('.street-cleaning-content').length > 0) {
        carLocationMap();
    }

    $('#change-loc-butt').on('click', function() {
        document.location.href = '/park';
    });

    $('#submit-new-location').on('click', function() {
        // assuming address coming in as NUMBER STREETNAME
        // as in.. before first space is the number and everything after
        // the first space will be the street information
        var address = $('.location-text').text();
        var streetNum = address.substr(0, address.indexOf(' '));
            streetName =  address.substr(address.indexOf(' ')+1);

        $.ajax({
            type: "Post",
            url: '/new-location',
            data: {
                streetNum: streetNum,
                streetName: streetName
            },
            success: function() {
                document.location.href = '/';
            },
            error: function() {
                alert('error submitting address');
            }
        })

    })
});


function carLocationMap() {
    var map = new google.maps.Map(document.getElementById('map-canvas'));
    var marker = new google.maps.Marker();
    var geocoder = new google.maps.Geocoder();
    var address = $('.location-text').text();

    geocoder.geocode({'address': address}, function (results, status) {
        var pos = new google.maps.LatLng(results[0]['geometry'].location.lat(),
                                        results[0]['geometry'].location.lng());

        marker.setOptions({
            map: map,
            position: pos
        });
        map.setOptions({
            center: pos,
            zoom: 17
        });
    });
}

function currentLocationMap() {
    var map = new google.maps.Map(document.getElementById('map-canvas'));
    var marker = new google.maps.Marker();
    var markersArray = [];
    var geocoder = new google.maps.Geocoder();


    //HTML geolocation
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = new google.maps.LatLng(position.coords.latitude,
                position.coords.longitude);

            updateAddress(pos.lat(), pos.lng());

            map.setOptions({
                center: pos,
                zoom: 17
            });

            addMarker(pos);

            google.maps.event.addListener(map, 'click', function(event) {
                removeMarkers();
                addMarker(event.latLng);
                updateAddress(event.latLng.lat(), event.latLng.lng());
            });

        }, function() {
            handleNoGeolocation(true, map);
        });

    } else {
        // browser doesn't support geolocation
        handleNoGeolocation(false, map);
    }

    function updateAddress(lat, lng) {
        var streetAddress;
        var pos = new google.maps.LatLng(lat, lng);

        geocoder.geocode({'latLng': pos}, function (results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                if (results[0]) {
                    // results is array, 0 idx being most specific postal address
                    streetAddress = results[0]['formatted_address'];
                    $('.location-text').text(streetAddress.split(',')[0]);
                } else {
                    $('.location-text').text('No Location Found');
                }
            } else {
                $('.location-text').text('Geocoder failed: ', status);
            }
        });
    }

    function addMarker(latlng) {
        var marker = new google.maps.Marker({
            position: latlng,
            map: map,
            draggable:true
        });

        google.maps.event.addListener(marker,'dragend',function(event) {
            updateAddress(event.latLng.lat(), event.latLng.lng());
        });

        markersArray.push(marker);
    }

    function removeMarkers() {
        for (var i=0; i<markersArray.length; i++) {
            markersArray[i].setMap(null);
        }
    }
}

function handleNoGeolocation(errorFlag, map) {
    if (errorFlag) {
        var content = 'Error: Geolocation failed.';
    } else {
        var content = 'Error: Your browser doesn\'t support geolocation.';
    }

    var options = {
        map: map,
        position: new google.maps.LatLng(60,105),
        content: content
    };

    var infowindow = new google.maps.InfoWindow(options);
    map.setCenter(options.position);
}

function detectBrowser() {
    var useragent = navigator.userAgent;
    var mapdiv = document.getElementById("map-canvas");
  
    if (useragent.indexOf('iPhone') != -1 || useragent.indexOf('Android') != -1 ) {
        mapdiv.style.width = '100%';
        mapdiv.style.height = '100%';
    } else {
        mapdiv.style.width = '600px';
        mapdiv.style.height = '800px';
    }
}
