# streamentry

Source and publication files for *Hướng Đến Nhập Lưu*, an A5 Vietnamese mindfulness handbook for lay readers. The book distinguishes early Pāli discourses, later Theravāda commentary, the *Visuddhimagga*, Mahāsi instructions, modern research, and editorial guidance.

The title describes a direction of practice, not a guarantee of spiritual attainment.

**Author:** CS Chánh Niệm + ChatGPT

## Build

```sh
typst compile --root . book/main.typ dist/huong-den-nhap-luu.pdf
```

The compiled handbook is available at [`dist/huong-den-nhap-luu.pdf`](dist/huong-den-nhap-luu.pdf). Source provenance is documented in [`book/references/claim-ledger.md`](book/references/claim-ledger.md).

The PDF uses an A5 print-safe white page background. Small neutral surfaces preserve hierarchy in grayscale without printing a full-page tint.
