// ========================
// MESSAGE POPUP FUNCTION
// ========================
function showMessage(message, type = "success") {
    let box = document.createElement("div");

    box.innerText = message;

    box.style.position = "fixed";
    box.style.top = "20px";
    box.style.right = "20px";
    box.style.padding = "12px 18px";
    box.style.borderRadius = "8px";
    box.style.color = "white";
    box.style.fontSize = "14px";
    box.style.zIndex = "9999";
    box.style.boxShadow = "0 4px 10px rgba(0,0,0,0.2)";
    box.style.fontFamily = "Arial";

    if (type === "success") {
        box.style.background = "#28a745";
    } else {
        box.style.background = "#dc3545";
    }

    document.body.appendChild(box);

    setTimeout(() => {
        box.remove();
    }, 3000);
}


// ========================
// REGISTER FORM HANDLER
// ========================
const registerForm = document.getElementById("registerForm");

if (registerForm) {
    registerForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        let formData = new FormData(this);

        try {
            let response = await fetch("/register/", {
                method: "POST",
                body: formData
            });

            let data = await response.json();

            if (data.status === "success") {
                showMessage("Registered Successfully ✅", "success");

                setTimeout(() => {
                    window.location.href = "/";
                }, 1200);
            } else {
                showMessage(data.message || "Registration Failed ❌", "error");
            }

        } catch (error) {
            showMessage("Server Error ❌", "error");
        }
    });
}


// ========================
// LOGIN FORM HANDLER
// ========================
const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        let formData = new FormData(this);

        try {
            let response = await fetch("/", {   // ✅ ROOT URL (correct)
                method: "POST",
                body: formData
            });

            let data = await response.json();

            if (data.status === "success") {

                if (data.role === "student") {
                    showMessage("Logged in as Student 🎓", "success");

                    setTimeout(() => {
                        window.location.href = "/student-dashboard/";
                    }, 800);
                }

                else if (data.role === "admin") {
                    showMessage("Logged in as Admin 🛠", "success");

                    setTimeout(() => {
                        window.location.href = "/admin-dashboard/";
                    }, 800);
                }

            } else {
                showMessage("Invalid credentials ❌", "error");
            }

        } catch (error) {
            console.log(error);
            showMessage("Server Error ❌", "error");
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const csrftoken = getCookie('csrftoken');

const profileForm = document.getElementById("profileForm");

if (profileForm) {
    profileForm.addEventListener("submit", async function(e){
        e.preventDefault();

        let formData = new FormData(this);

        try {
            let response = await fetch("/save-profile/", {   // ✅ FIXED
                method: "POST",
                body: formData
            });

            let data = await response.json();

            if (data.status === "success") {
                
                if (data.board === "CBSE") {
                    window.location.href = "/cbse/";
                }

                else if (data.board === "KERALA") {
                    window.location.href = "/kerala/";
                }

            } else {
                alert(data.message || "Error saving profile");
            }

        } catch (error) {
            alert("Server error");
        }
    });
}

// ========================
// DOB VALIDATION
// ========================

const dobInput = document.getElementById("dob");

if (dobInput) {

    // Prevent future dates
    let today = new Date().toISOString().split("T")[0];
    dobInput.max = today;

    dobInput.addEventListener("change", function () {

        let dob = new Date(this.value);
        let today = new Date();

        let age = today.getFullYear() - dob.getFullYear();

        let monthDiff = today.getMonth() - dob.getMonth();

        if (
            monthDiff < 0 ||
            (monthDiff === 0 && today.getDate() < dob.getDate())
        ) {
            age--;
        }

        if (age < 17) {

            showMessage("Minimum age should be 17 years ❌", "error");

            this.value = "";
        }
    });
}