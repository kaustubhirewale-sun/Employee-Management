document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       LEAVE DURATION
       Monday - Friday only
       ===================================================== */

    const startDate = document.getElementById("start_date");
    const endDate = document.getElementById("end_date");
    const durationValue = document.getElementById("durationValue");
    const durationInput = document.getElementById("leave_duration");


    function calculateWorkingDays() {

        if (!startDate.value || !endDate.value) {

            durationValue.textContent = "0 working days";
            durationInput.value = 0;

            return;
        }


        const start = new Date(startDate.value + "T00:00:00");
        const end = new Date(endDate.value + "T00:00:00");


        /* End date before start date */

        if (end < start) {

            durationValue.textContent =
                "Invalid date range";

            durationInput.value = 0;

            return;
        }


        let workingDays = 0;

        const current = new Date(start);


        while (current <= end) {

            const day = current.getDay();

            /*
                0 = Sunday
                6 = Saturday

                Monday-Friday = working days
            */

            if (day !== 0 && day !== 6) {
                workingDays++;
            }

            current.setDate(
                current.getDate() + 1
            );
        }


        durationValue.textContent =
            workingDays +
            (workingDays === 1
                ? " working day"
                : " working days");


        durationInput.value = workingDays;
    }


    startDate.addEventListener(
        "change",
        calculateWorkingDays
    );

    endDate.addEventListener(
        "change",
        calculateWorkingDays
    );


    /* =====================================================
       RESET DURATION
       ===================================================== */

    const form =
        document.getElementById("leaveRequestForm");


    form.addEventListener("reset", function () {

        setTimeout(function () {

            durationValue.textContent =
                "0 working days";

            durationInput.value = 0;

            const fileName =
                document.getElementById("file-name");

            if (fileName) {
                fileName.textContent = "No file chosen";
            }

        }, 0);

    });


    /* =====================================================
       EYE BUTTON - OPEN MODAL
       ===================================================== */

    const viewButtons =
        document.querySelectorAll(".view-leave-btn");


    viewButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const leaveId =
                button.dataset.leaveId;

            const modal =
                document.getElementById(
                    "details-" + leaveId
                );


            if (!modal) {
                return;
            }


            modal.classList.add("show");

            document.body.style.overflow = "hidden";

        });

    });


    /* =====================================================
       CLOSE MODAL - X BUTTON
       ===================================================== */

    const closeButtons =
        document.querySelectorAll(".close-details");


    closeButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const leaveId =
                button.dataset.leaveId;

            const modal =
                document.getElementById(
                    "details-" + leaveId
                );


            if (modal) {
                modal.classList.remove("show");
                document.body.style.overflow = "";
            }

        });

    });


    /* =====================================================
       CLOSE MODAL - CLICK OUTSIDE
       ===================================================== */

    document.querySelectorAll(".leave-modal-overlay")
        .forEach(function (overlay) {

            overlay.addEventListener("click", function (event) {

                if (event.target === overlay) {

                    overlay.classList.remove("show");

                    document.body.style.overflow = "";

                }

            });

        });


    /* =====================================================
       CLOSE MODAL - ESC KEY
       ===================================================== */

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {

            document.querySelectorAll(".leave-modal-overlay.show")
                .forEach(function (overlay) {

                    overlay.classList.remove("show");

                });

            document.body.style.overflow = "";

        }

    });


    /* =====================================================
       SEARCH
       ===================================================== */

    const searchInput =
        document.getElementById("leaveSearch");


    const statusFilter =
        document.getElementById("statusFilter");


    function filterLeaves() {

        const search =
            searchInput.value.toLowerCase().trim();

        const selectedStatus =
            statusFilter.value;


        const rows =
            document.querySelectorAll(
                "#leaveTable tbody tr"
            );


        rows.forEach(function (row) {

            const text =
                row.textContent.toLowerCase();


            const matchesSearch =
                text.includes(search);


            const statusElement =
                row.querySelector(".status");


            const rowStatus =
                statusElement
                    ? statusElement.textContent.trim()
                    : "";


            const matchesStatus =
                selectedStatus === "all" ||
                rowStatus === selectedStatus;


            if (
                matchesSearch &&
                matchesStatus
            ) {

                row.style.display = "";

            } else {

                row.style.display = "none";

            }

        });

    }


    searchInput.addEventListener(
        "input",
        filterLeaves
    );

    statusFilter.addEventListener(
        "change",
        filterLeaves
    );

});

document.addEventListener("DOMContentLoaded", function () {

    const attachment = document.getElementById("attachment");
    const fileName = document.getElementById("file-name");

    if (!attachment) {
        return;
    }

    attachment.addEventListener("change", function () {

        if (this.files && this.files.length > 0) {

            fileName.textContent = this.files[0].name;

        } else {

            fileName.textContent = "No file chosen";
        }
    });

});