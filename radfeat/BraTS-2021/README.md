### MGMT methylation status prediction for Brain tumor (BraTS-2021)

1. Register and download the data from [Synapse.org](https://www.synapse.org/#!Synapse:syn25829067/wiki/610865). Put them in one folder and update [config.py](radfeat/BraTS-2021/config.py).
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
