import unittest

import demo
from mivolo import cli


class CommandLineTests(unittest.TestCase):
    def test_parser_preserves_required_arguments_and_defaults_to_auto(self):
        arguments = cli.get_parser().parse_args(
            [
                "--input",
                "image.jpg",
                "--output",
                "output",
                "--detector-weights",
                "detector.pt",
                "--checkpoint",
                "checkpoint.pth.tar",
            ]
        )

        self.assertEqual(arguments.device, "auto")
        self.assertFalse(arguments.draw)
        self.assertFalse(arguments.with_persons)
        self.assertFalse(arguments.disable_faces)

    def test_parser_exposes_only_macos_devices(self):
        action = next(action for action in cli.get_parser()._actions if action.dest == "device")
        self.assertEqual(tuple(action.choices), ("auto", "mps", "cpu"))

    def test_root_demo_is_a_compatibility_shim(self):
        self.assertIs(demo.main, cli.main)
        self.assertIs(demo.get_parser, cli.get_parser)


if __name__ == "__main__":
    unittest.main()
