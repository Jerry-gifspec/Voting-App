// Select form elements
const adminLoginForm = document.getElementById("admin-login-form");
const voterLoginForm = document.getElementById("voter-login-form");
const voterRegisterForm = document.getElementById("voter-register-form");

// Admin login form submit event
if (adminLoginForm) {
  adminLoginForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent form from submitting traditionally

    const username = document.getElementById("admin-username").value;
    const password = document.getElementById("admin-password").value;

    const response = await fetch("/admin/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        username: username,
        password: password,
      }),
    });

    const data = await response.json();
    if (response.ok) {
      // If login successful, redirect to dashboard
      window.location.href = "/admin/dashboard";
    } else {
      // If login failed, show error message
      alert(data.message || "Login failed. Please try again.");
    }
  });
}

// Voter login form submit event
if (voterLoginForm) {
  voterLoginForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent form from submitting traditionally

    const voterUniqueId = document.getElementById("voter-unique-id").value;
    const password = document.getElementById("voter-password").value;

    const response = await fetch("/voter/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        voter_unique_id: voterUniqueId,
        password: password,
      }),
    });

    const data = await response.json();
    if (response.ok) {
      // If login successful, redirect to voting page
      window.location.href = "/vote";
    } else {
      // If login failed, show error message
      alert(data.message || "Login failed. Please try again.");
    }
  });
}

// Voter registration form submit event
if (voterRegisterForm) {
  voterRegisterForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent form from submitting traditionally

    const name = document.getElementById("voter-name").value;
    const email = document.getElementById("voter-email").value;
    const password = document.getElementById("voter-password").value;
    const voterUniqueId = document.getElementById("voter-unique-id").value;

    const response = await fetch("/voter/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        name: name,
        email: email,
        password: password,
        voter_unique_id: voterUniqueId,
      }),
    });

    const data = await response.json();
    if (response.ok) {
      // If registration successful, redirect to admin dashboard
      window.location.href = "/admin/dashboard";
    } else {
      // If registration failed, show error message
      alert(data.message || "Registration failed. Please try again.");
    }
  });
}

// Example of dynamically updating a page (e.g., displaying voters in admin dashboard)
async function loadVoters() {
  const response = await fetch("/admin/dashboard");
  const voters = await response.json();
  const voterList = document.getElementById("voter-list");

  if (voters.length > 0) {
    voters.forEach((voter) => {
      const listItem = document.createElement("li");
      listItem.textContent = `${voter.name} - ${voter.email}`;
      voterList.appendChild(listItem);
    });
  } else {
    voterList.innerHTML = "<li>No voters found</li>";
  }
}

// Call loadVoters if you're on the admin dashboard page
if (window.location.pathname === "/admin/dashboard") {
  loadVoters();
}
