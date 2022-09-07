/* 
 * il json ha come primo elemento un oggetto con i campi del controfattuale. Questi campi sono degli array contenenti il valore originale e tutti i valori
 * modificati (+0.5, +0.4, ..., -0.5). Questo oggetto serve per mettere i dati nei drop-down menu pi� comodamente
 */

var http = new XMLHttpRequest();



// crea l''interfaccia utente per la parte del controfattuale.
// bisogna passare come parametro l'array contenente gli array con i valori dei campi del controfattuale
function createCounterfactual(counterfactData) {
    document.getElementById("score_type").innerHTML = "controfattuale per lo score fisico";

    for (let i = 0; i < 2; i++) {
        let id = "counterfact" + i;
        let p = document.getElementById(id + "p");
        let select = document.getElementById(id + "sel");

        // nome del campo controfattuale in uno dei paragrafi
        p.innerHTML = counterfactData.physical[i][0];

        for (let j = 1; j < 10; j++) {
            let opt = document.createElement('option');
            opt.value = counterfactData.physical[i][j];
            opt.innerHTML = counterfactData.physical[i][j];
            if (j == 5) {
                opt.selected = "selected";
            }
            select.appendChild(opt);
        }
    }

    if ("mental" in counterfactData){
        document.getElementById("score_type2").innerHTML = "controfattuale per lo score mentale";
        for (let i = 5; i < 7; i++) {
            let id = "counterfact" + i;
            let p = document.getElementById(id + "p");
            let select = document.getElementById(id + "sel");

            p.innerHTML = counterfactData.mental[i-5][0];

            for (let j = 1; j < 10; j++) {
                let opt = document.createElement('option');
                opt.value = counterfactData.mental[i-5][j];
                opt.innerHTML = counterfactData.mental[i-5][j];
                if (j == 5) {
                    opt.selected = "selected";
                }
                select.appendChild(opt);
            }
        }
    } else if ("ODI" in counterfactData) {
        document.getElementById("score_type2").innerHTML = "controfattuale per lo score ODI";
        for (let i = 5; i < 7; i++) {
            let id = "counterfact" + i;
            let p = document.getElementById(id + "p");
            let select = document.getElementById(id + "sel");

            p.innerHTML = counterfactData.ODI[i-5][0];

            for (let j = 1; j < 10; j++) {
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



function newResultsP(data) {
    //const data = JSON.parse(sessionStorage.getItem('data'));
    const pred_len = data.predictions[1].length;

    let p0 = document.getElementById("counterfact0p").innerHTML;
    let select0 = document.getElementById("counterfact0sel");
    let p1 = document.getElementById("counterfact1p").innerHTML;
    let select1 = document.getElementById("counterfact1sel");
    // commentato per test
    /*
    let p2 = document.getElementById("counterfact2p").innerHTML;
    let select2 = document.getElementById("counterfact2sel");
    let p3 = document.getElementById("counterfact3p").innerHTML;
    let select3 = document.getElementById("counterfact3sel");
    let p4 = document.getElementById("counterfact4p").innerHTML;
    let select4 = document.getElementById("counterfact4sel");
    */

        
    // scorro l'attay delle predizioni controfattuali e:
    // 1) controllo che tutti i campi del controfattuale siano nell'oggetto corrente
    // 2) controllo che il valore dei campi dell'oggetto sia uguale al valore scelto dall'utente
    // se i controlli sono superati inserisco il valore della predizione nella tabella 
    for (let i = 0; i < pred_len; i++){
        if (p0 in data.predictions[1][i] && p1 in data.predictions[1][i]
        /* && p2 in data.predictions[1][i] && p3 in data.predictions[1][i] && p4 in data.predictions[1][i] */){
            if (select0.value == data.predictions[1][i][p0] && select1.value == data.predictions[1][i][p1] 
            /*&& select2.value == data.predictions[1][i][p2] && select3.value == data.predictions[1][i][p3] && select4.value == data.predictions[1][i][p4]*/){
                document.getElementById("valore1tab").innerHTML = data.predictions[1][i].prediction;
            }
        }
    }
}


function newResultsM(data) {
    //const data = JSON.parse(sessionStorage.getItem('data'));
    const pred_len = data.predictions[2].length;

    let p0 = document.getElementById("counterfact5p").innerHTML;
    let select0 = document.getElementById("counterfact5sel");
    let p1 = document.getElementById("counterfact6p").innerHTML;
    let select1 = document.getElementById("counterfact6sel");
    /*
    let p2 = document.getElementById("counterfact7p").innerHTML;
    let select2 = document.getElementById("counterfact7sel");
    let p3 = document.getElementById("counterfact8p").innerHTML;
    let select3 = document.getElementById("counterfact8sel");
    let p4 = document.getElementById("counterfact9p").innerHTML;
    let select4 = document.getElementById("counterfact9sel");
    */

        
    // confronto il mio oggetto "stringhificato" con gli oggetti del controfattuale "stringhitifati" 
    // e quando trovo una corrispondenza prendo il valore della predizione e lo metto nella tabella
    // dei risultati
    for (let i = 0; i < pred_len; i++){
        if (p0 in data.predictions[2][i] && p1 in data.predictions[2][i]
        /* && p2 in data.predictions[2][i] && p3 in data.predictions[2][i] && p4 in data.predictions[2][i] */){
            if (select0.value == data.predictions[2][i][p0] && select1.value == data.predictions[2][i][p1] 
            /*&& select2.value == data.predictions[2][i][p2] && select3.value == data.predictions[2][i][p3] && select4.value == data.predictions[2][i][p4]*/){
                document.getElementById("valore2tab").innerHTML = data.predictions[2][i].prediction;
            }
        }
    }
}


/*
http.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var rawdata = JSON.parse(this.responseText);
        if (typeof rawdata == 'string') {
            alert(this.responseText);
            return;
        } else {
            sessionStorage.setItem('data', JSON.stringify(rawdata));
            createCounterfactual(rawdata.counterfactual);
        }
    } else {
        if(this.readyState == 4 ) {
            transferFailed();
        }
    }
}
*/