function searchTable(identifier) {
  const filter = $(identifier).val().toUpperCase();
  const tableId = $(identifier).data("table");
  $(`#${tableId} tbody tr`).each(function() {
    const rowText = $(this).text().toUpperCase();
    if (rowText.includes(filter)) {
        $(this).show();
    } else {
        $(this).hide();
    }
  });
}

function deleteInlineForm(identifier) {
  const formId = $(identifier).data("formid")
  const form = $(`#${formId}`);
  form.remove();
}