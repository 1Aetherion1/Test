// Когда html документ готов (прорисован)
$(document).ready(function () {
    // Берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var successMessage = $("#jq-notification");

    // Ловим событие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины
        var goodsInCartCount = $("#goods-in-cart-count");

        // Получаем id товара из атрибута data-product-id
        var product_id = $(this).data("product-id");

        // Из атрибута href берем ссылку на контроллер django
        var add_to_cart_url = $(this).attr("href");

        // Делаем POST-запрос через ajax, не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.text(data.message);
                successMessage.fadeIn(400);

                // Через 7 сек. убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
                var cartCount = parseInt(goodsInCartCount.text(), 10) || 0;
                cartCount++;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины на ответ от django
                // (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },
            error: function (data) {
                console.error("Ошибка при добавлении товара в корзину", data);
            },
        });
    });

    // Ловим событие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины
        var goodsInCartCount = $("#goods-in-cart-count");

        // Получаем id корзины из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");

        // Из атрибута href берем ссылку на контроллер django
        var remove_from_cart = $(this).attr("href");

        // Делаем POST-запрос через ajax, не перезагружая страницу
        $.ajax({
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.text(data.message);
                successMessage.fadeIn(400);

                // Через 7 сек. убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Уменьшаем количество товаров в корзине (отрисовка)
                var cartCount = parseInt(goodsInCartCount.text(), 10) || 0;
                var quantityDeleted = Number(data.quantity_deleted);

                if (Number.isFinite(quantityDeleted)) {
                    cartCount -= quantityDeleted;
                    goodsInCartCount.text(Math.max(0, cartCount));
                } else {
                    console.error(
                        "В ответе cart_remove отсутствует число quantity_deleted",
                        data
                    );
                }

                // Меняем содержимое корзины на ответ от django
                // (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },
            error: function (data) {
                console.error("Ошибка при удалении товара из корзины", data);
            },
        });
    });

    // Теперь + - количества товара
    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function (e) {
        e.preventDefault();

        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");

        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");

        // Ищем ближайший input с количеством
        var $input = $(this).closest(".input-group").find(".number");

        // Берем значение количества товара
        var currentValue = parseInt($input.val(), 10);

        // Если количество больше одного, то только тогда делаем -1
        if (currentValue > 1) {
            // Запускаем функцию, определенную ниже,
            // с аргументами (id корзины, новое количество,
            // количество уменьшилось или прибавилось, url)
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function (e) {
        e.preventDefault();

        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");

        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");

        // Ищем ближайший input с количеством
        var $input = $(this).closest(".input-group").find(".number");

        // Берем значение количества товара
        var currentValue = parseInt($input.val(), 10);

        if (!Number.isFinite(currentValue)) {
            console.error("Некорректное количество товара");
            return;
        }

        // Запускаем функцию, определенную ниже,
        // с аргументами (id корзины, новое количество,
        // количество уменьшилось или прибавилось, url)
        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        if (!cartID || !url) {
            console.error(
                "У кнопки не заполнены data-cart-id или data-cart-change-url"
            );
            return;
        }

        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.text(data.message);
                successMessage.fadeIn(400);

                // Через 7 сек. убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Изменяем количество товаров в корзине
                var goodsInCartCount = $("#goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text(), 10) || 0;
                cartCount += change;
                goodsInCartCount.text(Math.max(0, cartCount));

                // Меняем содержимое корзины
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },
            error: function (data) {
                console.error("Ошибка при изменении количества товара", data);
            },
        });
    }

    // Берем из разметки элемент по id — оповещения от django
    var notification = $("#notification");

    // И через 7 сек. убираем
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert("close");
        }, 7000);
    }

    // При клике по значку корзины открываем всплывающее (модальное) окно
    $("#modalButton").click(function () {
        $("#exampleModal").appendTo("body");
        $("#exampleModal").modal("show");
    });

    // Событие клика по кнопке закрыть окно корзины
    $("#exampleModal .btn-close").click(function () {
        $("#exampleModal").modal("hide");
    });

    // Обработчик события радиокнопки выбора способа доставки
    $("input[name='requires_delivery']").change(function () {
        var selectedValue = $(this).val();

        // Скрываем или отображаем input ввода адреса доставки
        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        } else {
            $("#deliveryAddressField").hide();
        }
    });
});