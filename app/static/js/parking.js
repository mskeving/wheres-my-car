$(document).ready(function() {
    if ($('.new-location-content').length > 0) {
        currentLocationMap();
    } else if ($('.street-cleaning-content').length > 0) {
        carLocationMap();
    }

    $('#change-loc-butt').on('click', function() {
        document.location.href = '/park';
    });

});

function carLocationMap() {
    var address = $('.location-text').text(),
        carMarker = new google.maps.Marker(),
        geocoder = new google.maps.Geocoder();
        infowindow = new google.maps.InfoWindow(),
        map = new google.maps.Map(document.getElementById('map-canvas')),
        newMarker = new google.maps.Marker();

    // bounds for San Francisco, bias results to be in SF
    var sw = new google.maps.LatLng(37.701228, -122.508325),
        ne = new google.maps.LatLng(37.815500, -122.377691),
        bounds = new google.maps.LatLngBounds(sw, ne);

    geocoder.geocode({ 'address': address, 'bounds': bounds}, function (results, status) {
        var pos = new google.maps.LatLng(results[0]['geometry'].location.lat(),
            results[0]['geometry'].location.lng());

        carMarker.setOptions({
            position: pos,
            map: map,
            icon: '/static/images/suzuki.jpg'
        });

        map.setOptions({
            center: pos,
            zoom: 17,
        })
    });

    google.maps.event.addListener(map, 'click', function(event) {
        infowindow.close();
        moveMarker(event.latLng);
        lookupCleanings(event.latLng);
    });

    function lookupCleanings(pos) {
        geocoder.geocode({'latLng': pos}, function (results, status) {
            if (status != google.maps.GeocoderStatus.OK || !results[0]) {
                alert('problem with geocoding: ', status);
                return;
            }
            address = results[0]['formatted_address'].split(',')[0];
            fetchCleaningData(address, displayCleaningInfo.bind(this, address));
        });
    }

    function fetchCleaningData(address, callback) {
        var parts = address.split(' ');
        var streetNum = parts.shift();
        var streetName = parts.join(' ');
        $.ajax({
            type: "Post",
            url: '/lookup',
            dataType: 'json',
            data: {
                streetNum: streetNum,
                streetName: streetName
            },
            success: callback,
            error: function(jqXHR, textStatus, errorThrown) {
                infowindow.setContent('<div id="content">' +
                    '<div id="street-address">Error Accessing Server:' +
                    errorThrown + '</div>' + '</div>'
                );
            }
        });
    }

    function displayCleaningInfo(address, cleaningInfo) {
        infowindow.setContent('<div id="content">' +
            '<div id="street-address">' + address + '</div>' +
            cleaningInfo + '<div id="new-location">park here</div></div>'
        );
        infowindow.open(map, newMarker);
    }

    function moveMarker(latlng) {
        newMarker.setOptions({
            position: latlng,
            map: map,
            draggable:true
        });

        google.maps.event.addListener(newMarker, 'dragend', function(event) {
            lookupCleanings(event.latLng);
        });
    }

    google.maps.event.addListener(infowindow, 'domready', function() {
        $('#new-location').on('click', function(){
            var address = $('#street-address').text(),
                streetNum = address.substr(0, address.indexOf(' ')),
                streetName =  address.substr(address.indexOf(' ')+1);

            $.ajax({
                type: "Post",
                url: '/new-location',
                data: {
                    streetNum: streetNum,
                    streetName: streetName
                },
                success: function() {
                    $('.location-text').text(address);
                    infowindow.close();
                    newMarker.setMap(null);
                    carMarker.setOptions({position: newMarker.position});
                },
                error: function() {
                    alert('error submitting address');
                }
            })

        })
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

        google.maps.event.addListener(marker, 'dragend', function(event) {
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
