var http = new XMLHttpRequest();
let javascript_data = {};
let valid = false;
const dataStructAnca = [
    'score',
    'sesso',
    'anni_ricovero',
    'classe_asa',
    'VAS_Total_PreOp',
    'BMI_altezza_PreOp',
    'BMI_peso_PreOp',
    'SF12_autovalsalute_risp_0',
    'SF12_scale_risp_0',
    'SF12_ultimomeseresa_risp_0',
    'SF12_ultimomeselimite_risp_0',
    'SF12_ultimomeseemo_risp_0',
    'SF12_ultimomeseostacolo_risp_0',
    'SF12_ultimomesesereno_risp_0',
    'SF12_ultimomeseenergia_risp_0',
    'SF12_ultimomesetriste_risp_0',
    'SF12_ultimomesesociale_risp_0',
    'zona_operazione'

];

const dataStructSpine = [
    'score',
    'nome_operazione',
    'sesso',
    'anni_ricovero',
    'ODI_Total_PreOp',
    'Vas_Back_PreOp',
    'Vas_Leg_PreOp',
    'SF36_GeneralHealth_PreOp',
    'SF36_PhysicalFunctioning_PreOp',
    'SF36_RoleLimitPhysical_PreOp',
    'SF36_RoleLimitEmotional_PreOp',
    'SF36_SocialFunctioning_PreOp',
    'SF36_Pain_PreOp',
    'SF36_EnergyFatigue_PreOp',
    'SF36_EmotionalWellBeing_PreOp',
    'SF36_MentalScore_PreOp',
    'SF36_PhysicalScore_PreOp',
    'FABQ_Work_PreOp',
    'classe_asa_1',
    'MORBIDITY'
];

document.addEventListener('DOMContentLoaded', function() {
    controlProcedure();
}, false);

function goToNextStep(step) {
    const formData = document.getElementById('step' + step).elements;
    const next = Number(step) + 1;
    if(next < 4){
        const nextStep = document.getElementById('step' + next);
        nextStep.classList.add('d-block');
        const nextBtn = document.getElementById('btnStep' + next);
        nextBtn.classList.add('activeBtn');
        const nextLinea = document.getElementById('goStep' + next);
        nextLinea.classList.add('lineActive');
        if(step < 3){
            const hideNext = document.getElementById('clicked' + step);
            hideNext.classList.add('d-none');
        }
    }
}

function controlProcedure(){
    const procedureValue = document.getElementById('zona_operazione').value;
    let scoreSelect = document.getElementById('score');
    if(scoreSelect.options.length > 2){
        scoreSelect.remove(2);
    }
    if(procedureValue == 2){
        let opt = document.createElement('option');
        opt.value = 'ODI';
        opt.innerHTML = 'ODI';
        scoreSelect.appendChild(opt);
        for (let i=1; i<6; i++) {
            document.getElementById('isSpine' + i).classList.remove('d-none');
        }
        for (let i=1; i<5; i++) {
            document.getElementById('isAnca' + i).classList.add('d-none');
        }
    } else {
        let opt = document.createElement('option');
        opt.value = 'Mental';
        opt.innerHTML = 'Mental';
        scoreSelect.appendChild(opt);
        for (let i=1; i<6; i++) {
            document.getElementById('isSpine' + i).classList.add('d-none');
        }
        for (let i=1; i<5; i++) {
            document.getElementById('isAnca' + i).classList.remove('d-none');
        }
    }
}

const objFormSource = document.getElementById("objSource");
objFormSource.addEventListener('change', function (e) {
    const sourceValue = document.querySelector('input[name="dataSource"]:checked').value;
    if (sourceValue == 'manually') {
        const manualStep = document.getElementById('manuallyForm');
        manualStep.classList.add('d-block');
        const otherStep = document.getElementById('episodeForm');
        if (otherStep.classList.contains('d-block')) {
            otherStep.classList.remove('d-block');
        }

    } else if (sourceValue == 'patientEpisode') {
        const episodeStep = document.getElementById('episodeForm');
        episodeStep.classList.add('d-block');
        const otherStep = document.getElementById('manuallyForm');
        if (otherStep.classList.contains('d-block')) {
            otherStep.classList.remove('d-block');
        }
    }
});

const showError = (input, message) => {
    // get the form-field element
    const formField = input.parentElement;
    // add the error class
    formField.classList.remove('success');
    formField.classList.add('error');

    // show the error message
    const error = formField.querySelector('small');
    error.textContent = message;
};

const showSuccess = (input) => {
    // get the form-field element
    const formField = input.parentElement;

    // remove the error class
    formField.classList.remove('error');
    formField.classList.add('success');

    // hide the error message
    const error = formField.querySelector('small');
    error.textContent = '';
}

function validateForm(x){
    if (x == "") {
        // alert("Name must be filled out");
        return false;
    } else{
        return true;
    }
}

function goToResults() {
    const form = document.getElementById('formSteps');
    const data = new FormData(form);
    const procedureValue = document.getElementById('zona_operazione').value;
    if(procedureValue == 2){
        for (let i= 0; i < dataStructSpine.length; i++){
            const inputEl = document.querySelector('#' + dataStructSpine[i]);
            let x = document.forms["formSteps"][dataStructSpine[i]].value;
            if(validateForm(x)) {
                valid = true;
            }
        };
    } else  {
        for (let i= 0; i < dataStructAnca.length; i++){
            const inputEl = document.querySelector('#' + dataStructAnca[i]);
            let x = document.forms["formSteps"][dataStructAnca[i]].value;
            if(validateForm(x)) {
                valid = true;
            }
        };
    }
    if(valid) {
        getRequest(data);
    } else {
        alert('check the values of fields');
    }
}

function transferFailed(){
    return alert("An error occurred while transferring the file.");
}

function getRequest(data){
    http.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var rawdata = JSON.parse(this.responseText);
            if (typeof rawdata == 'string') {
                alert(this.responseText);
                return;
            } else {
                sessionStorage.setItem('dataEl', JSON.stringify(rawdata));
                sessionStorage.setItem('score',JSON.stringify(document.getElementById('score').value))
                window.location.href = 'results';
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
function setbmi(){
    let resultBMI = 0;
    const weight = parseInt(document.getElementById("bmi_peso_preOp").value);
    const height = parseInt(document.getElementById("bmi_altezza_preOp").value);
    if(weight && height){
        resultBMI = (weight / Math.pow( (height/100), 2 )).toFixed(1);
        document.getElementById("bmi_total_preOp").setAttribute('value', resultBMI);
    }
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
        .domain([3.5, 8])          // Note that here the Y scale is set manually
        .range([height, 0])
    svg.append("g").call(d3.axisLeft(y))

    // Build and Show the X scale. It is a band scale like for a boxplot: each group has an dedicated RANGE on the axis. This range has a length of x.bandwidth
    var x = d3.scaleBand()
        .range([0, 30])
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
    var sumstat = d3.rollup(data.value, function (d) {   // For each key..
        input = d.map(function (g) {
            return g.Sepal_Length;
        })    // Keep the variable called Sepal_Length
        bins = histogram(input)   // And compute the binning on it.
        return (bins)
    });
    var sumstat = d3.group().key(function (d) {
        return d.key;
    })
        .rollup(function (d) {   // For each key..
            input = d.map(function (g) {
                return g.Sepal_Length;
            })    // Keep the variable called Sepal_Length
            bins = histogram(input)   // And compute the binning on it.
            return (bins)
        })
        .entries(data)

    // What is the biggest number of value in a bin? We need it cause this value will have a width of 100% of the bandwidth.
    var maxNum = 0
    for (i in sumstat) {
        allBins = sumstat[i].value
        lengths = allBins.map(function (a) {
            return a.length;
        })
        longuest = d3.max(lengths)
        if (longuest > maxNum) {
            maxNum = longuest
        }
    }

    // The maximum width of a violin must be x.bandwidth = the width dedicated to a group
    var xNum = d3.scaleLinear()
        .range([0, x.bandwidth()])
        .domain([-maxNum, maxNum])

    // Add the shape to this svg!
    svg
        .selectAll("myViolin")
        .data(sumstat)
        .enter()        // So now we are working group per group
        .append("g")
        .attr("transform", function (d) {
            return ("translate(" + x(d.key) + " ,0)")
        }) // Translation on the right to be at the group position
        .append("path")
        .datum(function (d) {
            return (d.value)
        })     // So now we are working bin per bin
        .style("stroke", "none")
        .style("fill", "#69b3a2")
        .attr("d", d3.area()
            .x0(function (d) {
                return (xNum(-d.length))
            })
            .x1(function (d) {
                return (xNum(d.length))
            })
            .y(function (d) {
                return (y(d.x0))
            })
            .curve(d3.curveCatmullRom)    // This makes the line smoother to give the violin appearance. Try d3.curveStep to see the difference
        )
}