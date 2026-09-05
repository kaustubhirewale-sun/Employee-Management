document.addEventListener("DOMContentLoaded", function () {


    // =================================================
    // EDIT DEPARTMENT
    // =================================================

    const editButtons = document.querySelectorAll(".edit-department-btn");

editButtons.forEach(function (button) {

    button.addEventListener("click", function () {

        const deptId = this.dataset.id;
        const deptName = this.dataset.name;
        const deptHead = this.dataset.head;
        const description = this.dataset.description;
        const createdDate = this.dataset.createdDate;

        document.getElementById("editDeptName").value = deptName;
        document.getElementById("editDeptHead").value = deptHead;
        document.getElementById("editDeptDescription").value = description;

        document.getElementById("editDeptCreatedDate").value =
            createdDate;

        document.getElementById("editDepartmentForm").action =
            "/edit-department/" + deptId;

        document
            .getElementById("editDepartmentModal")
            .classList.add("active");

    });

});


function closeEditDepartment() {

    document
        .getElementById("editDepartmentModal")
        .classList.remove("active");

}

    // =================================================
    // DELETE DEPARTMENT
    // =================================================

    const deleteButtons =
        document.querySelectorAll(".delete-department-btn");

    deleteButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const deptId = this.dataset.id;


            if (!confirm(
                "Are you sure you want to delete this department?"
            )) {
                return;
            }


            fetch(
                "/delete-department/" + deptId,
                {
                    method: "POST"
                }
            )

            .then(function (response) {

                if (response.ok) {

                    window.location.reload();

                } else {

                    alert("Unable to delete department.");

                }

            })

            .catch(function () {

                alert("Unable to delete department.");

            });

        });

    });


    // =================================================
    // VIEW TEAM
    // =================================================

    const teamButtons =
        document.querySelectorAll(".view-team-btn");

    teamButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const deptId =
                this.dataset.deptId;


            fetch(
                "/department-team/" + deptId
            )

            .then(function (response) {

                if (!response.ok) {
                    throw new Error("Failed");
                }

                return response.json();

            })

            .then(function (data) {

                document.getElementById(
                    "teamDepartmentName"
                ).textContent = data.department;


                const membersBox =
                    document.getElementById("teamMembers");

                membersBox.innerHTML = "";


                if (data.employees.length === 0) {

                    membersBox.innerHTML =
                        '<p class="no-members">No employees in this department.</p>';

                } else {

                    data.employees.forEach(function (emp) {

                        const member =
                            document.createElement("button");

                        member.type = "button";

                        member.className =
                            "team-member";


                        member.innerHTML = `

                            <span class="member-icon">
                                👤
                            </span>

                            <span>

                                <strong>
                                    ${emp.first_name}
                                    ${emp.last_name}
                                </strong>

                                <small>
                                    ${emp.role || "Employee"}
                                </small>

                            </span>

                        `;


                        member.addEventListener(
                            "click",
                            function () {

                                openEmployeeProfile(emp);

                            }
                        );


                        membersBox.appendChild(member);

                    });

                }


                document
                    .getElementById("teamModal")
                    .classList.add("active");

            })

            .catch(function () {

                alert(
                    "Unable to load department team."
                );

            });

        });

    });


    // =================================================
    // CLOSE TEAM
    // =================================================

    const closeTeam =
        document.getElementById("closeTeamModal");

    if (closeTeam) {

        closeTeam.addEventListener(
            "click",
            function () {

                document
                    .getElementById("teamModal")
                    .classList.remove("active");

            }
        );

    }


    // =================================================
    // CLOSE PROFILE
    // =================================================

    const closeProfile =
        document.getElementById("closeProfileModal");

    if (closeProfile) {

        closeProfile.addEventListener(
            "click",
            function () {

                document
                    .getElementById("profileModal")
                    .classList.remove("active");

            }
        );

    }

});


// =================================================
// ADD DEPARTMENT
// =================================================

function openAddDepartment() {

    document
        .getElementById("addDepartmentModal")
        .classList.add("active");

}


function closeAddDepartment() {

    document
        .getElementById("addDepartmentModal")
        .classList.remove("active");

}


// =================================================
// EDIT DEPARTMENT
// =================================================

function closeEditDepartment() {

    document
        .getElementById("editDepartmentModal")
        .classList.remove("active");

}


// =================================================
// EMPLOYEE PROFILE
// =================================================

function openEmployeeProfile(emp) {

    document.getElementById(
        "employeeProfile"
    ).innerHTML = `

        <div class="profile-avatar">
            👤
        </div>

        <h2>
            ${emp.first_name}
            ${emp.last_name}
        </h2>

        <p class="profile-role">
            ${emp.role || "Employee"}
        </p>

        <div class="profile-details">

            <div>
                <span>Employee ID</span>
                <strong>
                    ${emp.employee_code}
                </strong>
            </div>

            <div>
                <span>Email</span>
                <strong>
                    ${emp.email || "—"}
                </strong>
            </div>

            <div>
                <span>Phone</span>
                <strong>
                    ${emp.phone || "—"}
                </strong>
            </div>

            <div>
                <span>Joining Date</span>
                <strong>
                    ${emp.join_date || "—"}
                </strong>
            </div>

            <div>
                <span>Birth Date</span>
                <strong>
                    ${emp.birth_date || "—"}
                </strong>
            </div>

            <div>
                <span>Role</span>
                <strong>
                    ${emp.role || "—"}
                </strong>
            </div>

        </div>
    `;


    document
        .getElementById("profileModal")
        .classList.add("active");

}

// ================= CREATED DATE =================

document.addEventListener("DOMContentLoaded", function () {

    const createdDate = document.getElementById("createdDate");

    if (createdDate) {

        const today = new Date();

        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, "0");
        const day = String(today.getDate()).padStart(2, "0");

        createdDate.value = `${year}-${month}-${day}`;
    }

});