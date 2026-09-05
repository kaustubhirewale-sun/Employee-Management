// ==========================================
// ROLE SWITCHING
// ==========================================

const adminTab = document.getElementById("admin-tab");
const employeeTab = document.getElementById("employee-tab");
const selectedRole = document.getElementById("selected-role");
const signupLink = document.getElementById("signup-link");


// Change role
function selectRole(role) {

    if (!adminTab || !employeeTab || !selectedRole) {
        return;
    }

    if (role === "employee") {

        employeeTab.classList.add("active");
        adminTab.classList.remove("active");

        selectedRole.value = "employee";

        if (signupLink) {
            signupLink.href = "/signup?role=employee";
        }

    } else {

        adminTab.classList.add("active");
        employeeTab.classList.remove("active");

        selectedRole.value = "admin";

        if (signupLink) {
            signupLink.href = "/signup?role=admin";
        }
    }
}


// Admin button
if (adminTab) {
    adminTab.addEventListener("click", function () {
        selectRole("admin");
    });
}


// Employee button
if (employeeTab) {
    employeeTab.addEventListener("click", function () {
        selectRole("employee");
    });
}


// ==========================================
// LOAD ROLE FROM URL
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    const urlParams = new URLSearchParams(window.location.search);
    const roleFromUrl = urlParams.get("role");

    if (roleFromUrl === "employee") {
        selectRole("employee");
    } else {
        selectRole("admin");
    }

});


// ==========================================
// PASSWORD SHOW / HIDE
// ==========================================

function togglePassword(inputId, button) {

    const input = document.getElementById(inputId);

    if (!input) {
        return;
    }

    if (input.type === "password") {

        input.type = "text";
        button.textContent = "🙈";
        button.setAttribute("aria-label", "Hide password");

    } else {

        input.type = "password";
        button.textContent = "👁";
        button.setAttribute("aria-label", "Show password");
    }
}


// ==========================================
// SIGNUP PASSWORD VALIDATION
// ==========================================

const passwordInput = document.getElementById("password");
const passwordMessage = document.getElementById("password-message");

if (passwordInput && passwordMessage) {

    passwordInput.addEventListener("input", function () {

        const password = this.value;

        const hasLength = password.length >= 8;
        const hasUppercase = /[A-Z]/.test(password);
        const hasLowercase = /[a-z]/.test(password);
        const hasNumber = /[0-9]/.test(password);
        const hasSpecial = /[^A-Za-z0-9]/.test(password);

        if (password.length === 0) {

            passwordMessage.style.display = "none";
            return;
        }

        if (
            hasLength &&
            hasUppercase &&
            hasLowercase &&
            hasNumber &&
            hasSpecial
        ) {

            passwordMessage.textContent = "✓ Strong password";
            passwordMessage.className = "password-message valid";

        } else {

            passwordMessage.textContent =
                "Password must contain 8+ characters, uppercase, lowercase, number and special character.";

            passwordMessage.className = "password-message invalid";
        }

        passwordMessage.style.display = "block";
    });
}