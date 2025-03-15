function openOrderForm() {
  document.getElementById("orderFormModal").style.display = "flex";
}

function closeOrderForm() {
  document.getElementById("orderFormModal").style.display = "none";
}

function submitOrder() {
  // implement form validation here if needed
  const form = document.getElementById("orderForm");

  // Reset fields
  form.reset();

  // Hide 
  document.getElementById("orderFormModal").style.display = "none";

  // Show  message
  document.getElementById("successMessage").style.display = "flex";
}

function closeSuccessMessage() {
  document.getElementById("successMessage").style.display = "none";
}


let inactivityTimer;

function resetInactivityTimer() {
  clearTimeout(inactivityTimer);
  inactivityTimer = setTimeout(() => {
    fetch('/logout_inactivity', { method: 'POST' })
      .then(() => {
        alert('You have been logged out due to inactivity.');
        window.location.href = '/login';
      })
      .catch(error => console.error('Error logging out:', error));
  }, 5 * 60 * 1000); // 5 minutes inactivity threshold
}

document.addEventListener('mousemove', resetInactivityTimer);
document.addEventListener('keydown', resetInactivityTimer);
document.addEventListener('click', resetInactivityTimer);
document.addEventListener('scroll', resetInactivityTimer);

resetInactivityTimer();
