
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
}