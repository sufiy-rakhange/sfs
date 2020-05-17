// Validations for Login
function login() {
  username = document.querySelector("#username");
  password = document.querySelector("#password");
  if (username.value.length == 0) {
    alert("Must Provide Username");
    username.focus();
    return false;
  }
  if (username.value.length < 3) {
    alert("Username Must be Atleast 3 Characters Long!!");
    username.focus();
    return false;
  }
  if (password.value.length == 0) {
    alert("Must Provide Password");
    password.focus();
    return false;
  }
  if (password.value.length < 8) {
    alert("Password Must be Atleast 8 Characters Long!!");
    password.focus();
    return false;
  }
  return true;
}

// Registration
function register() {
  firstname = document.querySelector("#firstname");
  if (firstname.value.length == 0) {
    alert("Must Provide First Name");
    password.focus();
    return false;
  }

  lastname = document.querySelector("#lastname");
  if (lastname.value.length == 0) {
    alert("Must Provide Last Name");
    password.focus();
    return false;
  }
  
  username = document.querySelector("#username");
  if (username.value.length == 0) {
    alert("Must Provide Username");
    username.focus();
    return false;
  }
  if (username.value.length < 3) {
    alert("Username Must be Atleast 3 Characters Long!!");
    username.focus();
    return false;
  }

  password = document.querySelector("#password");
  if (password.value.length == 0) {
    alert("Must Provide Password");
    password.focus();
    return false;
  }
  if (password.value.length < 8) {
    alert("Password Must be Atleast 8 Characters Long!!");
    password.focus();
    return false;
  }
  return true;
}

// To Hide And Display Questions
function show(q_id, btn_id, r_name) {
  flag = 0; // Temparory Variable
  var radios = document.getElementsByName(r_name);
  for (var i = 0; i < 6; i++) {
    // Performing operations with the checked radio value
    if (radios[i].checked) {
        // Operations for hiding buttons and displaying the Cards
        show_q = document.getElementById(q_id);
        hide_btn = document.getElementById(btn_id);
        if (q_id === "submit") {
          show_q.setAttribute("class", "mt-4 mb-3 slide");
        } else {
          show_q.setAttribute("class", "card mt-4 mb-3 slide");
        }
        hide_btn.setAttribute("class", "hide");
        flag = 1;
        // only one radio can be logically checked, don't check the rest
        break;
    }
  }
  // When the radio button is not selected
  if (flag == 0) {
    alert("You Should Make Your Choice!");
  }
}

function b(sel, bat) {
  var practical = document.getElementById('practical').value
  s = document.getElementById(sel);
  bt = document.getElementById(bat);
  if (practical == 'True') {
    s.setAttribute("class", "row mt-4");
    bt.setAttribute("class", "row mt-1");
    }
  else {
    s.setAttribute("class", "hide");
    bt.setAttribute("class", "hide");
  }
  }

// Validating the form of practical subjects for submission 
function validatePractical() {
  for ( var i=1; i <= 7; i++) {
    flag = 0; // Temparory Variable
    var radios = document.getElementsByName("option" + i);
    for (var j = 0; j < 6; j++) {
      if (radios[j].checked) {
        flag = 1;
        break;
      }
    }
    // When the form is submitted before clicking on SUBMIT
    if (flag == 0) {
      alert("Complete the Feedback!");
      return false;
    }
  }
}

function validate() {
  for ( var i=1; i <= 12; i++) {
    flag = 0; // Temparory Variable
    var radios = document.getElementsByName("option" + i);
    for (var j = 0; j < 6; j++) {
      if (radios[j].checked) {
        flag = 1;
        break;
      }
    }
    // When the form is submitted before clicking on SUBMIT
    if (flag == 0) {
      alert("Complete the Feedback!");
      return false;
    }
  }
}

// Focus on Next Button
function getFocus(btfocus) {          
  document.getElementById(btfocus).focus();
}

// Show/Hide Password
function show_hide() {
  eyeSlash = document.getElementById("pass");
  var x = document.getElementById("password");
  if (x.type == "password") {
    x.type = "text";
    eyeSlash.setAttribute("class", "fas fa-eye-slash");
  }
  else {
    x.type = "password";
    eyeSlash.setAttribute("class", "fas fa-eye");
  }
}

// Javascript for Responsive Search
function Search(input, body, mainTable, error) {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById(input);
  filter = input.value.toUpperCase();
  table = document.getElementById(body);
  tr = table.getElementsByTagName("tr");
  var flag = 1;
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    td2 = tr[i].getElementsByTagName("td")[2];
    if (td || td2) {
      txtValue = td.textContent || td.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 || txtValue2.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
        flag = 0;
      } else {
        tr[i].style.display = "none";
      }
    }
  }
  if (flag == 1) {
    var tables = document.getElementById(mainTable);
    tables.style.display = "none";
    var error = document.getElementById(error);
    error.style.display = "";
  }
  else {
    var tables = document.getElementById(mainTable);
    tables.style.display = "";
    var error = document.getElementById(error);
    error.style.display = "none";
  }
}

function loadingbar() {
  $('#pleaseWaitDialog').modal();
}

/* Information */
function list(ol, btn) {
  show_ol = document.getElementById(ol);
  hide_btn = document.getElementById(btn);
  show_ol.setAttribute("class", "more");
  hide_btn.setAttribute("class", "hide");
}

function less(ol, btn) {
  show_ol = document.getElementById(ol);
  hide_btn = document.getElementById(btn);
  show_ol.setAttribute("class", "btn btn-link");
  hide_btn.setAttribute("class", "less hide");y
}