from abc import ABC

from bunq.sdk.json import converter
from bunq.sdk.model.generated.endpoint import PaymentServiceProviderCredential, BunqResponseUserPaymentServiceProvider


class PaymentServiceProviderCredentialInternal(PaymentServiceProviderCredential, ABC):

    @classmethod
    def create_with_api_context(cls,
                                client_payment_service_provider_certificate,
                                client_payment_service_provider_certificate_chain,
                                client_public_key_signature,
                                api_context,
                                all_custom_header=None):
        if all_custom_header is None:
            all_custom_header = {}

        request_body = {
            cls.FIELD_CLIENT_PAYMENT_SERVICE_PROVIDER_CERTIFICATE: client_payment_service_provider_certificate,
            cls.FIELD_CLIENT_PAYMENT_SERVICE_PROVIDER_CERTIFICATE_CHAIN: client_payment_service_provider_certificate_chain,
            cls.FIELD_CLIENT_PUBLIC_KEY_SIGNATURE: client_public_key_signature
        }

        request_map_string = converter.class_to_json(request_body)
        request_map_string = cls._remove_field_for_request(request_map_string)

        from bunq.sdk.http.api_client import ApiClient
        api_client = ApiClient(api_context)

        request_bytes = request_map_string.encode()

        response_raw = api_client.post(
            cls._ENDPOINT_URL_CREATE,
            request_bytes,
            all_custom_header
        )

        credential = PaymentServiceProviderCredential._from_json(response_raw, PaymentServiceProviderCredential._OBJECT_TYPE_GET)

        return BunqResponseUserPaymentServiceProvider.cast_from_bunq_response(credential)
