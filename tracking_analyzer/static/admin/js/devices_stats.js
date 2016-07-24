/**
 * Requests per device statistics.
 *
 * Original code by Justin Palmer http://bl.ocks.org/Caged/6476579
 *
 * This script expects a `devices` var loaded with some JSON text in the 
 * template stated before it is loaded.
 **/

var margin = {top: 40, right: 20, bottom: 30, left: 50},
  width = 500 - margin.left - margin.right,
  height = 300 - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
    return "<strong>Requests:</strong> <span style='color:red'>" + d.count + "</span>";
  });

var svg = d3.select("#devices-stats").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.call(tip);

var data = JSON.parse(devices);

x.domain(data.map(function(d) { return d.device_type; }));
y.domain([0, d3.max(data, function(d) { return d.count; })]);

svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end");

svg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", function(d) { return x(d.device_type); })
    .attr("width", x.rangeBand())
    .attr("y", function(d) { return y(d.count); })
    .attr("height", function(d) { return height - y(d.count); })
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);

function type(d) {
  d.count = +d.count;
  return d;
}