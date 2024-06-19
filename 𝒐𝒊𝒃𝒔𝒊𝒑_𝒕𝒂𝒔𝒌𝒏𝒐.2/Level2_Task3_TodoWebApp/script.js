const inputField = document.getElementById("inputField");
const listContainer = document.getElementById("listContainer");

function addTask(){
    if(inputField.value === ''){
        alert("Please enter a task to add !");
    }
    else{
        let li = document.createElement("li");
        li.innerHTML = inputField.value;
        listContainer.appendChild(li);
        let span = document.createElement("span");
        span.innerHTML = "\u00d7";
        li.appendChild(span);
    }
    inputField.value = '';
    handleEmptyList();
    saveData();
}

listContainer.addEventListener("click", function(e){
    if(e.target.tagName === "LI"){
        e.target.classList.toggle("checked");
        saveData();
    }
    else if(e.target.tagName == "SPAN"){
        e.target.parentElement.remove();
        saveData();
        handleEmptyList();
    }
}, false);

function saveData(){
    localStorage.setItem("data", listContainer.innerHTML);
}

function getTask(){
    listContainer.innerHTML = localStorage.getItem("data");
}

function handleEmptyList(){
    let emptyListScreen = document.getElementById("emptyListScreen");
    let liCount = document.getElementsByTagName("LI").length;

    if(liCount === 0){
        emptyListScreen.style.display = "block";
    }  
    else if(liCount > 0){
        emptyListScreen.style.display = "none";
    }
}

getTask();
handleEmptyList();