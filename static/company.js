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
