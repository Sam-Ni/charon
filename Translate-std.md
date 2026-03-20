# Translating the Rust Standard Library Incrementally

This document explains how to incrementally translate parts of the Rust standard library using Charon. It originates from [this github issue](https://github.com/AeneasVerif/charon/issues/863) and the subsequent discussion on [zulip](https://aeneas-verif.zulipchat.com/#narrow/channel/423740-dev/topic/Extracting.20the.20standard.20library/with/546486336).

## Instructions

1. Navigate to the the `charon` subdirectory:

```
cd charon
```

2. Create a dummy Rust file with a `main` function (required for the translation process):

```
echo "fn main() {}" > file.rs
```

3. Build Charon:

```
cargo build
```

4. Translate the standard library module by module using the provided Python script:

```
python3 translate_std.py --sysroot "$(rustc --print sysroot)"
```

5. After execution, a directory named `std` and a file named `failed_modules.txt` will be created. For each standard library module:

  - If Charon translates it successfully, a file named `std_xxx_yyy.txt` is generated inside `translate_std`.
  - If translation fails, a file named `std_xxx_yyy_error.txt` is generated instead.
  - All modules that failed are listed in `failed_modules.txt`