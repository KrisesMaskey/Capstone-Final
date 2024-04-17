function peqHandler(e){
    e.preventDefault();
    const peq_1 = js_vars.activity_one == false ? document.querySelector('input[name="peq_1"]:checked') : {'value': '-'};
    const peq_2 = js_vars.activity_one == false ? document.querySelector('input[name="peq_2"]:checked') : {'value': '-'};
    const peq_3 = document.getElementById('peq_age').value;
    const peq_4 = document.querySelector('input[name="peq_gender"]:checked');
    const peq_5 = document.querySelector('input[name="peq_3"]:checked');
    const peq_6 = document.getElementById('location').value;
    const peq_7 = document.querySelector('input[name="peq_5"]:checked');
    const peq_8 = document.querySelector('input[name="peq_6"]:checked');

    if (!(peq_1 && peq_2 && peq_8 && peq_4 && peq_5 && peq_7 && (peq_3 !== '') && (peq_6.trim() !== ''))) {
        alert('Please select answers for all questions.');
    }else{
        liveSend({"val": 3,"answers": [peq_1.value, peq_2.value, peq_3, peq_4.value, peq_5.value, peq_6, peq_7.value, peq_8.value]});
    }

}

function liveRecv(value) {
    if (value.flag) {
        document.getElementById("invisibleButton").click();
    } 
}