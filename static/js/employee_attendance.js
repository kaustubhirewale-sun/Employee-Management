document.addEventListener("DOMContentLoaded", function () {

    const filterForm =
        document.getElementById("attendanceFilter");

    const monthInput =
        document.getElementById("month");

    const clearButton =
        document.getElementById("clearFilter");


    /* =====================================================
       SET CURRENT MONTH IF EMPTY
       ===================================================== */

    if (monthInput && !monthInput.value) {

        const today = new Date();

        const year = today.getFullYear();

        const month =
            String(today.getMonth() + 1).padStart(2, "0");

        monthInput.value = `${year}-${month}`;
    }


    /* =====================================================
       CLEAR FILTER
       ===================================================== */

    if (clearButton) {

        clearButton.addEventListener("click", function () {

            monthInput.value = "";

            window.location.href =
                window.location.pathname;

        });

    }


    /* =====================================================
       FORM VALIDATION
       ===================================================== */

    if (filterForm) {

        filterForm.addEventListener("submit", function (event) {

            if (!monthInput.value) {

                event.preventDefault();

                alert("Please select a month.");

                monthInput.focus();

            }

        });

    }


    /* =====================================================
       TABLE ROW HOVER
       ===================================================== */

    const rows =
        document.querySelectorAll("tbody tr");

    rows.forEach(function (row) {

        row.addEventListener("click", function () {

            row.classList.toggle("selected-row");

        });

    });

});