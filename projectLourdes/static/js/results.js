function getResults() {
    const data = localStorage.getItem('dataEl');
    http.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var rawdata = JSON.parse(this.responseText);
            if (typeof rawdata == 'string') {
                alert(this.responseText);
                return;
            } else {
                console.log(rawdata);
                let margin = {top: 10, right: 30, bottom: 100, left: 100},
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

                const scoreValue = document.getElementById('formScore').value;
                let dataViz = Object.values(rawdata[3]);
                let patientData = rawdata[0];
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
                // // X axis: scale and draw:
                // var x = d3.scaleLinear()
                //     .domain([0, 110])
                //     .range([0, width]);
                // svg.append("g")
                //     .attr("transform", "translate(0," + height + ")")
                //     .call(d3.axisBottom(x));
                //
                // // set the parameters for the histogram
                // var histogram = d3.histogram()
                //     .value(function (d) {
                //         return d
                //     })   // I need to give the vector of value
                //     .domain(x.domain())  // then the domain of the graphic
                //     .thresholds(x.ticks(70)); // then the numbers of bins
                //
                // // And apply this function to data to get the bins
                // var bins = histogram(data);
                //
                // // Y axis: scale and draw:
                // var y = d3.scaleLinear()
                //     .range([height, 0]);
                // y.domain([0, d3.max(bins, function (d) {
                //     return d.length;
                // })]);   // d3.hist has to be called before the Y axis obviously
                // svg.append("g")
                //     .call(d3.axisLeft(y));
                //
                // // append the bar rectangles to the svg element
                // svg.selectAll("rect")
                //     .data(bins)
                //     .enter()
                //     .append("rect")
                //     .attr("x", 1)
                //     .attr("transform", function (d) {
                //         return "translate(" + x(d.x0) + "," + y(d.length) + ")";
                //     })
                //     .attr("width", function (d) {
                //         return x(d.x1) - x(d.x0) - 1;
                //     })
                //     .attr("height", function (d) {
                //         return height - y(d.length);
                //     })
                //     .style("fill", "#69b3a2")

            }

        } else {
            if(this.readyState == 4 ) {
                transferFailed();
            }
        }
    };
    http.addEventListener("error", transferFailed);
    http.open('POST', 'http://127.0.0.1:5000/data/analysis');
    http.send(data);
}

function transferFailed(){
    return alert("An error occurred while transferring the file.");
}