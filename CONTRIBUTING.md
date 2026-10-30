# Contributing

Thank you for considering a contribution to Gear S3 Explorer.

## Before opening an issue
- Search existing issues for duplicates.
- Include Windows and Python versions, Gear S3 model, and Tizen firmware.
- Provide exact reproduction steps and sanitized logs.
- Never publish passwords, private keys, or personal device information.

## Pull requests
1. Fork the repository and create a focused branch.
2. Keep changes scoped and explain their user-visible impact.
3. Preserve the separation between `core/` and `ui/`.
4. Run `python -m compileall -q core ui main.py`.
5. Test hardware-dependent changes on a real device when possible.
6. Update documentation when setup, behavior, or compatibility changes.

Original contributions are provided under the repository's MIT license unless explicitly stated otherwise. Third-party files retain their own licenses.
