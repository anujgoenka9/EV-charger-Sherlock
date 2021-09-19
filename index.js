let map;

function initMap() {
  fetch("ev_station_ranveer.json")
  .then(response => response.json())
  .then(data =>{
     //console.log(data[0].Longitude)
    var points = []
    for(let i=0 ; i<data.length ; i++){
      //console.log(data[i])
      points.push({lat:JSON.parse(data[i].Latitude) , lng:JSON.parse(data[i].Longitude)})
    }
    
    for(let i=0 ; i<points.length ; i++){
      const marker = new google.maps.Marker({
        position: points[i],
        map: map,
        icon: 'evstation_icon.png'
      });
    }
  })
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: { lat: 47.6062095, lng: -122.3320708},
  });
  // NOTE: This uses cross-domain XHR, and may not work on older browsers.
  map.data.loadGeoJson(
    "seattle.json"
  );

  
}

