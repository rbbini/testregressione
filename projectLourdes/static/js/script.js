var http = new XMLHttpRequest();
let obj ={};
function goToNextStep(step) {
    const formData = document.getElementById('step' + step).elements;
    for(var i = 0 ; i < formData.length ; i++){
        var item = formData.item(i);
        obj[item.name] = item.value;
    }
    const next = Number(step) + 1;
    const nextStep = document.getElementById('step' + next);
    nextStep.classList.add('visible');
    console.log(obj);
}

function goToResults() {
    /* implemento domani */
    http.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var margin = {top: 10, right: 30, bottom: 30, left: 40},
                width = 460 - margin.left - margin.right,
                height = 400 - margin.top - margin.bottom;

            // append the svg object to the body of the page
            var svg = d3.select("#my_dataviz")
              .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
              .append("g")
                .attr("transform",
                      "translate(" + margin.left + "," + margin.top + ")");
            var  rawdata = JSON.parse(this.responseText);

            var data = Object.values(rawdata['SF12 MentalScore 6months']);

          // X axis: scale and draw:
          var x = d3.scaleLinear()
              .domain([0, 110])     // can use this instead of 1000 to have the max of data: d3.max(data, function(d) { return +d.price })
              .range([0, width]);
          svg.append("g")
              .attr("transform", "translate(0," + height + ")")
              .call(d3.axisBottom(x));

          // set the parameters for the histogram
          var histogram = d3.histogram()
              .value(function(d) { return d })   // I need to give the vector of value
              .domain(x.domain())  // then the domain of the graphic
              .thresholds(x.ticks(70)); // then the numbers of bins

          // And apply this function to data to get the bins
          var bins = histogram(data);

          // Y axis: scale and draw:
          var y = d3.scaleLinear()
              .range([height, 0]);
              y.domain([0, d3.max(bins, function(d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously
          svg.append("g")
              .call(d3.axisLeft(y));

          // append the bar rectangles to the svg element
          svg.selectAll("rect")
              .data(bins)
              .enter()
              .append("rect")
                .attr("x", 1)
                .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + y(d.length) + ")"; })
                .attr("width", function(d) { return x(d.x1) - x(d.x0) -1 ; })
                .attr("height", function(d) { return height - y(d.length); })
                .style("fill", "#69b3a2")

          console.log(this.responseText);
        }
      };
    http.open('POST', 'http://localhost:5000/data/analysis', true);
    http.setRequestHeader("Content-type", "application/json");
    http.send();
}