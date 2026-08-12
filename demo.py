"""Compatibility entry point for the original MiVOLO demo command."""

from mivolo.cli import get_direct_video_url, get_local_video_info, get_parser, main

__all__ = ["get_direct_video_url", "get_local_video_info", "get_parser", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
