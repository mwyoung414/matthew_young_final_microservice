document.addEventListener("DOMContentLoaded", () => {
  const addUserForm = document.getElementById("addUserForm");

  if (addUserForm) {

      addUserForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Collect form data
        const formData = new FormData(addUserForm);
        const data = Object.fromEntries(formData.entries()); // Convert FormData to a plain object

        try {
            // Send data to the server
            const response = await fetch("/admin/add_user", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                // Handle success (e.g., close the modal, show a success message)
                alert("User added successfully!");
                const modal = bootstrap.Modal.getInstance(document.getElementById("addUserModal"));
                modal.hide();
                addUserForm.reset(); // Reset the form
            } else {
                // Handle errors (e.g., show an error message)
                const errorData = await response.json();
                alert(`Error: ${errorData.message}`);
            }
        } catch (error) {
            console.error("Error adding user:", error);
            alert("An error occurred while adding the user.");
        }
    });
  }
});


function ViewUsers() {
    // Logic to view users
    window.location.href = "/admin/view_users";
}

window.addEventListener("error", function (event) {
    fetch("/log-js-error", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: event.message,
        source: event.filename,
        line: event.lineno,
        column: event.colno,
        stack: event.error?.stack
      })
    });
  });
  