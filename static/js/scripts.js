document.addEventListener("DOMContentLoaded", function () {
    const yearSelect = document.getElementById("year");
    const monthSelect = document.getElementById("month");
    const daySelect = document.getElementById("day");

    function updateDays() {
        const year = parseInt(yearSelect.value);
        const month = parseInt(monthSelect.value);

        // Clear existing options
        daySelect.innerHTML = "";

        // Always add default "Day" option
        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.text = "Day";
        daySelect.appendChild(defaultOption);

        if (!year || !month) return; // Don’t add days if no year/month selected

        // ✅ Get number of days in that month/year
        const daysInMonth = new Date(year, month, 0).getDate();

        // Append days dynamically
        for (let d = 1; d <= daysInMonth; d++) {
            const option = document.createElement("option");
            option.value = d;
            option.text = d;
            daySelect.appendChild(option);
        }
    }

    // Watch for changes in Year and Month
    yearSelect.addEventListener("change", updateDays);
    monthSelect.addEventListener("change", updateDays);
});

// To show and hide password
document.getElementById('show_password').addEventListener('click', function() {
  const passwordField = document.getElementById('password');
  if (passwordField.type === 'password') {
    passwordField.type = 'text';
    this.textContent = "Hide Password";
  } else {
    passwordField.type = 'password';
    this.textContent = "Show Password";
  }
});

document.getElementById('show_password1').addEventListener('click', function() {
  const passwordField = document.getElementById('password1');
  if (passwordField.type === 'password') {
    passwordField.type = 'text';
    this.textContent = "Hide Password";
  } else {
    passwordField.type = 'password';
    this.textContent = "Show Password";
  }
});

document.getElementById('show_password2').addEventListener('click', function() {
  const passwordField = document.getElementById('old_password');
  if (passwordField.type === 'password') {
    passwordField.type = 'text';
    this.textContent = "Hide Password";
  } else {
    passwordField.type = 'password';
    this.textContent = "Show Password";
  }
});
