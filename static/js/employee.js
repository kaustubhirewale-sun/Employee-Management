document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("employeeSearch");
    const searchButton = document.getElementById("searchButton");
    const searchMessage = document.getElementById("searchMessage");
    const rows = document.querySelectorAll("#employeeTableBody tr");

    function searchEmployees() {

        const searchText = searchInput.value.trim().toLowerCase();

        let found = false;

        // Clear previous message
        searchMessage.textContent = "";
        searchMessage.className = "";

        // Remove previous highlights
        document.querySelectorAll(".search-highlight").forEach(function (element) {
            const parent = element.parentNode;
            parent.replaceChild(
                document.createTextNode(element.textContent),
                element
            );
            parent.normalize();
        });

        // Empty search → show everything
        if (searchText === "") {

            rows.forEach(function (row) {
                row.style.display = "";
                row.classList.remove("search-result");
            });

            return;
        }

        // Search every employee row
        rows.forEach(function (row) {

            const rowText = row.textContent.toLowerCase();

            if (rowText.includes(searchText)) {

                row.style.display = "";
                row.classList.add("search-result");

                found = true;

                highlightText(row, searchText);

            } else {

                row.style.display = "";
                row.classList.remove("search-result");

                // Hide non-matching employee
                row.style.display = "none";
            }
        });

        // Nothing found
        if (!found) {

            searchMessage.textContent = "Employee not found.";
            searchMessage.className = "not-found-message";
        }
    }


    function highlightText(row, searchText) {

        const cells = row.querySelectorAll("td");

        cells.forEach(function (cell) {

            // Don't highlight Edit/Delete buttons
            if (cell.querySelector(".action-buttons")) {
                return;
            }

            const walker = document.createTreeWalker(
                cell,
                NodeFilter.SHOW_TEXT
            );

            const textNodes = [];

            while (walker.nextNode()) {
                textNodes.push(walker.currentNode);
            }

            textNodes.forEach(function (node) {

                const text = node.nodeValue;
                const lowerText = text.toLowerCase();

                const index = lowerText.indexOf(searchText);

                if (index === -1) {
                    return;
                }

                const before = text.substring(0, index);

                const match = text.substring(
                    index,
                    index + searchText.length
                );

                const after = text.substring(
                    index + searchText.length
                );

                const fragment = document.createDocumentFragment();

                if (before) {
                    fragment.appendChild(
                        document.createTextNode(before)
                    );
                }

                const highlight = document.createElement("span");

                highlight.className = "search-highlight";
                highlight.textContent = match;

                fragment.appendChild(highlight);

                if (after) {
                    fragment.appendChild(
                        document.createTextNode(after)
                    );
                }

                node.parentNode.replaceChild(fragment, node);
            });
        });
    }


    // SEARCH BUTTON
    searchButton.addEventListener("click", searchEmployees);


    // ENTER KEY
    searchInput.addEventListener("keydown", function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            searchEmployees();
        }
    });

});