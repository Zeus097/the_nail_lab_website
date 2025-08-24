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
        const maxPrice = selectedOption.getAttribute('data-max-price');
        const duration = selectedOption.getAttribute('data-duration');

        let priceText = '';
        if (price != null && price !== '') {
            if (maxPrice != null && maxPrice !== '' && maxPrice !== price) {
                priceText = `${price} лв. - ${maxPrice} лв.`;
            } else {
                priceText = `${price} лв.`;
            }
        }


        const parts = []
        if (priceText) parts.push(`<strong>Цена:</strong> ${priceText}`);
        if (duration != null && duration !== '') {
            parts.push(`<strong>Продължителност: ≈</strong> ${duration} мин.`);
        }

        serviceInfo.innerHTML = parts.join('<br>');

    }

    serviceSelect.addEventListener('change', servicePriceAndDuration);
});
