import unittest
from envcfg import envcfg
import os
import json

class TestEnvCfg(unittest.TestCase):
    def setUp(self):
        os.environ["WEB_DOMAIN"] = "localhost:5050"
        os.environ["WORKER_PORT"] = "2020"
        with open("test_data/config_a.json", 'r') as config_a:
            self.config_a = envcfg(json.load(config_a))

    def test_primitive_string(self):
        self.assertIsInstance(self.config_a["hosts"][0]["name"], str)
        self.assertIsInstance(self.config_a["hosts"][1]["name"], str)
        self.assertEqual(self.config_a["hosts"][0]["name"], "web")
        self.assertEqual(self.config_a["hosts"][1]["name"], "worker")

    def test_primitive_float(self):
        self.assertIsInstance(self.config_a["hosts"][0]["priority"], float)
        self.assertIsInstance(self.config_a["hosts"][1]["priority"], float)
        self.assertEqual(self.config_a["hosts"][0]["priority"], 0.1)
        self.assertEqual(self.config_a["hosts"][1]["priority"], 0.5)

    def test_primitive_int(self):
        self.assertIsInstance(self.config_a["n_threads"], int)
        self.assertEqual(self.config_a["n_threads"], 8)

    def test_primitive_list(self):
        self.assertIsInstance(self.config_a["hosts"], list)
        self.assertEqual(len(self.config_a["hosts"]), 2)

    def test_primitive_dict(self):
        self.assertIsInstance(self.config_a["hosts"][0], dict)
        self.assertIsInstance(self.config_a["hosts"][1], dict)

    def test_env_string(self):
        self.assertIsInstance(self.config_a["hosts"][0]["domain"], str)
        self.assertIsInstance(self.config_a["hosts"][1]["domain"], str)
        self.assertEqual(self.config_a["hosts"][0]["domain"], "localhost:5050")
        self.assertEqual(
                self.config_a["hosts"][1]["domain"], "worker.example.com")

    def test_env_int(self):
        self.assertIsInstance(self.config_a["hosts"][0]["port"], int)
        self.assertIsInstance(self.config_a["hosts"][1]["port"], int)
        self.assertEqual(self.config_a["hosts"][0]["port"], 80)
        self.assertEqual(self.config_a["hosts"][1]["port"], 2020)

    def test_env_float(self):
        self.assertIsInstance(self.config_a["hosts"][0]["load_ratio"], float)
        self.assertIsInstance(self.config_a["hosts"][1]["load_ratio"], float)
        self.assertEqual(self.config_a["hosts"][0]["load_ratio"], 0.6)
        self.assertEqual(self.config_a["hosts"][1]["load_ratio"], 0.8)

    def test_unsupported_type(self):
        # sets are unsupported
        bad_type = set([1, 5, "foo", 5.5])
        with self.assertRaises(TypeError):
            config = envcfg(bad_type)


