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
const radioButtons = document.querySelector('input[name="dataSource"]');
radioButtons.addEventListener('change',function(e){
    if(this.checked){
        if(this.value == 'manually'){
            const manualStep = document.getElementById('manuallyForm');
            manualStep.classList.add('visible');
            const otherStep = document.getElementById('episodeForm');
            if(otherStep.classList.contains('visible')){
                otherStep.classList.remove('visible');
            }

        } else if (this.value == 'patientEpisode'){
            const episodeStep = document.getElementById('episodeForm');
            episodeStep.classList.add('visible');
            const otherStep = document.getElementById('manuallyForm');
            if(otherStep.classList.contains('visible')){
                otherStep.classList.remove('visible');
            }
        }
    }
});
function goToResults() {
//    const formData = document.getElementById('step1').elements;
//    for(var i = 0 ; i < formData.length ; i++){
//        var item = formData.item(i);
//        obj[item.name] = item.value;
//    }
//    const hideStep = document.getElementById('step1');
//        hideStep.classList.add('hidden');
    /* passare obj se serve prendere l'oggetto che viene generato dal form per passarlo al backend
        {
            dataSource: "patientEpisode"
            flexRadioDefault: "on"
            patientEpisode: "1"
            procedure: "Anca"
            score: "Phisycal"
            step: "6"
        }
    */
    http.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        if(typeof this.responseText == 'string'){
            alert(this.responseText);
            return;
        } else {
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
//               violinPlot(data);

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

        }

        }
      };
    http.open('POST', 'http://127.0.0.1:5000/data/analysis', true);
    http.setRequestHeader("Content-type", "application/json");
    http.send();
}

function violinPlot(data) {

    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 40},
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#my_dataviz2")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    // Read the data and compute summary statistics for each specie

      // Build and Show the Y scale
      var y = d3.scaleLinear()
        .domain([ 3.5,8 ])          // Note that here the Y scale is set manually
        .range([height, 0])
      svg.append("g").call( d3.axisLeft(y) )

      // Build and Show the X scale. It is a band scale like for a boxplot: each group has an dedicated RANGE on the axis. This range has a length of x.bandwidth
      var x = d3.scaleBand()
        .range([ 0, 30 ])
        .domain(["prova"])
        .padding(0.05)     // This is important: it is the space between 2 groups. 0 means no padding. 1 is the maximum.
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))

      // Features of the histogram
      var histogram = d3.histogram()
            .domain(y.domain())
            .thresholds(y.ticks(20))    // Important: how many bins approx are going to be made? It is the 'resolution' of the violin plot
            .value(d => d)

      // Compute the binning for each group of the dataset
      var sumstat = d3.rollup(data.value, function(d) {   // For each key..
            input = d.map(function(g) { return g.Sepal_Length;})    // Keep the variable called Sepal_Length
            bins = histogram(input)   // And compute the binning on it.
            return(bins)
          });
      var sumstat = d3.group().key(function(d) { return d.key;})
        .rollup(function(d) {   // For each key..
          input = d.map(function(g) { return g.Sepal_Length;})    // Keep the variable called Sepal_Length
          bins = histogram(input)   // And compute the binning on it.
          return(bins)
        })
        .entries(data)

      // What is the biggest number of value in a bin? We need it cause this value will have a width of 100% of the bandwidth.
      var maxNum = 0
      for ( i in sumstat ){
        allBins = sumstat[i].value
        lengths = allBins.map(function(a){return a.length;})
        longuest = d3.max(lengths)
        if (longuest > maxNum) { maxNum = longuest }
      }

      // The maximum width of a violin must be x.bandwidth = the width dedicated to a group
      var xNum = d3.scaleLinear()
        .range([0, x.bandwidth()])
        .domain([-maxNum,maxNum])

      // Add the shape to this svg!
      svg
        .selectAll("myViolin")
        .data(sumstat)
        .enter()        // So now we are working group per group
        .append("g")
          .attr("transform", function(d){ return("translate(" + x(d.key) +" ,0)") } ) // Translation on the right to be at the group position
        .append("path")
            .datum(function(d){ return(d.value)})     // So now we are working bin per bin
            .style("stroke", "none")
            .style("fill","#69b3a2")
            .attr("d", d3.area()
                .x0(function(d){ return(xNum(-d.length)) } )
                .x1(function(d){ return(xNum(d.length)) } )
                .y(function(d){ return(y(d.x0)) } )
                .curve(d3.curveCatmullRom)    // This makes the line smoother to give the violin appearance. Try d3.curveStep to see the difference
            )
}