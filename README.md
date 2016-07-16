
# Karaoke Tools

This is just a simple set of tools I created to help manage my home karaoke system.
Most of these tools are not very refined or optimized. They are largely just a quick
hack to get the job done.


## Song List Generator

The song list generator will scan a directory containing MP3 files and generates a PDF
song list based upon the ID3 tags for each file. Groups songs by artist.

### Requirements
* Python 2.7+
* Mutagen
* Reportlab

### Usage
```
./generator.py --path=/location/of/mp3/files --output=Songlist.pdf
```

### Wishlist
- [ ] Ability to configure margins / spacing
- [ ] Ensure that new sections always start on odd pages
- [ ] Abstract the page templates, frames, and layout



## Metadata Cleanup

This tool is a quick hack to populate artist/song ID3 tags based upon the file name.
Many songs that I've purchased over the years, or songs that I have ripped from my
CD+G discs have inconsistent or nonexistent ID3 tags.

### Requirements
* Python 2.7+
* Mutagen
* Reportlab

### Usage
```
./fix_metadata.py --path=/location/of/mp3/files
```

### Wishlist
- [ ] Look up and correct meta-data using an online service


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

---
[MIT License](LICENSE.md) © Greg Crist
