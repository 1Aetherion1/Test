import re

from django import forms


class CreateOrderForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        label='Имя',
    )
    last_name = forms.CharField(
        max_length=150,
        label='Фамилия',
    )
    phone_number = forms.CharField(
        max_length=20,
        label='Номер телефона',
    )
    requires_delivery = forms.ChoiceField(
        choices=(
            ('1', 'Нужна доставка'),
            ('0', 'Самовывоз'),
        ),
        label='Способ доставки',
    )
    delivery_address = forms.CharField(
        required=False,
        label='Адрес доставки',
    )
    payment_on_get = forms.ChoiceField(
        choices=(
            ('0', 'Оплата картой'),
            ('1', 'Наличными/картой при получении'),
        ),
        label='Способ оплаты',
    )

    def clean(self):
        cleaned_data = super().clean()

        if (
            cleaned_data.get('requires_delivery') == '1'
            and not cleaned_data.get('delivery_address')
        ):
            self.add_error(
                'delivery_address',
                'Укажите адрес доставки.',
            )

        return cleaned_data

    def clean_phone_number(self):
        data = self.cleaned_data.get('phone_number')
        if not data.isdigit():
            raise forms.ValidationError('Номер телефона должен содержать только цифры')
        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError('Неверный формат номера ')

        return data

