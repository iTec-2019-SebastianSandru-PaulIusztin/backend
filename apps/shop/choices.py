class BuyerTypeChoices:
    PRIVATE = 'private'
    COMPANY = 'company'

    BUYER_TYPE_CHOICES = (
        (PRIVATE, 'Private'),
        (COMPANY, 'Company')
    )


class ProductTypeChoices:
    ITEM = 'item'
    KG = 'kg'

    PRODUCT_TYPE_CHOICES = (
        (ITEM, 'ITEM'),
        (KG, 'KG')
    )


class ProductOriginChoices:
    AGRICULTURAL = 'agricultural'
    HANDCRAFTED = 'handcrafted'

    PRODUCT_ORIGIN_CHOICES = (
        (AGRICULTURAL, 'Agricultural'),
        (HANDCRAFTED, 'Handcrafted')
    )


class PaymentChoices:
    PENDING = 'pending'
    SUCCESSFUL = 'successful'
    FAILED = 'failed'

    PAYMENT_CHOICES = (
        (PENDING, 'Pending'),
        (SUCCESSFUL, 'Successful'),
        (FAILED, 'failed')
    )


class ShipmentChoices:
    IN_DEPOSIT = 'in_deposit'
    SHIPPING = 'shipping'
    SHIPPED = 'shipped'

    SHIPPING_CHOICES = (
        (IN_DEPOSIT, 'In deposit'),
        (SHIPPING, 'Shipping'),
        (SHIPPED, 'Shipped')
    )


class ShippingProviderChoices:
    FAN_COURIER = 'fan'

    PROVIDER_CHOICES = (
        (FAN_COURIER, 'Fan Courier'),
    )
