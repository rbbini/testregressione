var http = new XMLHttpRequest();
let javascript_data = {};
let valid = false;
const dataStructAnca = [
    'score',
    'sesso',
    'anni_ricovero',
    'classe_asa',
    'VAS_Total_PreOp',
    'bmi_altezza_preOp',
    'bmi_peso_preOp',
    'physicalScore',
    'mentalScore',
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
    controlProcedure(true);
    let dashboard = document.getElementById('indexEl');
    dashboard.classList.remove('d-none');
    let spinner = document.getElementById('spinner');
    spinner.classList.add('d-none');
}, false);

function goToNextStep(step) {
    // const formData = document.getElementById('step' + step).elements;
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

function controlProcedure(isStart = false){
    const procedureValue = document.getElementById('zona_operazione').value;
    sessionStorage.setItem('zona_operazione', procedureValue);
    if(!isStart){
        goToNextStep(1);
    }
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
    input.classList.remove('is-valid');
    input.classList.add('is-invalid');

    // show the error message
    const error = formField.querySelector('small');
    error.textContent = message;
};

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
    valid = true;
    if(procedureValue == 2){
        for (let i= 0; i < dataStructSpine.length; i++){
            const inputEl = document.querySelector('#' + dataStructSpine[i]);
            let x = document.forms["formSteps"][dataStructSpine[i]].value;
            if(!validateForm(x)) {
                showError(inputEl, 'check the values of fields');
                valid = false;
            }
        };
    } else  {
        for (let i= 0; i < dataStructAnca.length; i++){
            const inputEl = document.querySelector('#' + dataStructAnca[i]);
            let x = document.forms["formSteps"][dataStructAnca[i]].value;
            if(!validateForm(x)) {
                showError(inputEl, 'check the values of fields');
                valid = false;
            }
        };
    }
    if(valid) {
        if(procedureValue == 2) {
            const operazioneTrue = document.getElementById('nome_operazione').value;
            const arrayOperazione = ['Artrodesi_Cervicale', 'Artrodesi_Lombare', 'Cifoplastiche', 'Decompressione_Lombare', 'Deformita_Degenerativa', 'Deformita_Idiopatica', 'Ernia_Cervicale',
                'Ernia_Lombare', 'Tumore_Vertebrale'];
            for (var i = 0; i < arrayOperazione.length; i++) {
                data.append(arrayOperazione[i], 0);
            }
            data.set(operazioneTrue, 1);
        }
        getRequest(data);
    } else {
        transferFailed();
    }
}

function transferFailed(){
    return alert("An error occurred while transferring the file.");
}

function getRequest(data){
    let dashboard = document.getElementById('indexEl');
    dashboard.classList.add('d-none');
    let spinner = document.getElementById('spinner');
    spinner.classList.add('d-flex');
    spinner.classList.remove('d-none');
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
                if(!valid){
                    showError(form, 'check the values of fields');
                } else {
                    transferFailed();
                }
            }
        }
    };
    http.addEventListener("error", transferFailed);
    http.open('POST', '/data/analysis');
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