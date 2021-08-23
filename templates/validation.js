function CheckFirstname() {
    const firstname = document.getElementById("firstname").value;
    const nameExp = /^[A-Za-z]+$/;
    if (!firstname.match(nameExp)) {
        document.getElementById("checkfirstname").innerHTML = "Please enter valid name.";
        document.getElementById("firstname").focus();
        return false;
    } else {
        document.getElementById("checkfirstname").innerHTML = "";
        return true;
    }
}

function CheckLastname() {
    const lastname = document.getElementById("lastname").value;
    const nameExp = /^[A-Za-z]+$/;
    if (!lastname.match(nameExp)) {
        document.getElementById("checklastname").innerHTML = "Please enter valid name.";
        document.getElementById("lastname").focus();
        return false;
    } else {
        document.getElementById("checklastname").innerHTML = "";
        return true;
    }
}

function CheckPhonenumber() {
    const phone = document.getElementById("phone").value;
    const phoneExp = /^[0-9]+$/;
    if (!phone.match(phoneExp) || phone.length !== 10) {
        document.getElementById("checkphonenumber").innerHTML = "Please enter valid phone number.";
        document.getElementById("phone").focus();
        return false;
    } else {
        document.getElementById("checkphonenumber").innerHTML = "";
        return true;
    }
}

function CheckEmail() {
    const email = document.getElementById("email").value;
    if (email.indexOf("@") === -1 || email.indexOf(".") === -1) {
        document.getElementById("checkemail").innerHTML = "Please enter valid email address.";
        document.getElementById("email").focus();
        return false;
    } else {
        document.getElementById("checkemail").innerHTML = "";
        return true;
    }
}

function CheckZipcode() {
    const zipcode = document.getElementById("zipcode").value;
    const phoneExp = /^[0-9]+$/;
    if (zipcode.length !== 5 || !zipcode.match(phoneExp)) {
        document.getElementById("checkzipcode").innerHTML = "Please enter valid zipcode.";
        document.getElementById("zipcode").focus();
        return false;
    } else {
        document.getElementById("checkzipcode").innerHTML = "";
        return true;
    }
}

function CheckDistance() {
    const distance = document.getElementById("distance").value;
    const phoneExp = /^[0-9]+$/;
    if (distance <= 0 || !distance.match(phoneExp)) {
        document.getElementById("checkdistance").innerHTML = "Value should be greater than 0.";
        document.getElementById("distance").focus();
        return false;
    } else {
        document.getElementById("checkdistance").innerHTML = "";
        return true;
    }
}

function CheckDay() {
    const days = ['day0', 'day1', 'day2', 'day3', 'day4']
    for (const day of days) {
        if (document.getElementById(day).checked) {
            document.getElementById("checkday").innerHTML = "";
            return true;
        }
    }
    document.getElementById("checkday").innerHTML = "Please select at least one day.";
    document.getElementById("day").focus();
    return false;
}

function CheckDate() {
    const dateafter = document.getElementById("dateafter").value;
    const datebefore = document.getElementById("datebefore").value;
    if (dateafter >= datebefore) {
        document.getElementById("checkdate").innerHTML = "Please select valid dates.";
        return false;
    } else {
        document.getElementById("checkdate").innerHTML = "";
        return true;
    }
}

function CheckTime() {
    for (let time = 0; time <= 9; time++) {
        if (document.getElementById(time).checked) {
            document.getElementById("checktime").innerHTML = "";
            return true;
        }
    }
    document.getElementById("checktime").innerHTML = "Please select at least one time.";
    return false;
}

function FormCheck() {
    return (CheckFirstname() && CheckLastname() && CheckPhonenumber() && CheckEmail() && CheckZipcode() && CheckDistance() && CheckDay() && CheckDate() && CheckTime());
}

