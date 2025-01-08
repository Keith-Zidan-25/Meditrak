function redirectPage(choice) {
    if (choice == 'Home') document.location.href = "./";
    else if (choice == 'Doctor') document.location.href = "./doctor_list";
    else if (choice == 'Apps') document.location.href = "./";
    else if (choice == 'Medicines') document.location.href = "./medicines";
    else if (choice == 'Profile') document.location.href = "./user_login";
    else if (choice == 'Register') document.location.href = "./patient_registration";
    else if (choice == 'Information') document.location.href = "./information";
    else if (choice == 'Feedback') document.location.href = "./";
    else if (choice == 'Help') document.location.href = "./";
    else if (choice == 'Services') document.location.href = "./";
    else if (choice == 'Logout') document.location.href = "./logout"
}
function redirectPriceComparison(medicine) {
    if (medicine === 'Crocin') window.location.href = "https://pharmeasy.in/health-care/products/crocin-pain-relief-strip-of-15-tablets-171921";
    else if (medicine === 'Dolo') window.location.href = "https://pharmeasy.in/online-medicine-order/dolo-650mg-strip-of-15-tablets-44140";
    else if (medicine === 'Combiflam') window.location.href = "https://pharmeasy.in/online-medicine-order/combiflam-strip-of-20-tablets-24074";
    else if (medicine === 'Allegra') window.location.href = "https://www.netmeds.com/prescriptions/allegra-120mg-tablet-10-s";
    else if (medicine === 'Volini') window.location.href = "https://pharmeasy.in/health-care/products/volini-pain-relief-gel-tube-of-75-g-22736";
}
function validateForm() {
    var date = document.getElementById("date").value;
    var time = document.getElementById("time").value;

    if (date === "" || time === "") {
        alert("Please select both date and time.");
        return false;
    }
    return true;
}
function book_appoint(){
    const urlparams = new URLSearchParams(window.location.search);
    var doctorID = urlparams.get('doctor');
    doctorID = doctorID[4];
    document.location.href = './book_appointment?doctorID='+doctorID;
}
function applyFilter() { 
    var specialization = document.getElementById("specialization").value; 
    var experience = document.getElementById("experience").value; 
    var doctorCards = document.getElementsByClassName("doctor-card"); 
    var notFoundMessage = document.getElementById("notFoundMessage"); 
    var matchFound = false; 

    for (var i = 0; i < doctorCards.length; i++) { 
        var lowerexperience = experience.split("-")
        var doctorCard = doctorCards[i];
        var cardSpecialization = doctorCard.querySelector(".specialization").textContent.split(": ")[1]; 
        var cardExperience = doctorCard.querySelector(".experience").textContent.split(": ")[1];

        if ((specialization === "all" || cardSpecialization === specialization) && 
            (experience === "all" || cardExperience >= lowerexperience)) { 
            doctorCard.style.display = "flex";
            matchFound = true; 
        } else { 
            doctorCard.style.display = "none"; 
        } 
    }
    if (matchFound) { 
        notFoundMessage.style.display = "none"; 
    } else { 
        notFoundMessage.style.display = "block"; 
    } 
}