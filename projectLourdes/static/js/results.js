var http = new XMLHttpRequest();
let javascript_data = {};

window.addEventListener('load', function () {
    getResults();
})
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
    // violinPlots(data);
}

function transferFailed(){
    return alert("An error occurred while transferring the file.");
}

function violinPlots(data){
    let violin1;
    let margin = {top: 10, right: 30, bottom: 100, left: 100},
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    let svg = d3.select("#violinPlot1")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");
    violin1 = makeDistroChart(data[1].others, 'SF12_MentalScore_6months', 'SF12_PhysicalScore_6months');
    violin1.bind("#violinPlot1",{chartSize:{height:420, width:960}, constrainExtremes:false, axisLabels: {xAxis: 'Years', yAxis: 'Values'}});
    violin1.renderViolinPlot({violinWidth:90, colors:["#555"]});
    violin1.renderBoxPlot({boxWidth:20, showOutliers:false});
}

function makeDistroChart(dataset, xGroup, yValue) {

}