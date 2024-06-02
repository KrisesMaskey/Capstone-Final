function highlight(inputs, color) {
    inputs.forEach(input => {
        if (input) {
            input.style.backgroundColor = color;
            input.style.borderRadius = '3px';
        }
    });
}

function peqHandler(e) {
    e.preventDefault();

    const peq_1 = js_vars.activity_one == false ? document.querySelector('input[name="peq_1"]:checked') : {'value': '-'};
    const peq_2 = js_vars.activity_one == false ? document.querySelector('input[name="peq_2"]:checked') : {'value': '-'};
    const peq_3 = document.getElementById('peq_age');
    const peq_4 = document.querySelector('input[name="peq_gender"]:checked');
    const peq_5 = document.querySelector('input[name="peq_3"]:checked');
    const peq_6 = document.getElementById('location');
    const peq_7 = document.querySelector('input[name="peq_5"]:checked');
    const peq_8 = document.querySelector('input[name="peq_6"]:checked');

    const age = peq_3 ? peq_3.value : '';
    const loc = peq_6 ? peq_6.value : '';

    // Get all question elements
    const allQuestions = Array.from(document.querySelectorAll('.options'));
    allQuestions.push(peq_3, peq_6);

    // Reset background color for all questions
    highlight(allQuestions, 'white');

    const invalidQuestions = [];
    if (!peq_1) invalidQuestions.push(document.querySelector('input[name="peq_1"]').closest('.options'));
    if (!peq_2) invalidQuestions.push(document.querySelector('input[name="peq_2"]').closest('.options'));
    if (!peq_4) invalidQuestions.push(document.querySelector('input[name="peq_gender"]').closest('.options'));
    if (!peq_5) invalidQuestions.push(document.querySelector('input[name="peq_3"]').closest('.options'));
    if (!peq_7) invalidQuestions.push(document.querySelector('input[name="peq_5"]').closest('.options'));
    if (!peq_8) invalidQuestions.push(document.querySelector('input[name="peq_6"]').closest('.options'));
    if (age === '') invalidQuestions.push(peq_3);
    if (loc.trim() === '') invalidQuestions.push(peq_6);

    if (invalidQuestions.length > 0) {
        alert('Please provide answers for all questions');
        console.log(invalidQuestions.length)
        highlight(invalidQuestions, '#FAA0A0');
    } else if (!/^\d+$/.test(age) || age < 1 || age > 95) {
        alert('Please enter a valid age (numbers only)');
        highlight([peq_3], '#FAA0A0');
    } else if (!/^[a-zA-Z\s]+$/.test(loc) || loc.trim().length < 3) {
        alert('Please enter a valid location (letters and spaces only)');
        highlight([peq_6], '#FAA0A0');
    } else {
        liveSend({"val": 3, "answers": [peq_1.value, peq_2.value, age, peq_4.value, peq_5.value, loc, peq_7.value, peq_8.value]});
    }
}

function liveRecv(value) {
    if (value.flag) {
        document.getElementById("invisibleButton").click();
    } 
}