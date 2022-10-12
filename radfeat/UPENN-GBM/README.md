### Overall survival for Glioblastoma

1. Download all the _Nifti files_ from [TCIA UPENN-GBM](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=70225642#70225642c94d520b7b5f42e7925602d723412459). Put them in one folder and update [config.py](radfeat/LNDb/config.py).
2. Run preprocessing:

```bash
   python preprocess.py
```

3. Run feature extraction:

```bash
   python extract.py
```

### Note

- In TCIA there are automatic segmentations for >470 patients, and manual masks only for >200. Only the automatic masks are used here.
