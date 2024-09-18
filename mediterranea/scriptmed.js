filterSelection("all")
function filterSelection(c) {
  var x, i;
  x = document.getElementsByClassName("filterDiv");
  if (c == "all") c = "";
  for (i = 0; i < x.length; i++) {
    w3RemoveClass(x[i], "show");
    if (x[i].className.indexOf(c) > -1) w3AddClass(x[i], "show");
  }
}

function w3AddClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    if (arr1.indexOf(arr2[i]) == -1) {element.className += " " + arr2[i];}
  }
}

function w3RemoveClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    while (arr1.indexOf(arr2[i]) > -1) {
      arr1.splice(arr1.indexOf(arr2[i]), 1);     
    }
  }
  element.className = arr1.join(" ");
}

// Add active class to the current button (highlight it)
var btnContainer = document.getElementById("myBtnContainer");
var btns = btnContainer.getElementsByClassName("btn");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function(){
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}

// Seleziona tutti gli elementi con la classe .filterDiv
const elements = document.querySelectorAll('.filterDiv');

// Itera su ciascun elemento e applica la logica
elements.forEach((element) => {
    // Ottieni il valore dell'attributo data-event
    const eventType = element.getAttribute('data-event');

    // Cambia il colore di sfondo in base al tipo di evento
    if (eventType === 'altro') {
        element.style.backgroundColor = '#4A4E55'; // Colore originale
    } else if (eventType === 'mare') {
        element.style.backgroundColor = '#174567';  
    } else if (eventType === 'nocpr') {
        element.style.backgroundColor = '#152227'; 
    } else if (eventType === 'ucraina') {
        element.style.backgroundColor = '#3E3B9F';  
    } else if (eventType === 'ambiente') {
        element.style.backgroundColor = '#257E4D';  
    } else if (eventType === 'salute') {
        element.style.backgroundColor = '#A52A09'; 
    } else if (eventType === 'intersezione') {
        element.style.backgroundColor = '#C17300'; 
    } else if (eventType === 'palestina') {
        element.style.backgroundColor = '#1E6427'; 
    } else if (eventType === 'aril') {
        element.style.backgroundColor = '#4F0002'; 
    } else if (eventType === 'minori') {
        element.style.backgroundColor = '#76287D';
    }
});

// Seleziona tutti gli elementi con la classe .dot
const elementsdot = document.querySelectorAll('.dot');

// Itera su ciascun elemento e applica la logica
elementsdot.forEach((elementdot) => {
    // Ottieni il valore dell'attributo data-event
    const eventType = elementdot.getAttribute('data-event');

    // Cambia il colore di sfondo in base al tipo di evento
    if (eventType === 'altro') {
      elementdot.style.backgroundColor = '#4A4E55'; // Colore originale
    } else if (eventType === 'mare') {
      elementdot.style.backgroundColor = '#174567';  
    } else if (eventType === 'nocpr') {
      elementdot.style.backgroundColor = '#152227'; 
    } else if (eventType === 'ucraina') {
      elementdot.style.backgroundColor = '#3E3B9F';  
    } else if (eventType === 'ambiente') {
      elementdot.style.backgroundColor = '#257E4D';  
    } else if (eventType === 'salute') {
      elementdot.style.backgroundColor = '#A52A09'; 
    } else if (eventType === 'intersezione') {
      elementdot.style.backgroundColor = '#C17300'; 
    } else if (eventType === 'palestina') {
      elementdot.style.backgroundColor = '#1E6427'; 
    } else if (eventType === 'aril') {
      elementdot.style.backgroundColor = '#4F0002'; 
    } else if (eventType === 'minori') {
      elementdot.style.backgroundColor = '#76287D';
    }
});