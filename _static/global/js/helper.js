let index = 0;

function move(e, n) {
    e.preventDefault();
    let tabs = document.getElementById('navbar').children;
    let contents = document.getElementsByClassName('tab-content');
    // Remove the 'active' class from the current tab content
    contents[index].classList.remove('active');
    index += n;
    if (index >= tabs.length) {
        index = 0;
    } else if (index < 0) {
        index = tabs.length - 1;
    }
    let tab = tabs[index].children[0];
    window.location.hash = tab.getAttribute('href');
    // Add the 'active' class to the new tab content
    contents[index].classList.add('active');
}

function idHandler(e){
    let inputbox = document.getElementById('MturkID');

    if(inputbox.value == ""){
        alert("ID cannot be blank!");
        e.preventDefault();
    }else{
        liveSend({"type":"MTurk-ID", "id": inputbox.value})
    }    
}

function liveRecv(value) {
    if (value.flag) {
        document.getElementById("invisibleButton").click();
    } 
    else{

        if(value.cnt == 1){
            document.getElementById("quiz_failed_once").style.display = 'block';
            move(event, 1);
        }

        else if(value.cnt > 1){
            document.getElementById("quiz_failed_once").style.display = 'none';
            document.getElementById("invisibleButton").click();
        }
    }
}