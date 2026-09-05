
/* =====================================================
   LEAVE MANAGEMENT JAVASCRIPT
   ===================================================== */

const leaveModal = document.getElementById("leaveModal");
const closeLeaveModal = document.getElementById("closeLeaveModal");

let selectedLeaveId = null;


/* =====================================================
   VIEW LEAVE DETAILS
   ===================================================== */

document.querySelectorAll(".view-btn").forEach(function (button) {

    button.addEventListener("click", function () {

        const row = button.closest("tr");

        selectedLeaveId = button.getAttribute("data-leave-id");

        /* Employee */

        const employee =
            row.querySelector(".employee-info strong").innerText.trim();

        const employeeCode =
            row.querySelector(".employee-info small").innerText.trim();

        const avatar =
            row.querySelector(".employee-avatar").innerText.trim();


        /* Table information */

        const department =
            row.children[1].innerText.trim();

        const leaveType =
            row.children[2].innerText.trim();

        const dates =
            row.children[3].innerText
                .trim()
                .replace(/\s+/g, " ");

        const days =
            row.children[4].innerText.trim();

        const priority =
            row.children[5].innerText.trim();

        const applied =
            row.children[6].innerText.trim();

        const status =
            row.getAttribute("data-status");


        /* Fill employee information */

        document.getElementById("modalEmployeeName").innerText =
            employee;

        document.getElementById("modalEmployeeCode").innerText =
            employeeCode;

        document.getElementById("modalDepartment").innerText =
            department;

        document.getElementById("modalAvatar").innerText =
            avatar;


        /* Leave ID */

        document.getElementById("modalLeaveId").innerText =
            "LR-" + String(selectedLeaveId).padStart(4, "0");


        /* Leave information */

        document.getElementById("modalLeaveType").innerText =
            leaveType;

        document.getElementById("modalDays").innerText =
            days;

        document.getElementById("modalAppliedOn").innerText =
            applied;

        document.getElementById("modalPriority").innerText =
            priority;


        /* Dates */

        const dateParts = dates.split("to");

        if (dateParts.length >= 2) {

            document.getElementById("modalStartDate").innerText =
                dateParts[0].trim();

            document.getElementById("modalEndDate").innerText =
                dateParts[1].trim();

        } else {

            document.getElementById("modalStartDate").innerText =
                dates;

            document.getElementById("modalEndDate").innerText =
                dates;

        }


        /* Status */

        const statusElement =
            document.getElementById("modalStatus");

        statusElement.className = "modal-status";


        if (status === "Approved") {

            statusElement.classList.add("status-approved");

            statusElement.innerText = "✓ Approved";

        }

        else if (status === "Rejected") {

            statusElement.classList.add("status-rejected");

            statusElement.innerText = "× Rejected";

        }

        else {

            statusElement.classList.add("status-pending");

            statusElement.innerText = "◷ Pending";

        }


        /* Get REAL leave details */

        fetch("/get-leave-details/" + selectedLeaveId)

            .then(response => response.json())

            .then(data => {

                if (data.success) {

                    document.getElementById("modalReason").innerText =
                        data.leave.reason || "No reason provided";


                    const documentBox =
                        document.getElementById("modalDocuments");

                    if (data.leave.attachment) {

                        documentBox.innerHTML = `
                            <div class="document-icon">📎</div>

                            <div>
                                <strong>${data.leave.attachment}</strong>

                                <small>
                                    Uploaded document
                                </small>

                                <a href="/static/uploads/${encodeURIComponent(data.leave.attachment)}"
                                   target="_blank">
                                    View Document
                                </a>
                            </div>
                        `;

                    } else {

                        documentBox.innerHTML = `
                            <div class="document-icon">📎</div>

                            <div>
                                <strong>No documents uploaded</strong>
                                <small>No attachment was provided</small>
                            </div>
                        `;
                    }

                }

                else {

                    document.getElementById("modalReason").innerText =
                        "Unable to load reason.";

                }

            })

            .catch(error => {

                console.error("Leave details error:", error);

                document.getElementById("modalReason").innerText =
                    "Unable to load leave details.";

            });


        /* Clear remarks */

        document.getElementById("adminRemarks").value = "";


        /* Enable/disable modal decision buttons */

        updateModalButtons(status);


        /* Open modal */

        leaveModal.classList.add("show");

        document.body.style.overflow = "hidden";

    });

});


/* =====================================================
   UPDATE MODAL BUTTONS
   ===================================================== */

function updateModalButtons(status) {

    const approveButton =
        document.getElementById("modalApproveBtn");

    const rejectButton =
        document.getElementById("modalRejectBtn");

    const saveButton =
        document.getElementById("saveDecisionBtn");


    if (status === "Pending") {

        approveButton.style.display = "inline-flex";
        rejectButton.style.display = "inline-flex";
        saveButton.style.display = "inline-flex";

    }

    else {

        approveButton.style.display = "none";
        rejectButton.style.display = "none";
        saveButton.style.display = "none";

    }

}


/* =====================================================
   APPROVE BUTTON
   ===================================================== */

document.querySelectorAll(".approve-btn").forEach(function (button) {

    button.addEventListener("click", function () {

        const leaveId =
            button.getAttribute("data-leave-id");

        updateLeaveStatus(leaveId, "Approved");

    });

});


/* =====================================================
   REJECT BUTTON
   ===================================================== */

document.querySelectorAll(".reject-btn").forEach(function (button) {

    button.addEventListener("click", function () {

        const leaveId =
            button.getAttribute("data-leave-id");

        updateLeaveStatus(leaveId, "Rejected");

    });

});


/* =====================================================
   MODAL APPROVE
   ===================================================== */

document.getElementById("modalApproveBtn")
    .addEventListener("click", function () {

        if (!selectedLeaveId) {

            alert("No leave request selected.");

            return;
        }

        updateLeaveStatus(
            selectedLeaveId,
            "Approved"
        );

    });


/* =====================================================
   MODAL REJECT
   ===================================================== */

document.getElementById("modalRejectBtn")
    .addEventListener("click", function () {

        if (!selectedLeaveId) {

            alert("No leave request selected.");

            return;
        }

        updateLeaveStatus(
            selectedLeaveId,
            "Rejected"
        );

    });


/* =====================================================
   UPDATE LEAVE STATUS
   ===================================================== */

function updateLeaveStatus(leaveId, status) {

    fetch("/update-leave-status", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            leave_id: leaveId,

            status: status

        })

    })

    .then(response => response.json())

    .then(data => {
if (data.success) {

    location.reload();

}

      else {

    console.error(data.message);

}

    })

    .catch(error => {

        console.error("Status update error:", error);

     

    });

}


document.querySelectorAll(".response-btn").forEach(function(button){

    button.addEventListener("click", function(){

        const leaveId =
            button.getAttribute("data-leave-id");

        const replyRow =
            document.getElementById("reply-row-" + leaveId);

        if(replyRow){

            if(replyRow.style.display === "table-row"){

                replyRow.style.display = "none";

            }else{

                document.querySelectorAll(".reply-row")
                    .forEach(row => {

                        row.style.display = "none";

                    });

                replyRow.style.display = "table-row";

            }
        }

    });

});
/* =====================================================
   SAVE DECISION
   ===================================================== */

document.getElementById("saveDecisionBtn")
    .addEventListener("click", function () {

        if (!selectedLeaveId) {

            
            return;
        }


        const remarks =
            document.getElementById("adminRemarks").value.trim();


        if (!remarks) {

            

            return;
        }


        fetch("/save-leave-response", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                leave_id: selectedLeaveId,

                remarks: remarks

            })

        })

        .then(response => response.json())

        .then(data => {
if (data.success) {

    location.reload();

}

           else {

    console.error(data.message);

}

        })

        .catch(error => {

            console.error("Response error:", error);

       

        });

    });


/* =====================================================
   CLOSE MODAL
   ===================================================== */

closeLeaveModal.addEventListener("click", function () {

    leaveModal.classList.remove("show");

    document.body.style.overflow = "";

});


/* =====================================================
   CLICK OUTSIDE MODAL
   ===================================================== */

leaveModal.addEventListener("click", function (event) {

    if (event.target === leaveModal) {

        leaveModal.classList.remove("show");

        document.body.style.overflow = "";

    }

});


/* =====================================================
   ESC KEY
   ===================================================== */

document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        leaveModal.classList.remove("show");

        document.body.style.overflow = "";

    }

});

/* =====================================================
   INLINE REPLY ROW — SEND / CANCEL
   ===================================================== */

document.querySelectorAll(".send-reply-btn").forEach(function (button) {

    button.addEventListener("click", function () {

        const leaveId = button.getAttribute("data-leave-id");

        const textarea = document.getElementById("reply-text-" + leaveId);

        const remarks = textarea.value.trim();

        if (!remarks) {
            alert("Please write a reply before sending.");
            return;
        }

        fetch("/save-leave-response", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                leave_id: leaveId,
                remarks: remarks
            })

        })

        .then(response => response.json())

        .then(data => {

            if (data.success) {
                location.reload();
            } else {
                console.error(data.message);
                alert("Failed to send reply.");
            }

        })

        .catch(error => {
            console.error("Reply send error:", error);
        });

    });

});

document.querySelectorAll(".cancel-reply-btn").forEach(function (button) {

    button.addEventListener("click", function () {

        const leaveId = button.getAttribute("data-leave-id");

        const replyRow = document.getElementById("reply-row-" + leaveId);

        if (replyRow) {
            replyRow.style.display = "none";
        }

    });

});


/* =====================================================
   FILTER BUTTONS
   ===================================================== */

document.querySelectorAll(".filter-btn").forEach(function (button) {

    button.addEventListener("click", function () {

        document.querySelectorAll(".filter-btn")
            .forEach(function (btn) {

                btn.classList.remove("active");

            });


        button.classList.add("active");


        const filter =
            button.getAttribute("data-filter");


        document.querySelectorAll("#leaveTable tbody tr")
            .forEach(function (row) {

                const status =
                    row.getAttribute("data-status");


                if (!status) {
                    return;
                }


                if (filter === "All" || status === filter) {

                    row.style.display = "";

                }

                else {

                    row.style.display = "none";

                }

            });

    });

});


