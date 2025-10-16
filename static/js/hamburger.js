const hamburgerBtn = document.getElementById('hamburgerBtn');
const menuItems = document.getElementById('menuItems');

hamburgerBtn.addEventListener('click', function (e) {
    e.stopPropagation(); // Предотвращаем закрытие при клике на кнопку
    this.classList.toggle('active');
    menuItems.classList.toggle('open');
});

// Закрываем меню при клике вне его области
document.addEventListener('click', function () {
    hamburgerBtn.classList.remove('active');
    menuItems.classList.remove('open');
});

// Предотвращаем закрытие при клике внутри меню
menuItems.addEventListener('click', function (e) {
    e.stopPropagation();
});


document.querySelectorAll('.has-submenu').forEach(item => {
    item.addEventListener('click', function (e) {
        e.preventDefault();
        const parent = this.parentElement;
        parent.classList.toggle('active');

        // Закрываем другие открытые подменю
        document.querySelectorAll('.menu-item-with-sub').forEach(otherItem => {
            if (otherItem !== parent && otherItem.classList.contains('active')) {
                otherItem.classList.remove('active');
            }
        });
    });
});

// Модифицируем существующий обработчик клика по документу
document.addEventListener('click', function () {
    hamburgerBtn.classList.remove('active');
    menuItems.classList.remove('open');
    document.querySelectorAll('.menu-item-with-sub.active').forEach(item => {
        item.classList.remove('active');
    });
});

// Предотвращаем закрытие при клике внутри меню
menuItems.addEventListener('click', function (e) {
    e.stopPropagation();
    // Если клик был по подменю, не закрываем основное меню
    if (e.target.closest('.submenu')) {
        hamburgerBtn.classList.add('active');
        menuItems.classList.add('open');
    }
});