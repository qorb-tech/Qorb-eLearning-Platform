$(function () {
    $('#datepicker').datepicker(
        {
            format: "dd/mm/yyyy",
            autoclose: true,
            todayHighlight: true,
            showOtherMonths: true,
            selectOtherMonths: true,
            autoclose: true,
            changeMonth: true,
            changeYear: true,
            orientation: "button"
        }
    );
});
