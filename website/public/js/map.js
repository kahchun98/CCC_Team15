/*
 *  Variable Declarations
*/

var width = 960,
    height = 1160;

var svg = d3.select(".content-wrapper").append("svg")
    .attr("width", width)
    .attr("height", height);

var g = svg.append("g");

var path = d3.geoPath();

/*
 *  D3 Functions
 */

d3.json("map-json/vic.json", function(au) {
  g.append("path")
    .datum(topojson.feature(au, au.objects.VIC_LOCALITY_POLYGON_SHP))
    .attr("d", path);
});
