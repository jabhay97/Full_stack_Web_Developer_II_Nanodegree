var map; //Global variable map

function mapError() {
    document.getElementById('map').innerHTML = "Their is an error loading the map"; // if map doesnt load successfully
}

function initMap() {
    ko.applyBindings(new viewModel());
}
var sites = [{ //Array of Sites 
        name: 'Elante Mall',
        location: {
            lat: 30.7045698,
            lng: 76.796752
        },
        locId: "5114cd90e4b06bb0ed15a97f",
        description: "Elante Mall is the biggest Mall in the Chandigarh",
        list: true
    },
    {
        name: 'Sukhna Lake',
        location: {
            lat: 30.7420749,
            lng: 76.8127027
        },
        locId: "4c456c4b8c1f20a14ebd3d99",
        description: "Sukhna Lake in Chandigarh, India, is a reservoir at the foothills (Shivalik hills) of the Himalayas.",
        list: true
    },
    {
        name: 'Zakir Hussain Rose Gardens',
        location: {
            lat: 30.7461143,
            lng: 76.7797887
        },
        locId: "4c0ba827009a0f47975cebbf",
        description: "Zakir Hussain Rose Garden, is a botanical garden located in Chandigarh, India and spread over 30 acres (120,000 m2) of land,[1] with 50,000 rose-bushes of 1600 different species.[2] Named after India's former president, Zakir Hussain",
        list: true
    },
    {
        name: 'Hotel JW Marriott',
        location: {
            lat: 30.726705,
            lng: 76.7649463
        },
        locId: "4dff0926d4c00c69c14b292a",
        description: "One of the best hotels of Chandigarh",
        list: true
    },
    {
        name: 'Nek Chand Rock Gardens',
        location: {
            lat: 30.7524073,
            lng: 76.8050706
        },
        locId: "4b6fe660f964a5206dff2ce3",
        description: "The Rock Garden of Chandigarh is a sculpture garden in Chandigarh, India, also known as Nek Chand's Rock Garden after its founder Nek Chand, a government official who started the garden secretly in his spare time in 1957",
        list: true
    },
    {
        name: 'Chandigarh Golf Club',
        location: {
            lat: 30.737874,
            lng: 76.8090959
        },
        locId: "4e97f82261af7d268f13d826",
        description: "Chandigarh Golf Club was was laid out in 1962 and is located just south of Sukhna Lake and adjacent to the residence of the Punjab Governor in Sector 6.",
        list: true
    },

    {
        name: 'Punjab University',
        location: {
            lat: 30.7600747,
            lng: 76.7641141
        },
        locId: "4c4ae6f0f7b49c74e81efdc1",
        description: "One of the oldest Universities of Punjab.",
        list: true
    }
];

function fourSquareData(marker, infoWindow) {
    var locId = marker.locId;
    $.ajax({
        url: "https://api.foursquare.com/v2/venues/" + locId + "?client_id=SIWTXR2ROKG1VWNJUUUPJUPSZ5F5ZL0FEZC5DELCCWO0IDD4&client_secret=HSD3MUFUWVGLSOEEJOQD1HZRPFOV3BCNFOIIHNOGJGY00AVW&v=20161016",
        dataType: 'json',
        success: function(data) {
            ven = data.response.venue;
            marker.likes = ven.likes.summary;
            marker.address = "";
            for (var i = 0; i < ven.location.formattedAddress.length; i++) {
                marker.address += ven.location.formattedAddress[i];
                marker.address += "<br>";
            }
            infoWindow.setContent('<div>' + marker.name + '<br>' + marker.description + '</div>' + marker.address + marker.likes);
        },
        error: function(data) {
            infoWindow.setContent('<div>' + marker.name + '<br>' + marker.description + '</div>' + 'Unable to get fourSquare data')
        }
    });
}

function populateInfo(marker, infoWindow) {
    if (infoWindow.marker != marker) { //ensures that only 1 infowindow is opened per marker
        infoWindow.marker = marker;
        infoWindow.setContent('<div>' + marker.name + '<br>' + marker.description + '</div>');
        fourSquareData(marker, infoWindow);
        infoWindow.open(map, marker);

        infoWindow.addListener('closeclick', function() {
            infoWindow.setMarker(null);
        });
    }
}

function markerListener() { //Animations on click
    var currentMarker = this;
    populateInfo(this, infoWindow); //
    currentMarker.setAnimation(google.maps.Animation.BOUNCE);
    setTimeout(function() {
        currentMarker.setAnimation(null);
    }, 1000);
}

var viewModel = function() {
    map = new google.maps.Map(document.getElementById('map'), { //map created and initial coords and zoom is set
        center: {
            lat: 30.726388,
            lng: 76.768300
        },
        zoom: 15
    });
    var self = this;
    self.markerArray = []; //array of markers
    infoWindow = new google.maps.InfoWindow(); //used to generate info windows
    var boundaries = new google.maps.LatLngBounds(); //used to set boundaries
    for (var i = 0; i < sites.length; i++) { //used to push the contents of array site to markerArray
        var positions = sites[i].location;
        var name = sites[i].name;
        var locId = sites[i].locId;
        var description = sites[i].description;
        var lists = sites[i].list;
        var marker = new google.maps.Marker({ //used to create markers
            map: map,
            position: positions,
            name: name,
            animation: google.maps.Animation.DROP,
            description: description,
            locId: locId,
            list: ko.observable(lists)
        });
        marker.addListener('click', markerListener);
        self.markerArray.push(marker); //Pushes various markers to an array
        boundaries.extend(marker.position); //verify boundaries

    }
    self.filteredLocation = ko.observable(""); // used to store value from list so as to filter
    /*Search or Filter Algorithm taken reference from stackoverflow*/
    self.test = function(viewModel, event) {
        if (self.filteredLocation().length === 0) {
            for (var i = 0; i < self.markerArray.length; i++) {
                self.markerArray[i].setVisible(true);
                self.markerArray[i].list(true);
            }
        } else {
            for (var k = 0; k < self.markerArray.length; k++) {
                if (self.markerArray[k].name.toLowerCase().indexOf(self.filteredLocation().toLowerCase()) >= 0) {
                    self.markerArray[k].setVisible(true);
                    self.markerArray[k].list(true);
                } else {
                    self.markerArray[k].setVisible(false);
                    self.markerArray[k].list(false);
                }
            }
        }
        infoWindow.close();
    };
    map.fitBounds(boundaries);
};