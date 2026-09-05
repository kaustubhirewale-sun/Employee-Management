
const searchInput = document.getElementById("employeeSearch");
const results = document.getElementById("searchResults");
const employeeId = document.getElementById("employeeId");

results.style.display = "none";

searchInput.addEventListener("keyup", function () {
    const value = this.value.toLowerCase();

    results.style.display = "block";

    document.querySelectorAll(".employee-option").forEach(option => {
        const name = option.dataset.name.toLowerCase();

        if (name.includes(value)) {
            option.style.display = "block";
        } else {
            option.style.display = "none";
        }
    });
});

document.querySelectorAll(".employee-option").forEach(option => {
    option.addEventListener("click", function () {
        searchInput.value = this.innerText;
        employeeId.value = this.dataset.id;
        results.style.display = "none";
    });
});


/* Close employee search when clicking outside */
document.addEventListener("click", function (e) {
    if (!searchInput.contains(e.target) &&
        !results.contains(e.target)) {
        results.style.display = "none";
    }
});


/* ================= STATUS EDIT ================= */

document.querySelectorAll('.edit-status-btn').forEach(button => {

    button.addEventListener('click', function (e) {

        e.stopPropagation();

        const id = this.dataset.id;

        const display = document.getElementById(`status-display-${id}`);
        const select = document.getElementById(`status-edit-${id}`);

        display.style.display = 'none';
        select.style.display = 'inline-block';

        select.focus();
    });

});


/* ================= UPDATE STATUS ================= */

document.querySelectorAll('.status-edit').forEach(select => {

    select.addEventListener('change', function () {

        const id = this.id.replace('status-edit-', '');
        const newStatus = this.value;

        fetch('/update-attendance-status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body:
                `attendance_id=${encodeURIComponent(id)}` +
                `&status=${encodeURIComponent(newStatus)}`
        })

        .then(response => {

            if (!response.ok) {
                throw new Error('Failed to update status');
            }

            /* Reload so Check In / Check Out
               is rendered according to new status */
            window.location.reload();

        })

        .catch(error => {

            console.error(error);
            alert('Unable to update attendance status.');

        });

    });

});

function validateEmployee() {

    const employeeId =
        document.getElementById("employeeId").value;

    if (!employeeId) {

        alert("Please select an employee from the list.");

        return false;
    }

    return true;
}