const selectAllCheckbox = document.getElementById('selectAll');
const checkboxes = document.querySelectorAll('.select-book');
const selectedCountElem = document.getElementById('selectedCount');
const checkoutBtn = document.getElementById('checkoutBtn');

function updateSelectedCount() {
  const selected = document.querySelectorAll('.select-book:checked').length;
  selectedCountElem.textContent = selected;
  checkoutBtn.disabled = selected === 0;
}

selectAllCheckbox.addEventListener('change', () => {
  checkboxes.forEach(chk => chk.checked = selectAllCheckbox.checked);
  updateSelectedCount();
});

checkboxes.forEach(chk =>
  chk.addEventListener('change', () => {
    if (!chk.checked) {
      selectAllCheckbox.checked = false;
    } else if (document.querySelectorAll('.select-book:checked').length === checkboxes.length) {
      selectAllCheckbox.checked = true;
    }
    updateSelectedCount();
  })
);

updateSelectedCount();

function toggleAddressField() {
  var deliveryMethod = document.getElementById('deliveryMethod').value;
  var addressField = document.getElementById('addressField');
  if (deliveryMethod === 'delivery') {
    addressField.style.display = 'block';
    document.getElementById('addressInput').setAttribute('required', 'required');
  } else {
    addressField.style.display = 'none';
    document.getElementById('addressInput').removeAttribute('required');
  }
}