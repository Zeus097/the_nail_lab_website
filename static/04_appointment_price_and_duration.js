document.addEventListener('DOMContentLoaded', function () {
    const serviceSelect = document.getElementById('id_service');
    const serviceInfo = document.getElementById('service-info');

    function servicePriceAndDuration() {
        const selectedOption = serviceSelect.options[serviceSelect.selectedIndex];
        if (!selectedOption || !selectedOption.value) {
            serviceInfo.innerHTML = '';
            return;
        }
        const price = selectedOption.getAttribute('data-price');
        const duration = selectedOption.getAttribute('data-duration');

        serviceInfo.innerHTML = `
            <strong>Цена:</strong> ${price} лв.<br>
            <strong>Продължителност: ≈</strong> ${duration} мин.
        `;
    }

    serviceSelect.addEventListener('change', servicePriceAndDuration);
});
