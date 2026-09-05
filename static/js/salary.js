document.addEventListener("DOMContentLoaded", function () {

    console.log("SALARY JS LOADED");

    const employeeSelect = document.getElementById("employeeSelect");
    const employeeNameSelect = document.getElementById("employeeNameSelect");

    console.log(employeeSelect);
    console.log(employeeNameSelect);

});
document.addEventListener("DOMContentLoaded", function () {

    const employeeSelect =
        document.getElementById("employeeSelect");

    const employeeNameSelect =
        document.getElementById("employeeNameSelect");

    const departmentSelect =
        document.getElementById("departmentSelect");


    // =====================================================
    // EMPLOYEE ID → EMPLOYEE NAME + DEPARTMENT
    // =====================================================

    employeeSelect.addEventListener("change", function () {

        const employeeId = this.value;

        if (!employeeId) {

            employeeNameSelect.value = "";
            departmentSelect.value = "";

            return;
        }


        // Select the same employee in Name dropdown
        employeeNameSelect.value = employeeId;


        // Get selected Employee ID option
        const selectedOption =
            employeeSelect.options[
                employeeSelect.selectedIndex
            ];


        // Automatically select department
        const departmentId =
            selectedOption.dataset.department;


        if (departmentId) {
            departmentSelect.value = departmentId;
        }

    });


    // =====================================================
    // EMPLOYEE NAME → EMPLOYEE ID + DEPARTMENT
    // =====================================================

    employeeNameSelect.addEventListener("change", function () {

        const employeeId = this.value;

        if (!employeeId) {

            employeeSelect.value = "";
            departmentSelect.value = "";

            return;
        }


        // Select the same employee in ID dropdown
        employeeSelect.value = employeeId;


        // Get corresponding Employee ID option
        const employeeOption =
            employeeSelect.options[
                employeeSelect.selectedIndex
            ];


        // Automatically select department
        const departmentId =
            employeeOption.dataset.department;


        if (departmentId) {
            departmentSelect.value = departmentId;
        }

    });


    // =====================================================
    // NET SALARY
    // Basic + Allowance - Deduction
    // =====================================================

    const basicSalary =
        document.getElementById("basicSalary");

    const allowance =
        document.getElementById("allowance");

    const deduction =
        document.getElementById("deduction");

  const netSalary = document.getElementById("netSalary");
const netSalaryInput = document.getElementById("netSalaryInput");


    function calculateNetSalary() {

        const basic =
            parseFloat(basicSalary.value) || 0;

        const allow =
            parseFloat(allowance.value) || 0;

        const deduct =
            parseFloat(deduction.value) || 0;


        let net =
            basic + allow - deduct;


        if (net < 0) {
            net = 0;
        }


        netSalary.value = net;
netSalaryInput.value = net;

    }


    basicSalary.addEventListener(
        "input",
        calculateNetSalary
    );

    allowance.addEventListener(
        "input",
        calculateNetSalary
    );

    deduction.addEventListener(
        "input",
        calculateNetSalary
    );

});

document.addEventListener("DOMContentLoaded", function () {

    const salaryMonth = document.getElementById("salaryMonth");

    if (salaryMonth && !salaryMonth.value) {
        const today = new Date();

        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, "0");

        salaryMonth.value = `${year}-${month}`;
    }

});


document.addEventListener("DOMContentLoaded", function () {

    const paymentStatus = document.getElementById("paymentStatus");

    const basicSalary = document.getElementById("basicSalary");
    const allowance = document.getElementById("allowance");
    const deduction = document.getElementById("deduction");

    function updateSalaryRequirements() {

        if (paymentStatus.value === "Pending") {

            basicSalary.removeAttribute("required");
            allowance.removeAttribute("required");
            deduction.removeAttribute("required");

            basicSalary.value = "";
            allowance.value = "";
            deduction.value = "";

        } else {

            basicSalary.setAttribute("required", "required");
            allowance.setAttribute("required", "required");
            deduction.setAttribute("required", "required");

        }
    }

    paymentStatus.addEventListener("change", updateSalaryRequirements);

    updateSalaryRequirements();

});
// =====================================================
// EDIT SALARY MODAL
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    const editButtons =
        document.querySelectorAll(".edit-salary-btn");

    const editModal =
        document.getElementById("editSalaryModal");

    const closeEdit =
        document.getElementById("closeEditSalary");

    editButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const id = this.dataset.id;

            // Open edit modal
            editModal.style.display = "flex";

            // Store salary ID in form action
            document.getElementById("editSalaryForm").action =
                "/update-salary/" + id;

        });

    });

    if (closeEdit) {
        closeEdit.addEventListener("click", function () {
            editModal.style.display = "none";
        });
    }

});

document.addEventListener("DOMContentLoaded", function () {

    const editEmployeeSelect =
        document.getElementById("editEmployeeSelect");

    const editEmployeeNameSelect =
        document.getElementById("editEmployeeNameSelect");

    const editDepartmentSelect =
        document.getElementById("editDepartmentSelect");

    if (!editEmployeeSelect || !editEmployeeNameSelect || !editDepartmentSelect) {
        return;
    }


    // Employee ID → Name + Department

    editEmployeeSelect.addEventListener("change", function () {

        const employeeId = this.value;

        editEmployeeNameSelect.value = employeeId;

        const selectedOption =
            this.options[this.selectedIndex];

        const departmentId =
            selectedOption.dataset.department;

        if (departmentId) {
            editDepartmentSelect.value = departmentId;
        }

    });


    // Employee Name → ID + Department

    editEmployeeNameSelect.addEventListener("change", function () {

        const employeeId = this.value;

        editEmployeeSelect.value = employeeId;

        const employeeOption =
            editEmployeeSelect.options[
                editEmployeeSelect.selectedIndex
            ];

        const departmentId =
            employeeOption.dataset.department;

        if (departmentId) {
            editDepartmentSelect.value = departmentId;
        }

    });

});

document.addEventListener("DOMContentLoaded", function () {

    const editBasicSalary =
        document.getElementById("editBasicSalary");

    const editAllowance =
        document.getElementById("editAllowance");

    const editDeduction =
        document.getElementById("editDeduction");

    const editNetSalary =
        document.getElementById("editNetSalary");

    const editNetSalaryInput =
        document.getElementById("editNetSalaryInput");


    if (
        !editBasicSalary ||
        !editAllowance ||
        !editDeduction ||
        !editNetSalary ||
        !editNetSalaryInput
    ) {
        return;
    }


    function calculateEditNetSalary() {

        const basic =
            parseFloat(editBasicSalary.value) || 0;

        const allowance =
            parseFloat(editAllowance.value) || 0;

        const deduction =
            parseFloat(editDeduction.value) || 0;


        let net =
            basic + allowance - deduction;


        if (net < 0) {
            net = 0;
        }


        editNetSalary.value = net;

        editNetSalaryInput.value = net;
    }


    editBasicSalary.addEventListener(
        "input",
        calculateEditNetSalary
    );

    editAllowance.addEventListener(
        "input",
        calculateEditNetSalary
    );

    editDeduction.addEventListener(
        "input",
        calculateEditNetSalary
    );


    // Calculate immediately when Edit modal opens

    calculateEditNetSalary();

});
function exportSalaryCSV() {

    const form = document.getElementById("salaryFilterForm");

    const params = new URLSearchParams(
        new FormData(form)
    );

    window.location.href =
        "/export-salary-csv?" + params.toString();
}

function exportSalaryCSV() {

    const form = document.getElementById("salaryFilterForm");

    const params = new URLSearchParams(
        new FormData(form)
    );

    window.location.href =
        "/export-salary-csv?" + params.toString();
}