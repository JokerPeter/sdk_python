import os

from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.api_environment_type import ApiEnvironmentType
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.model.generated import endpoint
from bunq.sdk.model.generated.object_ import Certificate
from bunq.sdk.security import security
from tests.bunq_test import BunqSdkTestCase


class TestPsd2Context(BunqSdkTestCase):
    """
    Tests:
        Psd2Context
    """

    # TODO: Implement PSD2

    _FILE_TEST_CONFIGURATION = '/assets/bunq-psd2-test.conf'
    _FILE_TEST_OAUTH = '/assets/bunq-oauth-test.conf'

    _FILE_TEST_CERTIFICATE = '/assets/certificate.pem'
    _FILE_TEST_CERTIFICATE_CHAIN = '/assets/certificate.pem'
    _FILE_TEST_PRIVATE_KEY = '/assets/key.pem'

    _TEST_DEVICE_DESCRIPTION = 'PSD2TestDevice'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._FILE_MODE_WRITE = ApiContext._FILE_MODE_WRITE

        if os.path.exists(cls._get_directory_test_root() + cls._FILE_TEST_CONFIGURATION):
            return

        try:
            BunqContext.load_api_context(cls.create_api_context())
        except FileNotFoundError:
            return

        api_context = ApiContext.restore(cls._get_directory_test_root() + cls._FILE_TEST_CONFIGURATION)
        BunqContext.load_api_context(api_context)

    def test_create_psd2_context(self):
        if os.path.exists(self._get_directory_test_root() + self._FILE_TEST_CONFIGURATION):
            return

        try:
            api_context = self.create_api_context()
            BunqContext.load_api_context(api_context)

            self.assertTrue(os.path.exists(self._get_directory_test_root() + self._FILE_TEST_CONFIGURATION))
        except FileNotFoundError as e:
            self.fail(str(e))

    def test_create_oauth_client(self):
        if os.path.exists(self._get_directory_test_root() + self._FILE_TEST_OAUTH):
            return

        try:
            client_id = endpoint.OauthClient.create().value
            oauth_client = endpoint.OauthClient.get(client_id).value

            self.assertIsNotNone(oauth_client)

            serialized_client = oauth_client.to_json()

            with open(self._get_directory_test_root() + self._FILE_TEST_OAUTH, self._FILE_MODE_WRITE) as file_:
                file_.write(serialized_client)

            self.assertTrue(os.path.exists(self._get_directory_test_root() + self._FILE_TEST_OAUTH))

        except FileNotFoundError as e:
            self.fail(str(e))

    @classmethod
    def create_api_context(cls):
        api_context = ApiContext.create_for_psd2(
            ApiEnvironmentType.SANDBOX,
            security.get_certificate_from_file(cls._get_directory_test_root() + cls._FILE_TEST_CERTIFICATE),
            security.get_private_key_from_file(cls._get_directory_test_root() + cls._FILE_TEST_PRIVATE_KEY),
            Certificate(
                security.get_certificate_from_file(cls._get_directory_test_root() + cls._FILE_TEST_CERTIFICATE_CHAIN)),
            cls._TEST_DEVICE_DESCRIPTION
        )

        api_context.save(cls._get_directory_test_root() + cls._FILE_TEST_CONFIGURATION)

        return api_context
