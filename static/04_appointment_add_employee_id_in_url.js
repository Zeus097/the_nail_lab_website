document.addEventListener('DOMContentLoaded', function () {
    const employeeSelect = document.querySelector('select[name="employee"]');
    if (employeeSelect) {
        employeeSelect.addEventListener('change', function () {
            const employeeId = this.value;
            const url = new URL(window.location.href);
            url.searchParams.set('employee_id', employeeId);
            window.location.href = url.toString();
        });
    }
});

