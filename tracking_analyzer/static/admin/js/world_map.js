/**
 * World map data rendering code from https://github.com/markmarkoh/datamaps
 *
 * Original code by Marc DiMarco. Licensed under MIT license.
 *
 * This script expects a `countries` var loaded with some JSON in the template
 * stated before it is loaded.
 **/

var dataset = {};

var onlyValues = countries.map(function(obj){ return obj[1]; });
var minValue = Math.min.apply(null, onlyValues),
    maxValue = Math.max.apply(null, onlyValues);

var paletteScale = d3.scale.linear().domain([minValue,maxValue]).range(["#EFEFFF","#02386F"]);

countries.forEach(function(item){
  var iso = item[0];
  var value = item[1];
  dataset[iso] = {
    requestsPerCountry: value,
    fillColor: paletteScale(value)
  };
});

new Datamap({
  element: document.getElementById('world-map'),
  projection: 'mercator',
  fills: { defaultFill: '#F5F5F5' },
  data: dataset,
  geographyConfig: {
    borderColor: '#DEDEDE',
    highlightBorderWidth: 2,
    highlightFillColor: function(geo) {
      return geo['fillColor'] || '#F5F5F5';
    },
    highlightBorderColor: '#B7B7B7',
    popupTemplate: function(geo, data) {
      if (!data) { return ; }
      return ['<div class="hoverinfo">',
        '<strong>', geo.properties.name, '</strong>',
        '<br>Requests: <strong>', data.requestsPerCountry, '</strong>',
        '</div>'].join('');
    }
  }
});