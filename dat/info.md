## Download instructions

The Vesuvius Challenge data files can be found here:

http://dl.ash2txt.org/ or http://dl2.ash2txt.org/ (mirror)

**username:** registeredusers, **password:** only

It is possible to use `wget` to download this data recursively like this:

```
wget --no-parent -r --user=registeredusers --password=only http://dl.ash2txt.org/fragments
```

The data for the full scrolls is so large (~11.5 TB); here is a command to download 1cm of scan data from the center of Scroll 1:

```
for i in `seq 6000 7250`; do wget --user=registeredusers --password=only http://dl.ash2txt.org/full-scrolls/Scroll1.volpkg/volumes/20230205180739/0$i.tif; done
```
## Faster downloads

For faster downloads, use `rclone`: 
```
rclone copy :http:/full-scrolls/ ./dl.ash2txt.org/full-scrolls/ --http-url http://registeredusers:only@dl.ash2txt.org/ --progress --multi-thread-streams=32 --transfers=32 --size-only
```

On Linux, follow [these instructions](https://atoonk.medium.com/tcp-bbr-exploring-tcp-congestion-control-84c9c11dc3a9) to make downloads much faster on linux without needing to use `rclone`.

On Windows, follow [these instructions](https://github.com/JamesDarby345/VesuviusDownloadScriptsWindows10).


## LICENSE

By registering for downloads from the EduceLab-Scrolls Dataset, and for the Vesuvius Challenge Discord Server, I agree to license the data from Vesuvius Challenge* under the following licensing terms:
- I agree that all points below apply to both the EduceLab-Scrolls Dataset downloaded from our webserver, as well as any data (e.g. text, pictures, code) downloaded from the Vesuvius Challenge Discord Server.
- I will not redistribute the data without the written approval of Vesuvius Challenge (if I am working in a team, every team member will sign this form separately).
Vesuvius Challenge reserves the right to use in any way, including in an academic or other publication, all submissions or results produced from this dataset.
- **I will not make public (outside of Discord) any revelation of hidden text (or associated code) without the written approval of Vesuvius Challenge.**
- I agree all publications and presentations resulting from any use of the EduceLab-Scrolls Dataset must cite use of the EduceLab-Scrolls Dataset as follows:
- In any published abstract, I will cite “EduceLab-Scrolls” as the source of the data in the abstract.
- In any published manuscripts using data from EduceLab-Scrolls, I will reference the following paper: Parsons, S., Parker, C. S., Chapman, C., Hayashida, M., & Seales, W. B. (2023). EduceLab-Scrolls: Verifiable Recovery of Text from Herculaneum Papyri using X-ray CT. ArXiv [Cs.CV]. https://doi.org/10.48550/arXiv.2304.02084.
- I will include language similar to the following in the methods section of my manuscripts in order to accurately acknowledge the data source: “Data used in the preparation of this article were obtained from the EduceLab-Scrolls dataset [above citation].”
- I understand that all submissions will be reviewed by the Vesuvius Challenge Review Team, and that prizes will be awarded as the sole discretion of Vesuvius Challenge.
When I post or upload data in Discord (e.g. text, pictures, code), I agree to license it to other participants under these same terms.

* All EduceLab-Scrolls data is copyrighted by EduceLab/The University of Kentucky. Permission to use the data linked herein according to the terms outlined above is granted to Vesuvius Challenge.