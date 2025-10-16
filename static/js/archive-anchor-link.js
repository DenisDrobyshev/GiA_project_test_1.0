document.addEventListener('DOMContentLoaded', function () {
    // Находим контейнер с кнопками годов
    const buttonsContainer = document.querySelector('.but-container');

    // Находим все кнопки годов
    const yearButtons = buttonsContainer.querySelectorAll('a');

    // Высота отступа (можно регулировать)
    const offset = 200; // 200px отступ сверху

    // Для каждой кнопки
    yearButtons.forEach(button => {
        // Получаем текст года (2020, 2021 и т.д.)
        const year = button.textContent.trim();

        // Устанавливаем href как якорную ссылку (#2020, #2021 и т.д.)
        button.href = `#${year}`;

        // Находим соответствующий блок года
        const yearBlocks = document.querySelectorAll('.arch-year h5');
        let targetBlock = null;

        yearBlocks.forEach(block => {
            if (block.textContent.trim() === year) {
                // Добавляем id к родительскому элементу .arch-year
                block.parentElement.id = year;
                targetBlock = block.parentElement;
            }
        });

        // Добавляем обработчик клика для плавной прокрутки
        button.addEventListener('click', function (e) {
            if (targetBlock) {
                e.preventDefault();

                // Получаем позицию блока относительно верха документа
                const elementPosition = targetBlock.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - offset;

                // Плавная прокрутка к целевому элементу с отступом
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });

                // Добавляем класс для подсветки (опционально)
                targetBlock.classList.add('highlight');

                // Убираем подсветку через 2 секунды
                setTimeout(() => {
                    targetBlock.classList.remove('highlight');
                }, 2000);
            }
        });
    });
});