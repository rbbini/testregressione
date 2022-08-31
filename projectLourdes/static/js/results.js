var http = new XMLHttpRequest();
let data;
let scoreValue;
let dataPreop;

window.addEventListener('load', function () {
    let dashboard = document.getElementById('results');
    dashboard.classList.remove('d-block');
    let spinner = document.getElementById('spinner');
    spinner.classList.add('d-block');
    data = JSON.parse(sessionStorage.getItem('dataEl'));
    scoreValue = JSON.parse(sessionStorage.getItem('score'));
    dataPreop = JSON.parse(sessionStorage.getItem('dataPreop'));
    createCounterfactual(data.predictionsR.counterfactual, scoreValue);
})

// crea l''interfaccia utente per la parte del controfattuale.
// bisogna passare come parametro l'array contenente gli array con i valori dei campi del controfattuale
function createCounterfactual(counterfactData, dataType) {
    if(dataType == 'Physical'){
        let isParam = document.getElementById('isPhysicalParam');
        isParam.classList.add('d-flex');
        for (let i = 0; i < 2; i++) {
            let id = "counterfact" + i;
            let p = document.getElementById(id + "p");
            let select = document.getElementById(id + "sel");

            // nome del campo controfattuale in uno dei paragrafi
            if(counterfactData.physical[i][0] == 'anni_ricovero'){
                p.innerHTML = 'Età';
                for (let j = 1; j < 10; j++) {
                    if (counterfactData.physical[i][j] > 0){
                        let opt = document.createElement('option');
                        opt.value = counterfactData.physical[i][j];
                        opt.innerHTML = Math.round(counterfactData.physical[i][j]);
                        if (j == 5) {
                            opt.selected = "selected";
                        }
                        select.appendChild(opt);
                    }
                }
            } else {
                p.innerHTML = counterfactData.physical[i][0].replace('_', " ");
                for (let j = 1; j < 10; j++) {
                    if (counterfactData.physical[i][j] > 0){
                        let opt = document.createElement('option');
                        opt.value = counterfactData.physical[i][j];
                        opt.innerHTML = counterfactData.physical[i][j].toFixed(2);
                        if (j == 5) {
                            opt.selected = "selected";
                        }
                        select.appendChild(opt);
                    }
                }
            }

        }
        newResultsP();
    } else if(dataType == 'Mental'){
        let isParam = document.getElementById('isMentalParam');
        isParam.classList.add('d-flex');
        for (let i = 5; i < 7; i++) {
            let id = "counterfact" + i;
            let p = document.getElementById(id + "p");
            let select = document.getElementById(id + "sel");

            p.innerHTML = counterfactData.mental[i-5][0].replace('_'," ");

            for (let j = 1; j < 10; j++) {
                if (counterfactData.physical[i-5][j] > 0){
                    let opt = document.createElement('option');
                    opt.value = counterfactData.mental[i-5][j];
                    opt.innerHTML = counterfactData.mental[i-5][j];
                    if (j == 5) {
                        opt.selected = "selected";
                    }
                    select.appendChild(opt);
                }
            }
        }
        newResultsM();
    } else if(dataType == 'ODI'){
        let isParam = document.getElementById('isODIParam');
        isParam.classList.add('d-flex');
        for (let i = 5; i < 7; i++) {
            let id = "counterfact" + i;
            let p = document.getElementById(id + "p");
            let select = document.getElementById(id + "sel");

            p.innerHTML = counterfactData.ODI[i-5][0].replace('_'," ");

            for (let j = 1; j < 10; j++) {
                if (counterfactData.physical[i-5][j] > 0){
                    let opt = document.createElement('option');
                    opt.value = counterfactData.ODI[i-5][j];
                    opt.innerHTML = counterfactData.ODI[i-5][j];
                    if (j == 5) {
                        opt.selected = "selected";
                    }
                    select.appendChild(opt);
                }
            }
        }
    }
}


function newResultsP() {
    const dataPrediction = data.predictionsR.predictions[1];
    const pred_len = dataPrediction.length;
    let objOfPatient;
    let p0 = document.getElementById("counterfact0p").innerHTML;
    if(p0 == 'Età'){
        p0 = 'anni_ricovero';
    }
    let select0 = document.getElementById("counterfact0sel");
    let p1 = document.getElementById("counterfact1p").innerHTML.replaceAll(' ',"_");
    let select1 = document.getElementById("counterfact1sel");


    // scorro l'attay delle predizioni controfattuali e:
    // 1) controllo che tutti i campi del controfattuale siano nell'oggetto corrente
    // 2) controllo che il valore dei campi dell'oggetto sia uguale al valore scelto dall'utente
    // se i controlli sono superati inserisco il valore della predizione nella tabella
    for (let i = 0; i < pred_len; i++){
        if (p0 in dataPrediction[i] && p1 in dataPrediction[i]
            /* && p2 in data.predictions[1][i] && p3 in data.predictions[1][i] && p4 in data.predictions[1][i] */){
            if (select0.value == dataPrediction[i][p0] && select1.value == dataPrediction[i][p1]
                /*&& select2.value == data.predictions[1][i][p2] && select3.value == data.predictions[1][i][p3] && select4.value == data.predictions[1][i][p4]*/){
                //document.getElementById("valore1tab").innerHTML = data.predictions[1][i].prediction;

                objOfPatient = {
                    predictionR_6M: dataPrediction[i].predictionR[0],
                    predictionC_6M: dataPrediction[i].predictionC[0],
                    SF12_PhysicalScore_6months: data.predictionsR.predictions[0].SF12_PhysicalScore_6months,
                    SF12_MentalScore_6months: data.predictionsR.predictions[0].SF12_MentalScore_6months,
                    physicalScore_preop: dataPrediction[i].SF12_PhysicalScore_PreOp,
                    mentalScore_preop: dataPreop.mentalScore_PreOp,
                    scoreCPreOp: data.predictionsC.physical_classif_score[0],
                    age: dataPrediction[i].anni_ricovero
                }
                clearViz();
                getResults(objOfPatient);
                // sessionStorage.setItem('physicalValPrediction', dataPrediction[i].prediction);
            }
        }
    }
}


function newResultsM() {
    //const data = JSON.parse(sessionStorage.getItem('data'));
    const dataPrediction = data.predictionsR.predictions[2];
    const pred_len = dataPrediction.length;
    let objOfPatient;

    let p0 = document.getElementById("counterfact5p").innerHTML.replaceAll(' ',"_");
    let select0 = document.getElementById("counterfact5sel");
    let p1 = document.getElementById("counterfact6p").innerHTML.replaceAll(' ',"_");
    let select1 = document.getElementById("counterfact6sel");

    // confronto il mio oggetto "stringhificato" con gli oggetti del controfattuale "stringhitifati"
    // e quando trovo una corrispondenza prendo il valore della predizione e lo metto nella tabella
    // dei risultati
    for (let i = 0; i < pred_len; i++){
        if (p0 in dataPrediction[i] && p1 in dataPrediction[i]
            /* && p2 in data.predictions[2][i] && p3 in data.predictions[2][i] && p4 in data.predictions[2][i] */){
            if (select0.value == dataPrediction[i][p0] && select1.value == dataPrediction[i][p1]
                /*&& select2.value == data.predictions[2][i][p2] && select3.value == data.predictions[2][i][p3] && select4.value == data.predictions[2][i][p4]*/){
                //document.getElementById("valore2tab").innerHTML = data.predictions[2][i].prediction;
                // sessionStorage.setItem('mentalValPrediction', dataPrediction[i].prediction);
                objOfPatient = {
                    predictionR_6M: dataPrediction[i].predictionR[0],
                    predictionC_6M: dataPrediction[i].predictionC[0],
                    SF12_PhysicalScore_6months: data.predictionsR.predictions[0].SF12_PhysicalScore_6months,
                    SF12_MentalScore_6months: data.predictionsR.predictions[0].SF12_MentalScore_6months,
                    physicalScore_preop: dataPrediction[i].SF12_PhysicalScore_PreOp,
                    mentalScore_preop: dataPrediction[i].SF12_MentalScore_PreOp,
                    scoreCPreOp: data.predictionsC.mental_classif_score[0],
                    age: data.predictionsR.predictions[0].age
                }
                clearViz();
                getResults(objOfPatient);
            }
        }
    }
}

function clearViz() {
    let scatter = document.getElementById('scatterPlot1');
    if(scatter.hasChildNodes()) {
        scatter.removeChild(scatter.children[0]);
    }
    let plotBox = document.getElementById('plotWBox');
    if(plotBox.childNodes.length > 0) {
        plotBox.removeChild(plotBox.children[0]);
    }
    let violin = document.getElementById('violinPlot1')
    if(violin.hasChildNodes()) {
        violin.removeChild(violin.children[0]);
    }
}
function getResults(patientObj) {
    let dashboard = document.getElementById('results');
    let spinner = document.getElementById('spinner');
    spinner.classList.add('d-block');
    /* scatter plot */
    let margin = {top: 10, right: 30, bottom: 100, left: 100},
        width = 400 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    let svg = d3.select("#scatterPlot1")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    /* aggiungere un controllo che fa visualizzare elementi nella tabella se zonaOp è settato a 2 (spine) o 0 e 1 (knee e hip)
    * così da gestire i dati che vengono visualizzati in tabella per i diversi tipi di classificazione
    * Volendo si può gestire la visualizzazione o meno di tabelle distinte a seconda del caso anche in relazione allo scoreValue */

    /* funzione separata per organizzare il codice */
    // controlloTabelle(zonaOp, scoreValue);
    let dataViz = data.predictionsR.similar_patients;
    let patientData = patientObj;
    let objToAnalyze = [];
    if(scoreValue == 'Physical'){
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

    // Add X axis
    var x = d3.scaleLinear()
        .domain([0, 100])
        .range([ 0, width ]);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(6));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, 100])
        .range([ height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y).ticks(6));

    var color = d3.scaleOrdinal()
        .domain(["yes", "noM", "noF" ])
        .range([ "#961A3C", "#E2A525", "#046697"])
    // Add dots
    if(scoreValue == 'Physical'){
        svg.append('g')
            .selectAll("dot")
            .data(objToAnalyze)
            .enter()
            .append("circle")
            .attr("cx", function (d) { return x(d.age); } )
            .attr("cy", function (d) { return y(d.SF12_PhysicalScore_6months); } )
            .attr("r", 3)
            .style("fill", function (d) { return color(d.isTester) } )

        svg.append("text")
            .attr("text-anchor", "start")
            .attr("x", width - 150)
            .attr("y", height + margin.top + 30)
            .text("Age");
        svg.append("text")
            .attr("text-anchor", "start")
            .attr("transform", "rotate(-90)")
            .attr("y", -margin.left+60)
            .attr("x", -margin.top - 150)
            .text("SF12 Physical Score");

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
        svg.append("text")
            .attr("text-anchor", "start")
            .attr("x", width - 150)
            .attr("y", height + margin.top + 30)
            .text("Age");
        svg.append("text")
            .attr("text-anchor", "start")
            .attr("transform", "rotate(-90)")
            .attr("y", -margin.left+60)
            .attr("x", -margin.top - 150)
            .text("SF12 Mental Score");
    }
    violinPlots(data.predictionsR.other_patients, patientData);
    plotWithBoxPlot(patientData, scoreValue);
    let barPosition = document.getElementById('valueBar');
    barPosition.style.left = 100 - patientObj.predictionC_6M * 100 + '%';
    let circlePosition = document.getElementById('circleGradient');
    circlePosition.style.backgroundPositionX = patientObj.predictionC_6M * 100 + '%';
    setTimeout(function() {
        dashboard.classList.add('d-block');
        spinner.classList.add('d-none');
    }, 3000);
}

function transferFailed(){
    return alert("An error occurred while transferring the file.");
}

function plotWithBoxPlot(dataset, scoreVAL){
    let newDataset = [];
    newDataset.push(dataset);
    let margin = {top: 10, right: 10, bottom: 40, left: 40},
        width = 350 - margin.left - margin.right,
        height = 350 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    let svg = d3.select("#plotWBox")
        .append("svg")
        .style("background-color", "transparent")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");
    // Add X axis
    var x = d3.scaleLinear()
        .domain([0, 100])
        .range([ 0, width ])
        .nice();
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(6));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, 100])
        .range([ height, 0])
        .nice();
    svg.append("g")
        .call(d3.axisLeft(y).ticks(6));


    if(scoreVAL == 'Physical') {
        svg.append('g')
            .selectAll("dot")
            .data(newDataset)
            .enter()
            .append("circle")
            .attr("cx", function (d) { return x(d.physicalScore_preop); } )
            .attr("cy", function (d) { return y(d.SF12_PhysicalScore_6months); } )
            .attr("r", 3)
            .style("fill", '#BADAE9' )

        svg.append('g')
            .selectAll("dot")
            .data(newDataset)
            .enter()
            .append('circle')
            .attr("cx", function (d) { return x(d.physicalScore_preop); } )
            .attr("cy", function (d) { return y(d.SF12_PhysicalScore_6months); } )
            .attr('r', 10)
            .attr('stroke', '#BADAE9')
            .attr('fill', 'none');

// Add the path using this helper function
        svg
            .append("g")
            .selectAll("dot")
            .data(newDataset)
            .enter()
            .append("line")
            .attr("x1", function(d){return(x(d.physicalScore_preop))})
            .attr("x2", function(d){return(x(d.physicalScore_preop))})
            .attr("y1", function(d){return(y(d.SF12_PhysicalScore_6months + 10))})
            .attr("y2", function(d){return(y(d.SF12_PhysicalScore_6months - 10))})
            .attr("stroke", "#BADAE9")
            .style("width", 1)

        svg.append("text")
            .attr("text-anchor", "start")
            .attr("x", width - 250)
            .attr("y", height + margin.top + 25)
            .text("Physical score preOp");
        svg.append("text")
            .attr("text-anchor", "start")
            .attr("transform", "rotate(-90)")
            .attr("y", -margin.left+12)
            .attr("x", -margin.top - 180)
            .text("Physical score 6 months");
    }
    if(scoreVAL == 'Mental') {
        svg.append('g')
            .selectAll("dot")
            .data(newDataset)
            .enter()
            .append("circle")
            .attr("cx", function (d) { return x(d.mentalScore_preop); } )
            .attr("cy", function (d) { return y(d.SF12_MentalScore_6months); } )
            .attr("r", 3)
            .style("fill", '#BADAE9' )

        svg.append('g')
            .selectAll("dot")
            .data(newDataset)
            .enter()
            .append('circle')
            .attr("cx", function (d) { return x(d.mentalScore_preop); } )
            .attr("cy", function (d) { return y(d.SF12_MentalScore_6months); } )
            .attr('r', 10)
            .attr('stroke', '#BADAE9')
            .attr('fill', 'none');

// Add the path using this helper function
        svg
            .append("g")
            .selectAll("dot")
            .data(newDataset)
            .enter()
            .append("line")
            .attr("x1", function(d){return(x(d.mentalScore_preop))})
            .attr("x2", function(d){return(x(d.mentalScore_preop))})
            .attr("y1", function(d){return(y(d.SF12_MentalScore_6months + 10))})
            .attr("y2", function(d){return(y(d.SF12_MentalScore_6months - 10))})
            .attr("stroke", "#BADAE9")
            .style("width", 1)

        svg.append("text")
            .attr("text-anchor", "start")
            .attr("x", width - 250)
            .attr("y", height + margin.top + 25)
            .text("Mental score preOp");
        svg.append("text")
            .attr("text-anchor", "start")
            .attr("transform", "rotate(-90)")
            .attr("y", -margin.left+12)
            .attr("x", -margin.top - 180)
            .text("Mental score 6 months");
    }
    if(scoreVAL == 'ODI') {
        svg.append("text")
            .attr("text-anchor", "start")
            .attr("x", width - 250)
            .attr("y", height + margin.top + 25)
            .text("ODI preOp");
        svg.append("text")
            .attr("text-anchor", "start")
            .attr("transform", "rotate(-90)")
            .attr("y", -margin.left+12)
            .attr("x", -margin.top - 180)
            .text("ODI 6 months");
    }
}

function violinPlots(dataset, patient){
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

        // Build and Show the Y scale
        var y = d3.scaleLinear()
            .domain([ 0,1 ])          // Note that here the Y scale is set manually
            .range([height, 0])
        svg.append("g").call( d3.axisLeft(y) )

        // Build and Show the X scale. It is a band scale like for a boxplot: each group has an dedicated RANGE on the axis. This range has a length of x.bandwidth
        var x = d3.scaleBand()
            .range([ 0, width ])
            .domain(["preOp", "6months"])
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
                input = d.map(function(g) { return g.score;})    // Keep the variable called Sepal_Length
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

        // Compute quartiles, median, inter quantile range min and max --> these info are then used to draw the box.
        var sumstatBox = d3.nest() // nest function allows to group the calculation per level of a factor
            .key(function(d) { return d.period;})
            .rollup(function(d) {
                q1 = d3.quantile(d.map(function(g) { return g.score;}).sort(d3.ascending),.25)
                median = d3.quantile(d.map(function(g) { return g.score;}).sort(d3.ascending),.5)
                patient = patient
                q3 = d3.quantile(d.map(function(g) { return g.score;}).sort(d3.ascending),.75)
                interQuantileRange = q3 - q1
                min = q1 - 1.5 * interQuantileRange
                max = q3 + 1.5 * interQuantileRange
                return({q1: q1, median: median, patient: patient, q3: q3, interQuantileRange: interQuantileRange, min: min, max: max})
            })
            .entries(dataset)

        // Show the X scale
        var x = d3.scaleBand()
            .range([ 0, width ])
            .domain(["preOp", "6months"])
            .paddingInner(10.2)
            .paddingOuter(.52)

        // Show the Y scale
        var y = d3.scaleLinear()
            .domain([0,1])
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

    // Draw the whiskers at the min for this series
        svg.selectAll("indPoints")
            .data(sumstatBox)
            .enter()
            .append("line")
            .attr("x1", function(d){return(x(d.key)-boxWidth/2) })
            .attr("x2", function(d){return(x(d.key)+boxWidth/2) })
            .attr("y1", function(d){return(y(d.value.patient.scoreCPreOp))})
            .attr("y2", function(d){return(y(d.value.patient.scoreCPreOp))})
            .attr("stroke", "#000")
            .attr("class", "lineP")
            .attr("stroke-width", 1)
            .attr("fill", "none");
    svg.selectAll("indPoints")
        .data(sumstatBox)
        .enter()
        .append("line")
        .attr("x1", function(d){return(x(d.key)-boxWidth/2) })
        .attr("x2", function(d){return(x(d.key)+boxWidth/2) })
        .attr("y1", function(d){return(y(d.value.patient.predictionC_6M))})
        .attr("y2", function(d){return(y(d.value.patient.predictionC_6M))})
        .attr("stroke", "#000")
        .attr("class", "line6")
        .attr("stroke-width", 1)
        .attr("fill", "none");
    let line_post = document.getElementsByClassName('line6');
    let line_pre = document.getElementsByClassName('lineP');
    line_post[0].classList.add('d-none');
    line_pre[1].classList.add('d-none');
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