import os

from absl.testing import absltest
from absl.testing import parameterized

from integration_tests.dataproc_test_case import DataprocTestCase


class FlinkTestCase(DataprocTestCase):
    COMPONENT = 'flink'
    INIT_ACTIONS = ['flink/flink.sh']
    TEST_SCRIPT_FILE_NAME = 'validate.sh'

    def verify_instance(self, name, yarn_session=True):
        test_script_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            self.TEST_SCRIPT_FILE_NAME)
        self.upload_test_file(test_script_path, name)
        self.__run_test_file(name, yarn_session)
        self.remove_test_script(self.TEST_SCRIPT_FILE_NAME, name)

    def __run_test_file(self, name, yarn_session):
        self.assert_instance_command(
            name, "bash {} {}".format(self.TEST_SCRIPT_FILE_NAME,
                                      yarn_session))

    @parameterized.parameters(
        ("STANDARD", ["m"]),
        ("HA", ["m-0", "m-1", "m-2"]),
    )
    def test_flink(self, configuration, machine_suffixes):
        self.createCluster(
            configuration, self.INIT_ACTIONS, machine_type="n1-standard-2")
        for machine_suffix in machine_suffixes:
            self.verify_instance("{}-{}".format(self.getClusterName(),
                                                machine_suffix))

    @parameterized.parameters(
        ("STANDARD", ["m"]),
        ("HA", ["m-0", "m-1", "m-2"]),
        ("SINGLE", ["m"]),
    )
    def test_flink_with_optional_metadata(self, configuration,
                                          machine_suffixes):
        self.createCluster(
            configuration,
            self.INIT_ACTIONS,
            machine_type="n1-standard-2",
            metadata="flink-start-yarn-session=false")
        for machine_suffix in machine_suffixes:
            self.verify_instance(
                "{}-{}".format(self.getClusterName(), machine_suffix),
                yarn_session=False)


if __name__ == '__main__':
    absltest.main()
