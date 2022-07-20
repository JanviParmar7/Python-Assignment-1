// for email
function emptyEmail() {
  var em = document.getElementById("em").value;
  var a = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,63}$/;

  if (a.test(em)) {
    document.getElementById("emailmsg").innerHTML = "";
    return true;
  }

  if (em == "") {
    document.getElementById("emailmsg").innerHTML = "Please provide an email address!";
    return false;
  } else {
    document.getElementById("emailmsg").innerHTML = "You have entered an invalid email address!";
    return false;
  }
}

//for password
function checkPassword() {
  var pw = document.getElementById("pw").value;

  //check empty password field
  if (pw == "") {
    document.getElementById("message").innerHTML = "Please provide the password!";
    return false;
  }

  //minimum password length validation
  else if (pw.length < 6) {
    document.getElementById("message").innerHTML = "Password must has at least 6 characters!";
    return false;
  }

  //maximum length of password validation
  else if (pw.length > 6) {
    document.getElementById("message").innerHTML = "Password can only contain 6 characters!";
    return false;
  } else {
    document.getElementById("message").innerHTML = "";
    return true;
  }


}
// for Confirm Password
function emptyConPassword() {
  var conPass = document.getElementById("conPass").value;

  if (conPass == "") {
    document.getElementById("cnmsg").innerHTML = "Please re-enter the password!";
    return false;
  } else {
    document.getElementById("cnmsg").innerHTML = "";
    return true;
  }
}

// for FirstName
function emptyFname() {
  var fnm = document.getElementById("fnm").value;
  var a = /^[A-Za-z]{2,25}([A-Za-z]{2,25})?$/;
  if (a.test(fnm)) {
    document.getElementById("fnmmsg").innerHTML = "";
    return true;
  }

  if (fnm == "") {
    document.getElementById("fnmmsg").innerHTML = "Please provide the first name!";
    return false;
  } else {
    document.getElementById("fnmmsg").innerHTML = "This field only contains characters!";
    return false;
  }
}

// for LastName
function emptyLname() {
  var lnm = document.getElementById("lnm").value;
  var a = /^[A-Za-z]{2,25}([A-Za-z]{2,25})?$/;
  if (a.test(lnm)) {
    document.getElementById("lnmmsg").innerHTML = "";
    return true;
  }
  if (lnm == "") {
    document.getElementById("lnmmsg").innerHTML = "Please provide the last name!";
    return false;
  } else {
    document.getElementById("lnmmsg").innerHTML = "This field only contains characters!";
    return false;
  }
}

// for Username
function emptyUname() {
  var unm = document.getElementById("unm").value;
  var a = /^[A-Za-z][A-Za-z0-9_]{4,29}$/;
  if (a.test(unm)) {
    document.getElementById("unmmsg").innerHTML = "";
    return true;
  }
  if (unm == "") {
    document.getElementById("unmmsg").innerHTML = "Please provide the username!";
    return false;
  } else {
    document.getElementById("unmmsg").innerHTML = "Please enter valid username!";
    return false;
  }
}

// for Address
function emptyAddress() {
  var add = document.getElementById("add").value;

  if (add == "") {
    document.getElementById("addmsg").innerHTML = "Please provide your address!";
    return false;
  } else {
    document.getElementById("addmsg").innerHTML = "";
    return true;
  }
}

// for City
function emptyCity() {
  var ct = document.getElementById("ct").value;
  if (ct == "") {
    document.getElementById("ctmsg").innerHTML = "Please provide your city name!";
    return false;
  } else {
    document.getElementById("ctmsg").innerHTML = "";
    return true;
  }
}


// for State
function emptyState() {
  var st = document.getElementById("st").value;
  if (st == "") {
    document.getElementById("stmsg").innerHTML = "Please provide your state name!";
    return false;
  } else {
    document.getElementById("stmsg").innerHTML = "";
    return true;
  }
}

//for mobile number
function CheckMobileNumber() {
  var mob = document.getElementById("mo_no").value;
  var a = /^[6789]\d{9}$/;
  if (a.test(mob)) {
    document.getElementById("msg").innerHTML = "";
    return true;
  }
  if (mob == "") {
    document.getElementById("msg").innerHTML = "Please provide your mobile number!";
    return false;
  }
  if (mob.length < 10) {
    document.getElementById("msg").innerHTML = "Mobile number must has 10 digits!";
    return false;
  }
  if (mob.length > 10) {
    document.getElementById("msg").innerHTML = "Mobile number can only contain 10 digits!";
    return false;
  } else {
    document.getElementById("msg").innerHTML = "Please enter valid mobile number!";
    return false;
  }
}

//for DOB
function underAgeValidate() {

  var userinput = document.getElementById("db").value;
  var dob = new Date(userinput);
  if (userinput == null || userinput == '') {
    document.getElementById("bdate").innerHTML = "Choose a date please!";
    return false;
  } else {
    //calculate month difference from current date in time
    var month_diff = Date.now() - dob.getTime();

    //convert the calculated difference in date format
    var age_dt = new Date(month_diff);

    //extract year from date
    var year = age_dt.getUTCFullYear();

    //now calculate the age of the user
    var age = Math.abs(year - 1970);
    //display the calculated age
    if (age < 18) {
      document.getElementById("bdate").innerHTML = "Age should be more than 18 years. please enter a valid date of birth";
      return false;
    }
    if (age > 50) {
      document.getElementById("bdate").innerHTML = "Age should be less than 50 years. please enter a valid date of birth";
      return false;
    } else {
      document.getElementById("bdate").innerHTML = "";
      return true;
    }

  }
}

//for zipcode
function isZipCode() {
  var zcode = document.getElementById("zcode1").value;
  var a = /^[0-9]{6}$/;
  if (a.test(zcode)) {
    return true;
  }
  if (zcode == "") {
    document.getElementById("zip").innerHTML = "Provide the zipcode please!";
    return false;
  }
  if (zcode.length < 6) {
    document.getElementById("zip").innerHTML = "Zipcode must has 6 digits!";
    return false;
  }
  if (zcode.length > 6) {
    document.getElementById("zip").innerHTML = "Zipcode can only contain 6 digits!";
    return false;
  } else {
    document.getElementById("zip").innerHTML = "Please enter valid zipcode! ";
    return false;
  }
}

//for gender
var male = document.getElementById("m");
var female = document.getElementById("f");
var checked = document.getElementById("sel").innerHTML;

if (checked == "male") {
  male.click()
} else if (checked == "female") {
  female.click()
} else {}


function fileValidation() {
  var fileInput =
    document.getElementById('pdf');

  var filePath = fileInput.value;

  // Allowing file type
  var allowedExtensions = /(\.pdf)$/i;
  if (filePath == "") {
    document.getElementById("filemsg").innerHTML = "Please provide your birth-certificate!";
    return false;
  }
  if (!allowedExtensions.exec(filePath)) {
    document.getElementById("filemsg").innerHTML = "Invalid file format!";
    fileInput.value = '';
    return false;
  }
  if (fileInput.files[0].size >= 20971520) {
    document.getElementById("filemsg").innerHTML = "File size should be less than or Equal to 20 MB";
  } else {
    document.getElementById("filemsg").innerHTML = "";
    return true;
  }

}

function photoValidation() {
  var fileInput = document.getElementById('file');
  var filePath = fileInput.value;
  var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
  if (filePath == "") {
    document.getElementById("photomsg").innerHTML = "Please provide your profile photo";
    return false;
  }
  if (!allowedExtensions.exec(filePath)) {
    document.getElementById("photomsg").innerHTML = "Invalid file format";
    fileInput.value = '';
    return false;
  } else {
    document.getElementById("photomsg").innerHTML = "";
    return true;
  }

}