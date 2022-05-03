//import { makeDistroChart } from './distrochart.js';
var http = new XMLHttpRequest();
let javascript_data = {};

window.addEventListener('load', function () {
    getResults();
})
let datasetCustom = [
    {period: 'preOp', SF12_MentalScore_6Months: 10.5},
    {period: '6Months', SF12_MentalScore_6Months: 12.5},
    {period: 'preOp', SF12_MentalScore_6Months: 14.5},
    {period: 'preOp', SF12_MentalScore_6Months: 15},
    {period: '6Months', SF12_MentalScore_6Months: 6},
    {period: '6Months', SF12_MentalScore_6Months: 20},
    {period: 'preOp', SF12_MentalScore_6Months: 35},
    {period: 'preOp', SF12_MentalScore_6Months: 10.5},
    {period: '6Months', SF12_MentalScore_6Months: 10.5},
    {period: 'preOp', SF12_MentalScore_6Months: 53},
    {period: '6Months', SF12_MentalScore_6Months: 44},
    {period: '6Months', SF12_MentalScore_6Months: 34},
    {period: 'preOp', SF12_MentalScore_6Months: 23},
    {period: 'preOp', SF12_MentalScore_6Months: 5},
    {period: '6Months', SF12_MentalScore_6Months: 10.5},
    {period: 'preOp', SF12_MentalScore_6Months: 14.5},
    {period: '6Months', SF12_MentalScore_6Months: 17.5},
    {period: 'preOp', SF12_MentalScore_6Months: 16.5},
    {period: '6Months', SF12_MentalScore_6Months: 15.5},
    {period: 'preOp', SF12_MentalScore_6Months: 10.5},
    {period: '6Months', SF12_MentalScore_6Months: 67},
    {period: 'preOp', SF12_MentalScore_6Months: 57},
    {period: '6Months', SF12_MentalScore_6Months: 19},
    {period: 'preOp', SF12_MentalScore_6Months: 44},
    {period: '6Months', SF12_MentalScore_6Months: 33},
    {period: 'preOp', SF12_MentalScore_6Months: 24}
]
function getResults() {
    const data = JSON.parse(localStorage.getItem('dataEl'));

    /* scatter plot */
    let margin = {top: 10, right: 30, bottom: 100, left: 100},
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    let svg = d3.select("#scatterPlot1")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    const scoreValue = localStorage.getItem('score');
    let dataViz = data[3];
    let patientData = data[0];
    let objToAnalyze = [];
    if(scoreValue == 'Phisycal'){
        objToAnalyze = dataViz.slice(0,4);
        objToAnalyze.forEach(el => {
            el.isTester = 'noF';
        })
    } else {
        objToAnalyze = dataViz.slice(5,9);
        objToAnalyze.forEach(el => {
            el.isTester = 'noM';
        })
    }
    patientData.isTester = 'yes';
    objToAnalyze.push(patientData);
//               violinPlot(data);
    // Add X axis
    var x = d3.scaleLinear()
        .domain([0, 100])
        .range([ 0, width ]);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, 100])
        .range([ height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    var color = d3.scaleOrdinal()
        .domain(["yes", "noM", "noF" ])
        .range([ "#961A3C", "#E2A525", "#046697"])
    // Add dots
    if(scoreValue == 'Phisycal'){
        svg.append('g')
            .selectAll("dot")
            .data(objToAnalyze)
            .enter()
            .append("circle")
            .attr("cx", function (d) { return x(d.age); } )
            .attr("cy", function (d) { return y(d.SF12_PhysicalScore_6months); } )
            .attr("r", 3)
            .style("fill", function (d) { return color(d.isTester) } )

    } else {
        svg.append('g')
            .selectAll("dot")
            .data(objToAnalyze)
            .enter()
            .append("circle")
            .attr("cx", function (d) { return x(d.age); } )
            .attr("cy", function (d) { return y(d.SF12_MentalScore_6months); } )
            .attr("r", 3)
            .style("fill", function (d) { return color(d.isTester) } )
    }
    violinPlots(datasetCustom, 'period', 'SF12_MentalScore_6Months');
}

function transferFailed(){
    return alert("An error occurred while transferring the file.");
}

function violinPlots(dataset, xGroup, yValue){
    /*http://bl.ocks.org/asielen/d15a4f16fa618273e10f
     woow http://bl.ocks.org/asielen/92929960988a8935d907e39e60ea8417*/
    var margin = {top: 10, right: 30, bottom: 30, left: 40},
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
    var svg = d3.select("#violinPlot1")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

// Read the data and compute summary statistics for each specie

        // Build and Show the Y scale
        var y = d3.scaleLinear()
            .domain([ 0,100 ])          // Note that here the Y scale is set manually
            .range([height, 0])
        svg.append("g").call( d3.axisLeft(y) )

        // Build and Show the X scale. It is a band scale like for a boxplot: each group has an dedicated RANGE on the axis. This range has a length of x.bandwidth
        var x = d3.scaleBand()
            .range([ 0, width ])
            .domain(["preOp", "6Months"])
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
       var sumstat = d3.nest()  // nest function allows to group the calculation per level of a factor
            .key(function(d) { return d.period;})
            .rollup(function(d) {   // For each key..
                input = d.map(function(g) { return g.SF12_MentalScore_6Months;})    // Keep the variable called Sepal_Length
                bins = histogram(input)   // And compute the binning on it.
                return(bins)
            })
            .entries(dataset);
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
         .style("fill","#C4C4C4")
         .attr("d", d3.area()
             .x0(function(d){ return(xNum(-d.length)) } )
             .x1(function(d){ return(xNum(d.length)) } )
             .y(function(d){ return(y(d.x0)) } )
             .curve(d3.curveCatmullRom)    // This makes the line smoother to give the violin appearance. Try d3.curveStep to see the difference
         )

    /* box plot in absolute

// append the svg object to the body of the page
    var svgBox = d3.select("#boxPlot1")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")"); */

        // Compute quartiles, median, inter quantile range min and max --> these info are then used to draw the box.
        var sumstatBox = d3.nest() // nest function allows to group the calculation per level of a factor
            .key(function(d) { return d.period;})
            .rollup(function(d) {
                q1 = d3.quantile(d.map(function(g) { return g.SF12_MentalScore_6Months;}).sort(d3.ascending),.25)
                median = d3.quantile(d.map(function(g) { return g.SF12_MentalScore_6Months;}).sort(d3.ascending),.5)
                patient = JSON.parse(localStorage.getItem('dataEl'))[0].SF12_PhysicalScore_6months[0]
                q3 = d3.quantile(d.map(function(g) { return g.SF12_MentalScore_6Months;}).sort(d3.ascending),.75)
                interQuantileRange = q3 - q1
                min = q1 - 1.5 * interQuantileRange
                max = q3 + 1.5 * interQuantileRange
                return({q1: q1, median: median, patient: patient, q3: q3, interQuantileRange: interQuantileRange, min: min, max: max})
            })
            .entries(dataset)

        // Show the X scale
        var x = d3.scaleBand()
            .range([ 0, width ])
            .domain(["preOp", "6Months"])
            .paddingInner(10.2)
            .paddingOuter(.52)

        // Show the Y scale
        var y = d3.scaleLinear()
            .domain([0,100])
            .range([height, 0])
    svg.append("g").call(d3.axisLeft(y))

    const createGradient = select => {
        const gradient = select
            .select('defs')
            .append('linearGradient')
            .attr('id', 'gradient')
            .attr('x1', '0%')
            .attr('y1', '100%')
            .attr('x2', '0%')
            .attr('y2', '35%');

        gradient
            .append('stop')
            .attr('offset', '35%')
            .attr('style', 'stop-color:#2CB7EA;stop-opacity:1');

        gradient
            .append('stop')
            .attr('offset', '65%')
            .attr('style', 'stop-color:#E3F4FC;stop-opacity:1');

        gradient
            .append('stop')
            .attr('offset', '100%')
            .attr('style', 'stop-color:#C02026;stop-opacity:1');
    };

    svg.append('defs');
    svg.call(createGradient);
        // Show the main vertical line
    svg
            .selectAll("vertLines")
            .data(sumstatBox)
            .enter()
            .append("line")
            .attr("x1", function(d){return(x(d.key))})
            .attr("x2", function(d){return(x(d.key))})
            .attr("y1", function(d){return(y(d.value.min))})
            .attr("y2", function(d){return(y(d.value.max))})
            .attr("stroke", "#A4A5A5")
            .style("width", 10)

        // rectangle for the main box
        var boxWidth = 20
    svg
            .selectAll("boxes")
            .data(sumstatBox)
            .enter()
            .append("rect")
            .attr("x", function(d){return(x(d.key)-boxWidth/2)})
            .attr("y", function(d){return(y(d.value.q3))})
            .attr("height", function(d){return(y(d.value.q1)-y(d.value.q3))})
            .attr("width", boxWidth )
            .attr("stroke", "white")
            .style('fill', 'url(#gradient)')

        // Show the median
    svg
            .selectAll("medianLines")
            .data(sumstatBox)
            .enter()
            .append("line")
            .attr("x1", function(d){return(x(d.key)-boxWidth/2) })
            .attr("x2", function(d){return(x(d.key)+boxWidth/2) })
            .attr("y1", function(d){return(y(d.value.median))})
            .attr("y2", function(d){return(y(d.value.median))})
            .attr("stroke", "#CFE6F3")
            .style("width", 20)

    console.log(sumstatBox)
    // Draw the whiskers at the min for this series
        svg.selectAll("indPoints")
            .data(sumstatBox)
            .enter()
            .append("line")
            .attr("x1", function(d){return(x(d.key)-boxWidth/2) })
            .attr("x2", function(d){return(x(d.key)+boxWidth/2) })
            .attr("y1", function(d){return(y(d.value.patient))})
            .attr("y2", function(d){return(y(d.value.patient))})
            .attr("stroke", "#000")
            .attr("stroke-width", 1)
            .attr("fill", "none");
}

function evalPred(type){
    let modale = document.getElementById('evalModal');
    if(!modale.classList.contains('show')){
        modale.classList.add('show');
        modale.classList.add('d-block');
    } else {
        modale.classList.remove('d-block');
        modale.classList.remove('show');
    }
}